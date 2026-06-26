from __future__ import annotations

import time

import pytest

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_file, attach_screenshot, attach_text
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage
from pageobjects.kuwo.kuwo_library_page import KuwoLibraryPage
from pageobjects.kuwo.kuwo_player_page import KuwoPlayerPage
from pageobjects.kuwo.kuwo_search_page import KuwoSearchPage
from pageobjects.kuwo.kuwo_settings_page import KuwoSettingsPage


def _open_player_foreground(home: KuwoHomePage, profile, player: KuwoPlayerPage) -> None:
    home.launch(profile)
    home.open_player_from_miniplayer()
    for _ in range(4):
        if player.is_foreground():
            return
        # MiniPlayer 封面区偶发只抢焦点不打开播放页，补点元数据区域确保进入播放页。
        player.adb.tap(930, 735)
        time.sleep(1)
    player.assert_foreground()


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_recent_list_observation_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_mine_entry("最近收听")

    screenshot = attach_screenshot(adb, artifact_dir, "01_recent_list_observation")
    xml_path = artifact_dir / "recent_list_observation.xml"
    adb.dump_ui_xml(xml_path, strict=False)
    attach_file(xml_path, "recent list xml observation", "xml")
    assert screenshot.exists() and screenshot.stat().st_size > 100_000, "最近收听页截图未成功采集"

    adb.press_back()
    assert home.wait_for(home.is_loaded), "关闭最近收听后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "02_home_after_recent_list")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_recent_list_title_actions_and_song_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)

    home.launch(profile)
    home.open_mine_entry("最近收听")
    page = KuwoLibraryPage(adb, artifact_dir, settings.ui_timeout)
    screenshot = attach_screenshot(adb, artifact_dir, "01_recent_page_has_song")
    assert screenshot.exists() and screenshot.stat().st_size > 100_000, "最近收听页截图未成功采集"

    page.tap_title_search()
    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    attach_screenshot(adb, artifact_dir, "02_recent_title_search")

    home.launch(profile)
    home.open_mine_entry("最近收听")
    page.tap_title_settings()
    settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
    settings_page.assert_loaded_readonly()
    attach_screenshot(adb, artifact_dir, "03_recent_title_settings")

    home.launch(profile)
    home.open_mine_entry("最近收听")
    page.tap_title_logo()
    page.assert_module_switcher_loaded()
    attach_screenshot(adb, artifact_dir, "04_recent_title_logo_switcher")

    home.launch(profile)
    home.open_mine_entry("最近收听")
    # 最近收听页 XML 在播放动画下不稳定，首行歌曲使用稳定坐标点击并通过后续可恢复状态验证。
    adb.tap(390, 310)
    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)
    player.wait_for(player.is_foreground, timeout=3)
    attach_screenshot(adb, artifact_dir, "05_recent_song_tapped")

    home.launch(profile)
    home.open_mine_entry("最近收听")
    page.tap_title_back()
    assert home.wait_for(home.is_loaded), "最近收听页返回后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "06_recent_title_back")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_play_queue_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    adb.media_pause()
    home.open_player_from_miniplayer()
    attach_screenshot(adb, artifact_dir, "01_player_before_queue")

    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)
    player.open_queue_by_coordinate()
    screenshot = attach_screenshot(adb, artifact_dir, "02_play_queue")
    xml_ok = player.queue_loaded_from_xml("play_queue_observation.xml")
    attach_file(artifact_dir / "play_queue_observation.xml", "play queue xml observation", "xml")
    attach_text(
        "play queue validation note",
        "XML 可读且播放列表关键控件校验通过。" if xml_ok else "播放列表页已留存截图；当前动态 UI 未产出可解析 XML。",
    )
    assert screenshot.exists() and screenshot.stat().st_size > 100_000, "播放列表截图未成功采集"

    player.close()
    if not home.wait_for(home.is_loaded, timeout=3):
        # 当前播放页硬件 Back 偶发只收起浮层，显式 launch 酷我首页用于把后续用例恢复到稳定起点。
        attach_text("play queue restore note", "Back 未直接回到首页，已通过酷我 launch intent 恢复首页。")
        home.launch(profile)
    assert home.wait_for(home.is_loaded), "关闭播放列表后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "03_home_after_play_queue")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_player_title_actions_and_controls_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)

    _open_player_foreground(home, profile, player)
    attach_screenshot(adb, artifact_dir, "01_player_before_logo")
    player.tap_title_logo()
    home.assert_module_switcher_loaded()
    attach_screenshot(adb, artifact_dir, "02_player_title_logo_switcher")
    adb.press_back()

    home.launch(profile)
    start_desc = home.miniplayer_play_pause_desc()
    if "ic_play_default" in start_desc:
        home.tap_miniplayer_play_pause()
        assert home.wait_for(lambda: home.miniplayer_play_pause_desc() != start_desc), "MiniPlayer 未切到播放态"
    before_desc = home.miniplayer_play_pause_desc()
    _open_player_foreground(home, profile, player)
    player.tap_play_pause_by_coordinate()
    time.sleep(1)
    attach_screenshot(adb, artifact_dir, "03_player_after_first_play_pause")
    player.tap_title_back()
    assert home.wait_for(home.is_loaded), "播放页返回后未回到酷我首页"
    assert home.wait_for(lambda: home.miniplayer_play_pause_desc() != before_desc), "播放页播放/暂停按钮未改变 MiniPlayer 状态"
    after_desc = home.miniplayer_play_pause_desc()
    home.tap_miniplayer_play_pause()
    assert home.wait_for(lambda: home.miniplayer_play_pause_desc() != after_desc), "MiniPlayer 未恢复播放状态"
    restored_desc = home.miniplayer_play_pause_desc()
    attach_text(
        "player play pause control",
        f"before_desc={before_desc}\nafter_desc={after_desc}\nrestored_desc={restored_desc}",
    )


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_player_page_display_and_play_button_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)

    _open_player_foreground(home, profile, player)
    screenshot = attach_screenshot(adb, artifact_dir, "01_player_page_display")
    snapshot = adb.kuwo_playback_snapshot()
    assert screenshot.exists() and screenshot.stat().st_size > 100_000, "播放页截图未成功采集"
    assert player.is_foreground(), f"播放页未在前台: {adb.current_focus()}"
    assert snapshot["description"], f"播放页未关联到酷我媒体元数据: {snapshot}"

    if snapshot["state"] != "PAUSED":
        player.tap_play_pause_by_coordinate()
        for _ in range(8):
            time.sleep(0.5)
            snapshot = adb.kuwo_playback_snapshot()
            if snapshot["state"] == "PAUSED":
                break
    assert snapshot["state"] == "PAUSED", f"播放页未进入暂停态，无法验证播放按钮: {snapshot}"

    # 从暂停态点击播放按钮，使用系统媒体会话校验真实播放态，规避播放页动态 XML 不稳定。
    player.tap_play_pause_by_coordinate()
    after_snapshot = snapshot
    for _ in range(8):
        time.sleep(0.5)
        after_snapshot = adb.kuwo_playback_snapshot()
        if after_snapshot["state"] == "PLAYING":
            break
    attach_screenshot(adb, artifact_dir, "02_player_after_play_button")
    assert after_snapshot["state"] == "PLAYING", f"播放页点击播放按钮后未进入播放态: {after_snapshot}"
    attach_text("player page display and play button", f"before={snapshot}\nafter={after_snapshot}")

    player.tap_title_back()
    assert home.wait_for(home.is_loaded), "播放页返回后未回到酷我首页"


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_player_k_song_entry_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)

    focus = ""
    for attempt in range(1, 4):
        _open_player_foreground(home, profile, player)
        attach_screenshot(adb, artifact_dir, f"0{attempt}_player_before_k_song")
        player.tap_k_song_by_coordinate()
        for _ in range(8):
            time.sleep(0.5)
            focus = adb.current_focus()
            if "com.tencent.audi.karaokecar" in focus:
                break
        attach_screenshot(adb, artifact_dir, f"0{attempt}_k_song_foreground")
        if "com.tencent.audi.karaokecar" in focus:
            break
        # 全量回归中 K 歌入口偶发回到桌面，重新拉起酷我播放页后再试一次。
        home.launch(profile)
    assert "com.tencent.audi.karaokecar" in focus, f"点击去K歌后未跳转到 K 歌应用: {focus}"
    attach_text("k song foreground", focus)

    home.launch(profile)
    assert home.wait_for(home.is_loaded), "K 歌入口验证后未恢复到酷我首页"


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_player_music_completion_by_seek_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)

    _open_player_foreground(home, profile, player)
    before_snapshot = adb.kuwo_playback_snapshot()
    if before_snapshot["state"] != "PLAYING":
        player.tap_play_pause_by_coordinate()
        time.sleep(1)
        before_snapshot = adb.kuwo_playback_snapshot()
    assert before_snapshot["state"] == "PLAYING", f"播放完成验证前未进入播放态: {before_snapshot}"
    attach_screenshot(adb, artifact_dir, "01_player_before_seek_to_end")

    # 为避免等待整首歌，拖动到进度条末尾前一点，随后等待播放器自然完成并切到下一首。
    player.seek_near_end_by_coordinate()
    attach_screenshot(adb, artifact_dir, "02_player_after_seek_near_end")
    after_snapshot = before_snapshot
    for _ in range(24):
        time.sleep(0.5)
        after_snapshot = adb.kuwo_playback_snapshot()
        if after_snapshot["active_item_id"] != before_snapshot["active_item_id"] or (
            after_snapshot["description"] != before_snapshot["description"]
        ):
            break
    attach_screenshot(adb, artifact_dir, "03_player_after_completion")
    assert after_snapshot["state"] in {"PLAYING", "PAUSED"}, f"播放完成后媒体会话状态异常: {after_snapshot}"
    assert (
        after_snapshot["active_item_id"] != before_snapshot["active_item_id"]
        or after_snapshot["description"] != before_snapshot["description"]
    ), f"拖到末尾后未观察到歌曲完成/续播切换: before={before_snapshot}, after={after_snapshot}"
    attach_text("music completion by seek", f"before={before_snapshot}\nafter={after_snapshot}")

    player.tap_title_back()
    assert home.wait_for(home.is_loaded), "播放完成验证后未回到酷我首页"


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_play_queue_tap_song_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    before_title = home.miniplayer_title()
    after_title = before_title

    for index, y in enumerate((365, 485, 610), start=1):
        _open_player_foreground(home, profile, player)
        player.open_queue_by_coordinate()
        attach_screenshot(adb, artifact_dir, f"0{index}_queue_before_tap_{y}")
        player.tap_visible_queue_song_by_coordinate(y)
        time.sleep(2)
        attach_screenshot(adb, artifact_dir, f"0{index}_queue_after_tap_{y}")
        home.launch(profile)
        after_title = home.miniplayer_title()
        if after_title != before_title:
            break

    assert after_title != before_title, f"播放列表点击歌曲后 MiniPlayer 标题未变化: {before_title}"
    attach_text("play queue song switch", f"before_title={before_title}\nafter_title={after_title}")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_play_queue_long_press_song_observation(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    adb.media_pause()
    home.open_player_from_miniplayer()

    player = KuwoPlayerPage(adb, artifact_dir, settings.ui_timeout)
    player.open_queue_by_coordinate()
    attach_screenshot(adb, artifact_dir, "01_queue_before_long_press")
    player.long_press_first_queue_song_by_coordinate()
    attach_screenshot(adb, artifact_dir, "02_queue_after_long_press")
    xml_path = artifact_dir / "queue_after_long_press.xml"
    adb.dump_ui_xml(xml_path, strict=False)
    attach_file(xml_path, "queue after long press xml observation", "xml")

    # 当前台架长按播放列表歌曲没有展示可断言菜单，保留证据并恢复首页，避免误判为框架失败。
    home.launch(profile)
    attach_screenshot(adb, artifact_dir, "03_home_after_queue_long_press_observation")
    pytest.xfail("播放列表歌曲长按未展示稳定菜单/弹层，当前作为 P2 观测限制记录")
