from __future__ import annotations

import re
from pathlib import Path

import pytest

from config.media_profiles import MediaProfile, get_media_profile
from config.settings import Settings, load_settings
from drivers.u2_driver import U2Driver
from helpers.adb_helper import ADBHelper
from helpers.allure_labels import apply_allure_case_metadata
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
    return ADBHelper(
        settings.device_serial,
        timeout=settings.adb_timeout,
        display_id=settings.display_id,
        remote_artifact_prefix=settings.remote_artifact_prefix,
    )


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
                f"remote.artifact.prefix={settings.remote_artifact_prefix}",
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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item: pytest.Item):
    # 等 Allure 自身完成 setup 元数据初始化后再覆盖标题和描述，避免中文信息被测试函数名回写。
    yield
    apply_allure_case_metadata(item.name, (marker.name for marker in item.iter_markers()))


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

    package = profile.package if isinstance(profile, MediaProfile) else None
    evidence_errors: list[str] = []

    # 失败取证不能反过来中断 pytest 主流程；网络 ADB 断连时保留错误文本即可。
    try:
        adb.capture_screenshot(screenshot)
        attach_file(screenshot, "failure screenshot", "png")
    except Exception as exc:
        evidence_errors.append(f"screenshot: {exc}")

    try:
        adb.dump_ui_xml(xml, strict=False)
        attach_file(xml, "failure ui xml", "xml")
    except Exception as exc:
        evidence_errors.append(f"ui xml: {exc}")

    try:
        context.write_text(adb.device_info(package), encoding="utf-8")
        attach_text("device context", context.read_text(encoding="utf-8"))
    except Exception as exc:
        evidence_errors.append(f"device context: {exc}")

    try:
        logcat.write_text(adb.logcat_tail(), encoding="utf-8")
        attach_text("logcat tail", logcat.read_text(encoding="utf-8"))
    except Exception as exc:
        evidence_errors.append(f"logcat: {exc}")

    if evidence_errors:
        try:
            attach_text("failure evidence capture errors", "\n".join(evidence_errors))
        except Exception:
            # 即使 Allure 附件系统本身异常，也不能把原始测试失败升级成 pytest INTERNALERROR。
            pass
