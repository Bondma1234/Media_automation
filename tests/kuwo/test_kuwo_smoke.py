from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 兼容 VSCode 右上角“Run Python File”直接执行单个测试文件的场景；
# 正常 pytest 执行时项目根目录已由 pytest.ini 注入，不会依赖这段兜底。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_file, attach_screenshot, attach_text
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage
from pageobjects.kuwo.kuwo_player_page import KuwoPlayerPage
from pageobjects.kuwo.kuwo_search_page import KuwoSearchPage
from pageobjects.kuwo.kuwo_settings_page import KuwoSettingsPage


@pytest.mark.p0
@pytest.mark.smoke
@pytest.mark.media
@pytest.mark.kuwo
def test_device_online(adb: ADBHelper, profile, artifact_dir):
    assert adb.is_online(), f"设备未在线: {adb.serial}"
    assert adb.package_version(profile.package), f"未读取到包版本: {profile.package}"
    attach_text("device context", adb.device_info(profile.package))
    attach_screenshot(adb, artifact_dir, "01_device_current_screen")


@pytest.mark.p0
@pytest.mark.smoke
@pytest.mark.media
@pytest.mark.kuwo
def test_launch_kuwo_home(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.assert_loaded()
    attach_screenshot(adb, artifact_dir, "01_kuwo_home_loaded")


@pytest.mark.p1
@pytest.mark.smoke
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_search_page_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_search()

    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    attach_screenshot(adb, artifact_dir, "01_kuwo_search_page")
    search.close()

    assert home.wait_for(home.is_loaded), "关闭搜索页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "02_home_after_search")


@pytest.mark.p1
@pytest.mark.smoke
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_settings_page_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_settings()

    settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
    settings_page.assert_loaded_readonly()
    attach_screenshot(adb, artifact_dir, "01_kuwo_settings_readonly")
    settings_page.close()

    assert home.wait_for(home.is_loaded), "关闭设置页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "02_home_after_settings")


@pytest.mark.p1
@pytest.mark.smoke
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_miniplayer_visible(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.assert_miniplayer_visible()
    attach_screenshot(adb, artifact_dir, "01_kuwo_miniplayer_visible")


@pytest.mark.p1
@pytest.mark.smoke
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_player_page_observation(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_player_from_miniplayer()
    attach_screenshot(adb, artifact_dir, "01_kuwo_player_page_opened")

    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)
    if not player.title_loaded():
        screenshot = adb.capture_screenshot(artifact_dir / "player_page_observation.png")
        attach_file(screenshot, "player page observation", "png")
        pytest.xfail("播放页动态动画导致 UIAutomator dump 未产出新 XML，已保留截图观测")
    if not player.has_visible_content():
        pytest.xfail("CAOIMEDIA-2024: 当前台架播放页内容区为空，先记录为已知缺陷观测")
    player.close()


if __name__ == "__main__":
    # 兼容 VSCode 右上角三角按钮：直接执行本文件时，转交给 pytest 跑冒烟用例。
    raise SystemExit(pytest.main([str(Path(__file__).resolve()), "-q", "-rs", "--clean-alluredir"]))
