from __future__ import annotations

from config.media_profiles import MediaProfile
from helpers.allure_helper import allure_step
from pagelocators.kuwo_locators import KuwoAccountLocators, KuwoHomeLocators
from pageobjects.base_page import BasePage


class KuwoHomePage(BasePage):
    @allure_step("打开酷我首页")
    def launch(self, profile: MediaProfile) -> None:
        self.adb.start_activity(profile)
        if self.wait_for(self.is_loaded, timeout=3):
            return
        # 同一个 Activity 内的搜索/设置/播放子页面可能不会被 launch intent 重置，逐级返回到首页。
        for _ in range(3):
            self.adb.press_back()
            if self.wait_for(self.is_loaded, timeout=3):
                return
        assert self.wait_for(self.is_loaded), "酷我首页未在超时时间内加载完成"

    def is_loaded(self) -> bool:
        return self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER) and self.exists_desc(
            KuwoHomeLocators.SEARCH_DESC
        ) and self.exists_text("热门")

    @allure_step("断言酷我首页已加载")
    def assert_loaded(self) -> None:
        self.refresh("kuwo_home.xml")
        assert self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER), "首页列表未展示"
        assert self.exists_desc(KuwoHomeLocators.SEARCH_DESC), "首页搜索入口未展示"
        assert self.exists_desc(KuwoHomeLocators.SETTINGS_DESC), "首页设置入口未展示"
        missing_tabs = [tab for tab in KuwoHomeLocators.TABS if not self.exists_text(tab)]
        assert not missing_tabs, f"首页 Tab 缺失: {missing_tabs}"

    @allure_step("断言首页 MiniPlayer 控件完整展示")
    def assert_miniplayer_visible(self) -> None:
        self.refresh("kuwo_miniplayer.xml")
        required = [
            KuwoHomeLocators.MINI_PREV,
            KuwoHomeLocators.MINI_PLAY_PAUSE,
            KuwoHomeLocators.MINI_NEXT,
            KuwoHomeLocators.MINI_TITLE,
            KuwoHomeLocators.MINI_SUBTITLE,
            KuwoHomeLocators.MINI_TIME,
        ]
        missing = [locator for locator in required if not self.exists_resource_id(locator)]
        assert not missing, f"MiniPlayer 控件缺失: {missing}"

    @allure_step("打开媒体模块切换弹层")
    def open_module_switcher(self) -> None:
        # 标题栏左侧酷我 logo 当前没有稳定 resource-id，使用固定 logo 区域坐标打开媒体模块切换弹层。
        self.adb.tap(315, 178)

    @allure_step("断言媒体模块切换弹层已展示")
    def assert_module_switcher_loaded(self) -> None:
        assert self.wait_for(
            lambda: all(self.exists_text(option) for option in KuwoHomeLocators.MODULE_SWITCH_OPTIONS)
        ), "媒体模块切换弹层未展示完整选项"

    @allure_step("关闭媒体模块切换弹层")
    def close_module_switcher(self) -> None:
        self.adb.press_back()

    def miniplayer_play_pause_desc(self) -> str:
        self.refresh("miniplayer_play_pause_state.xml")
        node = self.find_by_resource_id(KuwoHomeLocators.MINI_PLAY_PAUSE)
        assert node is not None, "MiniPlayer 播放/暂停按钮未展示"
        desc_values = [(node.attrib.get("content-desc") or "").strip()]
        desc_values.extend(
            (child.attrib.get("content-desc") or "").strip() for child in node.iter("node") if child is not node
        )
        return "|".join(value for value in desc_values if value)

    def miniplayer_title(self) -> str:
        self.refresh("miniplayer_title_state.xml")
        node = self.find_by_resource_id(KuwoHomeLocators.MINI_TITLE)
        assert node is not None, "MiniPlayer 歌曲标题未展示"
        title = (node.attrib.get("text") or "").strip()
        assert title, "MiniPlayer 歌曲标题为空"
        return title

    @allure_step("点击 MiniPlayer 播放暂停按钮")
    def tap_miniplayer_play_pause(self) -> None:
        self.refresh("before_tap_miniplayer_play_pause.xml")
        # 媒体播放/暂停属于允许的可恢复控制；用例结束会再次点击恢复到接近原状态。
        self.tap_resource_id(KuwoHomeLocators.MINI_PLAY_PAUSE)

    @allure_step("切换首页 Tab：{tab_name}")
    def switch_tab(self, tab_name: str) -> None:
        self.refresh(f"before_switch_tab_{tab_name}.xml")
        assert tab_name in KuwoHomeLocators.TABS, f"未登记的酷我首页 Tab: {tab_name}"
        if self.exists_desc(f"content={tab_name}"):
            self.tap_desc(f"content={tab_name}")
        else:
            self.tap_text(tab_name)
        assert self.wait_for(lambda: self.is_tab_selected(tab_name)), f"切换到 Tab 后页面未稳定: {tab_name}"

    def is_tab_selected(self, tab_name: str) -> bool:
        tab_node = self.find_by_desc(f"content={tab_name}", exact=True)
        return (
            tab_node is not None
            and tab_node.attrib.get("selected") == "true"
            and self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER)
        )

    @allure_step("断言首页 Tab 内容可读：{tab_name}")
    def assert_tab_content_readable(self, tab_name: str) -> None:
        self.refresh(f"tab_{tab_name}.xml")
        assert self.exists_text(tab_name), f"Tab 文案未展示: {tab_name}"
        assert self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER), f"Tab 内容列表未展示: {tab_name}"

    @allure_step("断言首页 Tab 已选中且内容非空：{tab_name}")
    def assert_tab_selected_and_non_empty(self, tab_name: str) -> None:
        self.refresh(f"strong_tab_{tab_name}.xml")
        tab_node = self.find_by_desc(f"content={tab_name}", exact=True)
        assert tab_node is not None, f"Tab 节点未展示: {tab_name}"
        assert tab_node.attrib.get("selected") == "true", f"Tab 未处于选中状态: {tab_name}"
        assert self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER), f"Tab 内容列表未展示: {tab_name}"
        if tab_name == "我的":
            # 我的页至少要展示三大稳定入口；账号态可能登录/未登录，但入口区必须可用。
            for entry_name in ("最近收听", "下载", "收藏"):
                assert self.exists_desc(entry_name), f"我的页入口未展示: {entry_name}"
            return
        assert (
            self.visible_card_title_count() > 0 or self.visible_content_text_count() > 0
        ), f"Tab 未展示可识别业务内容: {tab_name}"

    def visible_card_title_count(self) -> int:
        return sum(
            1
            for node in self.nodes()
            if node.attrib.get("resource-id") == KuwoHomeLocators.CARD_TITLE and (node.attrib.get("text") or "").strip()
        )

    def visible_content_text_count(self) -> int:
        ignored = set(KuwoHomeLocators.TABS) | {"搜索", "设置"}
        count = 0
        for node in self.nodes():
            text = (node.attrib.get("text") or "").strip()
            if text and text not in ignored:
                count += 1
        return count

    def first_content_card_title(self) -> str:
        self.refresh("before_read_first_card.xml")
        for node in self.nodes():
            if node.attrib.get("resource-id") == KuwoHomeLocators.CARD_TITLE:
                title = (node.attrib.get("text") or "").strip()
                if title:
                    return title
        raise AssertionError("首页未找到可进入的内容卡片标题")

    @allure_step("打开首页内容卡：{title}")
    def open_content_card_by_title(self, title: str) -> None:
        self.refresh(f"before_open_card_{title}.xml")
        # 内容卡片本身的 content-desc 包含标题，优先点父容器；找不到时再点标题文字中心。
        if self.exists_desc(title):
            self.tap_desc(title)
        else:
            self.tap_text(title)

    @allure_step("打开 {tab_name} Tab 首张内容卡")
    def open_first_content_card_from_tab(self, tab_name: str) -> str:
        self.switch_tab(tab_name)
        self.assert_tab_selected_and_non_empty(tab_name)
        title = self.first_content_card_title()
        self.open_content_card_by_title(title)
        self.assert_song_list_detail_loaded(title)
        return title

    @allure_step("断言歌曲列表详情页已加载：{title}")
    def assert_song_list_detail_loaded(self, title: str) -> None:
        def loaded() -> bool:
            title_node = self.find_by_resource_id(KuwoHomeLocators.DETAIL_TITLE)
            title_text = (title_node.attrib.get("text") or "").strip() if title_node is not None else ""
            return (
                title_text == title
                and self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER)
                and self.exists_resource_id(KuwoHomeLocators.SONG_NAME)
            )

        assert self.wait_for(loaded), f"歌单/歌曲列表页未加载: {title}"

    @allure_step("断言歌曲列表详情页已加载")
    def assert_any_song_list_detail_loaded(self) -> None:
        def loaded() -> bool:
            title_node = self.find_by_resource_id(KuwoHomeLocators.DETAIL_TITLE)
            title_text = (title_node.attrib.get("text") or "").strip() if title_node is not None else ""
            return bool(title_text) and self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER)

        assert self.wait_for(loaded), "歌曲/榜单/专辑列表详情页未加载"

    @allure_step("打开 {tab_name} Tab 分类：{category_name}")
    def open_category_from_tab(self, tab_name: str, category_name: str) -> None:
        self.switch_tab(tab_name)
        self.refresh(f"before_open_category_{tab_name}_{category_name}.xml")
        self.tap_text(category_name)
        assert self.wait_for(lambda: self.category_list_loaded(category_name)), f"分类列表未加载: {category_name}"

    def category_list_loaded(self, category_name: str) -> bool:
        title_node = self.find_by_resource_id(KuwoHomeLocators.DETAIL_TITLE)
        title_text = (title_node.attrib.get("text") or "").strip() if title_node is not None else ""
        return (
            title_text == category_name
            and self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER)
            and self.visible_card_title_count() > 0
        )

    @allure_step("断言听吧分类入口完整展示")
    def assert_radio_category_grid_loaded(self) -> None:
        self.refresh("tingba_category_grid.xml")
        required = ("推荐", "心情", "经典", "车载")
        missing = [name for name in required if not self.exists_text(name)]
        assert not missing, f"听吧分类入口缺失: {missing}"

    @allure_step("打开听吧分类：{category_name}")
    def open_radio_category_by_coordinate(self, category_name: str = "推荐") -> None:
        # 听吧分类入口没有稳定的 resource-id；首个分类“推荐”固定在内容区左上，用坐标进入电台列表。
        self.adb.tap(330, 330)
        assert self.wait_for(lambda: self.radio_list_loaded(category_name)), f"听吧分类列表未加载: {category_name}"

    def radio_list_loaded(self, category_name: str) -> bool:
        title_node = self.find_by_resource_id(KuwoHomeLocators.DETAIL_TITLE)
        title_text = (title_node.attrib.get("text") or "").strip() if title_node is not None else ""
        return (
            title_text == category_name
            and self.exists_resource_id(KuwoHomeLocators.HOME_RECYCLER)
            and self.exists_resource_id(KuwoHomeLocators.RADIO_NAME)
            and self.exists_resource_id(KuwoHomeLocators.RADIO_PLAY_COUNT)
        )

    @allure_step("点击首个电台条目")
    def tap_first_radio_item(self) -> str:
        self.refresh("before_tap_first_radio_item.xml")
        node = self.find_by_resource_id(KuwoHomeLocators.RADIO_NAME)
        assert node is not None, "听吧电台列表未展示电台条目"
        title = (node.attrib.get("text") or "").strip()
        assert title, "听吧电台条目标题为空"
        self.tap_node_center(node, "first radio item")
        return title

    @allure_step("点击详情页首条歌曲")
    def tap_first_song_in_detail(self) -> str:
        self.refresh("before_tap_first_detail_song.xml")
        node = self.find_by_resource_id(KuwoHomeLocators.SONG_NAME)
        assert node is not None, "详情页未展示歌曲条目"
        title = (node.attrib.get("text") or "").strip()
        assert title, "详情页首条歌曲标题为空"
        self.tap_node_center(node, "first detail song")
        return title

    @allure_step("关闭详情页并返回酷我首页")
    def close_detail_page(self) -> None:
        self.adb.press_back()
        assert self.wait_for(self.is_loaded), "返回后未回到酷我首页"

    @allure_step("点击详情页返回按钮")
    def tap_title_back(self) -> None:
        self.adb.tap(185, 178)

    @allure_step("点击详情页搜索入口")
    def tap_title_search(self) -> None:
        self.adb.tap(315, 178)

    @allure_step("点击详情页酷我 logo")
    def tap_title_logo(self) -> None:
        self.adb.tap(447, 178)

    @allure_step("点击详情页设置入口")
    def tap_title_settings(self) -> None:
        self.adb.tap(1855, 178)

    @allure_step("打开我的页入口：{entry_name}")
    def open_mine_entry(self, entry_name: str) -> None:
        self.switch_tab("我的")
        self.refresh(f"before_open_mine_entry_{entry_name}.xml")
        self.tap_desc(entry_name)

    def is_logged_in_on_mine(self) -> bool:
        self.refresh("mine_account_state.xml")
        return self.exists_resource_id(KuwoAccountLocators.NICKNAME) and self.exists_resource_id(
            KuwoAccountLocators.VIP_TIME
        )

    @allure_step("断言我的页已登录 VIP 信息展示")
    def assert_logged_in_vip_on_mine(self) -> None:
        self.switch_tab("我的")
        self.refresh("mine_logged_in_vip_state.xml")
        nickname = self.find_by_resource_id(KuwoAccountLocators.NICKNAME)
        vip_time = self.find_by_resource_id(KuwoAccountLocators.VIP_TIME)
        assert nickname is not None and (nickname.attrib.get("text") or "").strip(), "我的页未展示已登录昵称"
        assert vip_time is not None and "有效期至" in (vip_time.attrib.get("text") or ""), "我的页未展示 VIP 有效期"

    @allure_step("从我的页进入账户详情")
    def open_account_from_mine(self) -> None:
        self.switch_tab("我的")
        self.refresh("before_open_account_from_mine.xml")
        # 账号头像区域没有文案，使用稳定 resource-id 进入账户详情；不触碰登出、续费、绑定入口。
        self.tap_resource_id(KuwoAccountLocators.AVATAR)

    @allure_step("从酷我首页进入搜索页")
    def open_search(self) -> None:
        self.refresh("before_open_search.xml")
        self.tap_desc(KuwoHomeLocators.SEARCH_DESC)

    @allure_step("从酷我首页进入设置页")
    def open_settings(self) -> None:
        self.refresh("before_open_settings.xml")
        self.tap_desc(KuwoHomeLocators.SETTINGS_DESC)

    @allure_step("从 MiniPlayer 打开播放页")
    def open_player_from_miniplayer(self) -> None:
        self.refresh("before_open_player.xml")
        self.tap_resource_id(KuwoHomeLocators.MINI_COVER)
