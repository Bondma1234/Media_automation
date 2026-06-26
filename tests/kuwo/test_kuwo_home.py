from __future__ import annotations

import time

import pytest

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_screenshot, attach_text
from pagelocators.kuwo_locators import KuwoHomeLocators
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage
from pageobjects.kuwo.kuwo_search_page import KuwoSearchPage
from pageobjects.kuwo.kuwo_settings_page import KuwoSettingsPage


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_home_visible_tabs_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.assert_loaded()
    attach_screenshot(adb, artifact_dir, "01_home_initial")

    for index, tab_name in enumerate(KuwoHomeLocators.TABS, start=2):
        home.switch_tab(tab_name)
        home.assert_tab_content_readable(tab_name)
        home.assert_tab_selected_and_non_empty(tab_name)
        attach_screenshot(adb, artifact_dir, f"{index:02d}_tab_{tab_name}")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_home_content_card_enter_and_back(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.switch_tab("热门")
    card_title = home.first_content_card_title()
    attach_screenshot(adb, artifact_dir, "01_home_before_open_card")

    home.open_content_card_by_title(card_title)
    home.assert_song_list_detail_loaded(card_title)
    attach_screenshot(adb, artifact_dir, "02_song_list_detail")

    home.close_detail_page()
    attach_screenshot(adb, artifact_dir, "03_home_after_back_from_detail")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_song_list_title_actions_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)

    # 热门页当前首屏以“单曲推荐”卡片为主，点击后可能直接切歌；
    # 会员专区首屏是稳定歌单/专题卡，更适合做详情页标题栏强断言。
    for tab_name, prefix in (("会员专区", "song_list"), ("榜单", "ranking_list")):
        home.launch(profile)
        home.switch_tab(tab_name)
        card_title = home.first_content_card_title()
        home.open_content_card_by_title(card_title)
        home.assert_any_song_list_detail_loaded()
        attach_screenshot(adb, artifact_dir, f"01_{prefix}_detail")

        home.tap_title_search()
        search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
        search.assert_loaded()
        attach_screenshot(adb, artifact_dir, f"02_{prefix}_title_search")

        home.launch(profile)
        home.switch_tab(tab_name)
        card_title = home.first_content_card_title()
        home.open_content_card_by_title(card_title)
        home.assert_any_song_list_detail_loaded()
        home.tap_title_settings()
        settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
        settings_page.assert_loaded_readonly()
        attach_screenshot(adb, artifact_dir, f"03_{prefix}_title_settings")

        home.launch(profile)
        home.switch_tab(tab_name)
        card_title = home.first_content_card_title()
        home.open_content_card_by_title(card_title)
        home.assert_any_song_list_detail_loaded()
        home.tap_title_logo()
        home.assert_module_switcher_loaded()
        attach_screenshot(adb, artifact_dir, f"04_{prefix}_title_logo_switcher")

        home.launch(profile)
        home.switch_tab(tab_name)
        card_title = home.first_content_card_title()
        home.open_content_card_by_title(card_title)
        home.assert_any_song_list_detail_loaded()
        home.tap_title_back()
        assert home.wait_for(home.is_loaded), f"{tab_name} 详情页返回后未回到酷我首页"
        attach_screenshot(adb, artifact_dir, f"05_{prefix}_title_back")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_member_playlist_and_library_category_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)

    home.launch(profile)
    member_title = home.open_first_content_card_from_tab("会员专区")
    attach_text("member playlist title", member_title)
    attach_screenshot(adb, artifact_dir, "01_member_playlist_detail")
    home.close_detail_page()
    attach_screenshot(adb, artifact_dir, "02_home_after_member_playlist")

    home.launch(profile)
    home.open_category_from_tab("曲库", "抖音")
    attach_screenshot(adb, artifact_dir, "03_library_douyin_category")
    home.tap_title_back()
    assert home.wait_for(home.is_loaded), "曲库分类返回后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "04_home_after_library_category")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_tingba_category_and_radio_item_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.switch_tab("听吧")
    home.assert_radio_category_grid_loaded()
    attach_screenshot(adb, artifact_dir, "01_tingba_category_grid")

    before_title = home.miniplayer_title()
    home.open_radio_category_by_coordinate("推荐")
    attach_screenshot(adb, artifact_dir, "02_tingba_recommend_list")

    radio_name = home.tap_first_radio_item()
    time.sleep(2)
    attach_screenshot(adb, artifact_dir, "03_tingba_after_radio_tap")
    after_title = home.miniplayer_title()
    assert after_title != before_title, "点击听吧电台条目后 MiniPlayer 标题未变化"
    attach_text("tingba radio item", f"radio_name={radio_name}\nbefore_title={before_title}\nafter_title={after_title}")

    home.tap_title_back()
    assert home.wait_for(home.is_loaded), "听吧分类返回后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "04_home_after_tingba")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_hot_single_song_recommendation_play_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.switch_tab("热门")
    card_title = home.first_content_card_title()
    before_snapshot = adb.kuwo_playback_snapshot()
    attach_screenshot(adb, artifact_dir, "01_hot_single_song_before_tap")

    # 热门页首屏是“每日/语种单曲推荐”类卡片，先验证能进入推荐列表，再点击首行歌曲验证播放。
    home.open_content_card_by_title(card_title)
    first_song = ""
    detail_loaded = False
    for _ in range(12):
        time.sleep(0.5)
        try:
            home.refresh("hot_single_song_detail_state.xml")
            title_node = home.find_by_resource_id(KuwoHomeLocators.DETAIL_TITLE)
            song_node = home.find_by_resource_id(KuwoHomeLocators.SONG_NAME)
            detail_loaded = (
                title_node is not None
                and (title_node.attrib.get("text") or "").strip() == card_title
                and song_node is not None
            )
            if detail_loaded:
                first_song = (song_node.attrib.get("text") or "").strip()
                break
        except Exception:
            pass
    assert detail_loaded and first_song, f"热门推荐列表未加载到可点击歌曲: {card_title}"
    attach_screenshot(adb, artifact_dir, "02_hot_single_song_detail")
    home.tap_first_song_in_detail()
    after_snapshot = {}
    for _ in range(12):
        time.sleep(0.5)
        after_snapshot = adb.kuwo_playback_snapshot()
        if after_snapshot["state"] == "PLAYING":
            break
    attach_screenshot(adb, artifact_dir, "03_hot_single_song_after_tap")
    assert after_snapshot["state"] in {"PLAYING", "BUFFERING"}, f"点击热门单曲推荐后酷我未进入播放链路: {after_snapshot}"
    assert (
        first_song in after_snapshot["description"]
        or after_snapshot["description"] != before_snapshot["description"]
        or after_snapshot["updated"] != before_snapshot["updated"]
    ), "点击热门单曲推荐后媒体会话未发生播放切换"
    attach_text(
        "hot single song recommendation",
        f"card_title={card_title}\nfirst_song={first_song}\nbefore={before_snapshot}\nafter={after_snapshot}",
    )

    home.launch(profile)
    attach_screenshot(adb, artifact_dir, "04_home_after_hot_single_song")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_home_logo_module_switcher_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    attach_screenshot(adb, artifact_dir, "01_home_before_logo_switcher")

    home.open_module_switcher()
    home.assert_module_switcher_loaded()
    attach_screenshot(adb, artifact_dir, "02_logo_module_switcher")

    home.close_module_switcher()
    assert home.wait_for(home.is_loaded), "关闭媒体模块切换弹层后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "03_home_after_logo_switcher")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_song_list_miniplayer_play_pause_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    # 热门页推荐卡会随播放状态进入动态单曲榜单，MiniPlayer 控制验证使用会员专区稳定歌单详情。
    home.switch_tab("会员专区")
    card_title = home.first_content_card_title()
    home.open_content_card_by_title(card_title)
    home.assert_song_list_detail_loaded(card_title)
    attach_screenshot(adb, artifact_dir, "01_song_list_before_play_pause")

    before_desc = home.miniplayer_play_pause_desc()
    home.tap_miniplayer_play_pause()
    assert home.wait_for(lambda: home.miniplayer_play_pause_desc() != before_desc), "MiniPlayer 播放/暂停状态未切换"
    after_desc = home.miniplayer_play_pause_desc()
    attach_screenshot(adb, artifact_dir, "02_song_list_after_play_pause_tap")
    home.tap_miniplayer_play_pause()
    assert home.wait_for(lambda: home.miniplayer_play_pause_desc() != after_desc), "MiniPlayer 播放/暂停状态未恢复"
    restored_desc = home.miniplayer_play_pause_desc()
    attach_screenshot(adb, artifact_dir, "03_song_list_after_restore_tap")
    attach_text(
        "miniplayer play pause control",
        f"before_desc={before_desc}\nafter_desc={after_desc}\nrestored_desc={restored_desc}",
    )

    home.close_detail_page()
    attach_screenshot(adb, artifact_dir, "04_home_after_song_list_play_pause")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_mine_logged_in_vip_status_strong(adb: ADBHelper, profile, artifact_dir, settings):
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.assert_logged_in_vip_on_mine()
    attach_screenshot(adb, artifact_dir, "01_mine_logged_in_vip")
