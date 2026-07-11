"""Allure 业务行为分层元数据。

报告展示采用 Allure Behaviors 视图：
epic=酷我音乐，feature=页面/功能域，story=子功能，title=具体用例标题。
集中维护映射，避免在每个测试函数上重复堆叠装饰器。
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

try:
    import allure
except Exception:  # pragma: no cover - 兼容未安装 allure 的本地收集场景
    allure = None  # type: ignore[assignment]


EPIC_KUWO = "酷我音乐"


class Feature:
    ENV = "环境"
    HOME = "主页"
    SEARCH = "搜索"
    PLAYER = "播放页"
    PLAY_QUEUE = "播放列表"
    RECENT = "最近收听"
    SETTINGS = "设置"
    MINE = "我的"
    DOWNLOAD = "下载"
    FAVORITE = "收藏"
    DRIVING = "驾驶模式"


class Story:
    DEVICE = "设备可用性"
    HOME_DISPLAY = "主页显示"
    TAB_SWITCH = "tab 切换"
    ENTRY_JUMP = "入口跳转"
    SONG_LIST = "歌单详情"
    TITLE_ACTIONS = "标题栏操作"
    MINI_PLAYER = "MiniPlayer 控制"
    CONTENT_PLAY = "内容播放"
    SEARCH_PAGE = "搜索页展示"
    SEARCH_RESULT = "搜索主流程"
    SEARCH_HISTORY = "搜索历史"
    ARTIST_DETAIL = "歌手详情"
    PLAYER_DISPLAY = "播放页显示"
    PLAY_CONTROL = "播放控制"
    QUEUE_ACTION = "列表操作"
    LEGAL = "协议与关于"
    ACCOUNT = "已登录账号"
    DOWNLOAD_ACTION = "下载主流程"
    FAVORITE_ACTION = "收藏主流程"
    DRIVE_RESTRICT = "drive 限制"
    PARK_RESTORE = "park 恢复"


@dataclass(frozen=True)
class AllureCaseMeta:
    feature: str
    story: str
    title: str
    description: str
    severity: str = "normal"
    tags: tuple[str, ...] = ()


KUWO_CASE_META: dict[str, AllureCaseMeta] = {
    "test_device_online": AllureCaseMeta(
        Feature.ENV,
        Story.DEVICE,
        "设备在线并读取媒体包版本",
        "验证台架 ADB 在线，媒体包可读取版本，并采集设备上下文和当前屏幕。",
        "critical",
        ("kuwo", "env", "p0"),
    ),
    "test_launch_kuwo_home": AllureCaseMeta(
        Feature.HOME,
        Story.HOME_DISPLAY,
        "启动酷我并展示主页",
        "通过显式 Activity 拉起酷我，验证首页列表、搜索/设置入口和首页 tab 完整展示。",
        "critical",
        ("kuwo", "home", "smoke"),
    ),
    "test_kuwo_search_page_readonly": AllureCaseMeta(
        Feature.HOME,
        Story.ENTRY_JUMP,
        "主页进入搜索页并返回",
        "从酷我主页点击搜索入口，验证搜索页展示，再关闭返回首页。",
        "critical",
        ("kuwo", "home", "search"),
    ),
    "test_kuwo_settings_page_readonly": AllureCaseMeta(
        Feature.HOME,
        Story.ENTRY_JUMP,
        "主页进入设置页并返回",
        "从酷我主页点击设置入口，验证设置页关键条目展示，再关闭返回首页。",
        "critical",
        ("kuwo", "home", "settings"),
    ),
    "test_kuwo_miniplayer_visible": AllureCaseMeta(
        Feature.HOME,
        Story.MINI_PLAYER,
        "主页展示 MiniPlayer 控件",
        "验证首页底部 MiniPlayer 的上一首、播放暂停、下一首、标题、歌手和时间控件完整展示。",
        "critical",
        ("kuwo", "home", "miniplayer"),
    ),
    "test_kuwo_player_page_observation": AllureCaseMeta(
        Feature.PLAYER,
        Story.PLAYER_DISPLAY,
        "从 MiniPlayer 打开播放页观测",
        "从首页 MiniPlayer 打开播放页，保留播放页截图；动态 XML 不稳定时记录为已知观测。",
        "normal",
        ("kuwo", "player"),
    ),
    "test_kuwo_home_visible_tabs_readonly": AllureCaseMeta(
        Feature.HOME,
        Story.TAB_SWITCH,
        "主页 tab 逐项切换并展示内容",
        "依次切换我的、热门、榜单、会员专区、听吧、曲库 tab，验证 tab 选中和内容区展示。",
        "critical",
        ("kuwo", "home", "tab"),
    ),
    "test_kuwo_home_content_card_enter_and_back": AllureCaseMeta(
        Feature.HOME,
        Story.SONG_LIST,
        "主页内容卡进入歌单详情并返回",
        "从主页内容卡进入歌曲列表详情页，验证详情页展示并返回酷我主页。",
        "critical",
        ("kuwo", "home", "playlist"),
    ),
    "test_kuwo_song_list_title_actions_strong": AllureCaseMeta(
        Feature.HOME,
        Story.TITLE_ACTIONS,
        "歌单详情页标题栏入口验证",
        "进入歌单详情页后验证搜索、设置、酷我 logo 和返回等标题栏入口可用。",
        "critical",
        ("kuwo", "playlist", "titlebar"),
    ),
    "test_kuwo_member_playlist_and_library_category_strong": AllureCaseMeta(
        Feature.HOME,
        Story.CONTENT_PLAY,
        "会员专区歌单和曲库类目主流程",
        "验证会员专区歌单详情和曲库类目入口可进入并展示业务内容。",
        "critical",
        ("kuwo", "home", "library"),
    ),
    "test_kuwo_tingba_category_and_radio_item_strong": AllureCaseMeta(
        Feature.HOME,
        Story.CONTENT_PLAY,
        "听吧分类进入并播放电台",
        "验证听吧分类入口、分类列表和电台条目点击播放主流程。",
        "critical",
        ("kuwo", "tingba", "radio"),
    ),
    "test_kuwo_hot_single_song_recommendation_play_strong": AllureCaseMeta(
        Feature.HOME,
        Story.CONTENT_PLAY,
        "热门推荐卡点击歌曲并播放",
        "从热门推荐内容进入详情页，点击首行歌曲，通过媒体会话验证播放。",
        "critical",
        ("kuwo", "home", "play"),
    ),
    "test_kuwo_home_logo_module_switcher_readonly": AllureCaseMeta(
        Feature.HOME,
        Story.ENTRY_JUMP,
        "主页酷我 logo 打开媒体模块切换",
        "点击主页酷我 logo 区域，验证媒体模块切换弹层选项完整展示。",
        "normal",
        ("kuwo", "home", "switcher"),
    ),
    "test_kuwo_song_list_miniplayer_play_pause_readonly": AllureCaseMeta(
        Feature.HOME,
        Story.MINI_PLAYER,
        "歌单详情页 MiniPlayer 播放暂停切换",
        "进入稳定歌单详情页，点击 MiniPlayer 播放/暂停并验证状态变化和恢复。",
        "critical",
        ("kuwo", "miniplayer", "play"),
    ),
    "test_kuwo_mine_logged_in_vip_status_strong": AllureCaseMeta(
        Feature.MINE,
        Story.ACCOUNT,
        "我的页展示已登录 VIP 账号信息",
        "切换到我的页，验证已登录昵称、VIP 有效期和账号入口展示。",
        "critical",
        ("kuwo", "mine", "vip"),
    ),
    "test_kuwo_search_history_keyword_results_readonly": AllureCaseMeta(
        Feature.SEARCH,
        Story.SEARCH_RESULT,
        "点击历史词进入搜索结果页",
        "复用搜索页历史词/推荐词进入结果页，验证歌曲结果展示并返回首页。",
        "critical",
        ("kuwo", "search"),
    ),
    "test_kuwo_search_artist_section_readonly": AllureCaseMeta(
        Feature.SEARCH,
        Story.SEARCH_RESULT,
        "搜索结果页展示歌手分组",
        "进入搜索结果页后滑动到歌手分组，验证歌手、歌曲数和专辑数展示。",
        "normal",
        ("kuwo", "search", "artist"),
    ),
    "test_kuwo_search_multiple_result_song_switch_strong": AllureCaseMeta(
        Feature.SEARCH,
        Story.SEARCH_RESULT,
        "搜索结果页多歌曲切换播放",
        "点击搜索结果前两首歌曲，验证当前播放标题发生变化。",
        "critical",
        ("kuwo", "search", "play"),
    ),
    "test_kuwo_search_artist_detail_readonly": AllureCaseMeta(
        Feature.SEARCH,
        Story.ARTIST_DETAIL,
        "搜索结果进入歌手详情并返回",
        "从搜索结果歌手分组进入歌手详情，验证介绍、单曲、专辑 tab 展示并返回。",
        "normal",
        ("kuwo", "search", "artist"),
    ),
    "test_kuwo_artist_detail_title_actions_strong": AllureCaseMeta(
        Feature.SEARCH,
        Story.ARTIST_DETAIL,
        "歌手详情页标题栏入口验证",
        "在歌手详情页验证搜索、设置、酷我 logo 等标题栏入口可用。",
        "normal",
        ("kuwo", "artist", "titlebar"),
    ),
    "test_kuwo_search_history_added_stateful": AllureCaseMeta(
        Feature.SEARCH,
        Story.SEARCH_HISTORY,
        "搜索页新增搜索历史",
        "输入 ASCII 测试词完成搜索，重新进入搜索页验证历史记录新增。",
        "critical",
        ("kuwo", "search", "history", "stateful"),
    ),
    "test_kuwo_settings_about_readonly": AllureCaseMeta(
        Feature.SETTINGS,
        Story.LEGAL,
        "设置页进入关于页并返回",
        "进入设置关于页，验证版本名称、用户协议、隐私政策、开源免责声明入口。",
        "normal",
        ("kuwo", "settings", "about"),
    ),
    "test_kuwo_settings_legal_documents_readonly": AllureCaseMeta(
        Feature.SETTINGS,
        Story.LEGAL,
        "设置页协议隐私开源文档只读展示",
        "逐个进入用户协议、隐私政策和开源免责声明页面，验证只读展示并恢复首页。",
        "normal",
        ("kuwo", "settings", "legal"),
    ),
    "test_kuwo_recent_list_observation_readonly": AllureCaseMeta(
        Feature.RECENT,
        Story.HOME_DISPLAY,
        "最近收听页只读展示",
        "从我的页进入最近收听，采集截图和 XML，验证页面可观测并返回首页。",
        "normal",
        ("kuwo", "recent"),
    ),
    "test_kuwo_recent_list_title_actions_and_song_strong": AllureCaseMeta(
        Feature.RECENT,
        Story.TITLE_ACTIONS,
        "最近收听页标题栏和歌曲点击验证",
        "验证最近收听页搜索、设置、酷我 logo、歌曲点击和返回路径。",
        "critical",
        ("kuwo", "recent", "play"),
    ),
    "test_kuwo_play_queue_readonly": AllureCaseMeta(
        Feature.PLAY_QUEUE,
        Story.HOME_DISPLAY,
        "播放页打开播放列表",
        "从播放页打开播放列表，验证标题和列表展示，XML 不稳定时保留截图证据。",
        "normal",
        ("kuwo", "queue"),
    ),
    "test_kuwo_player_title_actions_and_controls_strong": AllureCaseMeta(
        Feature.PLAYER,
        Story.PLAY_CONTROL,
        "播放页标题栏和播放暂停控制",
        "验证播放页酷我 logo、返回、播放暂停按钮和 MiniPlayer 状态联动。",
        "critical",
        ("kuwo", "player", "control"),
    ),
    "test_kuwo_player_page_display_and_play_button_strong": AllureCaseMeta(
        Feature.PLAYER,
        Story.PLAY_CONTROL,
        "播放页展示并点击播放按钮",
        "验证播放页前台、媒体元数据可用，并从暂停态点击播放进入 PLAYING。",
        "critical",
        ("kuwo", "player", "play"),
    ),
    "test_kuwo_player_k_song_entry_strong": AllureCaseMeta(
        Feature.PLAYER,
        Story.ENTRY_JUMP,
        "播放页点击去 K 歌入口",
        "点击播放页去 K 歌入口，验证前台跳转到 K 歌应用并恢复酷我首页。",
        "normal",
        ("kuwo", "player", "ksong"),
    ),
    "test_kuwo_player_music_completion_by_seek_strong": AllureCaseMeta(
        Feature.PLAYER,
        Story.PLAY_CONTROL,
        "拖动进度条验证歌曲播放完成",
        "将播放进度拖到末尾附近，等待媒体会话切换，验证歌曲完成/续播链路。",
        "critical",
        ("kuwo", "player", "completion"),
    ),
    "test_kuwo_play_queue_tap_song_strong": AllureCaseMeta(
        Feature.PLAY_QUEUE,
        Story.QUEUE_ACTION,
        "播放列表点击歌曲切换播放",
        "打开播放列表并点击可见歌曲，验证 MiniPlayer 当前播放标题发生变化。",
        "critical",
        ("kuwo", "queue", "play"),
    ),
    "test_kuwo_play_queue_long_press_song_observation": AllureCaseMeta(
        Feature.PLAY_QUEUE,
        Story.QUEUE_ACTION,
        "播放列表长按歌曲观测",
        "长按播放列表首行歌曲并保留截图/XML；当前产品未展示稳定菜单时记录为已知观测。",
        "normal",
        ("kuwo", "queue", "longpress"),
    ),
    "test_kuwo_download_page_title_actions_stateful": AllureCaseMeta(
        Feature.DOWNLOAD,
        Story.TITLE_ACTIONS,
        "下载页标题栏入口验证",
        "从我的页进入下载页，验证返回、搜索、设置和酷我 logo 标题栏入口。",
        "normal",
        ("kuwo", "download", "stateful"),
    ),
    "test_kuwo_player_vip_download_current_song_stateful": AllureCaseMeta(
        Feature.DOWNLOAD,
        Story.DOWNLOAD_ACTION,
        "会员账号播放页下载当前歌曲",
        "在已登录会员账号态下从播放页点击下载，验证下载页可看到已下载歌曲。",
        "critical",
        ("kuwo", "download", "vip", "stateful"),
    ),
    "test_kuwo_favorite_page_title_actions_stateful": AllureCaseMeta(
        Feature.FAVORITE,
        Story.TITLE_ACTIONS,
        "收藏页标题栏入口验证",
        "从我的页进入收藏页，验证返回、搜索、设置和酷我 logo 标题栏入口。",
        "normal",
        ("kuwo", "favorite", "stateful"),
    ),
    "test_kuwo_favorite_album_playlist_play_buttons_stateful": AllureCaseMeta(
        Feature.FAVORITE,
        Story.FAVORITE_ACTION,
        "收藏专辑和收藏歌单封面播放",
        "验证收藏专辑/收藏歌单首卡封面播放按钮；无预置数据时保留空态证据并跳过。",
        "critical",
        ("kuwo", "favorite", "play", "stateful"),
    ),
    "test_kuwo_favorite_album_detail_song_strong": AllureCaseMeta(
        Feature.FAVORITE,
        Story.FAVORITE_ACTION,
        "收藏专辑详情页点击歌曲播放",
        "进入收藏专辑详情并点击首行歌曲，通过媒体会话验证播放状态和元数据变化。",
        "critical",
        ("kuwo", "favorite", "album", "play"),
    ),
    "test_kuwo_driving_mode_about_entries_blocked_stateful": AllureCaseMeta(
        Feature.DRIVING,
        Story.DRIVE_RESTRICT,
        "驾驶模式下关于页入口受限",
        "开启 drive 状态后点击用户协议、隐私政策、开源免责声明，验证停留或展示限制页。",
        "critical",
        ("kuwo", "driving", "drive"),
    ),
    "test_kuwo_driving_mode_legal_pages_restrict_and_restore_stateful": AllureCaseMeta(
        Feature.DRIVING,
        Story.PARK_RESTORE,
        "协议页面 drive 限制和 park 恢复",
        "park 状态打开协议/隐私/开源页，切 drive 验证限制，再切 park 验证内容恢复。",
        "critical",
        ("kuwo", "driving", "park"),
    ),
    "test_kuwo_driving_mode_logged_in_account_entry_stateful": AllureCaseMeta(
        Feature.DRIVING,
        Story.ACCOUNT,
        "驾驶模式下进入已登录账户页",
        "已登录账号态下开启 drive 后进入账户页，验证昵称、会员有效期和操作入口展示。",
        "normal",
        ("kuwo", "driving", "account"),
    ),
}


def apply_allure_case_metadata(node_name: str, marker_names: Iterable[str] = ()) -> None:
    """按 pytest 节点名注入 Allure Behaviors 元数据。"""
    if allure is None:
        return
    case_name = node_name.split("[", 1)[0]
    meta = KUWO_CASE_META.get(case_name)
    if meta is None:
        return
    allure.dynamic.epic(EPIC_KUWO)
    allure.dynamic.feature(meta.feature)
    allure.dynamic.story(meta.story)
    allure.dynamic.title(meta.title)
    allure.dynamic.description(meta.description)
    allure.dynamic.severity(meta.severity)
    existing_tags = set(marker_names)
    business_tags: list[str] = []
    for tag in meta.tags:
        if tag in existing_tags:
            continue
        existing_tags.add(tag)
        business_tags.append(tag)
    if business_tags:
        allure.dynamic.tag(*business_tags)
