from __future__ import annotations

from helpers.allure_helper import allure_step
from pagelocators.kuwo_locators import KuwoAccountLocators
from pageobjects.base_page import BasePage


class KuwoAccountPage(BasePage):
    def is_logged_in_loaded(self) -> bool:
        return (
            self.exists_text(KuwoAccountLocators.TITLE)
            and self.exists_resource_id(KuwoAccountLocators.NICKNAME)
            and self.exists_resource_id(KuwoAccountLocators.VIP_TIME)
        )

    @allure_step("断言已登录账户页昵称和会员有效期展示")
    def assert_logged_in_loaded(self) -> None:
        assert self.wait_for(self.is_logged_in_loaded), "已登录账户页未展示昵称/会员有效期"

    @allure_step("断言已登录账户页操作入口展示")
    def assert_logged_in_actions_visible(self) -> None:
        self.refresh("account_logged_in_actions.xml")
        # 仅校验入口可见，不点击登出、续费、绑定，避免改变账号状态或触发支付/绑定流程。
        missing = [
            text
            for text in (
                KuwoAccountLocators.LOGOUT,
                KuwoAccountLocators.RENEW,
                KuwoAccountLocators.LINK_MYAUDI,
            )
            if not self.exists_text(text)
        ]
        assert not missing, f"已登录账户页操作入口缺失: {missing}"
