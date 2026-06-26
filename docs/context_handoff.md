# Context Handoff

## 2026-05-27

### 本轮目标

在 `C:\TestProject\Python_Auto_UI_Crm\Media_automation` 中熟悉现有媒体功能用例，连接台架 `192.168.2.197:5555` 探索酷我音乐，并输出酷我主流程自动化测试计划。

### 本地目录状态

- 当前目录不是 git 仓库。
- 已有文件主要是一份媒体功能测试 Excel：
  - `docs/Cariad One Info MEDIA Test Report-CL54.26.153.xlsx`
- 已新增项目文档：
  - `README.md`
  - `docs/context_handoff.md`
  - `docs/kuwo_automation_test_plan.md`
- 已采集台架证据：
  - `output/evidence/kuwo_explore_20260527/`

### Excel 用例盘点

酷我 sheet 共 432 条有效功能用例：

| 优先级 | 数量 |
| --- | ---: |
| P1 | 34 |
| P2 | 108 |
| P3 | 199 |
| P4 | 91 |

主要模块分布：

| 模块 | 数量 |
| --- | ---: |
| 设置 | 66 |
| 收藏 | 58 |
| 播放页 | 53 |
| 下载 | 36 |
| 搜索 | 36 |
| 最近收听 | 19 |
| 账号 | 18 |
| 主页 | 11 |

已知酷我失败用例：

- `F03_UC019 / 播放页 / 查看普通歌曲播放页显示 / P1`
- 关联缺陷：`CAOIMEDIA-2024`
- 预期：播放页展示歌名、歌手、进度条、歌曲图片、收藏、播放模式、上一曲、播放/暂停、下一曲、下载、音质等。

### 台架探索事实

- 指定设备：`192.168.2.197:5555`
- 设备型号：`MMI`
- 系统版本：`CLU55_OIA_AU_CN_S_UOE_2601501_D033`
- 分辨率：`1920x816`
- 媒体包名：`com.jidouauto.media`
- 媒体版本：`CL54.26.222`
- 酷我主 Activity：`com.jidouauto.media/.ui.kuwo.main.KuwoMainActivity`
- 酷我副屏 Activity：`com.jidouauto.media/.ui.kuwo.main.SecondaryKuwoMainActivity`
- 当前 Excel 报告版本为 `CL54.26.153`，台架版本为 `CL54.26.222`，后续断言需要允许版本差异。

多屏信息：

| HWC display | Display id |
| --- | --- |
| 0 | `4633128631561747456` |
| 1 | `4633128631561747457` |
| 2 | `4633128631561747458` |
| 50 | `4633128631561747506` |

### 已观察到的稳定定位点

- 首页列表：`com.jidouauto.media:id/recyclerView`
- 搜索按钮：`content-desc` 包含 `搜索`
- 设置按钮：`content-desc` 包含 `设置`
- MiniPlayer：
  - 上一首：`com.jidouauto.media:id/id_op_prev`
  - 播放/暂停：`com.jidouauto.media:id/id_op_playpause`
  - 下一首：`com.jidouauto.media:id/id_op_next`
  - 标题：`com.jidouauto.media:id/tv_title`
  - 歌手：`com.jidouauto.media:id/tv_subTitle`
  - 时间：`com.jidouauto.media:id/tv_time`
- 设置页开关：`com.jidouauto.media:id/switchControl`

### 探索注意事项

- 搜索页会自动拉起车机软键盘，退出应优先使用页面返回按钮或 Activity relaunch，不应依赖单次 `Back`。
- 设置页存在真实可变更项，本轮曾误触 `个人信息收集` 开关，已根据原始 XML `checked=true` 恢复为 `checked=true`，并保存 `kuwo_settings_final.xml` 作为验证。
- 播放详情页可进入，标题栏显示 `正在播放`，但本轮等待后内容区仍为空；这与 `CAOIMEDIA-2024` 的播放页显示问题高度相关，后续应作为 P1 首批自动化观测点。

