from __future__ import annotations

from helpers.allure_helper import allure_step
from pagelocators.kuwo_locators import KuwoSettingsLocators
from pageobjects.base_page import BasePage


class KuwoSettingsPage(BasePage):
    @allure_step("断言设置页只读条目已展示")
    def assert_loaded_readonly(self) -> None:
        assert self.wait_for(lambda: self.exists_text(KuwoSettingsLocators.TITLE)), "设置页标题未展示"
        missing = [text for text in KuwoSettingsLocators.LIST_TEXTS if not self.exists_text(text)]
        assert not missing, f"设置页列表项缺失: {missing}"

    def scroll_to_bottom(self) -> None:
        # 设置页底部才展示“关于”入口，滑动只用于暴露只读入口，不点击任何开关。
        self.adb.swipe(1000, 720, 1000, 280, 700)

    @allure_step("进入设置关于页")
    def open_about(self) -> None:
        self.scroll_to_bottom()
        self.refresh("before_open_settings_about.xml")
        self.tap_text(KuwoSettingsLocators.ABOUT)
        assert self.wait_for(self.is_about_loaded), "关于页未展示"

    def is_about_loaded(self) -> bool:
        return (
            self.exists_text(KuwoSettingsLocators.ABOUT_TITLE)
            and self.exists_text(KuwoSettingsLocators.VERSION_NAME)
            and self.exists_text(KuwoSettingsLocators.USER_AGREEMENT)
            and self.exists_text(KuwoSettingsLocators.PRIVACY_POLICY)
            and self.exists_text(KuwoSettingsLocators.OPEN_SOURCE_DISCLAIMER)
        )

    @allure_step("断言设置关于页已加载")
    def assert_about_loaded(self) -> None:
        self.refresh("settings_about.xml")
        assert self.is_about_loaded(), "关于页关键条目未展示"

    @allure_step("打开关于页入口：{entry_name}")
    def open_about_entry(self, entry_name: str) -> None:
        self.refresh(f"before_open_about_entry_{entry_name}.xml")
        self.tap_text(entry_name)

    @allure_step("断言法律信息页已加载")
    def assert_legal_info_loaded(self) -> None:
        def loaded() -> bool:
            return self.exists_text(KuwoSettingsLocators.LEGAL_TITLE) and self.exists_resource_id(
                KuwoSettingsLocators.LEGAL_ROOT
            )

        assert self.wait_for(loaded), "法律信息页未展示"

    def is_driving_restricted(self) -> bool:
        return (
            self.exists_text(KuwoSettingsLocators.LEGAL_DRIVING_RESTRICTED_TEXT)
            or self.exists_text(KuwoSettingsLocators.MEDIA_DRIVING_UNAVAILABLE_TEXT)
            or self.exists_resource_id(KuwoSettingsLocators.OPEN_SOURCE_DRIVING_RESTRICTED)
            or self.exists_text("行驶期间", exact=False)
        )

    @allure_step("断言驾驶模式限制文案已展示")
    def assert_driving_restricted(self) -> None:
        # 法律跨包页和酷我内置长文本页的驾驶限制文案不同，用“行驶期间”做兜底增强兼容。
        assert self.wait_for(self.is_driving_restricted), "驾驶模式限制文案未展示"

    @allure_step("断言开源免责声明页已加载")
    def assert_open_source_loaded(self) -> None:
        def loaded() -> bool:
            return (
                self.exists_text(KuwoSettingsLocators.OPEN_SOURCE_DISCLAIMER)
                and self.exists_resource_id(KuwoSettingsLocators.OPEN_SOURCE_LIST)
                and self.exists_resource_id(KuwoSettingsLocators.OPEN_SOURCE_ITEM)
            )

        assert self.wait_for(loaded), "开源免责声明页未展示"

    @allure_step("关闭设置子页面")
    def close_subpage(self) -> None:
        self.adb.press_back()

    @allure_step("关闭设置页")
    def close(self) -> None:
        self.refresh("before_close_settings.xml")
        self.adb.press_back()
