# 酷我音乐自动化测试计划

## 1. 目标

基于现有功能测试用例，优先完成酷我音乐主流程自动化覆盖，并为后续喜马拉雅、爱奇艺、乐听以及 HCP3 独立包迁移预留配置化能力。

本阶段重点不是一次性追求全量自动化，而是先建立稳定的车机自动化骨架：可连接、可启动、可定位、可截图、失败可追溯、用例可按模块和优先级筛选。

## 2. 范围

### 优先自动化

- 酷我启动和首页可达性。
- 首页 Tab 和推荐/热门/榜单/会员专区/听吧/曲库/我的入口。
- 搜索页进入、返回、常规关键词结果展示。
- 设置页展示断言，只读校验，不修改设置。
- MiniPlayer 展示、歌曲元信息、上一首/播放暂停/下一首基础控制。
- 播放详情页可达性和关键控件展示。
- 歌单/榜单/专辑列表页进入和返回。
- 最近收听、播放列表的只读展示和基础播放。

### 默认不做全自动

- 购买会员、续费会员、支付链路。
- 二维码登录、账号绑定/解绑、退出账号。
- 清缓存、删除下载、取消收藏、批量编辑等不可恢复或强状态变更操作。
- 需要固定 VIP 权益、版权资源、历史数据或手工扫码的数据前置。
- 无网络、境外 IP、许可证过期等环境类用例，先作为专项或半自动。

这些用例后续可以用 `manual_auth`、`stateful`、`env_required` 等 marker 管理，避免 CI 中误跑。

## 3. 当前事实

### 功能用例来源

- 文件：`docs/Cariad One Info MEDIA Test Report-CL54.26.153.xlsx`
- Sheet：`酷我`
- 有效用例数：432

| 优先级 | 数量 |
| --- | ---: |
| P1 | 34 |
| P2 | 108 |
| P3 | 199 |
| P4 | 91 |

### 台架环境

| 项 | 值 |
| --- | --- |
| ADB serial | `192.168.2.197:5555` |
| 设备 | `MMI` |
| 系统版本 | `CLU55_OIA_AU_CN_S_UOE_2601501_D033` |
| 分辨率 | `1920x816` |
| 当前媒体包 | `com.jidouauto.media` |
| 当前媒体版本 | `CL54.26.222` |
| 酷我主 Activity | `com.jidouauto.media/.ui.kuwo.main.KuwoMainActivity` |
| 酷我副屏 Activity | `com.jidouauto.media/.ui.kuwo.main.SecondaryKuwoMainActivity` |

> Excel 报告版本为 `CL54.26.153`，台架版本为 `CL54.26.222`。自动化断言需要优先校验稳定 UI 语义，不应强依赖旧版本文案和排序。

### HCP3 包名适配

框架需要通过 profile 管理包名和启动参数：

| 模块 | One Info | HCP3 |
| --- | --- | --- |
| 酷我 | `com.jidouauto.media` | `com.jidouauto.media.kuwo` |
| 爱奇艺 | `com.jidouauto.media` | `com.jidouauto.media.iqiyi` |
| 喜马拉雅 | `com.jidouauto.media` | `com.jidouauto.media.ximalaya` |
| 乐听 | `com.jidouauto.media` | `com.jidouauto.media.leting` |

## 4. 框架架构

建议目录结构：

```text
Media_automation/
  config/
    settings.py
    media_profiles.py
  helpers/
    adb_helper.py
    allure_helper.py
    wait_helper.py
  drivers/
    u2_driver.py
  pagelocators/
    kuwo_locators.py
  pageobjects/
    base_page.py
    kuwo/
      kuwo_home_page.py
      kuwo_search_page.py
      kuwo_settings_page.py
      kuwo_player_page.py
  tests/
    kuwo/
      test_kuwo_smoke.py
      test_kuwo_home.py
      test_kuwo_search.py
      test_kuwo_player.py
  docs/
  output/
```

分层职责：

| 层 | 职责 |
| --- | --- |
| `config` | 设备 serial、包名 profile、超时、报告路径、display id |
| `helpers` | ADB 命令、截图、XML dump、logcat、Allure 附件 |
| `drivers` | uiautomator2 连接、App 启动、设备恢复 |
| `pagelocators` | resource-id、content-desc、text、XPath 统一管理 |
| `pageobjects` | 页面动作和页面级断言，核心逻辑写中文注释 |
| `tests` | pytest 用例，只表达业务步骤和断言 |

