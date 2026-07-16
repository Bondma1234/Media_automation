from __future__ import annotations

from pathlib import Path
import subprocess
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import pytest

import helpers.adb_helper as adb_helper_module
import pageobjects.base_page as base_page_module
from helpers.adb_helper import ADBHelper, CommandResult
from pagelocators.kuwo_locators import KuwoHomeLocators
from pageobjects.base_page import BasePage
from pageobjects.kuwo.kuwo_home_page import KuwoHomePage


class XmlADB:
    def __init__(self, xml: str) -> None:
        self.xml = xml
        self.timeouts: list[float | None] = []

    def dump_ui_xml(
        self,
        local_path: Path,
        strict: bool = True,
        timeout: float | None = None,
        retries: int = 3,
    ) -> Path:
        self.timeouts.append(timeout)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text(self.xml, encoding="utf-8")
        return local_path


class LaunchADB:
    def __init__(
        self,
        package: str,
        xml: str,
        *,
        after_start_xml: str | None = None,
        after_back_xml: list[str] | None = None,
    ) -> None:
        self.package = package
        self.activity = ".ui.kuwo.main.KuwoMainActivity"
        self.xml = xml
        self.after_start_xml = after_start_xml
        self.after_back_xml = list(after_back_xml or [])
        self.start_calls = 0
        self.back_calls = 0

    def dump_ui_xml(
        self,
        local_path: Path,
        strict: bool = True,
        timeout: float | None = None,
        retries: int = 3,
    ) -> Path:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text(self.xml, encoding="utf-8")
        return local_path

    def foreground_package_activity(self) -> tuple[str, str]:
        return self.package, self.activity

    def start_activity(self, profile) -> str:
        self.start_calls += 1
        self.package = profile.package
        if self.after_start_xml is not None:
            self.xml = self.after_start_xml
        return "ok"

    def press_back(self) -> None:
        self.back_calls += 1
        if self.after_back_xml:
            self.xml = self.after_back_xml.pop(0)


def _home_xml(labels: tuple[str, ...], selected: str) -> str:
    root = ET.Element("hierarchy", bounds="[0,0][1920,816]")
    ET.SubElement(root, "node", {"resource-id": KuwoHomeLocators.TITLE_ACTIONS})
    ET.SubElement(root, "node", {"resource-id": KuwoHomeLocators.SETTINGS_ACTIONS})
    tabs = ET.SubElement(root, "node", {"resource-id": KuwoHomeLocators.TAB_LAYOUT})
    for label in labels:
        tab = ET.SubElement(
            tabs,
            "node",
            {
                "content-desc": f"content={label}",
                "selected": str(label == selected).lower(),
                "bounds": "[100,100][300,200]",
            },
        )
        ET.SubElement(tab, "node", {"resource-id": "android:id/text1", "text": label})
    content = ET.SubElement(root, "node", {"resource-id": KuwoHomeLocators.HOME_RECYCLER})
    ET.SubElement(content, "node", {"resource-id": KuwoHomeLocators.CARD_TITLE, "text": "Card"})
    return ET.tostring(root, encoding="unicode")


def _media_child_xml(title: str) -> str:
    root = ET.Element("hierarchy", bounds="[0,0][1920,816]")
    ET.SubElement(
        root,
        "node",
        {"package": "com.jidouauto.media", "content-desc": "###Back"},
    )
    ET.SubElement(
        root,
        "node",
        {
            "package": "com.jidouauto.media",
            "resource-id": KuwoHomeLocators.DETAIL_TITLE,
            "text": title,
        },
    )
    return ET.tostring(root, encoding="unicode")


def _unknown_media_xml() -> str:
    return '<hierarchy><node package="com.jidouauto.media" resource-id="unknown" /></hierarchy>'


def _loading_xml() -> str:
    return (
        '<hierarchy><node package="com.jidouauto.media" '
        f'resource-id="{KuwoHomeLocators.INIT_PROGRESS}" /></hierarchy>'
    )


