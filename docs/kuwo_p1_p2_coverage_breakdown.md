# 酷我 P1/P2 覆盖拆分清单

## 1. 口径说明

当前按「台架保持 VIP 已登录账号」作为自动化前置，强自动化覆盖为 `79/142 = 55.6%`。
自动化证据覆盖为 `83/142 = 58.5%`，包括强覆盖、部分覆盖和已知缺陷观测。
扫码登录、未登录账号态、支付/权益、账号绑定/解绑、删除/清缓存等仍按人工或专项半自动处理，不硬算强覆盖。

## 2. 强自动化覆盖清单

| Excel ID | 优先级 | 模块 | 功能用例 | 自动化 case |
| ---: | --- | --- | --- | --- |
| 1 | P1 | 主页 | 查看酷我主页显示 | `tests/kuwo/test_kuwo_smoke.py::test_launch_kuwo_home` |
| 2 | P2 | 主页 | 酷我主页点击搜索按钮 | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_search_page_readonly` |
| 3 | P2 | 主页 | 酷我主页点击设置按钮 | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_settings_page_readonly` |
| 4 | P2 | 主页 | 酷我主页点击酷我icon | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_logo_module_switcher_readonly` |
| 5 | P1 | 主页 | 酷我主页点击推荐 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 6 | P1 | 主页 | 酷我主页点击会员专区 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 7 | P1 | 主页 | 酷我主页点击热点 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 8 | P1 | 主页 | 酷我主页点击电台 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 9 | P1 | 主页 | 酷我主页点击曲库 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 10 | P1 | 主页 | 酷我主页点击我的 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 11 | P2 | 推荐页面 | 酷我主页划动页面 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 12 | P2 | 推荐页面 | 查看推荐页面显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 13 | P2 | 推荐页面 | 推荐页中点击歌单 | `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` |
| 14 | P2 | 推荐页面 | 推荐页中点击只有一首歌曲的歌单 | `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` |
| 15 | P2 | 会员专区 | 查看会员专区页显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 16 | P2 | 会员专区 | 会员专区页中点击歌单 | `tests/kuwo/test_kuwo_home.py::test_kuwo_member_playlist_and_library_category_strong` |
| 17 | P2 | 热门 | 查看热点页面显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 18 | P2 | 热门 | 热点页面点击榜单验证 | `tests/kuwo/test_kuwo_home.py::test_kuwo_hot_single_song_recommendation_play_strong` |
| 19 | P2 | 电台 | 查看电台页显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 20 | P2 | 电台 | 点击电台页中的类目验证 | `tests/kuwo/test_kuwo_home.py::test_kuwo_tingba_category_and_radio_item_strong` |
| 21 | P2 | 电台 | 电台分类页中点击分类 | `tests/kuwo/test_kuwo_home.py::test_kuwo_tingba_category_and_radio_item_strong` |
| 22 | P2 | 曲库 | 查看曲库页面显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 24 | P2 | 曲库 | 点击场景中的类目 | `tests/kuwo/test_kuwo_home.py::test_kuwo_member_playlist_and_library_category_strong` |
| 25 | P1 | 主页 | 点击歌单中的播放/暂停按钮 | `tests/kuwo/test_kuwo_home.py::test_kuwo_song_list_miniplayer_play_pause_readonly` |
| 26 | P2 | 歌单详情页 | 歌单-歌曲列表页点击搜索按钮 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 27 | P2 | 歌单详情页 | 歌单-歌曲列表页点击设置按钮 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 28 | P2 | 歌单详情页 | 歌单-歌曲列表页点击酷我icon | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 29 | P2 | 歌单详情页 | 歌单-歌曲列表页点击返回按钮 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 32 | P2 | 榜单列表页 | 榜单-歌曲列表页点击设置按钮 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 33 | P2 | 榜单列表页 | 榜单-歌曲列表页点击酷我icon | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 34 | P2 | 榜单列表页 | 榜单-歌曲列表页点击返回按钮 | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 36 | P2 | 我的 | 已登录账号查看我的页面显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_mine_logged_in_vip_status_strong` |
| 38 | P2 | 我的 | 已登录VIP账号查看我的页面显示 | `tests/kuwo/test_kuwo_home.py::test_kuwo_mine_logged_in_vip_status_strong` |
| 49 | P2 | 最近收听 | 最近收听页面点击搜索 | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 50 | P2 | 最近收听 | 最近收听页面点击设置 | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 51 | P2 | 最近收听 | 最近收听页面点击酷我ICON | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 53 | P1 | 最近收听 | 最近收听页点击音乐 | `tests/kuwo/test_kuwo_library.py::test_kuwo_recent_list_observation_readonly` |
| 65 | P2 | 下载 | 下载页面点击返回 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 66 | P2 | 下载 | 下载页面点击搜索 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 67 | P2 | 下载 | 下载页面点击设置 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 68 | P2 | 下载 | 下载页面点击酷我ICON | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_download_page_title_actions_stateful` |
| 77 | P2 | 下载 | 会员账号下载需VIP下载的单曲 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_player_vip_download_current_song_stateful` |
| 95 | P2 | 收藏 | 收藏页面点击返回 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 96 | P2 | 收藏 | 收藏页面点击搜索 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 97 | P2 | 收藏 | 收藏页面点击设置 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 98 | P2 | 收藏 | 收藏页面点击酷我ICON | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_page_title_actions_stateful` |
| 126 | P1 | 收藏 | 收藏专辑页点击图片中的播放/暂停按钮 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful` |
| 139 | P1 | 收藏 | 收藏歌单页点击图片中的播放/暂停按钮 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_playlist_play_buttons_stateful` |
| 206 | P1 | 播放页 | 查看普通歌曲播放页显示 | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_page_display_and_play_button_strong` |
| 210 | P2 | 播放页 | 播放页点击返回按钮 | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` |
| 211 | P2 | 播放页 | 播放页点击播放列表按钮 | `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_readonly` |
| 212 | P2 | 播放页 | 播放页点击酷我ICON | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` |
| 213 | P2 | 播放页 | CHCL46MEDIA-1008 播放页点击去K歌icon | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_k_song_entry_strong` |
| 242 | P2 | 播放页 | 播放页点击播放按钮 | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_page_display_and_play_button_strong` |
| 243 | P2 | 播放页 | 播放页点击暂停按钮 | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_title_actions_and_controls_strong` |
| 244 | P2 | 播放页 | 音乐播放完验证 | `tests/kuwo/test_kuwo_library.py::test_kuwo_player_music_completion_by_seek_strong` |
| 259 | P2 | miniplayer | 退出播放详情页 | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` |
| 263 | P2 | miniplayer | 播放状态播放条中点击播放按钮 | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` |
| 264 | P2 | miniplayer | 暂停播放状态播放条中点击播放按钮 | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_miniplayer_visible` |
| 269 | P2 | 播放列表 | 播放列表页面点击歌曲 | `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_tap_song_strong` |
| 283 | P2 | 专辑列表页 | 专辑列表页点击歌曲 | `tests/kuwo/test_kuwo_stateful_pages.py::test_kuwo_favorite_album_detail_song_strong` |
| 288 | P2 | 歌手介绍页 | 歌手详情页点击搜索 | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` |
| 289 | P2 | 歌手介绍页 | 歌手详情页点击设置 | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` |
| 290 | P2 | 歌手介绍页 | 歌手详情页点击酷我icon | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_detail_readonly` |
| 302 | P1 | 设置 | 查看设置页面显示 | `tests/kuwo/test_kuwo_smoke.py::test_kuwo_settings_page_readonly` |
| 379 | P2 | 搜索 | 搜索组合的数据 | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_artist_section_readonly` |
| 390 | P1 | 搜索 | 搜索页多个搜索结果间来回切换播放 | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_multiple_result_song_switch_strong` |
| 400 | P1 | 搜索 | 搜索页观察搜索历史新增 | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_added_stateful` |
| 401 | P1 | 搜索 | 搜索页点击历史搜索记录 | `tests/kuwo/test_kuwo_search.py::test_kuwo_search_history_keyword_results_readonly` |
| 407 | P2 | 驾驶模式 | 开启了驾驶模式，点击用户协议 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` |
| 408 | P2 | 驾驶模式 | 开启了驾驶模式，点击隐私政策 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` |
| 409 | P2 | 驾驶模式 | 开启了驾驶模式，点击开源免责声明 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_about_entries_blocked_stateful` |
| 410 | P2 | 驾驶模式 | 进入用户协议页面后开启驾驶模式 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 411 | P2 | 驾驶模式 | 进入隐私政策页面后开启驾驶模式 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 412 | P2 | 驾驶模式 | 进入开源免责声明后开启驾驶模式 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 413 | P2 | 驾驶模式 | 处于用户协议页面，关闭驾驶模式验证 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 414 | P2 | 驾驶模式 | 处于隐私政策页面，关闭驾驶模式验证 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 415 | P2 | 驾驶模式 | 处于开源免责声明页面，关闭驾驶模式验证 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful` |
| 417 | P2 | 驾驶模式 | 开启驾驶模式后已登录进入帐户页面 | `tests/kuwo/test_kuwo_driving_mode.py::test_kuwo_driving_mode_logged_in_account_entry_stateful` |