## 5. Allure 证据策略

每条 Appium/uiautomator2 用例失败时自动附加：

- 当前截图。
- 当前 UI XML。
- 前台包名和 Activity。
- 设备信息、系统版本、App 版本。
- 最近 logcat 摘要。
- 用例 marker、包名 profile、display id。

正常执行的 P0/P1 smoke 建议保留关键步骤截图，方便报告里直接复盘页面状态。

## 6. 酷我主流程用例分期

### P0：框架可用性

| 编号 | 自动化点 | 验证 |
| --- | --- | --- |
| KWO-P0-001 | ADB 连接指定台架 | `192.168.2.197:5555` 在线 |
| KWO-P0-002 | 启动酷我主 Activity | 前台为 `KuwoMainActivity` |
| KWO-P0-003 | 首页 UI XML 可读 | 能读取 `recyclerView` 和 title line |
| KWO-P0-004 | 截图和 XML 进 Allure | 报告中可查看页面证据 |
| KWO-P0-005 | 失败自动收集上下文 | 截图、XML、Activity、logcat 附件齐全 |

### P1：主流程 smoke

| 编号 | 覆盖模块 | 自动化点 |
| --- | --- | --- |
| KWO-P1-001 | 主页 | 首页展示、酷我图标、Tab、推荐内容 |
| KWO-P1-002 | 主页 Tab | 热门、榜单、会员专区、听吧、曲库、我的可切换 |
| KWO-P1-003 | 搜索 | 进入搜索页、推荐词显示、返回首页 |
| KWO-P1-004 | 设置 | 设置页标题和列表项展示，只读不修改 |
| KWO-P1-005 | MiniPlayer | 歌名、歌手、时间、上一首/播放暂停/下一首控件存在 |
| KWO-P1-006 | 播放页 | 播放详情页可达，标题和核心内容区展示 |
| KWO-P1-007 | 列表页 | 推荐歌单/榜单/专辑进入和返回 |
| KWO-P1-008 | 回归恢复 | 用例结束回到酷我首页 |

### P2：扩展主流程

| 覆盖模块 | 自动化点 |
| --- | --- |
| 搜索 | 输入固定关键词、结果分类切换、结果播放、历史记录只读校验 |
| 播放页 | 播放/暂停、上一首、下一首、播放模式只读观察、进度变化 |
| 最近收听 | 入口展示、列表项进入、播放后记录出现 |
| 播放列表 | 展开、歌曲切换、返回 |
| 歌手/专辑/歌单 | 详情页展示、列表滚动、播放入口 |
| 我的 | 未登录/已登录状态页面展示，登录动作走 `manual_auth` |

### P3：专项和半自动

| 类型 | 处理方式 |
| --- | --- |
| 账号、二维码、绑定/解绑 | `manual_auth`，只自动化页面可达和二维码展示 |
| VIP、会员音乐 | 需要固定会员账号和版权稳定测试数据 |
| 下载、删除、清缓存 | `stateful`，需明确可清理目录和恢复策略 |
| 无网络、许可证、境外 IP | `env_required`，由专项环境触发 |
| 购买、支付 | 默认人工执行，不进入自动化 CI |

## 7. 覆盖率评估

以酷我 432 条功能用例为基准：

| 阶段 | 预计覆盖 | 覆盖率 |
| --- | ---: | ---: |
| 首批 P0/P1 smoke | 55-65 条 | 13%-15% |
| 酷我 P1/P2 主流程完成 | 115-125 条 P1/P2 | P1/P2 覆盖 81%-88% |
| 稳定 CI 回归集 | 210-230 条 | 49%-53% |
| 最终安全自动化覆盖 | 260-280 条 | 60%-65% |

结论：

- 酷我 P1/P2 主流程最终可达到约 80%-85% 自动化覆盖。
- 酷我全量 432 条用例最终可达到约 60%-65% 稳定自动化覆盖。
- 剩余 35%-40% 主要受账号、支付、会员权益、版权资源、下载/收藏/清缓存状态变更、环境构造限制影响，建议保留为手工、半自动或专项自动化。

