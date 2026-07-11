# Media Automation

车机端媒体自动化测试工程，从酷我音乐主流程开始搭建，后续覆盖喜马拉雅、爱奇艺、乐听以及 HCP3 独立包形态。

## 技术栈

- Python + pytest
- openatx/uiautomator2 + ADB Helper
- Page Object Model
- Allure 报告，失败时自动附加截图、UI XML、设备上下文和 logcat 摘要

## 当前包名

| 阶段 | 模块 | 包名 |
| --- | --- | --- |
| One Info | 媒体中心聚合包 | `com.jidouauto.media` |
| HCP3 | 酷我音乐 | `com.jidouauto.media.kuwo` |
| HCP3 | 爱奇艺 | `com.jidouauto.media.iqiyi` |
| HCP3 | 喜马拉雅 | `com.jidouauto.media.ximalaya` |
| HCP3 | 乐听 | `com.jidouauto.media.leting` |

> 本轮台架实际安装包为 `com.jidouauto.media`。用户口述中的 `com.jiouauto.media` 与设备实际包名不一致，后续以设备和 HCP3 包名清单为准。

## 本轮输入

- 功能用例来源：[docs/Cariad One Info MEDIA Test Report-CL54.26.153.xlsx](docs/Cariad%20One%20Info%20MEDIA%20Test%20Report-CL54.26.153.xlsx)
- 酷我自动化计划：[docs/kuwo_automation_test_plan.md](docs/kuwo_automation_test_plan.md)
- 酷我 P1/P2 映射：[docs/kuwo_case_mapping.md](docs/kuwo_case_mapping.md)
- 酷我自动化 case 覆盖说明：[docs/kuwo_automation_case_coverage.md](docs/kuwo_automation_case_coverage.md)
- 酷我 P1/P2 覆盖拆分清单：[docs/kuwo_p1_p2_coverage_breakdown.md](docs/kuwo_p1_p2_coverage_breakdown.md)
- 上下文交接：[docs/context_handoff.md](docs/context_handoff.md)
- 台架证据：本地执行后生成在 `output/` 下，属于运行产物，不纳入 Git 版本管理。

## 已落地骨架

```text
config/          包名 profile、设备 serial、输出目录等运行配置
helpers/         ADB、Allure、等待等通用封装
drivers/         uiautomator2 连接入口
pagelocators/    酷我定位器
pageobjects/     酷我首页、搜索页、设置页、播放页 POM
tests/kuwo/      酷我 smoke、首页、搜索、最近收听、播放列表用例
```

## 常用命令

首次拉取后先复制环境变量模板：

```powershell
Copy-Item .\.env.example .\.env
```

按实际台架修改 `.env`：

```text
MEDIA_DEVICE_SERIAL=192.168.2.197:5555
MEDIA_PROFILE=oneinfo_kuwo
```

```powershell
python -m pytest --collect-only -q
python .\main.py .\tests\kuwo\test_kuwo_smoke.py -q -rs
python .\main.py -m "smoke and kuwo" -q -rs
python .\main.py .\tests\kuwo -q -rs
allure generate .\output\allure_results -o .\output\allure_report --clean
```

VSCode 运行说明：

- 推荐使用左侧 Testing 面板或 Run and Debug 中的 `Pytest: smoke` / `Pytest: current file`。
- `tests/kuwo/test_kuwo_smoke.py` 已兼容右上角三角按钮，直接运行该文件时会自动转交给 pytest 跑冒烟用例。
- 其他测试文件仍建议用 pytest 入口运行，避免绕过 fixture、Allure 和项目根路径配置。

当前用例规模：