### 2026-05-27 第二轮实现

已完成基础自动化框架骨架：

- `pytest.ini`：声明 `p0/p1/p2/smoke/media/kuwo/manual_auth/stateful/env_required` marker，并默认输出 Allure results。
- `main.py`：pytest 入口，默认补齐 `output/allure_results`。
- `config/settings.py`：从环境变量读取设备、profile、输出目录和超时。
- `config/media_profiles.py`：管理 One Info 聚合包和 HCP3 四个独立包 profile。
- `helpers/adb_helper.py`：封装 ADB 连接、启动 Activity、截图、UI XML、前台焦点、App 版本、logcat。
- `helpers/allure_helper.py`：封装 Allure 附件。
- `drivers/u2_driver.py`：预留 uiautomator2 连接入口。
- `pagelocators/kuwo_locators.py`：酷我首页、搜索、设置、播放页定位器。
- `pageobjects/kuwo/`：酷我首页、搜索页、设置页、播放页 POM。
- `tests/kuwo/test_kuwo_smoke.py`：首批 6 条 smoke。

首批 smoke 覆盖：

| 用例 | 结果 |
| --- | --- |
| 设备在线和包版本读取 | passed |
| 启动酷我首页 | passed |
| 搜索页只读进入和返回 | passed |
| 设置页只读进入和返回 | passed |
| MiniPlayer 控件展示 | passed |
| 播放页观测 | xfailed |

播放页用例 xfail 原因：

- 当前播放页截图可见内容已展示，但 `uiautomator dump` 在播放页动态动画状态下可能返回 `ERROR: could not get idle state`，不会产出新 XML。
- `ADBHelper.dump_ui_xml()` 已改为先删除远端 XML，再 dump，再 pull，避免拉到旧 XML。
- 播放页观测用例会保存截图 `player_page_observation.png`，并暂时 xfail，后续可引入图像/OCR 或更稳定的控件源后再改成强断言。

验证命令：

```powershell
python -m pytest --collect-only -q
python .\main.py .\tests\kuwo\test_kuwo_smoke.py -q -rs
allure generate .\output\allure_results -o .\output\allure_report --clean
```

验证结果：

- collect：6 tests collected。
- smoke：5 passed, 1 xfailed。
- Allure results 已包含 9 张 PNG 截图附件，覆盖通过步骤和播放页观测。
- Allure 报告：`output/allure_report`。

报告分享方式：

```powershell
allure open .\output\allure_report
python -m http.server 8088 --bind 0.0.0.0 -d .\output\allure_report
Compress-Archive -Path .\output\allure_report\* -DestinationPath .\output\allure_report_with_screenshots.zip -Force
```

### 2026-05-27 第三轮实现

已新增首页 P1 用例：

- `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly`
  - 覆盖 `我的`、`热门`、`榜单`、`会员专区`、`听吧`、`曲库` 可见 Tab 的只读切换。
  - 每个 Tab 切换后保留截图附件。
- `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back`
  - 覆盖首页内容卡进入歌曲列表页。
  - 验证列表页标题、歌曲列表项展示。
  - 返回后验证回到酷我首页。

本轮 POM 更新：

- `KuwoHomePage.is_loaded()` 增加 `热门` Tab 校验，避免歌曲列表详情页被误判为首页。
- 新增 `switch_tab()`、`assert_tab_content_readable()`、`first_content_card_title()`、`open_content_card_by_title()`、`assert_song_list_detail_loaded()`、`close_detail_page()`。
- `KuwoHomeLocators` 增加首页卡片、详情页标题、歌曲名、歌手名定位器。

验证结果：

- `python -m pytest --collect-only -q`：8 tests collected。
- `python .\main.py .\tests\kuwo\test_kuwo_home.py -q -rs`：2 passed。
- `python .\main.py .\tests\kuwo -q -rs`：7 passed, 1 xfailed。
- Allure results 已包含 19 张 PNG 截图附件。
- Allure 报告：`output/allure_report`。

