"""媒体应用包名和启动参数配置。

One Info 当前是聚合包，HCP3 后续会拆成独立包。测试代码只读取 profile，
不直接写死包名，这样拆包时主要改配置而不是改用例。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MediaProfile:
    name: str
    module: str
    package: str
    activity: str | None
    launch_action: str | None = None
    search_activity: str | None = None

    @property
    def component(self) -> str | None:
        if not self.activity:
            return None
        if self.activity.startswith("."):
            return f"{self.package}/{self.activity}"
        if "/" in self.activity:
            return self.activity
        return f"{self.package}/{self.activity}"


MEDIA_PROFILES: dict[str, MediaProfile] = {
    "oneinfo_kuwo": MediaProfile(
        name="oneinfo_kuwo",
        module="kuwo",
        package="com.jidouauto.media",
        activity=".ui.kuwo.main.KuwoMainActivity",
        launch_action="com.jidouauto.media.kuwo.LAUNCH_INTENT",
        search_activity=".ui.main.KuwoSearchActivity",
    ),
    "hcp3_kuwo": MediaProfile(
        name="hcp3_kuwo",
        module="kuwo",
        package="com.jidouauto.media.kuwo",
        activity=".ui.kuwo.main.KuwoMainActivity",
        launch_action="com.jidouauto.media.kuwo.LAUNCH_INTENT",
    ),
    "hcp3_iqiyi": MediaProfile(
        name="hcp3_iqiyi",
        module="iqiyi",
        package="com.jidouauto.media.iqiyi",
        activity=".ui.iqiyi.main.IqiyiMainActivity",
        launch_action="com.jidouauto.media.iqiyi.LAUNCH_INTENT",
    ),
    "hcp3_ximalaya": MediaProfile(
        name="hcp3_ximalaya",
        module="ximalaya",
        package="com.jidouauto.media.ximalaya",
        activity=".ui.ximalaya.main.XimalayaMainActivity",
        launch_action="com.jidouauto.media.ximalaya.LAUNCH_INTENT",
    ),
    "hcp3_leting": MediaProfile(
        name="hcp3_leting",
        module="leting",
        package="com.jidouauto.media.leting",
        activity=".ui.leting.main.LetingMainActivity",
        launch_action="com.jidouauto.media.leting.LAUNCH_INTENT",
    ),
}


def get_media_profile(name: str) -> MediaProfile:
    try:
        return MEDIA_PROFILES[name]
    except KeyError as exc:
        valid = ", ".join(sorted(MEDIA_PROFILES))
        raise ValueError(f"未知媒体 profile: {name}. 可选值: {valid}") from exc
