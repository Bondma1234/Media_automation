"""uiautomator2 驱动封装。

当前 smoke 以 ADB XML 为兜底，uiautomator2 作为后续精细控件操作入口。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class U2Driver:
    serial: str
    device: object | None = None

    def connect(self) -> object | None:
        try:
            import uiautomator2 as u2
        except Exception:
            self.device = None
            return None
        # 连接失败不直接让框架崩溃，P0 会用 ADB 继续给出可诊断证据。
        self.device = u2.connect(self.serial)
        return self.device