## 8. 本轮探索结论

已采集证据目录：`output/evidence/kuwo_explore_20260527/`

关键截图：

- 首页：`kuwo_home.png`
- 搜索页：`kuwo_search.png`
- 设置页：`kuwo_settings.png`
- 播放页：`kuwo_player_wait.png`

重要发现：

1. 首页和 MiniPlayer 控件树稳定，适合作为首批 smoke。
2. 搜索页会拉起软键盘，返回策略需要在 Page Object 中封装。
3. 设置页是高风险页面，自动化默认只读验证，不点击可变更项。
4. 播放详情页可达但内容区等待后仍为空，与 `CAOIMEDIA-2024` 高度相关，应纳入 P1 观测。
5. 当前为多屏环境，截图命令需要固定 display id，避免后续证据采错屏。

## 9. 下一轮落地任务

已完成：

1. 新建基础工程结构和依赖文件。
2. 实现 `ADBHelper`，封装连接、截图、UI dump、前台 Activity、logcat。
3. 实现 pytest fixture 和 Allure 失败附件 hook。
4. 实现酷我首页、搜索页、设置页、播放页 Page Object。
5. 首批落地 `test_kuwo_smoke.py`，覆盖启动、首页、搜索入口、设置只读、MiniPlayer、播放页观测。
6. 每次新增代码同步更新 `README.md` 和 `docs/context_handoff.md`。

本轮验证结果：

| 命令 | 结果 |
| --- | --- |
| `python -m pytest --collect-only -q` | 6 tests collected |
| `python .\main.py .\tests\kuwo\test_kuwo_smoke.py -q -rs` | 5 passed, 1 xfailed，包含 9 张截图附件 |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功 |

播放页说明：

- 播放页截图可见内容正常展示，但 `uiautomator dump` 在动态播放页可能无法产出新 XML。
- 当前用例将播放页观测标记为 xfail，并保留截图证据。
- 后续可通过暂停播放后 dump、图像/OCR 基准或 App 侧更稳定的 accessibility 信息提升为强断言。

## 10. 下一轮任务

已完成：

1. 将首页 Tab 和列表页进入/返回拆成独立 P1 用例。

本轮新增覆盖：

| 自动化用例 | 覆盖点 | 状态 |
| --- | --- | --- |
| `test_kuwo_home_visible_tabs_readonly` | 首页可见 Tab 只读切换：我的、热门、榜单、会员专区、听吧、曲库 | passed |
| `test_kuwo_home_content_card_enter_and_back` | 首页内容卡进入歌曲列表页、列表展示、返回首页 | passed |

当前验证结果：

| 命令 | 结果 |
| --- | --- |
| `python -m pytest --collect-only -q` | 8 tests collected |
| `python .\main.py .\tests\kuwo\test_kuwo_home.py -q -rs` | 2 passed |
| `python .\main.py .\tests\kuwo -q -rs` | 7 passed, 1 xfailed，包含 19 张截图附件 |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功 |

## 11. 下一轮任务

已完成：

1. 为搜索页加入固定关键词搜索和结果页只读校验。
2. 建立酷我 Excel 用例到自动化用例的映射表。

本轮新增覆盖：

| 自动化用例 | 覆盖点 | 状态 |
| --- | --- | --- |
| `test_kuwo_search_history_keyword_results_readonly` | 复用历史词 `周杰伦` 进入搜索结果页，校验歌曲结果展示，返回首页 | passed |

P1/P2 映射产物：

| 文件 | 内容 |
| --- | --- |
| `docs/kuwo_p1_p2_case_mapping.csv` | 酷我 142 条 P1/P2 明细映射 |
| `docs/kuwo_case_mapping.md` | 汇总统计和已覆盖明细 |

当前映射统计：

| 状态 | 数量 |
| --- | ---: |
| `AUTOMATED` | 6 |
| `PARTIAL` | 39 |
| `XFAIL_KNOWN_DEFECT` | 1 |
| `PLANNED` | 36 |
| `STATEFUL` | 25 |
| `MANUAL_AUTH` | 35 |

当前验证结果：

