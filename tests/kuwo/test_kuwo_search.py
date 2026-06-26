from __future__ import annotations

import time

import pytest

from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_screenshot, attach_text
from pagelocators.kuwo_locators import KuwoSearchLocators
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage
from pageobjects.kuwo.kuwo_search_page import KuwoSearchPage
from pageobjects.kuwo.kuwo_settings_page import KuwoSettingsPage


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_search_history_keyword_results_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    keyword = "周杰伦"
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_search()

    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    attach_screenshot(adb, artifact_dir, "01_search_page_history")
    if not search.has_keyword_entry(keyword):
        pytest.skip(f"搜索页未发现可复用历史词/推荐词: {keyword}")

    search.search_by_existing_keyword(keyword)
    search.assert_result_loaded(keyword)
    attach_screenshot(adb, artifact_dir, "02_search_result_keyword")

    search.close()
    assert home.wait_for(home.is_loaded), "关闭搜索结果页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "03_home_after_search_result")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_search_artist_section_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    keyword = "周杰伦"
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_search()

    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    if not search.has_keyword_entry(keyword):
        pytest.skip(f"搜索页未发现可复用历史词/推荐词: {keyword}")

    search.search_by_existing_keyword(keyword)
    search.assert_result_loaded(keyword)
    attach_screenshot(adb, artifact_dir, "01_song_result_section")

    search.scroll_to_artist_section()
    search.assert_artist_section_loaded(keyword)
    attach_screenshot(adb, artifact_dir, "02_artist_result_section")

    search.close()
    assert home.wait_for(home.is_loaded), "关闭搜索结果页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "03_home_after_artist_section")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_search_multiple_result_song_switch_strong(adb: ADBHelper, profile, artifact_dir, settings):
    keyword = "周杰伦"
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_search()

    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    if not search.has_keyword_entry(keyword):
        pytest.skip(f"搜索页未发现可复用历史词/推荐词: {keyword}")

    search.search_by_existing_keyword(keyword)
    search.assert_result_loaded(keyword)
    titles = search.result_song_titles()
    assert len(titles) >= 2, f"搜索结果歌曲数量不足，无法验证多结果切换: {titles}"
    attach_screenshot(adb, artifact_dir, "01_search_results_before_switch")

    first_title = search.tap_song_result_by_index(0)
    time.sleep(2)
    first_playing = search.playing_result_title()
    attach_screenshot(adb, artifact_dir, "02_search_first_song_playing")

    second_title = search.tap_song_result_by_index(1)
    time.sleep(2)
    second_playing = search.playing_result_title()
    attach_screenshot(adb, artifact_dir, "03_search_second_song_playing")

    assert first_playing != second_playing, f"搜索结果切歌后 MiniPlayer 标题未变化: {first_playing}"
    attach_text(
        "search result song switch",
        f"first_tapped={first_title}\nfirst_playing={first_playing}\nsecond_tapped={second_title}\nsecond_playing={second_playing}",
    )

    search.close()
    assert home.wait_for(home.is_loaded), "关闭搜索结果页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "04_home_after_search_result_switch")


@pytest.mark.p1
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_search_artist_detail_readonly(adb: ADBHelper, profile, artifact_dir, settings):
    keyword = "周杰伦"
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_search()

    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    if not search.has_keyword_entry(keyword):
        pytest.skip(f"搜索页未发现可复用历史词/推荐词: {keyword}")

    search.search_by_existing_keyword(keyword)
    search.assert_result_loaded(keyword)
    search.scroll_to_artist_section()
    search.assert_artist_section_loaded(keyword)
    attach_screenshot(adb, artifact_dir, "01_artist_section_before_detail")

    search.open_first_artist_detail()
    search.assert_artist_detail_loaded(keyword)
    attach_screenshot(adb, artifact_dir, "02_artist_detail")

    search.close_artist_detail()
    assert search.wait_for(lambda: search.exists_text("歌手") and search.exists_resource_id(KuwoSearchLocators.ARTIST_NAME)), (
        "关闭歌手详情后未回到搜索结果页"
    )
    search.close()
    assert home.wait_for(home.is_loaded), "关闭搜索结果页后未回到酷我首页"
    attach_screenshot(adb, artifact_dir, "03_home_after_artist_detail")


@pytest.mark.p2
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_artist_detail_title_actions_strong(adb: ADBHelper, profile, artifact_dir, settings):
    keyword = "周杰伦"
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)

    for action_name in ("search", "settings", "logo"):
        home.launch(profile)
        home.open_search()
        search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
        search.assert_loaded()
        if not search.has_keyword_entry(keyword):
            pytest.skip(f"搜索页未发现可复用历史词/推荐词: {keyword}")

        search.search_by_existing_keyword(keyword)
        search.assert_result_loaded(keyword)
        search.scroll_to_artist_section()
        search.assert_artist_section_loaded(keyword)
        search.open_first_artist_detail()
        search.assert_artist_detail_loaded(keyword)
        attach_screenshot(adb, artifact_dir, f"01_artist_detail_before_{action_name}")

        if action_name == "search":
            search.tap_title_search()
            search.assert_loaded()
        elif action_name == "settings":
            search.tap_title_settings()
            settings_page = KuwoSettingsPage(adb, artifact_dir, settings.ui_timeout)
            settings_page.assert_loaded_readonly()
        else:
            search.tap_title_logo()
            home.assert_module_switcher_loaded()
        attach_screenshot(adb, artifact_dir, f"02_artist_detail_{action_name}_opened")


@pytest.mark.p1
@pytest.mark.stateful
@pytest.mark.media
@pytest.mark.kuwo
def test_kuwo_search_history_added_stateful(adb: ADBHelper, profile, artifact_dir, settings):
    keyword = "autotest0528"
    home = KuwoHomePage(adb, artifact_dir, settings.ui_timeout)
    home.launch(profile)
    home.open_search()

    search = KuwoSearchPage(adb, artifact_dir, settings.ui_timeout)
    search.assert_loaded()
    attach_screenshot(adb, artifact_dir, "01_search_before_ascii_keyword")
    search.search_by_ascii_keyword(keyword)
    search.assert_result_loaded(keyword)
    attach_screenshot(adb, artifact_dir, "02_search_result_ascii_keyword")

    search.close()
    if not home.wait_for(home.is_loaded, timeout=3):
        home.launch(profile)
    home.open_search()
    search.assert_loaded()
    assert search.has_keyword_entry(keyword), f"搜索历史未新增测试词: {keyword}"
    attach_screenshot(adb, artifact_dir, "03_search_history_after_ascii_keyword")

    search.close()
    assert home.wait_for(home.is_loaded), "关闭搜索页后未回到酷我首页"
