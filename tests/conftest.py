from __future__ import annotations

import re
from pathlib import Path

import pytest

from config.media_profiles import MediaProfile, get_media_profile
from config.settings import Settings, load_settings
from drivers.u2_driver import U2Driver
from helpers.adb_helper import ADBHelper
from helpers.allure_helper import attach_file, attach_text


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


@pytest.fixture(scope="session")
def settings() -> Settings:
    loaded = load_settings()
    loaded.output_dir.mkdir(parents=True, exist_ok=True)
    loaded.allure_results_dir.mkdir(parents=True, exist_ok=True)
    loaded.artifacts_dir.mkdir(parents=True, exist_ok=True)
    return loaded


@pytest.fixture(scope="session")
def profile(settings: Settings) -> MediaProfile:
    return get_media_profile(settings.media_profile)


@pytest.fixture(scope="session")
def adb(settings: Settings) -> ADBHelper:
    return ADBHelper(settings.device_serial, timeout=settings.adb_timeout, display_id=settings.display_id)


@pytest.fixture(scope="session", autouse=True)
def allure_environment(settings: Settings, adb: ADBHelper, profile: MediaProfile) -> None:
    env_file = settings.allure_results_dir / "environment.properties"
    # Allure 环境页用于给报告审阅人直接展示台架、包名、profile 和版本信息。
    env_file.write_text(
        "\n".join(
            [
                f"device.serial={settings.device_serial}",
                f"media.profile={profile.name}",
                f"media.package={profile.package}",
                f"media.activity={profile.activity}",
                f"media.version={adb.package_version(profile.package)}",
                f"ui.timeout={settings.ui_timeout}",
                f"adb.timeout={settings.adb_timeout}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


@pytest.fixture(scope="session")
def u2_device(settings: Settings) -> object | None:
    driver = U2Driver(settings.device_serial)
    return driver.connect()


@pytest.fixture()
def artifact_dir(settings: Settings, request: pytest.FixtureRequest) -> Path:
    path = settings.artifacts_dir / _safe_name(request.node.nodeid)
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    adb = item.funcargs.get("adb")
    artifact_dir = item.funcargs.get("artifact_dir")
    profile = item.funcargs.get("profile")
    if not isinstance(adb, ADBHelper) or not isinstance(artifact_dir, Path):
        return

    # 失败时立即采集现场。截图、XML、设备上下文是后续定位车机 UI 问题的最小证据链。
    screenshot = artifact_dir / "failure.png"
    xml = artifact_dir / "failure.xml"
    context = artifact_dir / "device_context.txt"
    logcat = artifact_dir / "logcat_tail.txt"

    adb.capture_screenshot(screenshot)
    adb.dump_ui_xml(xml, strict=False)
    package = profile.package if isinstance(profile, MediaProfile) else None
    context.write_text(adb.device_info(package), encoding="utf-8")
    logcat.write_text(adb.logcat_tail(), encoding="utf-8")

    attach_file(screenshot, "failure screenshot", "png")
    attach_file(xml, "failure ui xml", "xml")
    attach_text("device context", context.read_text(encoding="utf-8"))
    attach_text("logcat tail", logcat.read_text(encoding="utf-8"))