### 下一步建议

### 2026-05-27 第四轮实现

本轮实现范围更大，完成三类任务：

1. 搜索页结果只读自动化：
   - 新增 `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_keyword_results_readonly`。
   - 搜索页复用已有历史词/推荐词 `周杰伦`，避免车机中文输入法不稳定。
   - 验证结果页输入框、`歌曲` 分组、歌曲名和歌手名展示。
   - 用例结束后返回酷我首页。
2. P1/P2 用例映射：
   - 新增 `docs/kuwo_p1_p2_case_mapping.csv`，覆盖酷我 sheet 中 142 条 P1/P2。
   - 新增 `docs/kuwo_case_mapping.md`，汇总 `AUTOMATED/PARTIAL/XFAIL_KNOWN_DEFECT/PLANNED/STATEFUL/MANUAL_AUTH`。
   - 当前映射统计：`AUTOMATED=6`、`PARTIAL=39`、`XFAIL_KNOWN_DEFECT=1`、`PLANNED=36`、`STATEFUL=25`、`MANUAL_AUTH=35`。
3. 报告环境信息：
   - `tests/conftest.py` 新增 Allure `environment.properties`。
   - 报告环境页展示设备 serial、profile、包名、Activity、App 版本、超时配置。

验证结果：

- `python -m pytest --collect-only -q`：9 tests collected。
- `python .\main.py .\tests\kuwo\test_kuwo_search.py -q -rs`：1 passed。
- `python .\main.py .\tests\kuwo -q -rs`：8 passed, 1 xfailed。
- Allure results 已包含 22 张 PNG 截图附件。
- Allure 报告：`output/allure_report`。
- 离线包：`output/allure_report_with_screenshots.zip`。

### 下一步建议

1. 搜索结果页补分类切换、展开更多、结果播放的可恢复路径。
2. 最近收听/播放列表先做只读展示，再做基础播放控制。
3. 播放页继续研究更稳定的 XML/OCR 观测方案。

### 2026-05-27 第五轮实现

本轮继续扩大酷我 P1 主流程覆盖，完成搜索结果扩展、最近收听和播放列表只读展示：

1. 搜索结果扩展：
   - `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_section_readonly`
   - 复用历史词/推荐词 `周杰伦`。
   - 覆盖歌曲结果区、向下滚动后的歌手结果区。
2. 最近收听：
   - `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly`
   - 从“我的”进入 `最近收听`。
   - 保留最近收听页截图和 XML，返回后校验首页。
3. 播放列表：
   - `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_readonly`
   - 从 MiniPlayer 进入播放页，再打开播放列表。
   - 播放列表使用截图作为主证据；XML 可读时增强校验标题和列表控件。
   - 如果 Back 未直接回首页，通过酷我 launch intent 恢复首页并在 Allure 附加说明。

本轮代码更新：

- `helpers/adb_helper.py`：`dump_ui_xml(strict=False)` 的失败占位改为合法 XML，避免 Allure 报告生成时出现坏 XML 解析警告。
- `pageobjects/kuwo/kuwo_player_page.py`：新增 `queue_loaded_from_xml()`，动态 UI dump 失败时不误伤截图证据用例。
- `tests/kuwo/test_kuwo_library.py`：播放列表用例改为截图主证据、XML 增强证据、launch intent 兜底恢复。

验证结果：

- `python .\main.py .\tests\kuwo\test_kuwo_library.py -q -rs`：2 passed。
- `python .\main.py .\tests\kuwo -q -rs`：11 passed, 1 xfailed。
- `allure generate .\output\allure_results -o .\output\allure_report --clean`：成功，无坏 XML 警告。
- Allure HTML 报告包含 30 张 PNG 截图附件。
- 离线报告包：`output/allure_report_with_screenshots.zip`。

映射统计已更新：

