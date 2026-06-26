from __future__ import annotations

from pagelocators.kuwo_locators import KuwoHomeLocators, KuwoLibraryLocators
from pageobjects.base_page import BasePage


class KuwoLibraryPage(BasePage):
    def tap_title_back(self) -> None:
        self.adb.tap(185, 178)

    def tap_title_search(self) -> None:
        self.adb.tap(315, 178)

    def tap_title_logo(self) -> None:
        # 下载页加载态下 XML 偶发不可读，标题栏酷我 logo 使用固定坐标兜底。
        self.adb.tap(447, 178)

    def tap_title_settings(self) -> None:
        self.adb.tap(1855, 178)

    def assert_module_switcher_loaded(self) -> None:
        assert self.wait_for(
            lambda: all(self.exists_text(option) for option in KuwoHomeLocators.MODULE_SWITCH_OPTIONS)
        ), "媒体模块切换弹层未展示完整选项"

    def assert_favorite_loaded(self) -> None:
        def loaded() -> bool:
            return self.exists_text(KuwoLibraryLocators.FAVORITE_TITLE) and all(
                self.exists_text(tab) for tab in KuwoLibraryLocators.FAVORITE_TABS
            )

        assert self.wait_for(loaded), "收藏页未展示"

    def assert_recent_loaded(self) -> None:
        def loaded() -> bool:
            return self.exists_text(KuwoLibraryLocators.RECENT_TITLE) and self.exists_resource_id(
                KuwoHomeLocators.HOME_RECYCLER
            )

        assert self.wait_for(loaded), "最近收听页未展示"

    def recent_has_song(self) -> bool:
        self.refresh("recent_list_has_song.xml")
        return self.exists_resource_id(KuwoHomeLocators.SONG_NAME)

    def assert_recent_has_song(self) -> None:
        assert self.wait_for(self.recent_has_song), "最近收听页未展示歌曲记录"

    def tap_first_recent_song(self) -> None:
        self.refresh("before_tap_first_recent_song.xml")
        # 最近收听首行歌曲有稳定 audio_name resource-id，点击文本中心可进入/切换播放。
        self.tap_resource_id(KuwoHomeLocators.SONG_NAME)

    def assert_download_has_song(self) -> None:
        def loaded() -> bool:
            return self.exists_text(KuwoLibraryLocators.DOWNLOAD_TITLE) and self.exists_resource_id(
                KuwoHomeLocators.SONG_NAME
            )

        assert self.wait_for(loaded), "下载页未展示已下载歌曲"

    def switch_favorite_tab(self, tab_name: str) -> None:
        self.refresh(f"before_switch_favorite_tab_{tab_name}.xml")
        assert tab_name in KuwoLibraryLocators.FAVORITE_TABS, f"未登记的收藏 Tab: {tab_name}"
        self.tap_text(tab_name)
        assert self.wait_for(lambda: self.exists_text(tab_name)), f"收藏 Tab 未展示: {tab_name}"

    def assert_favorite_tab_has_content(self, tab_name: str) -> None:
        assert self.favorite_tab_has_content(tab_name), f"收藏 {tab_name} 未展示可播放内容"

    def favorite_tab_has_content(self, tab_name: str) -> bool:
        self.refresh(f"favorite_tab_{tab_name}.xml")
        if tab_name == "单曲":
            return self.exists_resource_id(KuwoHomeLocators.SONG_NAME)
        return self.exists_resource_id(KuwoLibraryLocators.CARD_TITLE)

    def tap_first_favorite_card_play(self) -> None:
        # 收藏专辑/歌单卡片的播放按钮位于首张封面右下角，当前没有独立 resource-id。
        self.adb.tap(398, 592)

    def open_first_favorite_card_detail(self) -> str:
        self.refresh("before_open_first_favorite_card_detail.xml")
        for node in self.nodes():
            desc = (node.attrib.get("content-desc") or "").strip()
            if not desc.startswith("###"):
                continue
            left, top = self._center_of(node)
            bounds = node.attrib.get("bounds", "")
            # 收藏卡片父容器可点击且 content-desc 带标题；排除标题栏按钮和 MiniPlayer 控件。
            if node.attrib.get("clickable") == "true" and top < 640 and desc not in {"###Back", "###搜索", "###设置"}:
                title = desc.removeprefix("###").strip()
                self.adb.tap(left, top)
                return title
        raise AssertionError("收藏页未找到可进入详情的专辑/歌单卡片")
