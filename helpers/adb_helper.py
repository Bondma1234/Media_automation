"""ADB 操作封装。

所有设备命令统一从这里出去，方便后续做日志、重试、多屏 display id 和
HCP3 多包名适配。页面对象不要直接拼 `adb` 命令。
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from config.media_profiles import MediaProfile


_REMOTE_ARTIFACT_PREFIX_INVALID = re.compile(r"[^A-Za-z0-9_.-]+")
_REMOTE_ARTIFACT_PREFIX_MAX_LENGTH = 64


def _safe_remote_artifact_prefix(value: str) -> str:
    """把外部 job 标识转换为安全且不易冲突的 /sdcard 文件名前缀。"""
    normalized = _REMOTE_ARTIFACT_PREFIX_INVALID.sub("_", value).strip("._-")
    if not normalized:
        normalized = f"media_auto_{os.getpid()}"
    if len(normalized) <= _REMOTE_ARTIFACT_PREFIX_MAX_LENGTH:
        return normalized
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    stem_limit = _REMOTE_ARTIFACT_PREFIX_MAX_LENGTH - len(digest) - 1
    return f"{normalized[:stem_limit]}_{digest}"


@dataclass(frozen=True)
class CommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


class ADBCommandError(RuntimeError):
    def __init__(self, result: CommandResult) -> None:
        message = (
            f"ADB 命令失败: {' '.join(result.args)}\n"
            f"returncode={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
        super().__init__(message)
        self.result = result


class ADBHelper:
    def __init__(
        self,
        serial: str,
        timeout: int = 30,
        display_id: str | None = None,
        remote_artifact_prefix: str | None = None,
    ) -> None:
        self.serial = serial
        self.timeout = timeout
        self.display_id = display_id
        requested_prefix = (
            remote_artifact_prefix
            or os.getenv("MEDIA_REMOTE_ARTIFACT_PREFIX")
            or f"media_auto_{os.getpid()}"
        )
        self.remote_artifact_prefix = _safe_remote_artifact_prefix(requested_prefix)

    def run(self, args: list[str], check: bool = True, timeout: float | None = None) -> CommandResult:
        command = ["adb", "-s", self.serial, *args]
        completed = subprocess.run(
            command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout if timeout is None else timeout,
        )
        result = CommandResult(command, completed.returncode, completed.stdout, completed.stderr)
        if check and result.returncode != 0:
            raise ADBCommandError(result)
        return result

    def shell(self, command: str, check: bool = True, timeout: float | None = None) -> str:
        return self.run(["shell", command], check=check, timeout=timeout).stdout.strip()

    def is_online(self) -> bool:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout,
        )
        return f"{self.serial}\tdevice" in result.stdout

    def start_activity(self, profile: MediaProfile) -> str:
        if not profile.component:
            raise ValueError(f"profile {profile.name} 缺少 activity，无法显式启动")
        parts = ["am", "start", "-W"]
        if profile.launch_action:
            parts.extend(["-a", profile.launch_action])
        parts.extend(["-n", profile.component])
        # 显式 Activity + action 可绕开桌面入口，让 smoke 更可重复。
        return self.shell(" ".join(parts), timeout=20)

    def press_back(self) -> None:
        self.shell("input keyevent 4")

    def media_pause(self) -> None:
        self.shell("input keyevent 127", check=False)

    def driving_drive(self) -> str:
        # 台架驾驶模式开启命令；所有用例必须在 teardown 中调用 driving_park 恢复。
        return self.shell("dumpsys car_service emulate-driving-state drive", check=False, timeout=20)

    def driving_park(self) -> str:
        # 台架驾驶模式关闭/驻车命令，作为驾驶模式用例的恢复兜底。
        return self.shell("dumpsys car_service emulate-driving-state park", check=False, timeout=20)

    def tap(self, x: int, y: int) -> None:
        self.shell(f"input tap {x} {y}")

    def input_text(self, text: str) -> None:
        # 仅用于 ASCII 测试词；中文输入仍优先复用历史词，避免车机输入法噪声。
        escaped = text.replace(" ", "%s")
        self.shell(f"input text {escaped}", check=False)

    def press_enter(self) -> None:
        self.shell("input keyevent 66", check=False)

    def long_press(self, x: int, y: int, duration_ms: int = 1300) -> None:
        # ADB 没有独立 long click 命令，固定起终点 swipe 可模拟长按。
        self.swipe(x, y, x, y, duration_ms)

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 700) -> None:
        self.shell(f"input swipe {start_x} {start_y} {end_x} {end_y} {duration_ms}")

    def dump_ui_xml(
        self,
        local_path: Path,
        strict: bool = True,
        timeout: float | None = None,
        retries: int = 3,
    ) -> Path:
        """在一个总超时预算内生成并拉取 UI XML。

        ``timeout`` 是整个 dump（删除、生成、拉取、重试）的墙钟预算，而不是
        每条 ADB 命令各自的预算。这样 ``wait_for(timeout=3)`` 不会被三轮
        20 秒命令放大成数分钟。
        """
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.unlink(missing_ok=True)
        remote_path = f"/sdcard/{self.remote_artifact_prefix}_window.xml"
        total_budget = float(self.timeout if timeout is None else timeout)
        deadline = time.monotonic() + max(0.0, total_budget)
        dump_output = ""
        pull_result: CommandResult | None = None

        def remaining(command_cap: float) -> float:
            value = deadline - time.monotonic()
            if value <= 0:
                raise TimeoutError(f"UI dump 超过总预算 {total_budget:.2f}s")
            return max(0.05, min(command_cap, value))

        for attempt in range(max(1, retries)):
            try:
                self.shell(f"rm -f {remote_path}", check=False, timeout=remaining(5.0))
                # 动态播放页/多窗口切换时 uiautomator 偶尔不会产出 XML；
                # 重试共享同一个总预算，不能逐命令重复消耗完整 timeout。
                dump_output = self.shell(
                    f"uiautomator dump {remote_path}",
                    check=False,
                    timeout=remaining(20.0),
                )
                pull_result = self.run(
                    ["pull", remote_path, str(local_path)],
                    check=False,
                    timeout=remaining(20.0),
                )
            except (subprocess.TimeoutExpired, TimeoutError) as exc:
                pull_result = CommandResult(
                    ["adb", "-s", self.serial, "pull", remote_path, str(local_path)],
                    124,
                    "",
                    f"UI dump timeout: {exc}",
                )
            if pull_result.returncode == 0:
                break
            delay = 0.6 + attempt * 0.4
            remaining_budget = deadline - time.monotonic()
            if remaining_budget <= 0 or attempt + 1 >= max(1, retries):
                break
            time.sleep(min(delay, remaining_budget))

        if pull_result is None:
            pull_result = CommandResult(
                ["adb", "-s", self.serial, "pull", remote_path, str(local_path)],
                124,
                "",
                f"UI dump timeout: no command could start within {total_budget:.2f}s",
            )
        if pull_result.returncode != 0:
            message = (
                "<hierarchy dump_failed=\"true\">"
                "<message>uiautomator dump failed; no fresh XML was produced.</message>"
                f"<dump_output>{escape(dump_output)}</dump_output>"
                f"<pull_stderr>{escape(pull_result.stderr)}</pull_stderr>"
                "</hierarchy>\n"
            )
            local_path.write_text(message, encoding="utf-8")
            if strict:
                raise ADBCommandError(pull_result)
        return local_path

    def capture_screenshot(self, local_path: Path) -> Path:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        remote_path = f"/sdcard/{self.remote_artifact_prefix}_screen.png"
        display_arg = f"-d {self.display_id} " if self.display_id else ""
        # 先保存到设备再 pull，避免 Windows 管道把 PNG 换行字节改坏。
        self.shell(f"screencap {display_arg}-p {remote_path}", check=False, timeout=20)
        self.run(["pull", remote_path, str(local_path)], timeout=20)
        return local_path

    def current_focus(self) -> str:
        raw = self.shell("dumpsys window", check=False, timeout=20)
        matches = re.findall(r"mCurrentFocus=Window\{[^ ]+ [^ ]+ ([^}]+)\}", raw)
        return matches[-1] if matches else ""

    def foreground_package_activity(self) -> tuple[str, str]:
        focus = self.current_focus()
        if "/" not in focus:
            return "", focus
        package, activity = focus.split("/", 1)
        return package, activity

    def package_version(self, package: str) -> str:
        raw = self.shell(f"dumpsys package {package}", check=False, timeout=20)
        match = re.search(r"versionName=([^\s]+)", raw)
        return match.group(1) if match else ""

    def device_info(self, package: str | None = None) -> str:
        lines = [
            f"serial={self.serial}",
            f"model={self.shell('getprop ro.product.model', check=False)}",
            f"build={self.shell('getprop ro.build.display.id', check=False)}",
            f"wm_size={self.shell('wm size', check=False)}",
            f"wm_density={self.shell('wm density', check=False)}",
            f"focus={self.current_focus()}",
        ]
        if package:
            lines.append(f"{package}_version={self.package_version(package)}")
        return "\n".join(lines)

    def logcat_tail(self, lines: int = 300) -> str:
        return self.shell(f"logcat -d -t {lines}", check=False, timeout=20)

    def kuwo_playback_snapshot(self) -> dict[str, str]:
        """读取酷我媒体会话快照，用于播放页 XML 不稳定时验证真实播放状态。"""
        raw = self.shell("dumpsys media_session", check=False, timeout=20)
        marker = "com.jidouauto.media.kuwo.player.KuwoPlayer"
        marker_index = raw.find(marker)
        block = raw[marker_index : marker_index + 3000] if marker_index >= 0 else raw
        state_match = re.search(
            r"state=PlaybackState \{state=([A-Z_]+)\((\d+)\).*?updated=(\d+).*?active item id=([^,}]+)",
            block,
            re.S,
        )
        desc_match = re.search(r"metadata:.*?description=([^\n]+)", block)
        return {
            "state": state_match.group(1) if state_match else "",
            "state_code": state_match.group(2) if state_match else "",
            "updated": state_match.group(3) if state_match else "",
            "active_item_id": state_match.group(4).strip() if state_match else "",
            "description": desc_match.group(1).strip() if desc_match else "",
        }