- `python -m pytest --collect-only -q tests\kuwo`：40 tests collected。
- 最近一次全量回归（2026-07-10，设备 `192.168.2.89:5555`，版本 `CL54.26.225`）：40 total，23 passed，15 failed，2 xfailed，耗时 1841.88s（30m41.88s）。
- 酷我 P1/P2 映射：142/142 已完成分类；按当前 VIP 登录账号前置，强自动化覆盖 79/142（55.6%），自动化证据覆盖 83/142（58.5%）。
- 本机最新 Allure 报告目录：`output/run_192_168_2_89_20260710_174314/allure_report`；默认报告仍可生成到 `output/allure_report`。
- 本次 Allure HTML 中包含 94 张 PNG 附件；报告统计为 40 total，23 passed，11 failed，4 broken，2 skipped（对应 pytest 的 2 条 xfailed）。
- 失败集中在搜索页“无搜索结果”空态（10 条）、动态标题生成 Windows 非法文件名（3 条）、收藏专辑 XML dump 瞬时失败（1 条）和设置关于页跳转失败（1 条）。其中非法文件名和 Allure 中文标题注入已在回归后修复，尚待下一轮全量复验。
- `output/`、`.env`、`.pytest_cache/`、`__pycache__/` 为本地运行产物或个人配置，默认不提交到 Git。

已覆盖的酷我自动化入口：

- P0：设备在线、包版本读取、酷我首页启动。
- P1：搜索页只读进入/返回、设置页只读进入/返回、MiniPlayer 展示、播放页观测。
- P1：首页可见 Tab 只读切换。
- P1：首页内容卡进入歌曲列表页并返回。
- P1：搜索页复用历史词 `周杰伦` 进入结果页，只读校验歌曲结果展示。
- P1：搜索结果页歌曲区、歌手区只读展示。
- P1：最近收听页只读展示，截图和 XML 进 Allure。
- P1：播放页打开播放列表，截图为主证据，XML 可读时增强校验。
- P1：设置-关于页、用户协议、隐私政策、开源免责声明只读展示。
- P1：搜索结果页进入歌手详情页并返回。
- P1/P2：首页酷我 logo 模块切换弹层、歌单 MiniPlayer 播放/暂停控制、播放列表长按歌曲观测。
- P1/P2：听吧电台分类进入和电台播放、收藏专辑/收藏歌单封面播放、收藏专辑详情点歌媒体会话断言。
- P1/P2：热门推荐卡点击播放、播放页展示/播放按钮、播放页去K歌入口均已补强为媒体会话或前台包名强断言。
- P1/P2：播放完成通过进度条拖至近尾并观察媒体会话切换，已补强为强断言。
- P1/P2：下载页标题栏动作、会员账号播放页下载前置检查、收藏页标题栏动作、搜索历史新增。
- P1/P2：驾驶模式 drive/park 下协议、隐私政策、开源免责声明限制和恢复；已登录账户页路径已实现，当前未登录环境下 skip。
- 管理：已生成并更新酷我 P1/P2 用例映射 CSV/Markdown；当前 P1/P2 已完成 142/142 分类，自动化证据覆盖 83/142。

## 查看和分享 Allure 报告

当前报告已按 Allure Behaviors 业务行为分层展示：

```text
酷我音乐
  环境 / 主页 / 搜索 / 播放页 / 播放列表 / 最近收听 / 设置 / 我的 / 下载 / 收藏 / 驾驶模式
    子功能
      中文用例标题
```

实现方式：

- `helpers/allure_labels.py` 集中维护 40 条酷我用例的 `epic/feature/story/title/description/severity/tag`。
- `tests/conftest.py` 在 Allure 完成 setup 初始化后统一注入元数据，避免每个测试函数重复编写装饰器。
- Page Object 常用动作和断言通过 `helpers/allure_helper.py::allure_step` 生成执行步骤。

本机查看：

```powershell
allure open .\output\allure_report
```

给同网段其他人查看：

```powershell
python -m http.server 8088 --bind 0.0.0.0 -d .\output\allure_report
```

然后把 `http://<你的电脑IP>:8088/` 发给别人。直接双击 `index.html` 可能因为浏览器本地文件限制看不到完整数据或附件，建议用上面的 HTTP 服务方式。

离线分发：

```powershell
Compress-Archive -Path .\output\allure_report\* -DestinationPath .\output\allure_report_with_screenshots.zip -Force
```

## 近期原则

- 优先覆盖酷我 P1/P2 主流程。
- 搜索、设置、播放页、MiniPlayer、主页 Tab 先做稳定 smoke。
- 账号绑定、二维码登录、购买会员、支付、清缓存、删除下载、修改设置等用例默认标记为 `manual_auth` 或半自动，不在未授权情况下执行。
- 每轮新增代码或探索结果都同步更新文档。
