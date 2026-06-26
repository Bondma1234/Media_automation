# 酷我 P1/P2 自动化用例映射

来源：`docs/Cariad One Info MEDIA Test Report-CL54.26.153.xlsx` 的 `酷我` sheet。

范围：仅统计 P1/P2，共 `142` 条。完整明细见 `docs/kuwo_p1_p2_case_mapping.csv`。

## 状态汇总

| 状态 | 数量 | 说明 |
| --- | ---: | --- |
| `AUTOMATED` | 79 | 已由当前自动化用例完整覆盖。 |
| `PARTIAL` | 3 | 已覆盖入口、展示或只读主路径，深层动作或强断言仍受页面动态、账号/数据前置或可恢复性影响。 |
| `XFAIL_KNOWN_DEFECT` | 1 | 已自动化观测，但受已知缺陷或动态 UI 采集限制。 |
| `PLANNED` | 0 | 后续正常自动化计划。 |
| `STATEFUL` | 11 | 仍涉及删除、清缓存等强状态变更，需隔离数据或专项恢复策略。 |
| `MANUAL_AUTH` | 48 | 涉及账号、扫码、会员、支付、权益边界或账号态切换，默认人工/半自动。 |

当前 P1/P2 分类完成：142/142（100%）；自动化强覆盖：79/142（55.6%）；自动化证据覆盖（AUTOMATED + PARTIAL + XFAIL）：83/142（58.5%）。

## 模块分布

| 模块 | P1/P2 数量 |
| --- | ---: |
| 驾驶模式 | 13 |
| 播放页 | 12 |
| 账号 | 12 |
| 下载 | 11 |
| 主页 | 11 |
| 购买会员 | 10 |
| 关联账号 | 9 |
| 自建歌单 | 8 |
| 收藏 | 6 |
| 播放列表 | 5 |
| 歌单详情页 | 5 |
| 推荐页面 | 4 |
| 搜索 | 4 |
| 播放歌曲 | 4 |
| 最近收听 | 4 |
| 榜单列表页 | 4 |
| miniplayer | 3 |
| 我的 | 3 |
| 歌手介绍页 | 3 |
| 电台 | 3 |
| 会员专区 | 2 |
| 曲库 | 2 |
| 热门 | 2 |
| 专辑列表页 | 1 |
| 设置 | 1 |

## 自动化和证据覆盖明细

