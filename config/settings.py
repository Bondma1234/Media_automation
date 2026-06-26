"""运行时配置。

优先从环境变量读取，默认值指向本轮已验证的酷我台架。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    device_serial: str
    media_profile: str
    output_dir: Path
    adb_timeout: int
    ui_timeout: int
    display_id: str | None

    @property
    def allure_results_dir(self) -> Path:
        return self.output_dir / "allure_results"

    @property
    def artifacts_dir(self) -> Path:
        return self.output_dir / "artifacts"


def load_settings() -> Settings:
    display_id = os.getenv("MEDIA_DISPLAY_ID") or None
    return Settings(
        device_serial=os.getenv("MEDIA_DEVICE_SERIAL", "192.168.2.197:5555"),
        media_profile=os.getenv("MEDIA_PROFILE", "oneinfo_kuwo"),
        output_dir=Path(os.getenv("MEDIA_OUTPUT_DIR", "output")),
        adb_timeout=_env_int("MEDIA_ADB_TIMEOUT", 30),
        ui_timeout=_env_int("MEDIA_UI_TIMEOUT", 10),
        display_id=display_id,
    )