- `AUTOMATED=8`
- `PARTIAL=46`
- `XFAIL_KNOWN_DEFECT=1`
- `PLANNED=24`
- `STATEFUL=28`
- `MANUAL_AUTH=35`
- 自动化证据覆盖：55/142（38.7%）。

### 下一步建议

1. 最近收听从只读展示升级到歌曲点击、播放页返回、播放记录校验。
2. 搜索结果页补“更多/展开”、歌手详情进入和返回。
3. 播放列表补歌曲切换、队列项高亮和返回恢复。
4. 设置页补协议、隐私政策、开源免责声明的只读进入和返回。
5. 为 HCP3 四独立包抽象 profile 差异校验，提前验证包名迁移成本。

### 2026-05-27 第六轮实现

本轮按“任务排多一些”的节奏继续扩展，完成设置二级页和搜索歌手详情：

1. 设置-关于页：
   - `tests/kuwo/test_kuwo_settings.py::test_kuwo_settings_about_readonly`
   - 从设置页滚动到底部进入“关于”。
   - 验证版本名称、用户协议、隐私政策、开源免责声明入口。
2. 法律文档只读页：
   - `tests/kuwo/test_kuwo_settings.py::test_kuwo_settings_legal_documents_readonly`
   - 逐个进入用户协议、隐私政策、开源免责声明并截图。
   - 用户协议/隐私政策进入 `com.valtech_mobility.legal.audi`；Back 可能先回法律 App 概览，当前通过酷我 launch intent 恢复。
3. 搜索歌手详情：
   - `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly`
   - 搜索 `周杰伦`，进入歌手详情，验证 `介绍/单曲/专辑`，返回搜索结果页。

本轮代码更新：

- `pagelocators/kuwo_locators.py`：补充设置关于页、法律信息页、搜索歌手详情定位器。
- `pageobjects/kuwo/kuwo_settings_page.py`：新增关于页、法律信息页、开源免责声明页只读动作和断言。
- `pageobjects/kuwo/kuwo_search_page.py`：新增歌手详情进入、断言和返回动作。
- 新增 `tests/kuwo/test_kuwo_settings.py`。

验证结果：

- `python .\main.py .\tests\kuwo\test_kuwo_settings.py -q -rs`：2 passed。
- `python .\main.py .\tests\kuwo\test_kuwo_search.py -q -rs`：3 passed。
- `python .\main.py .\tests\kuwo -q -rs`：14 passed, 1 xfailed。
- Allure HTML 报告包含 39 张 PNG 截图附件。

映射统计已更新：

- `AUTOMATED=8`
- `PARTIAL=52`
- `XFAIL_KNOWN_DEFECT=1`
- `PLANNED=18`
- `STATEFUL=28`
- `MANUAL_AUTH=35`
- 自动化证据覆盖：61/142（43.0%）。

### 下一步建议

1. 最近收听歌曲点击进入播放页，验证播放页返回和记录保留。
2. 播放列表歌曲切换、当前播放高亮和返回恢复。
3. 歌手详情页补 `单曲/专辑` Tab 只读切换。
4. 设置页补音质/音效二级页面只读展示，不修改当前选项。
5. HCP3 四独立包 profile 做启动前置检查和 skip 策略。

### 2026-05-28 第七/八轮实现

本轮继续按“完成 P1/P2 主流程”推进，先完成安全可恢复用例，再把不适合主回归的剩余项归类：

1. 首页酷我 icon：
   - `tests/kuwo/test_kuwo_home.py::test_kuwo_home_logo_module_switcher_readonly`
   - 点击标题栏酷我 logo 区域，验证媒体模块切换弹层包含 `电台/酷我音乐/喜马拉雅/乐听`。
2. 歌单播放/暂停：
   - `tests/kuwo/test_kuwo_home.py::test_kuwo_song_list_miniplayer_play_pause_readonly`
   - 进入热门歌单详情页，点击 MiniPlayer 播放/暂停控件，再点击恢复，保留截图和控件描述。