@pytest.mark.parametrize(
    ("labels", "selected", "business_tab"),
    [
        (("我的", "热门", "榜单", "会员专区", "听吧", "曲库"), "我的", "我的"),
        (("My", "Popular", "TOP", "Car VIP", "Podcast", "Library"), "Popular", "热门"),
    ],
)
def test_home_readiness_and_tab_selection_are_locale_independent(
    tmp_path: Path,
    labels: tuple[str, ...],
    selected: str,
    business_tab: str,
) -> None:
    adb = XmlADB(_home_xml(labels, selected))
    page = KuwoHomePage(adb, tmp_path, ui_timeout=4)

    page.refresh()

    assert page.is_loaded()
    assert page.is_tab_selected(business_tab)
    page.assert_loaded()
    assert adb.timeouts == [4.0, 4.0]


def test_recycler_without_home_tab_structure_is_not_home(tmp_path: Path) -> None:
    xml = (
        '<hierarchy bounds="[0,0][1920,816]">'
        f'<node resource-id="{KuwoHomeLocators.HOME_RECYCLER}" />'
        "</hierarchy>"
    )
    page = KuwoHomePage(XmlADB(xml), tmp_path)

    page.refresh()

    assert not page.is_loaded()


def test_launch_recovers_known_about_and_settings_pages(tmp_path: Path) -> None:
    profile = SimpleNamespace(package="com.jidouauto.media")
    home_xml = _home_xml(("My", "Popular", "TOP", "Car VIP", "Podcast", "Library"), "Popular")
    adb = LaunchADB(
        profile.package,
        _media_child_xml("关于"),
        after_back_xml=[_media_child_xml("设置"), home_xml],
    )
    page = KuwoHomePage(adb, tmp_path, ui_timeout=10)

    page.launch(profile)

    assert adb.start_calls == 0
    assert adb.back_calls == 2
    assert page.is_loaded()


def test_launch_from_launcher_starts_home_without_back(tmp_path: Path) -> None:
    profile = SimpleNamespace(package="com.jidouauto.media")
    home_xml = _home_xml(("我的", "热门", "榜单", "会员专区", "听吧", "曲库"), "热门")
    adb = LaunchADB(
        "com.jidouauto.dashboard",
        '<hierarchy><node package="com.jidouauto.dashboard" /></hierarchy>',
        after_start_xml=home_xml,
    )
    adb.activity = "com.jidouauto.dashboard.MainLauncher"
    page = KuwoHomePage(adb, tmp_path, ui_timeout=7)

    page.launch(profile)

    assert adb.start_calls == 1
    assert adb.back_calls == 0