## 3. 有证据但未达到强断言的清单

| Excel ID | 优先级 | 模块 | 功能用例 | 状态 | 自动化 case |
| ---: | --- | --- | --- | --- | --- |
| 30 | P2 | 歌单详情页 | 歌单-歌曲列表页长按歌曲 | `PARTIAL` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 35 | P2 | 榜单列表页 | 榜单-歌曲列表页长按歌曲 | `PARTIAL` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_content_card_enter_and_back` |
| 37 | P2 | 我的 | 未登录账号查看我的页面显示 | `PARTIAL` | `tests/kuwo/test_kuwo_home.py::test_kuwo_home_visible_tabs_readonly` |
| 270 | P2 | 播放列表 | 播放列表页长按歌曲 | `XFAIL_KNOWN_DEFECT` | `tests/kuwo/test_kuwo_library.py::test_kuwo_play_queue_long_press_song_observation` |

## 4. 手工/专项范围

| Excel ID | 优先级 | 模块 | 功能用例 | 状态 | 说明 |
| ---: | --- | --- | --- | --- | --- |
| 79 | P2 | 下载 | 会员账号下载次数已用完下载需VIP下载的单曲 | `MANUAL_AUTH` | 需构造会员下载次数耗尽账号，当前台架账号有效期至 2072-09-03，不能通过自动化消耗权益。 |
| 80 | P2 | 下载 | 会员账号下载次数已用完下载需VIP且历史下载过的单曲 | `MANUAL_AUTH` | 需构造下载次数耗尽且历史已下载资源的账号态，当前环境不具备该权益边界。 |
| 81 | P2 | 下载 | 非会员下载免费下载的单曲 | `MANUAL_AUTH` | 需切换非会员账号并准备免费资源；当前台架为会员账号，不执行登出/切号。 |
| 82 | P2 | 下载 | 非会员账号下载需vip下载的单曲 | `MANUAL_AUTH` | 需切换非会员账号并准备 VIP 资源；当前台架为会员账号，不执行登出/切号。 |
| 83 | P2 | 下载 | 未登录账号下载免费下载的单曲 | `MANUAL_AUTH` | 需未登录账号态；当前台架为已登录账号，不执行登出。 |
| 84 | P2 | 下载 | 未登录账号下载需vip下载的单曲 | `MANUAL_AUTH` | 需未登录账号态和 VIP 资源；当前台架为已登录账号，不执行登出。 |
| 156 | P2 | 自建歌单 | 自建歌单页面点击搜索 | `STATEFUL` | ???????????????????????????? |
| 157 | P2 | 自建歌单 | 自建歌单页面点击设置 | `STATEFUL` | ???????????????????????????? |
| 158 | P2 | 自建歌单 | 自建歌单页面点击酷我ICON | `STATEFUL` | ???????????????????????????? |
| 159 | P2 | 自建歌单 | 登录的账号有自建歌单手机端删除歌单查看自建歌单页面显示 | `STATEFUL` | ???????????????????????????? |
| 160 | P2 | 自建歌单 | 登录的账号有自建歌单手机端新建歌单查看自建歌单页面显示 | `STATEFUL` | ???????????????????????????? |
| 161 | P2 | 自建歌单 | 歌单中有歌曲点击自建歌单封面 | `STATEFUL` | ???????????????????????????? |
| 163 | P2 | 自建歌单 | 登录的账号有自建歌单手机端删除歌单中的歌曲查看自建歌单页面显示 | `STATEFUL` | ???????????????????????????? |
| 164 | P2 | 自建歌单 | 登录的账号有自建歌单手机端添加歌单中的歌曲查看自建歌单页面显示 | `STATEFUL` | ???????????????????????????? |
| 165 | P1 | 账号 | 未登录我的页面点击默认头像 | `MANUAL_AUTH` | ??????????????????/???? |
| 166 | P1 | 账号 | 已登录账号我的页面点击用户头像 | `MANUAL_AUTH` | ??????????????????/???? |
| 167 | P1 | 账号 | 未登录账号查看账号页面显示 | `MANUAL_AUTH` | ??????????????????/???? |
| 168 | P1 | 账号 | 登录VIP账号查看账号页面显示 | `MANUAL_AUTH` | ??????????????????/???? |
| 169 | P1 | 账号 | 登录普通账号查看账号页面显示 | `MANUAL_AUTH` | ??????????????????/???? |
| 171 | P2 | 账号 | 账号页面点击搜索 | `MANUAL_AUTH` | ??????????????????/???? |
| 172 | P2 | 账号 | 账号页面点击设置 | `MANUAL_AUTH` | ??????????????????/???? |
| 173 | P2 | 账号 | 账号页面点击酷我ICON | `MANUAL_AUTH` | ??????????????????/???? |
| 177 | P1 | 账号 | 使用酷我扫描二维码 | `MANUAL_AUTH` | ??????????????????/???? |
| 179 | P2 | 账号 | 账号页面点击退出账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 180 | P2 | 账号 | 账号页面关闭退登弹框 | `MANUAL_AUTH` | ??????????????????/???? |
| 181 | P1 | 账号 | 账号页面确认退出账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 183 | P2 | 购买会员 | 账号页面点击购买会员 | `MANUAL_AUTH` | ??????????????????/???? |
| 184 | P2 | 购买会员 | 账号页面点击续费 | `MANUAL_AUTH` | ??????????????????/???? |
| 185 | P1 | 购买会员 | 续费会员 | `MANUAL_AUTH` | ??????????????????/???? |
| 186 | P1 | 购买会员 | 开通会员 | `MANUAL_AUTH` | ??????????????????/???? |
| 187 | P2 | 购买会员 | 支付会员费用失败 | `MANUAL_AUTH` | ??????????????????/???? |
| 188 | P2 | 购买会员 | 使用微信支付 | `MANUAL_AUTH` | ??????????????????/???? |
| 189 | P2 | 购买会员 | 使用支付宝支付 | `MANUAL_AUTH` | ??????????????????/???? |
| 190 | P2 | 购买会员 | 使用云闪付支付 | `MANUAL_AUTH` | ??????????????????/???? |
| 191 | P2 | 购买会员 | 使用银行APP支付 | `MANUAL_AUTH` | ??????????????????/???? |
| 192 | P2 | 购买会员 | 支付成功后订单异常未生效验证 | `MANUAL_AUTH` | ??????????????????/???? |
| 193 | P1 | 关联账号 | 账号页面点击关联账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 194 | P2 | 关联账号 | 登录的酷我、车机都未绑定账号，绑定账号页面绑定账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 195 | P2 | 关联账号 | 登录的酷我已绑定其他车机账号，绑定账号页面绑定账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 196 | P2 | 关联账号 | 登录的车机已绑定其他酷我账号，绑定账号页面绑定账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 197 | P2 | 关联账号 | 登录的车机和酷我都绑定了其他账号，绑定账号页面绑定账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 198 | P2 | 关联账号 | 已绑定AF清除缓存查看登录绑定状态 | `MANUAL_AUTH` | ??????????????????/???? |
| 199 | P2 | 关联账号 | 已登录未绑定AF清除缓存查看登录绑定状态 | `MANUAL_AUTH` | ??????????????????/???? |
| 200 | P1 | 关联账号 | 【账户】已绑定账号页面点击取消关联我的账号 | `MANUAL_AUTH` | ??????????????????/???? |
| 201 | P1 | 关联账号 | 【账户】解绑页面点击解绑 | `MANUAL_AUTH` | ??????????????????/???? |
| 202 | P1 | 播放歌曲 | 非会员播放支持试听的会员音乐 | `MANUAL_AUTH` | 涉及非会员试听会员音乐，需要固定账号/版权资源，默认人工或半自动。 |
| 203 | P1 | 播放歌曲 | 非会员播放不支持试听的会员音乐 | `MANUAL_AUTH` | 涉及非会员不可试听会员音乐，需要固定账号/版权资源，默认人工或半自动。 |
| 204 | P1 | 播放歌曲 | 非会员试听结束验证 | `MANUAL_AUTH` | 涉及会员音乐试听结束状态，需要固定账号/版权资源，默认人工或半自动。 |
| 205 | P1 | 播放歌曲 | 会员播放VIP音乐验证 | `MANUAL_AUTH` | 涉及会员账号播放 VIP 音乐，需要固定会员账号和版权资源。 |
| 207 | P1 | 播放页 | 非会员查看VIP歌曲播放页显示 | `MANUAL_AUTH` | ?? VIP?????????????/???? |
| 208 | P1 | 播放页 | 会员查看VIP歌曲播放页显示 | `MANUAL_AUTH` | ?? VIP?????????????/???? |
| 214 | P2 | 播放页 | 未登录账号点击播放页购买会员按钮 | `MANUAL_AUTH` | ?? VIP?????????????/???? |
| 215 | P2 | 播放页 | 非会员账号点击播放页购买会员按钮 | `MANUAL_AUTH` | ?? VIP?????????????/???? |
| 271 | P2 | 播放列表 | 播放列表页删除歌曲 | `STATEFUL` | 删除播放列表歌曲会改变数据，需隔离账号/队列后执行。 |
| 272 | P2 | 播放列表 | 播放列表页删除全部歌曲 | `STATEFUL` | 删除全部歌曲会改变数据，需隔离账号/队列后执行。 |
| 273 | P2 | 播放列表 | 播放列表页删除正在播放的歌曲 | `STATEFUL` | 删除正在播放歌曲会改变数据，需隔离账号/队列后执行。 |
| 416 | P2 | 驾驶模式 | 开启驾驶模式后未登录进入帐户页面 | `MANUAL_AUTH` | 需未登录账号态；当前台架为 zhanghao001 已登录会员账号，不执行登出。 |
| 418 | P2 | 驾驶模式 | 进入扫码登陆页面后开启驾驶模式 | `MANUAL_AUTH` | 需未登录扫码登录页；当前账号已登录，不执行登出或扫码登录。 |
| 419 | P2 | 驾驶模式 | 处于登陆二维码页面，关闭驾驶模式验证 | `MANUAL_AUTH` | 需未登录扫码登录页；当前账号已登录，不执行登出或扫码登录。 |