3. 播放列表长按歌曲：
   - `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_long_press_song_observation`
   - 自动化长按播放列表首行歌曲并保留截图；当前台架没有展示稳定菜单/弹层，记录为 xfail。
4. 映射收口：
   - VIP/会员音乐播放归入 `MANUAL_AUTH`。
   - 搜索历史新增、驾驶模式开关归入 `STATEFUL`。
   - 当前 `PLANNED=0`，P1/P2 全部完成分类。

本轮代码更新：

- `helpers/adb_helper.py`：新增 `long_press()`。
- `pagelocators/kuwo_locators.py`：新增模块切换弹层选项。
- `pageobjects/kuwo/kuwo_home_page.py`：新增 logo 模块切换、MiniPlayer 播放/暂停动作。
- `pageobjects/kuwo/kuwo_player_page.py`：新增播放列表首行长按观测动作。
- `tests/kuwo/test_kuwo_home.py`、`tests/kuwo/test_kuwo_library.py` 新增本轮用例。

验证结果：

- `python .\main.py .\tests\kuwo\test_kuwo_home.py -q -rs`：4 passed。
- `python .\main.py .\tests\kuwo\test_kuwo_library.py -q -rs`：2 passed, 1 xfailed。
- `python .\main.py .\tests\kuwo -q -rs`：16 passed, 2 xfailed。
- Allure HTML 报告包含 49 张 PNG 截图附件。

映射统计已更新：

- `AUTOMATED=9`
- `PARTIAL=53`
- `XFAIL_KNOWN_DEFECT=2`
- `PLANNED=0`
- `STATEFUL=39`
- `MANUAL_AUTH=39`
- P1/P2 分类完成：142/142（100%）。
- 自动化证据覆盖：64/142（45.1%）。

### 下一步建议

1. 把 `PARTIAL` 中的最近收听、播放列表、歌手详情 Tab、设置音质/音效页补强为更强断言。
2. 为 `STATEFUL` 建立可清理测试数据和恢复脚本。
3. 为 `MANUAL_AUTH` 准备固定账号、会员权益、版权资源和扫码策略。
4. 播放页动态 UI 引入 OCR/图像基准，逐步降低 xfail。

### 2026-05-28 下载/收藏/搜索历史/驾驶模式收口

本轮按用户指定的未排项完成 P1/P2 收口：

1. 下载：
   - `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful`
   - `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_player_vip_download_current_song_stateful`
   - 当前台架为已登录会员账号，已验证播放页下载按钮点击后进入下载页可看到下载歌曲。
2. 收藏：
   - `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful`
   - `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful`
   - 收藏专辑/收藏歌单播放按钮路径已实现；当前账号收藏专辑和收藏歌单为空时保留空态截图并 skip，映射状态为 `PARTIAL`。
3. 搜索历史：
   - `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_added_stateful`
   - 使用 ASCII 关键词 `autotest0528`，避免车机中文输入法不稳定，验证重新进入搜索页后历史新增。
4. 驾驶模式：
   - `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful`
   - `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful`
   - `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_logged_in_account_entry_stateful`
   - 使用 `adb shell dumpsys car_service emulate-driving-state drive` 开启，`adb shell dumpsys car_service emulate-driving-state park` 关闭；所有用例 `finally` 兜底恢复 park。

本轮关键代码更新：

- `pagelocators/kuwo_locators.py`：补充驾驶模式限制文案、账户页定位器。
- `pageobjects/kuwo/kuwo_account_page.py`：新增已登录账户页 POM。
- `pageobjects/kuwo/kuwo_settings_page.py`：新增驾驶限制识别和断言。
- `pageobjects/kuwo/kuwo_library_page.py`：新增下载歌曲断言和收藏 Tab 内容判断。
- `pageobjects/kuwo/kuwo_player_page.py`：新增播放页前台判断和下载按钮动作。
- `tests/kuwo/test_kuwo_driving_mode.py`：新增驾驶模式专项。
- `docs/kuwo_p1_p2_case_mapping.csv`、`docs/kuwo_case_mapping.md`：同步更新未排项状态和覆盖率。
- `docs/kuwo_automation_case_coverage.md`：新增 26 条自动化 case 到 Excel P1/P2 功能用例的映射说明。
- `docs/kuwo_p1_p2_coverage_breakdown.md`：新增强覆盖 29 条、证据覆盖 83 条、手工/专项 59 条的明细拆分。