def test_launch_waits_through_transient_unknown_state_after_start(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = SimpleNamespace(package="com.jidouauto.media")
    adb = LaunchADB(
        "com.jidouauto.dashboard",
        '<hierarchy><node package="com.jidouauto.dashboard" /></hierarchy>',
    )
    adb.activity = "com.jidouauto.dashboard.MainLauncher"
    page = KuwoHomePage(adb, tmp_path, ui_timeout=3)
    states = iter(("other_app", "unknown_media", "home"))
    monkeypatch.setattr(page, "_observe_page_state", lambda _profile, timeout: next(states))

    page.launch(profile)

    assert adb.start_calls == 1
    assert adb.back_calls == 0


def test_launch_waits_through_transient_unknown_state_after_back(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = SimpleNamespace(package="com.jidouauto.media")
    adb = LaunchADB(profile.package, _media_child_xml("关于"))
    page = KuwoHomePage(adb, tmp_path, ui_timeout=3)
    states = iter(("known_child", "unknown_media", "home"))
    monkeypatch.setattr(page, "_observe_page_state", lambda _profile, timeout: next(states))

    page.launch(profile)

    assert adb.start_calls == 0
    assert adb.back_calls == 1


def test_launch_unknown_media_page_never_blindly_backs(tmp_path: Path) -> None:
    profile = SimpleNamespace(package="com.jidouauto.media")
    adb = LaunchADB(profile.package, _unknown_media_xml())
    page = KuwoHomePage(adb, tmp_path, ui_timeout=2)

    with pytest.raises(AssertionError, match="state=unknown_media"):
        page.launch(profile)

    assert adb.start_calls == 1
    assert adb.back_calls == 0


def test_launch_loading_page_waits_but_never_backs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    profile = SimpleNamespace(package="com.jidouauto.media")
    adb = LaunchADB(profile.package, _loading_xml())
    page = KuwoHomePage(adb, tmp_path, ui_timeout=2)
    monkeypatch.setattr(page, "wait_for", lambda condition, timeout=None: False)

    with pytest.raises(AssertionError, match="初始化页持续未完成"):
        page.launch(profile)

    assert adb.start_calls == 0
    assert adb.back_calls == 0


def test_wait_for_shares_one_wall_clock_budget_with_ui_dump(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    class Clock:
        now = 0.0

        def monotonic(self) -> float:
            return self.now

        def sleep(self, seconds: float) -> None:
            self.now += seconds

    class TimeoutADB:
        def __init__(self, clock: Clock) -> None:
            self.clock = clock
            self.timeouts: list[float] = []

        def dump_ui_xml(self, local_path: Path, strict: bool = True, timeout: float | None = None) -> Path:
            assert timeout is not None
            self.timeouts.append(timeout)
            self.clock.now += min(timeout, 1.5)
            raise TimeoutError("simulated slow uiautomator")

    clock = Clock()
    adb = TimeoutADB(clock)
    monkeypatch.setattr(
        base_page_module,
        "time",
        SimpleNamespace(monotonic=clock.monotonic, sleep=clock.sleep),
    )
    page = BasePage(adb, tmp_path, ui_timeout=10)

    assert not page.wait_for(lambda: True, timeout=3)
    assert clock.now == pytest.approx(3.0)
    assert len(adb.timeouts) == 2
    assert adb.timeouts[0] == pytest.approx(3.0)
    assert adb.timeouts[1] == pytest.approx(1.0)


def test_remote_artifacts_use_sanitized_job_prefix(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    helper = ADBHelper("serial", remote_artifact_prefix="portal job/2089")
    shell_commands: list[str] = []
    pull_args: list[list[str]] = []

    def fake_shell(command: str, check: bool = True, timeout: float | None = None) -> str:
        shell_commands.append(command)
        return "UI hierchary dumped"

    def fake_run(args: list[str], check: bool = True, timeout: float | None = None) -> CommandResult:
        pull_args.append(args)
        return CommandResult(["adb", "-s", "serial", *args], 0, "ok", "")

    monkeypatch.setattr(helper, "shell", fake_shell)
    monkeypatch.setattr(helper, "run", fake_run)

    helper.dump_ui_xml(tmp_path / "window.xml", timeout=2)
    helper.capture_screenshot(tmp_path / "screen.png")

    assert helper.remote_artifact_prefix == "portal_job_2089"
    assert any("/sdcard/portal_job_2089_window.xml" in command for command in shell_commands)
    assert any("/sdcard/portal_job_2089_screen.png" in command for command in shell_commands)
    assert ["pull", "/sdcard/portal_job_2089_window.xml", str(tmp_path / "window.xml")] in pull_args
    assert ["pull", "/sdcard/portal_job_2089_screen.png", str(tmp_path / "screen.png")] in pull_args


def test_ui_dump_retries_share_one_total_timeout_budget(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    class Clock:
        now = 0.0

        def monotonic(self) -> float:
            return self.now

        def sleep(self, seconds: float) -> None:
            self.now += seconds

    clock = Clock()
    helper = ADBHelper("serial", remote_artifact_prefix="job-1")
    command_timeouts: list[float] = []

    def slow_shell(command: str, check: bool = True, timeout: float | None = None) -> str:
        assert timeout is not None
        command_timeouts.append(timeout)
        clock.now += timeout
        raise subprocess.TimeoutExpired(command, timeout)

    monkeypatch.setattr(
        adb_helper_module,
        "time",
        SimpleNamespace(monotonic=clock.monotonic, sleep=clock.sleep),
    )
    monkeypatch.setattr(helper, "shell", slow_shell)

    target = helper.dump_ui_xml(tmp_path / "timeout.xml", strict=False, timeout=3, retries=3)

    assert target.read_text(encoding="utf-8").startswith('<hierarchy dump_failed="true">')
    assert clock.now == pytest.approx(3.0)
    assert command_timeouts == [pytest.approx(3.0)]
