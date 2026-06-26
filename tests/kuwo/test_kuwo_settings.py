from __future__ import annotations

import pytest

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_screenshot
from pagelocators.kuwo_locators import KuwoSettingsLocators
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


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_settings_about_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home, settings_page = _open_settings_about(adb, profile, artifact_dir, settings)

    settings_page.assert_about_loaded()
    attach_screenshot(adb, artifact_dir, "01_settings_about")

    settings_page.close_subpage()
    assert settings_page.wait_for(lambda: settings_page.exists_text(KuwoSettingsLocators.TITLE)), "关闭关于页后未回到设置页"
    settings_page.close()
    assert home.wait_for(home.is_loaded), "关闭设置页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "02_home_after_settings_about")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_settings_legal_documents_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home, settings_page = _open_settings_about(adb, profile, artifact_dir, settings)

    legal_entries = (
        (KuwoSettingsLocators.USER_AGREEMENT, "user_agreement", settings_page.assert_legal_info_loaded),
        (KuwoSettingsLocators.PRIVACY_POLICY, "privacy_policy", settings_page.assert_legal_info_loaded),
        (
            KuwoSettingsLocators.OPEN_SOURCE_DISCLAIMER,
            "open_source_disclaimer",
            settings_page.assert_open_source_loaded,
        ),
    )
    for entry_name, screenshot_name, assertion in legal_entries:
        settings_page.open_about_entry(entry_name)
        assertion()
        attach_screenshot(adb, artifact_dir, f"01_{screenshot_name}")
        settings_page.close_subpage()
        if not settings_page.wait_for(settings_page.is_about_loaded, timeout=3):
            # 法律信息页属于跨包 Activity，Back 可能先回到法律 App 概览；用 launch intent 恢复酷我首页再进入关于页。
            home.launch(profile)
            home.open_settings()
            settings_page.assert_loaded_readonly()
            settings_page.open_about()

    settings_page.close_subpage()
    assert settings_page.wait_for(lambda: settings_page.exists_text(KuwoSettingsLocators.TITLE)), "关闭关于页后未回到设置页"
    settings_page.close()
    assert home.wait_for(home.is_loaded), "关闭设置页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "02_home_after_legal_documents")
