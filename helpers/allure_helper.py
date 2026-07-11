"""Allure 附件封装。

如果本地暂时没有 allure 插件，辅助函数会静默跳过附件，不影响 pytest 主流程。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import allure
except Exception:  # pragma: no cover - 兼容无 allure 环境
    allure = None  # type: ignore[assignment]


def attach_text(name: str, text: str) -> None:
    if allure is None:
        return
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_file(path: Path, name: str, attachment_type: str | None = None) -> None:
    if allure is None or not path.exists():
        return
    if attachment_type == "png":
        allure_type = allure.attachment_type.PNG
    elif attachment_type == "xml":
        allure_type = allure.attachment_type.XML
    else:
        allure_type = allure.attachment_type.TEXT
    allure.attach.file(str(path), name=name, attachment_type=allure_type)


def allure_step(title: str):
    """Allure step 装饰器；未安装 allure 时保持原函数不变。"""
    if allure is not None:
        return allure.step(title)

    def decorator(func):
        return func

    return decorator


def attach_screenshot(adb: Any, artifact_dir: Path, name: str) -> Path:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "screenshot"
    path = artifact_dir / f"{safe_name}.png"
    # 正常通过的关键步骤也要留截图，报告审阅人不用复跑台架就能看到页面状态。
    adb.capture_screenshot(path)
    attach_file(path, name, "png")
    return path
