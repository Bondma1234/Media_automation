"""酷我音乐定位器。"""


class KuwoHomeLocators:
    SEARCH_DESC = "搜索"
    SETTINGS_DESC = "设置"
    SEARCH_DESC_ALIASES = ("搜索", "Search")
    SETTINGS_DESC_ALIASES = ("设置", "Settings")
    MODULE_SWITCH_OPTIONS = ("电台", "酷我音乐", "喜马拉雅", "乐听")
    TAB_LAYOUT = "com.jidouauto.media:id/tabLayout"
    TITLE_ACTIONS = "com.jidouauto.media:id/actionButtons"
    SETTINGS_ACTIONS = "com.jidouauto.media:id/menuActionContainer"
    INIT_PROGRESS = "com.jidouauto.media:id/initScreenProgressBar"
    # OneInfo 在中英文系统中的返回按钮 content-desc 会带业务前缀（例如 ###Back）。
    # 页面恢复只在 XML 已成功读取且确认存在返回控件时才允许发送 Back。
    BACK_DESC_ALIASES = ("Back", "返回")
    HOME_RECYCLER = "com.jidouauto.media:id/recyclerView"
    MINI_PREV = "com.jidouauto.media:id/id_op_prev"
    MINI_PLAY_PAUSE = "com.jidouauto.media:id/id_op_playpause"
    MINI_NEXT = "com.jidouauto.media:id/id_op_next"
    MINI_COVER = "com.jidouauto.media:id/iv_cover"
    MINI_TITLE = "com.jidouauto.media:id/tv_title"
    MINI_SUBTITLE = "com.jidouauto.media:id/tv_subTitle"
    MINI_TIME = "com.jidouauto.media:id/tv_time"
    # Key 保持现有中文业务名，value 对应同一台架在 zh/en locale 下的实际 content-desc。
    # 页面识别和切换优先使用 content-desc + selected，不依赖当前显示语言的 text。
    TAB_ALIASES = {
        "我的": ("我的", "My"),
        "热门": ("热门", "Popular"),
        "榜单": ("榜单", "TOP"),
        "会员专区": ("会员专区", "Car VIP"),
        "听吧": ("听吧", "Podcast"),
        "曲库": ("曲库", "Library"),
    }
    TABS = tuple(TAB_ALIASES)
    CARD_TITLE = "com.jidouauto.media:id/title"
    DETAIL_TITLE = "com.jidouauto.media:id/titleTextViewRef"
    SONG_NAME = "com.jidouauto.media:id/audio_name"
    SONG_SUBTITLE = "com.jidouauto.media:id/subTitle"
    RADIO_NAME = "com.jidouauto.media:id/radio_name"
    RADIO_PLAY_COUNT = "com.jidouauto.media:id/play_count"


class KuwoSearchLocators:
    BACK_DESC = "返回"
    EDIT_TEXT = "com.jidouauto.media:id/editText"
    SEARCH_RECYCLER = "com.jidouauto.media:id/recyclerView"
    DETAIL_TITLE = "com.jidouauto.media:id/titleTextViewRef"
    RESULT_HEADER = "com.jidouauto.media:id/listItemHeader"
    RESULT_SONG_NAME = "com.jidouauto.media:id/audio_name"
    RESULT_SONG_SUBTITLE = "com.jidouauto.media:id/subTitle"
    ARTIST_NAME = "com.jidouauto.media:id/tv_artist_name"
    ARTIST_MUSIC_COUNT = "com.jidouauto.media:id/tv_music_count"
    ARTIST_ALBUM_COUNT = "com.jidouauto.media:id/tv_album_count"
    ARTIST_DETAIL_TABS = ("介绍", "单曲", "专辑")


class KuwoSettingsLocators:
    BACK_DESC = "Back"
    TITLE = "设置"
    LIST_TEXTS = ("选择播放音质", "选择下载音质", "缓存", "音效", "个人信息收集")
    SWITCH = "com.jidouauto.media:id/switchControl"
    ABOUT = "关于"
    ABOUT_TITLE = "关于"
    VERSION_NAME = "版本名称"
    USER_AGREEMENT = "用户协议"
    PRIVACY_POLICY = "隐私政策"
    OPEN_SOURCE_DISCLAIMER = "开源免责声明"
    LEGAL_TITLE = "法律信息"
    LEGAL_ROOT = "com.valtech_mobility.legal.audi:id/navHostFragment"
    LEGAL_DRIVING_RESTRICTED_TEXT = "为了安全起见, 在行驶期间操作受限."
    MEDIA_DRIVING_UNAVAILABLE_TEXT = "为了您的安全, 该功能在行驶期间不可用."
    OPEN_SOURCE_LIST = "com.jidouauto.media:id/osdTextList"
    OPEN_SOURCE_ITEM = "com.jidouauto.media:id/longTextDisclaimerListItem"
    OPEN_SOURCE_DRIVING_RESTRICTED = "com.jidouauto.media:id/fullscreenDisclaimerText"


class KuwoPlayerLocators:
    BACK_DESC = "返回"
    TITLE = "正在播放"
    QUEUE_TITLE = "播放列表"
    ROOT = "com.jidouauto.media:id/play_pop_layout"
    CONTENT = "com.jidouauto.media:id/content"
    QUEUE_PLAYING = "com.jidouauto.media:id/view_playing"


class KuwoMineLocators:
    RECENT = "最近收听"
    DOWNLOAD = "下载"
    FAVORITE = "收藏"
    PLAYLIST = "自建歌单"


class KuwoAccountLocators:
    TITLE = "账户"
    AVATAR = "com.jidouauto.media:id/iv_avater"
    NICKNAME = "com.jidouauto.media:id/tv_nickname"
    VIP_TIME = "com.jidouauto.media:id/tv_time"
    LOGOUT = "登出"
    RENEW = "续费"
    LINK_MYAUDI = "绑定 myAudi 账户"


class KuwoLibraryLocators:
    RECENT_TITLE = "最近收听"
    DOWNLOAD_TITLE = "下载"
    FAVORITE_TITLE = "收藏"
    FAVORITE_TABS = ("单曲", "专辑", "收藏歌单")
    CARD_TITLE = "com.jidouauto.media:id/title"