| 命令 | 结果 |
| --- | --- |
| `python -m pytest --collect-only -q` | 9 tests collected |
| `python .\main.py .\tests\kuwo\test_kuwo_search.py -q -rs` | 1 passed |
| `python .\main.py .\tests\kuwo -q -rs` | 8 passed, 1 xfailed，包含 22 张截图附件 |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功 |

## 12. 下一轮任务

1. 搜索结果页补分类切换、展开更多、结果播放的可恢复路径。
2. 最近收听/播放列表先做只读展示，再做基础播放控制。
3. 播放页继续研究更稳定的 XML/OCR 观测方案。

## 13. 本轮任务

已完成：

1. 搜索结果页补充歌手区只读观察，复用历史词 `周杰伦`，避免车机中文输入法不稳定。
2. 新增最近收听页只读展示用例，保留页面截图和 XML。
3. 新增播放列表只读展示用例，使用截图作为主证据，XML 可读时做增强校验。
4. `ADBHelper.dump_ui_xml()` 的失败占位改为合法 XML，避免 Allure 生成报告时出现坏 XML 警告。
5. 更新 P1/P2 映射，删除类播放列表用例归入 `STATEFUL`，避免未授权状态变更。

本轮新增覆盖：

| 自动化用例 | 覆盖点 | 状态 |
| --- | --- | --- |
| `test_kuwo_search_artist_section_readonly` | 搜索结果页歌曲区、歌手区只读展示 | passed |
| `test_kuwo_recent_list_observation_readonly` | 最近收听页入口、列表展示、返回首页 | passed |
| `test_kuwo_play_queue_readonly` | 播放页打开播放列表、截图证据、返回恢复 | passed |

当前验证结果：

| 命令 | 结果 |
| --- | --- |
| `python .\main.py .\tests\kuwo\test_kuwo_library.py -q -rs` | 2 passed |
| `python .\main.py .\tests\kuwo -q -rs` | 11 passed, 1 xfailed |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功，包含 30 张 PNG 截图 |

当前 P1/P2 映射统计：

| 状态 | 数量 |
| --- | ---: |
| `AUTOMATED` | 8 |
| `PARTIAL` | 46 |
| `XFAIL_KNOWN_DEFECT` | 1 |
| `PLANNED` | 24 |
| `STATEFUL` | 28 |
| `MANUAL_AUTH` | 35 |

当前自动化强覆盖为 8/142（5.6%），自动化证据覆盖为 55/142（38.7%）。预计最终在准备稳定账号、版权资源和可恢复测试数据后，酷我 P1/P2 主流程仍可达到约 80%-85% 自动化覆盖；全量 432 条用例可达到约 60%-65% 稳定自动化覆盖。

## 14. 下一轮任务

1. 最近收听从只读展示升级到歌曲点击、播放页返回、播放记录校验。
2. 搜索结果页继续补“更多/展开”、歌手详情进入和返回。
3. 播放列表补歌曲切换、队列项高亮和返回恢复策略。
4. 设置页补协议/隐私/开源免责声明页面的只读进入和返回。
5. 开始为 HCP3 四独立包抽象 profile 差异校验，确保包名迁移时用例可复用。

## 15. 本轮任务

已完成：

1. 设置页滚动到底部，进入“关于”页并验证版本、用户协议、隐私政策、开源免责声明入口。
2. 逐个进入用户协议、隐私政策、开源免责声明，保留截图；跨包法律信息页通过 launch intent 恢复酷我首页。
3. 搜索结果页进入歌手详情页，验证 `介绍/单曲/专辑` Tab，并返回搜索结果页。
4. 将歌手详情页、法律文档入口更新到 P1/P2 映射。

本轮新增覆盖：

| 自动化用例 | 覆盖点 | 状态 |
| --- | --- | --- |
| `test_kuwo_settings_about_readonly` | 设置-关于页展示和返回 | passed |
| `test_kuwo_settings_legal_documents_readonly` | 用户协议、隐私政策、开源免责声明只读进入 | passed |
| `test_kuwo_search_artist_detail_readonly` | 搜索结果歌手详情进入、展示、返回 | passed |

当前验证结果：

