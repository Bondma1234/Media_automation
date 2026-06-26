"""Page Object 基类。"""

from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable

from helpers.adb_helper import ADBHelper


class BasePage:
    def __init__(self, adb: ADBHelper, artifact_dir: Path, ui_timeout: int = 10) -> None:
        self.adb = adb
        self.artifact_dir = artifact_dir
        self.ui_timeout = ui_timeout
        self._last_xml_path = artifact_dir / "current_window.xml"
        self._root: ET.Element | None = None

    def refresh(self, name: str = "current_window.xml") -> ET.Element:
        self._last_xml_path = self.artifact_dir / name
        self.adb.dump_ui_xml(self._last_xml_path)
        self._root = ET.parse(self._last_xml_path).getroot()
        return self._root

    @property
    def root(self) -> ET.Element:
        if self._root is None:
            return self.refresh()
        return self._root

    def wait_for(self, condition: Callable[[], bool], timeout: int | None = None) -> bool:
        end_time = time.time() + (timeout or self.ui_timeout)
        while time.time() < end_time:
            try:
                self.refresh()
                if condition():
                    return True
            except Exception:
                # 播放页等动态界面可能让 uiautomator 暂时拿不到 idle，等待循环继续重试。
                pass
            time.sleep(0.5)
        try:
            self.refresh()
            return condition()
        except Exception:
            return False

    def nodes(self) -> list[ET.Element]:
        return list(self.root.iter("node"))

    def texts(self) -> list[str]:
        values: list[str] = []
        for node in self.nodes():
            text = (node.attrib.get("text") or "").strip()
            if text:
                values.append(text)
        return values

    def find_by_resource_id(self, resource_id: str) -> ET.Element | None:
        return self._find(lambda node: node.attrib.get("resource-id") == resource_id)

    def find_by_text(self, text: str, exact: bool = True) -> ET.Element | None:
        if exact:
            return self._find(lambda node: (node.attrib.get("text") or "").strip() == text)
        return self._find(lambda node: text in (node.attrib.get("text") or ""))

    def find_by_desc(self, desc: str, exact: bool = False) -> ET.Element | None:
        if exact:
            return self._find(lambda node: (node.attrib.get("content-desc") or "").strip() == desc)
        return self._find(lambda node: desc in (node.attrib.get("content-desc") or ""))

    def exists_resource_id(self, resource_id: str) -> bool:
        return self.find_by_resource_id(resource_id) is not None

    def exists_text(self, text: str, exact: bool = True) -> bool:
        return self.find_by_text(text, exact=exact) is not None

    def exists_desc(self, desc: str, exact: bool = False) -> bool:
        return self.find_by_desc(desc, exact=exact) is not None

    def tap_resource_id(self, resource_id: str) -> None:
        self._tap_required(self.find_by_resource_id(resource_id), f"resource-id={resource_id}")

    def tap_text(self, text: str, exact: bool = True) -> None:
        self._tap_required(self.find_by_text(text, exact=exact), f"text={text}")

    def tap_desc(self, desc: str, exact: bool = False) -> None:
        self._tap_required(self.find_by_desc(desc, exact=exact), f"content-desc={desc}")

    def tap_node_center(self, node: ET.Element, label: str = "node") -> None:
        x, y = self._tap_center_of(node)
        self.adb.tap(x, y)

    def _find(self, predicate: Callable[[ET.Element], bool]) -> ET.Element | None:
        for node in self.nodes():
            if predicate(node):
                return node
        return None

    def _tap_required(self, node: ET.Element | None, label: str) -> None:
        if node is None:
            raise AssertionError(f"未找到可点击元素: {label}")
        x, y = self._tap_center_of(node)
        # 车机 UI 有些子节点不标记 clickable，但点击其 bounds 中心会由父容器接收。
        self.adb.tap(x, y)

    def _tap_center_of(self, node: ET.Element) -> tuple[int, int]:
        x, y = self._center_of(node)
        root_bounds = self.root.attrib.get("bounds", "")
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", root_bounds)
        if not match:
            return x, y
        left, top, right, bottom = map(int, match.groups())
        # 部分车机多屏窗口 dump 出 1920x390 的局部坐标；ADB tap 使用主屏全局坐标，需要补回媒体窗口偏移。
        if left == 0 and top == 0 and right == 1920 and bottom <= 420:
            return x + 120, y + 119
        return x, y

    @staticmethod
    def _center_of(node: ET.Element) -> tuple[int, int]:
        bounds = node.attrib.get("bounds", "")
        match = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
        if not match:
            raise AssertionError(f"节点缺少有效 bounds: {ET.tostring(node, encoding='unicode')}")
        left, top, right, bottom = map(int, match.groups())
        return (left + right) // 2, (top + bottom) // 2