| Excel ID | 优先级 | 模块 | 用例标题 | 状态 | 自动化用例 |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | 主页 | 查看酷我主页显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_launch_kuwo_home` |
| 2 | P2 | 主页 | 酷我主页点击搜索按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_search_page_readonly` |
| 3 | P2 | 主页 | 酷我主页点击设置按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_settings_page_readonly` |
| 4 | P2 | 主页 | 酷我主页点击酷我icon | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_logo_module_switcher_readonly` |
| 5 | P1 | 主页 | 酷我主页点击推荐 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 6 | P1 | 主页 | 酷我主页点击会员专区 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 7 | P1 | 主页 | 酷我主页点击热点 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 8 | P1 | 主页 | 酷我主页点击电台 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 9 | P1 | 主页 | 酷我主页点击曲库 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 10 | P1 | 主页 | 酷我主页点击我的 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 11 | P2 | 推荐页面 | 酷我主页划动页面 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 12 | P2 | 推荐页面 | 查看推荐页面显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 13 | P2 | 推荐页面 | 推荐页中点击歌单 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` |
| 14 | P2 | 推荐页面 | 推荐页中点击只有一首歌曲的歌单 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` |
| 15 | P2 | 会员专区 | 查看会员专区页显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 16 | P2 | 会员专区 | 会员专区页中点击歌单 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_member_playlist_and_library_category_strong` |
| 17 | P2 | 热门 | 查看热点页面显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 18 | P2 | 热门 | 热点页面点击榜单验证 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` |
| 19 | P2 | 电台 | 查看电台页显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 20 | P2 | 电台 | 点击电台页中的类目验证 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_tingba_category_and_radio_item_strong` |
| 21 | P2 | 电台 | 电台分类页中点击分类 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_tingba_category_and_radio_item_strong` |
| 22 | P2 | 曲库 | 查看曲库页面显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 24 | P2 | 曲库 | 点击场景中的类目 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_member_playlist_and_library_category_strong` |
| 25 | P1 | 主页 | 点击歌单中的播放/暂停按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_song_list_miniplayer_play_pause_readonly` |
| 26 | P2 | 歌单详情页 | 歌单-歌曲列表页点击搜索按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 27 | P2 | 歌单详情页 | 歌单-歌曲列表页点击设置按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 28 | P2 | 歌单详情页 | 歌单-歌曲列表页点击酷我icon | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 29 | P2 | 歌单详情页 | 歌单-歌曲列表页点击返回按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 30 | P2 | 歌单详情页 | 歌单-歌曲列表页长按歌曲 | `PARTIAL` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 32 | P2 | 榜单列表页 | 榜单-歌曲列表页点击设置按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 33 | P2 | 榜单列表页 | 榜单-歌曲列表页点击酷我icon | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 34 | P2 | 榜单列表页 | 榜单-歌曲列表页点击返回按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 35 | P2 | 榜单列表页 | 榜单-歌曲列表页长按歌曲 | `PARTIAL` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 36 | P2 | 我的 | 已登录账号查看我的页面显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_mine_logged_in_vip_status_strong` |
| 37 | P2 | 我的 | 未登录账号查看我的页面显示 | `PARTIAL` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 38 | P2 | 我的 | 已登录VIP账号查看我的页面显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_home.py::test_kuwo_mine_logged_in_vip_status_strong` |
| 49 | P2 | 最近收听 | 最近收听页面点击搜索 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 50 | P2 | 最近收听 | 最近收听页面点击设置 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 51 | P2 | 最近收听 | 最近收听页面点击酷我ICON | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 53 | P1 | 最近收听 | 最近收听页点击音乐 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 65 | P2 | 下载 | 下载页面点击返回 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 66 | P2 | 下载 | 下载页面点击搜索 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 67 | P2 | 下载 | 下载页面点击设置 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 68 | P2 | 下载 | 下载页面点击酷我ICON | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 77 | P2 | 下载 | 会员账号下载需VIP下载的单曲 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_player_vip_download_current_song_stateful` |
| 95 | P2 | 收藏 | 收藏页面点击返回 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 96 | P2 | 收藏 | 收藏页面点击搜索 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 97 | P2 | 收藏 | 收藏页面点击设置 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 98 | P2 | 收藏 | 收藏页面点击酷我ICON | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 126 | P1 | 收藏 | 收藏专辑页点击图片中的播放/暂停按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful` |
| 139 | P1 | 收藏 | 收藏歌单页点击图片中的播放/暂停按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful` |
| 206 | P1 | 播放页 | 查看普通歌曲播放页显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_page_display_and_play_button_strong` |
| 210 | P2 | 播放页 | 播放页点击返回按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` |
| 211 | P2 | 播放页 | 播放页点击播放列表按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_readonly` |
| 212 | P2 | 播放页 | 播放页点击酷我ICON | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` |
| 213 | P2 | 播放页 | CHCL46MEDIA-1008 播放页点击去K歌icon | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_k_song_entry_strong` |
| 242 | P2 | 播放页 | 播放页点击播放按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_page_display_and_play_button_strong` |
| 243 | P2 | 播放页 | 播放页点击暂停按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` |
| 244 | P2 | 播放页 | 音乐播放完验证 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_music_completion_by_seek_strong` |
| 259 | P2 | miniplayer | 退出播放详情页 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` |
| 263 | P2 | miniplayer | 播放状态播放条中点击播放按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` |
| 264 | P2 | miniplayer | 暂停播放状态播放条中点击播放按钮 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` |
| 269 | P2 | 播放列表 | 播放列表页面点击歌曲 | `AUTOMATED` | `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_tap_song_strong` |
| 270 | P2 | 播放列表 | 播放列表页长按歌曲 | `XFAIL_KNOWN_DEFECT` | `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_long_press_song_observation` |
| 283 | P2 | 专辑列表页 | 专辑列表页点击歌曲 | `AUTOMATED` | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_detail_song_strong` |
| 288 | P2 | 歌手介绍页 | 歌手详情页点击搜索 | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` |
| 289 | P2 | 歌手介绍页 | 歌手详情页点击设置 | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` |
| 290 | P2 | 歌手介绍页 | 歌手详情页点击酷我icon | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` |
| 302 | P1 | 设置 | 查看设置页面显示 | `AUTOMATED` | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_settings_page_readonly` |
| 379 | P2 | 搜索 | 搜索组合的数据 | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_section_readonly` |
| 390 | P1 | 搜索 | 搜索页多个搜索结果间来回切换播放 | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_multiple_result_song_switch_strong` |
| 400 | P1 | 搜索 | 搜索页观察搜索历史新增 | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_added_stateful` |
| 401 | P1 | 搜索 | 搜索页点击历史搜索记录 | `AUTOMATED` | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_keyword_results_readonly` |
| 407 | P2 | 驾驶模式 | 开启了驾驶模式，点击用户协议 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` |
| 408 | P2 | 驾驶模式 | 开启了驾驶模式，点击隐私政策 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` |
| 409 | P2 | 驾驶模式 | 开启了驾驶模式，点击开源免责声明 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` |
| 410 | P2 | 驾驶模式 | 进入用户协议页面后开启驾驶模式 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 411 | P2 | 驾驶模式 | 进入隐私政策页面后开启驾驶模式 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 412 | P2 | 驾驶模式 | 进入开源免责声明后开启驾驶模式 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 413 | P2 | 驾驶模式 | 处于用户协议页面，关闭驾驶模式验证 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 414 | P2 | 驾驶模式 | 处于隐私政策页面，关闭驾驶模式验证 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 415 | P2 | 驾驶模式 | 处于开源免责声明页面，关闭驾驶模式验证 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 417 | P2 | 驾驶模式 | 开启驾驶模式后已登录进入帐户页面 | `AUTOMATED` | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_logged_in_account_entry_stateful` |