| 命令 | 结果 |
| --- | --- |
| `python .\main.py .\tests\kuwo\test_kuwo_settings.py -q -rs` | 2 passed |
| `python .\main.py .\tests\kuwo\test_kuwo_search.py -q -rs` | 3 passed |
| `python .\main.py .\tests\kuwo -q -rs` | 14 passed, 1 xfailed |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功，包含 39 张 PNG 截图 |

当前 P1/P2 映射统计：

| 状态 | 数量 |
| --- | ---: |
| `AUTOMATED` | 8 |
| `PARTIAL` | 52 |
| `XFAIL_KNOWN_DEFECT` | 1 |
| `PLANNED` | 18 |
| `STATEFUL` | 28 |
| `MANUAL_AUTH` | 35 |

当前自动化强覆盖为 8/142（5.6%），自动化证据覆盖为 61/142（43.0%）。

## 16. 下一轮任务

1. 最近收听歌曲点击进入播放页，验证播放页返回和记录保留。
2. 播放列表歌曲切换、当前播放高亮和返回恢复。
3. 歌手详情页补“单曲/专辑”Tab 只读切换。
4. 设置页补音质/音效二级页面只读展示，但不修改当前选项。
5. HCP3 四独立包 profile 做启动前置检查和 skip 策略。

## 17. 本轮任务

已完成：

1. 首页酷我 logo 点击后展示媒体模块切换弹层，验证 `电台/酷我音乐/喜马拉雅/乐听`。
2. 歌单详情页点击底部 MiniPlayer 播放/暂停控件，并再次点击恢复，保留截图和控件描述。
3. 播放列表歌曲长按已自动化观测；当前台架未展示稳定菜单/弹层，记录为 xfail。
4. VIP 会员音乐、搜索历史新增、驾驶模式开关类用例已从 `PLANNED` 归类到 `MANUAL_AUTH` 或 `STATEFUL`，避免主回归误跑。

本轮新增覆盖：

| 自动化用例 | 覆盖点 | 状态 |
| --- | --- | --- |
| `test_kuwo_home_logo_module_switcher_readonly` | 首页酷我 logo 打开媒体模块切换弹层 | passed |
| `test_kuwo_song_list_miniplayer_play_pause_readonly` | 歌单详情页播放/暂停控件可点击并恢复 | passed |
| `test_kuwo_play_queue_long_press_song_observation` | 播放列表歌曲长按观测 | xfailed |

当前验证结果：

| 命令 | 结果 |
| --- | --- |
| `python .\main.py .\tests\kuwo\test_kuwo_home.py -q -rs` | 4 passed |
| `python .\main.py .\tests\kuwo\test_kuwo_library.py -q -rs` | 2 passed, 1 xfailed |
| `python .\main.py .\tests\kuwo -q -rs` | 16 passed, 2 xfailed |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功，包含 49 张 PNG 截图 |

当前 P1/P2 映射统计：

| 状态 | 数量 |
| --- | ---: |
| `AUTOMATED` | 9 |
| `PARTIAL` | 53 |
| `XFAIL_KNOWN_DEFECT` | 2 |
| `PLANNED` | 0 |
| `STATEFUL` | 39 |
| `MANUAL_AUTH` | 39 |

当前 P1/P2 分类完成 142/142（100%），自动化强覆盖为 9/142（6.3%），自动化证据覆盖为 64/142（45.1%）。后续主攻方向从“消灭 PLANNED”转为把 `PARTIAL` 补强到更高断言强度，并为 `STATEFUL/MANUAL_AUTH` 准备专项前置条件。

## 18. 下一轮任务

1. 将最近收听歌曲点击、播放页返回、记录保留做成可恢复强断言。
2. 播放列表歌曲切换和当前播放高亮补强，长按菜单继续作为产品/动态 UI 限制跟踪。
3. 歌手详情页补 `单曲/专辑` Tab 只读切换。
4. 设置音质/音效二级页只读展示，不修改当前选项。
5. 为 `STATEFUL` 和 `MANUAL_AUTH` 建立专项执行清单、账号/数据前置和跳过策略。

## 19. 本轮任务

本轮按用户指定的“未排部分”继续收口，重点完成下载、收藏、搜索历史和驾驶模式：

1. 下载：
   - `test_kuwo_download_page_title_actions_stateful` 覆盖下载页返回、搜索、设置、酷我 icon。
   - `test_kuwo_player_vip_download_current_song_stateful` 覆盖已登录会员账号在播放页点击下载、下载成功后进入下载页验证歌曲展示。
