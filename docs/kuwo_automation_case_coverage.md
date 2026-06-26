# 酷我自动化用例覆盖说明

本文说明当前 `tests/kuwo` 下 40 条 pytest 自动化 case 与 Excel P1/P2 功能用例的映射关系。

## 1. 汇总

| 项 | 数量 | 说明 |
| --- | ---: | --- |
| 当前自动化 case | 40 | `python -m pytest --collect-only -q tests\kuwo` 收集结果。 |
| P1/P2 功能用例总数 | 142 | 来源于酷我 sheet。 |
| 强自动化覆盖 | 79/142，55.6% | 当前自动化能完整校验的 Excel 功能用例数。 |
| 自动化证据覆盖 | 83/142，58.5% | 包含强覆盖、部分覆盖、已知缺陷观测。 |
| 手工/专项范围 | 59/142 | 账号态、扫码、支付权益、删除清缓存等。 |

## 2. 自动化 Case 映射

| 自动化 case | 覆盖功能用例 |
| --- | --- |
| `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` | 407 P2 驾驶模式「开启了驾驶模式，点击用户协议」[AUTOMATED]<br>408 P2 驾驶模式「开启了驾驶模式，点击隐私政策」[AUTOMATED]<br>409 P2 驾驶模式「开启了驾驶模式，点击开源免责声明」[AUTOMATED] |
| `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` | 410 P2 驾驶模式「进入用户协议页面后开启驾驶模式」[AUTOMATED]<br>411 P2 驾驶模式「进入隐私政策页面后开启驾驶模式」[AUTOMATED]<br>412 P2 驾驶模式「进入开源免责声明后开启驾驶模式」[AUTOMATED]<br>413 P2 驾驶模式「处于用户协议页面，关闭驾驶模式验证」[AUTOMATED]<br>414 P2 驾驶模式「处于隐私政策页面，关闭驾驶模式验证」[AUTOMATED]<br>415 P2 驾驶模式「处于开源免责声明页面，关闭驾驶模式验证」[AUTOMATED] |
| `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_logged_in_account_entry_stateful` | 417 P2 驾驶模式「开启驾驶模式后已登录进入帐户页面」[AUTOMATED] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` | 26 P2 歌单详情页「歌单-歌曲列表页点击搜索按钮」[AUTOMATED]<br>27 P2 歌单详情页「歌单-歌曲列表页点击设置按钮」[AUTOMATED]<br>28 P2 歌单详情页「歌单-歌曲列表页点击酷我icon」[AUTOMATED]<br>29 P2 歌单详情页「歌单-歌曲列表页点击返回按钮」[AUTOMATED]<br>30 P2 歌单详情页「歌单-歌曲列表页长按歌曲」[PARTIAL]<br>32 P2 榜单列表页「榜单-歌曲列表页点击设置按钮」[AUTOMATED]<br>33 P2 榜单列表页「榜单-歌曲列表页点击酷我icon」[AUTOMATED]<br>34 P2 榜单列表页「榜单-歌曲列表页点击返回按钮」[AUTOMATED]<br>35 P2 榜单列表页「榜单-歌曲列表页长按歌曲」[PARTIAL] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_home_logo_module_switcher_readonly` | 4 P2 主页「酷我主页点击酷我icon」[AUTOMATED] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` | 5 P1 主页「酷我主页点击推荐」[AUTOMATED]<br>6 P1 主页「酷我主页点击会员专区」[AUTOMATED]<br>7 P1 主页「酷我主页点击热点」[AUTOMATED]<br>8 P1 主页「酷我主页点击电台」[AUTOMATED]<br>9 P1 主页「酷我主页点击曲库」[AUTOMATED]<br>10 P1 主页「酷我主页点击我的」[AUTOMATED]<br>11 P2 推荐页面「酷我主页划动页面」[AUTOMATED]<br>12 P2 推荐页面「查看推荐页面显示」[AUTOMATED]<br>15 P2 会员专区「查看会员专区页显示」[AUTOMATED]<br>17 P2 热门「查看热点页面显示」[AUTOMATED]<br>19 P2 电台「查看电台页显示」[AUTOMATED]<br>22 P2 曲库「查看曲库页面显示」[AUTOMATED]<br>37 P2 我的「未登录账号查看我的页面显示」[PARTIAL] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` | 13 P2 推荐页面「推荐页中点击歌单」[AUTOMATED]<br>14 P2 推荐页面「推荐页中点击只有一首歌曲的歌单」[AUTOMATED]<br>18 P2 热门「热点页面点击榜单验证」[AUTOMATED] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_member_playlist_and_library_category_strong` | 16 P2 会员专区「会员专区页中点击歌单」[AUTOMATED]<br>24 P2 曲库「点击场景中的类目」[AUTOMATED] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_mine_logged_in_vip_status_strong` | 36 P2 我的「已登录账号查看我的页面显示」[AUTOMATED]<br>38 P2 我的「已登录VIP账号查看我的页面显示」[AUTOMATED] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_song_list_miniplayer_play_pause_readonly` | 25 P1 主页「点击歌单中的播放/暂停按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_home.py::test_kuwo_tingba_category_and_radio_item_strong` | 20 P2 电台「点击电台页中的类目验证」[AUTOMATED]<br>21 P2 电台「电台分类页中点击分类」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_long_press_song_observation` | 270 P2 播放列表「播放列表页长按歌曲」[XFAIL_KNOWN_DEFECT] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_readonly` | 211 P2 播放页「播放页点击播放列表按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_tap_song_strong` | 269 P2 播放列表「播放列表页面点击歌曲」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_player_k_song_entry_strong` | 213 P2 播放页「CHCL46MEDIA-1008 播放页点击去K歌icon」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_player_music_completion_by_seek_strong` | 244 P2 播放页「音乐播放完验证」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_player_page_display_and_play_button_strong` | 206 P1 播放页「查看普通歌曲播放页显示」[AUTOMATED]<br>242 P2 播放页「播放页点击播放按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` | 210 P2 播放页「播放页点击返回按钮」[AUTOMATED]<br>212 P2 播放页「播放页点击酷我ICON」[AUTOMATED]<br>243 P2 播放页「播放页点击暂停按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` | 49 P2 最近收听「最近收听页面点击搜索」[AUTOMATED]<br>50 P2 最近收听「最近收听页面点击设置」[AUTOMATED]<br>51 P2 最近收听「最近收听页面点击酷我ICON」[AUTOMATED]<br>53 P1 最近收听「最近收听页点击音乐」[AUTOMATED] |
| `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` | 288 P2 歌手介绍页「歌手详情页点击搜索」[AUTOMATED]<br>289 P2 歌手介绍页「歌手详情页点击设置」[AUTOMATED]<br>290 P2 歌手介绍页「歌手详情页点击酷我icon」[AUTOMATED] |
| `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_section_readonly` | 379 P2 搜索「搜索组合的数据」[AUTOMATED] |
| `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_added_stateful` | 400 P1 搜索「搜索页观察搜索历史新增」[AUTOMATED] |
| `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_keyword_results_readonly` | 401 P1 搜索「搜索页点击历史搜索记录」[AUTOMATED] |
| `tests/kuwo/test_kuwo_search.py::test_kuwo_search_multiple_result_song_switch_strong` | 390 P1 搜索「搜索页多个搜索结果间来回切换播放」[AUTOMATED] |
| `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` | 259 P2 miniplayer「退出播放详情页」[AUTOMATED]<br>263 P2 miniplayer「播放状态播放条中点击播放按钮」[AUTOMATED]<br>264 P2 miniplayer「暂停播放状态播放条中点击播放按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_smoke.py::test_kuwo_search_page_readonly` | 2 P2 主页「酷我主页点击搜索按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_smoke.py::test_kuwo_settings_page_readonly` | 3 P2 主页「酷我主页点击设置按钮」[AUTOMATED]<br>302 P1 设置「查看设置页面显示」[AUTOMATED] |
| `tests/kuwo/test_kuwo_smoke.py::test_launch_kuwo_home` | 1 P1 主页「查看酷我主页显示」[AUTOMATED] |
| `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` | 65 P2 下载「下载页面点击返回」[AUTOMATED]<br>66 P2 下载「下载页面点击搜索」[AUTOMATED]<br>67 P2 下载「下载页面点击设置」[AUTOMATED]<br>68 P2 下载「下载页面点击酷我ICON」[AUTOMATED] |
| `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_detail_song_strong` | 283 P2 专辑列表页「专辑列表页点击歌曲」[AUTOMATED] |
| `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful` | 126 P1 收藏「收藏专辑页点击图片中的播放/暂停按钮」[AUTOMATED]<br>139 P1 收藏「收藏歌单页点击图片中的播放/暂停按钮」[AUTOMATED] |
| `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` | 95 P2 收藏「收藏页面点击返回」[AUTOMATED]<br>96 P2 收藏「收藏页面点击搜索」[AUTOMATED]<br>97 P2 收藏「收藏页面点击设置」[AUTOMATED]<br>98 P2 收藏「收藏页面点击酷我ICON」[AUTOMATED] |
| `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_player_vip_download_current_song_stateful` | 77 P2 下载「会员账号下载需VIP下载的单曲」[AUTOMATED] |

## 3. 本阶段手工范围

扫码登录、未登录账号态、支付/购买会员/权益边界、账号绑定/解绑、退出登录、删除下载、删除播放列表、清缓存等仍不纳入当前主回归强自动化。
