from __future__ import annotations

import xml.etree.ElementTree as ET

from pagelocators.kuwo_locators import KuwoPlayerLocators
from pageobjects.base_page import BasePage


class KuwoPlayerPage(BasePage):
    def is_foreground(self) -> bool:
        return "PlayPopupActivity" in self.adb.current_focus()

    def assert_foreground(self) -> None:
        assert self.is_foreground(), "播放页未进入前台"

    def title_loaded(self) -> bool:
        try:
            return self.wait_for(lambda: self.exists_text(KuwoPlayerLocators.TITLE))
        except Exception:
            return False

    def assert_title_loaded(self) -> None:
        assert self.title_loaded(), "播放页标题未展示"

    def has_visible_content(self) -> bool:
        try:
            self.refresh("kuwo_player_observation.xml")
        except Exception:
            return False
        # 当前版本已知播放内容区可能为空；这里先做观测判断，避免把环境问题误判成框架失败。
        meaningful_texts = [text for text in self.texts() if text not in {"正在播放", "去K歌"}]
        return bool(meaningful_texts)

    def close(self) -> None:
        self.adb.press_back()

    def tap_title_back(self) -> None:
        self.adb.tap(185, 178)

    def tap_title_logo(self) -> None:
        self.adb.tap(447, 178)

    def open_queue_by_coordinate(self) -> None:
        # 播放页的播放列表按钮当前没有稳定 resource-id，使用标题栏左侧固定区域兜底。
        self.adb.tap(315, 178)

    def tap_visible_queue_song_by_coordinate(self, y: int = 365) -> None:
        # 播放列表 XML 在动态歌词/播放动画下不可稳定读取，点击首个完整可见歌曲行中部切歌。
        self.adb.tap(510, y)

    def long_press_first_queue_song_by_coordinate(self) -> None:
        # 播放列表浮层 XML 经常不可读，使用首行歌曲标题区域坐标做长按观测。
        self.adb.long_press(350, 295, duration_ms=1600)

    def tap_play_pause_by_coordinate(self) -> None:
        # 播放页底部播放/暂停按钮没有稳定 XML 标识，坐标命中底部控制条第二个按钮。
        self.adb.tap(512, 756)

    def tap_download_button_by_coordinate(self) -> None:
        # 播放页底部下载按钮目前没有稳定 XML 标识，坐标命中 VIP 下载图标区域。
        self.adb.tap(1530, 755)

    def tap_k_song_by_coordinate(self) -> None:
        # “去K歌”是播放页标题栏右侧入口，当前仅做跳转校验，不触碰 K 歌内的登录/购买/授权动作。
        self.adb.tap(1670, 180)

    def seek_near_end_by_coordinate(self) -> None:
        # 进度条没有稳定 resource-id；拖到末尾前一点后等待自然播完，用于验证播放完成/续播链路。
        self.adb.swipe(900, 598, 1785, 598, duration_ms=900)

    def queue_loaded_from_xml(self, xml_name: str = "kuwo_play_queue_observation.xml") -> bool:
        """XML 可读时增强校验播放列表；动态播放页 dump 失败时返回 False 交给截图证据兜底。"""
        self._last_xml_path = self.artifact_dir / xml_name
        self.adb.dump_ui_xml(self._last_xml_path, strict=False)
        try:
            self._root = ET.parse(self._last_xml_path).getroot()
        except ET.ParseError:
            return False

        # 播放列表浮层的关键稳定信号：标题 + RecyclerView；歌曲行字段可能受账号/版权/队列数据影响。
        return self.exists_text(KuwoPlayerLocators.QUEUE_TITLE) and self.exists_resource_id(
            "com.jidouauto.media:id/recyclerView"
        )

    def assert_queue_loaded(self) -> None:
        assert self.wait_for(lambda: self.exists_text(KuwoPlayerLocators.QUEUE_TITLE)), "播放列表标题未展示"
        assert self.exists_resource_id("com.jidouauto.media:id/recyclerView"), "播放列表未展示"
        assert self.exists_resource_id("com.jidouauto.media:id/audio_name"), "播放列表歌曲名未展示"
        assert self.exists_resource_id("com.jidouauto.media:id/subTitle"), "播放列表歌手名未展示"