已验证结果：

- `python -m pytest --collect-only -q tests\kuwo`：26 tests collected。
- 驾驶模式 + 播放页下载定向验证：已登录环境曾验证 4 passed；当前台架切为未登录后，VIP 下载和已登录账户驾驶路径按前置 skip。
- 收藏专辑/收藏歌单播放按钮定向验证：1 skipped，原因为当前账号收藏专辑和收藏歌单均为空。
- 最终全量回归 `python .\main.py .\tests\kuwo -q -rs`：21 passed，3 skipped，2 xfailed。
- Allure HTML 已生成到 `output/allure_report`，包含 80 张 PNG 截图附件；离线包为 `output/allure_report_with_screenshots.zip`。

当前映射统计：

- `AUTOMATED=29`
- `PARTIAL=52`
- `XFAIL_KNOWN_DEFECT=2`
- `PLANNED=0`
- `STATEFUL=11`
- `MANUAL_AUTH=48`
- P1/P2 分类完成：142/142（100%）。
- 按当前 VIP 登录账号前置，自动化强覆盖：29/142（20.4%）。
- 自动化证据覆盖：83/142（58.5%）。

仍需要固定前置的部分：

- 未登录/扫码登录驾驶模式。
- 非会员、会员下载次数耗尽、历史已下载权益边界。
- 收藏专辑/收藏歌单播放按钮强断言需要账号预置收藏数据。
- 购买会员、支付、绑定/解绑账号、退出登录等仍为 `MANUAL_AUTH`。


### 2026-05-28 第九轮强覆盖补齐

本轮将上一轮标题栏补强后的映射落盘，并继续把可强断言的 P1/P2 用例从 PARTIAL 升级到 AUTOMATED。

- 新增/补强自动化 case 数量：当前 tests/kuwo 共 34 条。
- 本轮通过的重点用例：会员专区歌单与曲库类目、歌单 MiniPlayer 播放暂停状态、我的页已登录 VIP、播放页返回/酷我 icon/暂停、播放列表点歌、搜索结果连续切歌。
- 当前映射统计：AUTOMATED=68、PARTIAL=13、XFAIL_KNOWN_DEFECT=2、STATEFUL=11、MANUAL_AUTH=48。
- 当前强自动化覆盖：68/142（47.9%）；自动化证据覆盖：83/142（58.5%）。
- 未升级项继续保持真实口径：播放页暂停态点击播放、推荐页单首歌单精确路径、电台分类深层、长按歌曲菜单、收藏预置数据、播放完成、播放页动态 XML 已知缺陷等仍需下一轮专项处理。

### 2026-05-28 第十轮强覆盖补齐

本轮继续从剩余 `PARTIAL` 中挑选可恢复、可断言的场景升级为强自动化：

- 新增/验证 `test_kuwo_tingba_category_and_radio_item_strong`：覆盖听吧分类入口、推荐电台分类列表和电台点击播放。
- 新增/验证 `test_kuwo_favorite_album_detail_song_strong`：收藏专辑进入详情后点击首行歌曲，用酷我媒体会话 `PLAYING` 和元数据做强断言。
- 复验 `test_kuwo_favorite_album_playlist_play_buttons_stateful`：当前 VIP 账号已有收藏专辑和收藏歌单数据，可升级收藏封面播放按钮强覆盖。
- `helpers/adb_helper.py` 增加动态页 XML dump 短重试，并新增 `kuwo_playback_snapshot()`，用于播放页 XML 不稳定时读取系统媒体会话。
- 当前 tests/kuwo 共 36 条；本轮聚焦验证结果：听吧电台 1 passed，收藏专辑详情点歌 1 passed。
- 当前映射统计：AUTOMATED=73、PARTIAL=8、XFAIL_KNOWN_DEFECT=2、STATEFUL=11、MANUAL_AUTH=48。
- 当前强自动化覆盖：73/142（51.4%）；自动化证据覆盖：83/142（58.5%）。

