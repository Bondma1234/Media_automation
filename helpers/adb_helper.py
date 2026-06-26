"""ADB 操作封装。

所有设备命令统一从这里出去，方便后续做日志、重试、多屏 display id 和
HCP3 多包名适配。页面对象不要直接拼 `adb` 命令。
"""

from __future__ import annotations

import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from config.media_profiles import MediaProfile


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
    def __init__(self, serial: str, timeout: int = 30, display_id: str | None = None) -> None:
        self.serial = serial
        self.timeout = timeout
        self.display_id = display_id

    def run(self, args: list[str], check: bool = True, timeout: int | None = None) -> CommandResult:
        command = ["adb", "-s", self.serial, *args]
        completed = subprocess.run(
            command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout or self.timeout,
        )
        result = CommandResult(command, completed.returncode, completed.stdout, completed.stderr)
        if check and result.returncode != 0:
            raise ADBCommandError(result)
        return result

    def shell(self, command: str, check: bool = True, timeout: int | None = None) -> str:
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

    def dump_ui_xml(self, local_path: Path, strict: bool = True) -> Path:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        remote_path = "/sdcard/media_auto_window.xml"
        dump_output = ""
        pull_result: CommandResult | None = None
        for attempt in range(3):
            self.shell(f"rm -f {remote_path}", check=False, timeout=10)
            # 动态播放页/多窗口切换时 uiautomator 偶尔不会产出 XML，短重试可避免把瞬时读树失败误判为业务失败。
            dump_output = self.shell(f"uiautomator dump {remote_path}", check=False, timeout=20)
            pull_result = self.run(["pull", remote_path, str(local_path)], check=False, timeout=20)
            if pull_result.returncode == 0:
                break
            time.sleep(0.6 + attempt * 0.4)
        assert pull_result is not None
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
        remote_path = "/sdcard/media_auto_screen.png"
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