2. 收藏：
   - `test_kuwo_favorite_page_title_actions_stateful` 覆盖收藏页返回、搜索、设置、酷我 icon。
   - `test_kuwo_favorite_album_playlist_play_buttons_stateful` 已实现收藏专辑/收藏歌单首卡播放按钮路径；当前账号收藏专辑/歌单可能为空，空数据时保留截图并 skip，需预置收藏数据才能强断言播放按钮。
3. 搜索历史：
   - `test_kuwo_search_history_added_stateful` 使用 ASCII 测试词 `autotest0528` 搜索，重新进入搜索页验证历史新增。
4. 驾驶模式：
   - 新增 `tests/kuwo/test_kuwo_driving_mode.py`。
   - 覆盖 drive 模式下点击用户协议、隐私政策、开源免责声明的限制表现。
   - 覆盖 park 打开协议页后切 drive 出现限制，再切 park 恢复内容。
   - 覆盖已登录账号态 drive 后进入账户页，验证昵称、会员有效期、续费/绑定入口展示。
   - 所有驾驶模式用例在 `finally` 中恢复 `adb shell dumpsys car_service emulate-driving-state park`。

本轮新增/更新代码：

| 文件 | 说明 |
| --- | --- |
| `pagelocators/kuwo_locators.py` | 补充驾驶限制文案、开源免责声明限制控件、账户页定位器。 |
| `pageobjects/kuwo/kuwo_home_page.py` | 补充“我的”页已登录判断和头像进入账户页动作。 |
| `pageobjects/kuwo/kuwo_account_page.py` | 新增已登录账户页断言。 |
| `pageobjects/kuwo/kuwo_settings_page.py` | 新增驾驶限制识别和断言。 |
| `pageobjects/kuwo/kuwo_library_page.py` | 新增下载歌曲断言、收藏 Tab 内容判断。 |
| `pageobjects/kuwo/kuwo_player_page.py` | 新增播放页前台判断和下载按钮坐标动作。 |
| `tests/kuwo/test_kuwo_stateful_pages.py` | 新增下载、收藏、播放页下载和空收藏数据处理。 |
| `tests/kuwo/test_kuwo_driving_mode.py` | 新增驾驶模式三条专项用例。 |

本轮验证结果：

| 命令 | 结果 |
| --- | --- |
| `python -m pytest --collect-only -q tests\kuwo` | 26 tests collected |
| `python .\main.py .\tests\kuwo\test_kuwo_driving_mode.py .\tests\kuwo\test_kuwo_stateful_pages.py::test_kuwo_player_vip_download_current_song_stateful -q -rs` | 已登录环境曾验证 4 passed；当前台架切为未登录后，VIP 下载和已登录账户驾驶路径按前置 skip |
| `python .\main.py .\tests\kuwo\test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful -q -rs` | 1 skipped，当前账号收藏专辑和收藏歌单均为空 |
| `python .\main.py .\tests\kuwo -q -rs` | 21 passed，3 skipped，2 xfailed |
| `allure generate .\output\allure_results -o .\output\allure_report --clean` | 报告生成成功，包含 80 张 PNG 截图附件 |

当前 P1/P2 映射统计：

| 状态 | 数量 |
| --- | ---: |
| `AUTOMATED` | 29 |
| `PARTIAL` | 52 |
| `XFAIL_KNOWN_DEFECT` | 2 |
| `PLANNED` | 0 |
| `STATEFUL` | 11 |
| `MANUAL_AUTH` | 48 |

当前 P1/P2 分类完成 142/142（100%），按当前 VIP 登录账号前置，自动化强覆盖为 29/142（20.4%），自动化证据覆盖为 83/142（58.5%）。受扫码登录、未登录账号态、支付、购买会员、权益边界、收藏预置数据、下载次数耗尽等限制影响的用例已转为 `PARTIAL`、`STATEFUL` 或 `MANUAL_AUTH`，不再作为未排项遗漏。自动化 case 明细见 `docs/kuwo_automation_case_coverage.md`。Allure 报告中 skipped=5，对应 pytest 的 3 skipped + 2 xfailed。


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

