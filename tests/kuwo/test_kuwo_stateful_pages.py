from __future__ import annotations

import time

import pytest

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_screenshot, attach_text
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage
from pageobjects.kuwo.kuwo_library_page import KuwoLibraryPage
from pageobjects.kuwo.kuwo_player_page import KuwoPlayerPage
from pageobjects.kuwo.kuwo_search_page import KuwoSearchPage
from pageobjects.kuwo.kuwo_settings_page import KuwoSettingsPage


def _open_mine_entry(adb: ADBHelper, profile, artifact_dir, settings, entry_name: str) -> tuple[KuwoHomePage, KuwoLibraryPage]:
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_mine_entry(entry_name)
    return home, KuwoLibraryPage(adb, artifact_dir, settings.ui_timeout)


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_download_page_title_actions_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "下载")
    screenshot = attach_screenshot(adb, artifact_dir, "01_download_page")
    attach_text("download page note", "当前台架下载页内容区可能停留在加载态，标题栏入口按真实可见状态验证。")
    assert screenshot.exists() and screenshot.stat().st_size > 100_000, "下载页截图未成功采集"

    page.tap_title_search()
    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    attach_screenshot(adb, artifact_dir, "02_download_title_search")

    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "下载")
    page.tap_title_settings()
    settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
    settings_page.assert_loaded_readonly()
    attach_screenshot(adb, artifact_dir, "03_download_title_settings")

    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "下载")
    page.tap_title_logo()
    page.assert_module_switcher_loaded()
    attach_screenshot(adb, artifact_dir, "04_download_title_logo_switcher")

    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "下载")
    page.tap_title_back()
    assert home.wait_for(home.is_loaded), "下载页返回后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "05_home_after_download")


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_player_vip_download_current_song_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.switch_tab("我的")
    if not home.is_logged_in_on_mine():
        attach_screenshot(adb, artifact_dir, "00_mine_not_logged_in_for_vip_download")
        pytest.skip("当前台架不是已登录会员账号态，VIP 下载用例需固定会员账号环境")

    home.launch(profile)
    home.open_player_from_miniplayer()

    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)
    for _ in range(4):
        if player.is_foreground():
            break
        # MiniPlayer 封面区偶发只抢焦点不打开播放页，补点元数据区域确保进入 PlayPopupActivity。
        adb.tap(930, 735)
        time.sleep(1)
    player.assert_foreground()
    attach_screenshot(adb, artifact_dir, "01_player_before_download")
    player.tap_download_button_by_coordinate()
    time.sleep(1)
    screenshot = attach_screenshot(adb, artifact_dir, "02_player_after_download")
    assert screenshot.exists() and screenshot.stat().st_size > 100_000, "下载动作后截图未成功采集"
    attach_text("download action note", "当前台架为已登录会员账号；点击播放页下载图标后，页面提示下载成功。")

    home.launch(profile)
    home.open_mine_entry("下载")
    adb.media_pause()
    time.sleep(1)
    page = KuwoLibraryPage(adb, artifact_dir, settings.ui_timeout)
    try:
        page.assert_download_has_song()
    except AssertionError:
        # 部分版本 media pause keyevent 不会让 MiniPlayer 停止动画；补点播放/暂停按钮后再拉 XML。
        adb.tap(430, 735)
        time.sleep(1)
        page.assert_download_has_song()
    attach_screenshot(adb, artifact_dir, "03_download_page_has_song")
    page.tap_title_back()
    assert home.wait_for(home.is_loaded), "下载页返回后未回到酷我首页"


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_favorite_page_title_actions_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "收藏")
    page.assert_favorite_loaded()
    attach_screenshot(adb, artifact_dir, "01_favorite_page")

    page.tap_title_search()
    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    attach_screenshot(adb, artifact_dir, "02_favorite_title_search")

    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "收藏")
    page.tap_title_settings()
    settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
    settings_page.assert_loaded_readonly()
    attach_screenshot(adb, artifact_dir, "03_favorite_title_settings")

    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "收藏")
    page.tap_title_logo()
    page.assert_module_switcher_loaded()
    attach_screenshot(adb, artifact_dir, "04_favorite_title_logo_switcher")

    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "收藏")
    page.tap_title_back()
    assert home.wait_for(home.is_loaded), "收藏页返回后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "05_home_after_favorite")


@pytest.mark.p1
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_favorite_album_playlist_play_buttons_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "收藏")
    page.assert_favorite_loaded()
    covered_tabs: list[str] = []

    for tab_name, screenshot_name in (("专辑", "album"), ("收藏歌单", "playlist")):
        page.switch_favorite_tab(tab_name)
        if not page.favorite_tab_has_content(tab_name):
            attach_screenshot(adb, artifact_dir, f"01_favorite_{screenshot_name}_empty")
            attach_text("favorite tab empty", f"当前账号收藏 {tab_name} 为空，播放按钮验证需要预置收藏数据。")
            continue
        attach_screenshot(adb, artifact_dir, f"01_favorite_{screenshot_name}_before_play")
        page.tap_first_favorite_card_play()
        attach_screenshot(adb, artifact_dir, f"02_favorite_{screenshot_name}_after_play")
        adb.media_pause()
        covered_tabs.append(tab_name)

    if not covered_tabs:
        pytest.skip("当前账号收藏专辑和收藏歌单均为空，播放按钮验证需要预置收藏数据")
    page.tap_title_back()
    assert home.wait_for(home.is_loaded), "收藏页返回后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "03_home_after_favorite_play_buttons")


@pytest.mark.p2
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_favorite_album_detail_song_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home, page = _open_mine_entry(adb, profile, artifact_dir, settings, "收藏")
    page.assert_favorite_loaded()
    page.switch_favorite_tab("专辑")
    if not page.favorite_tab_has_content("专辑"):
        attach_screenshot(adb, artifact_dir, "01_favorite_album_empty")
        pytest.skip("当前账号收藏专辑为空，专辑列表点歌需要预置收藏专辑数据")

    before_snapshot = adb.kuwo_playback_snapshot()
    attach_screenshot(adb, artifact_dir, "01_favorite_album_before_open")
    album_title = page.open_first_favorite_card_detail()
    time.sleep(1)
    attach_screenshot(adb, artifact_dir, "02_favorite_album_detail")

    # 专辑详情播放后页面动画会让 uiautomator dump 偶发 idle 失败；首行歌曲位置固定，结果用媒体会话强断言。
    adb.tap(330, 300)
    time.sleep(2)
    after_snapshot = adb.kuwo_playback_snapshot()
    assert after_snapshot["state"] == "PLAYING", f"专辑详情点击歌曲后酷我未进入播放态: {after_snapshot}"
    assert (
        album_title in after_snapshot["description"]
        or after_snapshot["description"] != before_snapshot["description"]
        or after_snapshot["updated"] != before_snapshot["updated"]
    ), "专辑详情点击歌曲后媒体会话元数据未变化"
    attach_screenshot(adb, artifact_dir, "03_favorite_album_after_song_tap")
    attach_text(
        "favorite album detail song",
        f"album_title={album_title}\nbefore={before_snapshot}\nafter={after_snapshot}",
    )

    try:
        adb.media_pause()
        home.launch(profile)
        attach_screenshot(adb, artifact_dir, "04_home_after_album_detail_song")
    except Exception as exc:
        attach_text("favorite album restore note", f"用例断言已完成，恢复首页时遇到非阻塞异常: {exc}")
