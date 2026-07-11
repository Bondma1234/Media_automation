from __future__ import annotations

from helpers.allure_helper import allure_step
from pagelocators.kuwo_locators import KuwoHomeLocators, KuwoSearchLocators
from pageobjects.base_page import BasePage


class KuwoSearchPage(BasePage):
    @allure_step("断言搜索页已加载")
    def assert_loaded(self) -> None:
        assert self.wait_for(lambda: self.exists_resource_id(KuwoSearchLocators.EDIT_TEXT)), "搜索输入框未展示"
        assert self.exists_resource_id(KuwoSearchLocators.SEARCH_RECYCLER), "搜索推荐列表未展示"

    @allure_step("关闭搜索页")
    def close(self) -> None:
        self.refresh("before_close_search.xml")
        # 搜索页会拉起软键盘，优先点页面返回按钮，避免一次 Back 只收起键盘。
        self.tap_desc(KuwoSearchLocators.BACK_DESC)

    def has_keyword_entry(self, keyword: str) -> bool:
        self.refresh(f"search_keyword_entry_{keyword}.xml")
        return self.exists_text(keyword)

    @allure_step("点击已有搜索词：{keyword}")
    def search_by_existing_keyword(self, keyword: str) -> None:
        self.refresh(f"before_search_keyword_{keyword}.xml")
        # 中文输入在车机软键盘上不稳定，优先复用搜索页已有历史词/推荐词，避免引入输入法噪声。
        self.tap_text(keyword)

    @allure_step("输入 ASCII 搜索词：{keyword}")
    def search_by_ascii_keyword(self, keyword: str) -> None:
        self.refresh(f"before_input_ascii_keyword_{keyword}.xml")
        self.tap_resource_id(KuwoSearchLocators.EDIT_TEXT)
        # ASCII 词通过 ADB 输入并回车，专门用于验证搜索历史新增。
        self.adb.input_text(keyword)
        self.adb.press_enter()

    @allure_step("断言搜索结果页已加载：{keyword}")
    def assert_result_loaded(self, keyword: str) -> None:
        def loaded() -> bool:
            edit = self.find_by_resource_id(KuwoSearchLocators.EDIT_TEXT)
            edit_text = (edit.attrib.get("text") or "").strip() if edit is not None else ""
            return (
                keyword in edit_text
                and self.exists_resource_id(KuwoSearchLocators.SEARCH_RECYCLER)
                and self.exists_text("歌曲")
                and self.exists_resource_id(KuwoSearchLocators.RESULT_SONG_NAME)
                and self.exists_resource_id(KuwoSearchLocators.RESULT_SONG_SUBTITLE)
            )

        assert self.wait_for(loaded), f"搜索结果页未稳定展示: {keyword}"

    @allure_step("滑动到搜索结果歌手分组")
    def scroll_to_artist_section(self) -> None:
        self.adb.swipe(1000, 720, 1000, 350, 700)

    @allure_step("断言搜索结果歌手分组已展示：{keyword}")
    def assert_artist_section_loaded(self, keyword: str) -> None:
        def loaded() -> bool:
            edit = self.find_by_resource_id(KuwoSearchLocators.EDIT_TEXT)
            edit_text = (edit.attrib.get("text") or "").strip() if edit is not None else ""
            return (
                keyword in edit_text
                and self.exists_text("歌手")
                and self.exists_resource_id(KuwoSearchLocators.ARTIST_NAME)
                and self.exists_resource_id(KuwoSearchLocators.ARTIST_MUSIC_COUNT)
                and self.exists_resource_id(KuwoSearchLocators.ARTIST_ALBUM_COUNT)
            )

        assert self.wait_for(loaded), f"搜索结果歌手分组未展示: {keyword}"

    @allure_step("进入首个歌手详情")
    def open_first_artist_detail(self) -> None:
        self.refresh("before_open_first_artist_detail.xml")
        # 歌手名节点位于歌手结果行内，点击其 bounds 中心能进入歌手详情，不触发歌曲播放。
        self.tap_resource_id(KuwoSearchLocators.ARTIST_NAME)

    def result_song_titles(self) -> list[str]:
        self.refresh("search_result_song_titles.xml")
        titles: list[str] = []
        for node in self.nodes():
            if node.attrib.get("resource-id") == KuwoSearchLocators.RESULT_SONG_NAME:
                title = (node.attrib.get("text") or "").strip()
                if title and title not in titles:
                    titles.append(title)
        return titles

    @allure_step("点击搜索结果歌曲索引：{index}")
    def tap_song_result_by_index(self, index: int) -> str:
        self.refresh(f"before_tap_song_result_{index}.xml")
        song_nodes = [
            node for node in self.nodes() if node.attrib.get("resource-id") == KuwoSearchLocators.RESULT_SONG_NAME
        ]
        assert len(song_nodes) > index, f"搜索结果歌曲数量不足，无法点击第 {index + 1} 首"
        title = (song_nodes[index].attrib.get("text") or "").strip()
        assert title, f"搜索结果第 {index + 1} 首歌曲标题为空"
        self.tap_node_center(song_nodes[index], f"search song result {index + 1}")
        return title

    def miniplayer_title(self) -> str:
        self.refresh("search_miniplayer_title.xml")
        node = self.find_by_resource_id(KuwoHomeLocators.MINI_TITLE)
        assert node is not None, "搜索结果页 MiniPlayer 歌曲标题未展示"
        title = (node.attrib.get("text") or "").strip()
        assert title, "搜索结果页 MiniPlayer 歌曲标题为空"
        return title

    def playing_result_title(self) -> str:
        self.refresh("search_playing_result_title.xml")
        for row in self.nodes():
            if row.attrib.get("class") != "android.widget.LinearLayout":
                continue
            if not (row.attrib.get("content-desc") or "").startswith("###"):
                continue
            has_playing_time = any(
                child.attrib.get("resource-id") == "com.jidouauto.media:id/view_playing" for child in row.iter("node")
            )
            if not has_playing_time:
                continue
            for child in row.iter("node"):
                if child.attrib.get("resource-id") == KuwoSearchLocators.RESULT_SONG_NAME:
                    title = (child.attrib.get("text") or "").strip()
                    if title:
                        return title
        raise AssertionError("搜索结果页未找到正在播放的歌曲行")

    @allure_step("断言歌手详情页已加载：{artist_name}")
    def assert_artist_detail_loaded(self, artist_name: str) -> None:
        def loaded() -> bool:
            title = self.find_by_resource_id(KuwoSearchLocators.DETAIL_TITLE)
            title_text = (title.attrib.get("text") or "").strip() if title is not None else ""
            return title_text == artist_name and all(tab in self.texts() for tab in KuwoSearchLocators.ARTIST_DETAIL_TABS)

        assert self.wait_for(loaded), f"歌手详情页未展示: {artist_name}"

    @allure_step("关闭歌手详情页")
    def close_artist_detail(self) -> None:
        self.adb.press_back()

    @allure_step("点击歌手详情页搜索入口")
    def tap_title_search(self) -> None:
        self.adb.tap(315, 178)

    @allure_step("点击歌手详情页酷我 logo")
    def tap_title_logo(self) -> None:
        self.adb.tap(447, 178)

    @allure_step("点击歌手详情页设置入口")
    def tap_title_settings(self) -> None:
        self.adb.tap(1855, 178)
