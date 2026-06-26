from __future__ import annotations

import time

import pytest

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_screenshot, attach_text
from pagelocators.kuwo_locators import KuwoSettingsLocators
from pageobjects.kuwo.kuwo_account_page import KuwoAccountPage
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage
from pageobjects.kuwo.kuwo_settings_page import KuwoSettingsPage


def _open_settings_about(adb: ADBHelper, profile, artifact_dir, settings) -> tuple[KuwoHomePage, KuwoSettingsPage]:
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_settings()
    settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
    settings_page.assert_loaded_readonly()
    settings_page.open_about()
    return home, settings_page


def _restore_park_home(adb: ADBHelper, home: KuwoHomePage, profile) -> None:
    # 驾驶模式测试必须兜底恢复驻车，避免影响后续用例和人工台架使用。
    adb.driving_park()
    home.launch(profile)


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_driving_mode_about_entries_blocked_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    home, settings_page = _open_settings_about(adb, profile, artifact_dir, settings)
    entries = (
        (KuwoSettingsLocators.USER_AGREEMENT, "user_agreement"),
        (KuwoSettingsLocators.PRIVACY_POLICY, "privacy_policy"),
        (KuwoSettingsLocators.OPEN_SOURCE_DISCLAIMER, "open_source_disclaimer"),
    )

    try:
        adb.driving_drive()
        attach_screenshot(adb, artifact_dir, "01_about_drive_enabled")
        for entry_name, screenshot_name in entries:
            settings_page.open_about_entry(entry_name)
            attach_screenshot(adb, artifact_dir, f"02_about_drive_tap_{screenshot_name}")
            assert settings_page.wait_for(
                lambda: settings_page.is_about_loaded() or settings_page.is_driving_restricted(), timeout=3
            ), f"驾驶模式下点击 {entry_name} 后未停留在关于页或展示限制页"
            if not settings_page.is_about_loaded():
                settings_page.close_subpage()
                assert settings_page.wait_for(settings_page.is_about_loaded, timeout=3), "关闭限制页后未回到关于页"
    finally:
        _restore_park_home(adb, home, profile)

    attach_screenshot(adb, artifact_dir, "03_home_after_about_drive_entries")


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    entries = (
        (KuwoSettingsLocators.USER_AGREEMENT, "user_agreement", "legal"),
        (KuwoSettingsLocators.PRIVACY_POLICY, "privacy_policy", "legal"),
        (KuwoSettingsLocators.OPEN_SOURCE_DISCLAIMER, "open_source_disclaimer", "open_source"),
    )
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)

    try:
        for entry_name, screenshot_name, page_type in entries:
            home, settings_page = _open_settings_about(adb, profile, artifact_dir, settings)
            settings_page.open_about_entry(entry_name)
            if page_type == "legal":
                settings_page.assert_legal_info_loaded()
            else:
                settings_page.assert_open_source_loaded()
            attach_screenshot(adb, artifact_dir, f"01_{screenshot_name}_park_open")

            adb.driving_drive()
            time.sleep(1)
            attach_screenshot(adb, artifact_dir, f"02_{screenshot_name}_drive_restricted")
            settings_page.assert_driving_restricted()

            adb.driving_park()
            time.sleep(1)
            if page_type == "legal":
                settings_page.assert_legal_info_loaded()
            else:
                settings_page.assert_open_source_loaded()
            attach_screenshot(adb, artifact_dir, f"03_{screenshot_name}_park_restored")
            settings_page.close_subpage()
    finally:
        _restore_park_home(adb, home, profile)

    attach_screenshot(adb, artifact_dir, "04_home_after_legal_drive")


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_driving_mode_logged_in_account_entry_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    try:
        adb.driving_park()
        home.launch(profile)
        home.switch_tab("我的")
        if not home.is_logged_in_on_mine():
            pytest.skip("当前台架不是已登录账号态，已登录账户驾驶模式用例需会员账号环境")
        attach_screenshot(adb, artifact_dir, "01_mine_logged_in_before_drive")

        adb.driving_drive()
        home.open_account_from_mine()
        account = KuwoAccountPage(adb, artifact_dir, settings.ui_timeout)
        account.assert_logged_in_loaded()
        account.assert_logged_in_actions_visible()
        attach_screenshot(adb, artifact_dir, "02_account_opened_in_drive")

        adb.driving_park()
        account.assert_logged_in_loaded()
        attach_screenshot(adb, artifact_dir, "03_account_after_park")
        attach_text("account state note", "当前台架账号为已登录会员态；未登录/扫码登录驾驶模式需切换账号态后专项执行。")
    finally:
        _restore_park_home(adb, home, profile)