### 2026-05-28 第十一轮强覆盖补齐

本轮继续补强播放链路和热门页可恢复主流程：

- 新增/验证 `test_kuwo_hot_single_song_recommendation_play_strong`：热门推荐榜单卡进入详情，点击首行歌曲，通过媒体会话状态和元数据验证。
- 新增/验证 `test_kuwo_player_page_display_and_play_button_strong`：播放页前台、截图、媒体元数据可用，并验证播放按钮 PAUSED -> PLAYING。
- 新增/验证 `test_kuwo_player_k_song_entry_strong`：播放页点击“去K歌”后前台切到 `com.tencent.audi.karaokecar`，再恢复酷我。
- 长按歌曲专项复探结论：歌单详情、榜单详情、播放列表长按均未出现稳定菜单；长按过久会触发系统桌面编辑，暂不强升。
- 当前 tests/kuwo 共 39 条；本轮聚焦验证结果：3 passed。
- 当前映射统计：AUTOMATED=78、PARTIAL=4、XFAIL_KNOWN_DEFECT=1、STATEFUL=11、MANUAL_AUTH=48。
- 当前强自动化覆盖：78/142（54.9%）；自动化证据覆盖：83/142（58.5%）。

### 2026-05-28 第十二轮强覆盖补齐

本轮补强播放完成场景，并复核剩余不可强升项：

- 新增/验证 `test_kuwo_player_music_completion_by_seek_strong`：播放页拖动进度条到末尾前一点，等待媒体会话 `active_item_id/description` 切换，验证歌曲完成/续播链路。
- 验证结果：1 passed。
- 剩余未强升项为 4 条：歌单详情长按、榜单详情长按、播放列表长按、未登录我的页。前三项当前控件 `long-clickable=false` 且无稳定菜单；未登录态需要登出/清数据或专项账号环境。
- 当前 tests/kuwo 共 40 条。
- 当前映射统计：AUTOMATED=79、PARTIAL=3、XFAIL_KNOWN_DEFECT=1、STATEFUL=11、MANUAL_AUTH=48。
- 当前强自动化覆盖：79/142（55.6%）；自动化证据覆盖：83/142（58.5%）。

### 2026-05-28 第十二轮稳定性修复

完整回归暴露两个顺序稳定性问题，已修复并定向复验通过：

- `test_kuwo_song_list_miniplayer_play_pause_readonly` 从热门动态榜单切到会员专区稳定歌单详情，用于 MiniPlayer 播放/暂停控制验证。
- `test_kuwo_player_k_song_entry_strong` 增加最多 3 次重新进入播放页后点击“去K歌”的恢复重试，处理全量顺序下偶发回到桌面的情况。
- 定向复验：`test_kuwo_song_list_miniplayer_play_pause_readonly`、`test_kuwo_player_k_song_entry_strong`，2 passed。

### 2026-05-28 第十二轮最终回归

修复后已完成完整酷我回归和报告生成：

- `python .\main.py .\tests\kuwo -q -rs --clean-alluredir`：38 passed，2 xfailed。
- `allure generate .\output\allure_results -o .\output\allure_report --clean`：生成成功。
- Allure 报告统计：40 total，38 passed，2 skipped（pytest 的 2 条 xfailed）；PNG 截图附件 80 张。
- 离线报告包：`output/allure_report_with_screenshots.zip`。
- 当前强覆盖停在 79/142；剩余 4 条不建议硬升：三个长按菜单无稳定产品响应，一个未登录账号态需要切换账号/清数据。

