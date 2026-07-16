from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "02_口播视频原稿" / "视频源文件.mp4"
SCREEN_RECORDING = ROOT / "03_剪辑物料" / "录屏" / "Codex演示_界面与热点任务.mp4"
BGM = ROOT / "03_剪辑物料" / "BGM_Codex教学_v1_ToolThatLands.wav"
SUBTITLES = ROOT / "04_剪辑方案" / "字幕工作区" / "字幕_校对v1.srt"
ASSET_DIR = ROOT / "03_剪辑物料" / "剪辑素材"
OUTPUT_DIR = ROOT / "05_成片"
EDIT_DIR = ROOT / "edit"

FPS = 30
DURATION = 229.778
DESIGN_SIZE = (1920, 1080)
FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
ACCENT = "#69FF75"

SCREEN_INSERT = {
    "start": 131.0,
    "end": 154.4,
    "source_start": 0.0,
}

PROGRESS_ICON = ASSET_DIR / "genji像素小人.png"
PROGRESS_SECTIONS = [
    {"id": "entry", "label": "入门", "start": 0.0, "end": 26.54},
    {"id": "intro", "label": "认识", "start": 26.54, "end": 52.84},
    {"id": "difference", "label": "区别", "start": 52.84, "end": 78.56},
    {"id": "execution", "label": "执行", "start": 78.56, "end": 105.1},
    {"id": "agent", "label": "Agent", "start": 105.1, "end": 128.32},
    {"id": "demo", "label": "演示", "start": 128.32, "end": 154.56},
    {"id": "scenes", "label": "场景", "start": 154.56, "end": 180.14},
    {"id": "cases", "label": "案例", "start": 180.14, "end": 204.98},
    {"id": "ending", "label": "收尾", "start": 204.98, "end": DURATION},
]

# v2 keeps brand marks only. Explanatory content is rendered through the
# consistent UI card system below instead of unrelated sticker illustrations.
OVERLAYS = [
    {"file": "Codex图标.png", "start": 4.8, "end": 8.1, "width": 170, "x": "W-w-90", "y": "80"},
    {"file": "Codex图标.png", "start": 16.3, "end": 21.7, "width": 135, "x": "W-w-100", "y": "80"},
    {"file": "图标/OpenAI.png", "start": 43.5, "end": 52.5, "width": 175, "x": "80", "y": "80"},
    {"file": "Codex图标.png", "start": 218.6, "end": 229.1, "width": 220, "x": "W-w-100", "y": "100"},
]

# Cards mirror the benchmark's restrained visual language: dark translucent
# panels, one green accent, short labels and generous empty space.
UI_CARDS = [
    {"id": "hook", "title": "AI 圈新选手", "lines": ["OpenClaw  ·  Claude Code", "Codex 正式上桌"], "start": 1.9, "end": 8.1, "x": "70", "y": "70"},
    {"id": "benefits", "title": "Codex 上桌门槛", "lines": ["额度更高  ·  功能更全", "上手更快  ·  账号直登"], "start": 8.3, "end": 13.8, "x": "70", "y": "70"},
    {"id": "simple", "title": "操作足够简单", "lines": ["不用命令行", "网页下载即可开始"], "start": 14.0, "end": 16.3, "x": "W-w-70", "y": "70"},
    {"id": "install", "title": "三步开始", "lines": ["官网下载  →  GPT 登录", "打开即可使用"], "start": 16.3, "end": 21.7, "x": "70", "y": "70"},
    {"id": "magic", "title": "注册入口", "lines": ["评论区置顶链接", "领取注册“魔法”"], "start": 26.5, "end": 29.2, "x": "W-w-70", "y": "70"},
    {"id": "identity", "title": "GENJI", "lines": ["AIGC 一线实践", "手把手带你做出结果"], "start": 30.0, "end": 35.6, "x": "70", "y": "70"},
    {"id": "summit", "title": "AI 峰会归来", "lines": ["实战经验现场拆解", "先做出一个小成绩"], "start": 35.6, "end": 41.9, "x": "W-w-70", "y": "70"},
    {"id": "abilities", "title": "CODEX 能做什么", "lines": ["代码  ·  PPT  ·  Excel", "浏览器  ·  视频剪辑"], "start": 43.5, "end": 52.5, "x": "W-w-70", "y": "70"},
    {"id": "gpt_recipe", "title": "GPT", "lines": ["给你一份菜谱", "执行仍然要靠自己"], "start": 53.7, "end": 62.0, "x": "70", "y": "70"},
    {"id": "recipe_steps", "title": "只有操作建议", "lines": ["先准备食材", "再按步骤下锅"], "start": 62.0, "end": 71.9, "x": "W-w-70", "y": "70"},
    {"id": "kitchen_tasks", "title": "真正执行时", "lines": ["备菜  ·  控制火候", "清理灶台  ·  自己判断"], "start": 71.9, "end": 80.5, "x": "70", "y": "70"},
    {"id": "codex_cook", "title": "CODEX", "lines": ["不只告诉你怎么做", "直接把活干完"], "start": 80.5, "end": 94.8, "x": "W-w-70", "y": "70"},
    {"id": "parallel", "title": "并行开工", "lines": ["检索  →  处理  →  校验", "多个小工互不打扰"], "start": 95.4, "end": 100.0, "x": "70", "y": "70"},
    {"id": "real_work", "title": "落到实际工作", "lines": ["不只回答问题", "开始操作真实项目"], "start": 106.6, "end": 110.4, "x": "70", "y": "70"},
    {"id": "workflow", "title": "AGENT 工作流", "lines": ["打开项目  →  改代码", "查资料  →  部署上线"], "start": 110.4, "end": 114.0, "x": "W-w-70", "y": "70"},
    {"id": "agent_name", "title": "所以叫 AGENT", "lines": ["理解目标", "自主完成连续动作"], "start": 125.7, "end": 127.9, "x": "W-w-70", "y": "70"},
    {"id": "download", "title": "安装与界面", "lines": ["下载  ·  登录  ·  新建任务", "接下来进入实机演示"], "start": 128.3, "end": 131.0, "x": "70", "y": "70"},
    {"id": "screen_regions", "title": "界面结构", "lines": ["任务列表  ·  对话区", "多功能工作区"], "start": 143.4, "end": 149.6, "x": "W-w-70", "y": "60"},
    {"id": "task_demo", "title": "任务演示", "lines": ["收集近期 AI 热点", "正在联网检索"], "start": 149.6, "end": 154.4, "x": "W-w-70", "y": "60"},
    {"id": "appetizer", "title": "这只是开胃菜", "lines": ["先看清工具能力", "再进入真实业务"], "start": 154.6, "end": 162.6, "x": "70", "y": "70"},
    {"id": "authority", "title": "长期一线经验", "lines": ["深耕 AIGC 六年", "2025 百大讲师"], "start": 162.6, "end": 174.5, "x": "70", "y": "70"},
    {"id": "creator_case", "title": "内容创作", "lines": ["流程打包交付", "从重复劳动中释放"], "start": 175.1, "end": 179.0, "x": "W-w-70", "y": "70"},
    {"id": "commerce_case", "title": "电商增长", "lines": ["批量处理  ·  稳定复用", "把工具变成生产力"], "start": 188.0, "end": 192.0, "x": "70", "y": "70"},
    {"id": "sop", "title": "完整 SOP", "lines": ["提示词  ·  流程  ·  模板", "直接照着跑一遍"], "start": 201.0, "end": 209.4, "x": "70", "y": "70"},
    {"id": "cta", "title": "三连领取", "lines": ["完整可视化 SOP", "跟着流程直接开工"], "start": 209.4, "end": 214.4, "x": "W-w-70", "y": "70"},
    {"id": "ending", "title": "新窗口已经开了", "lines": ["先做出来  ·  再慢慢变好", "现在上桌"], "start": 218.6, "end": 229.1, "x": "70", "y": "70"},
]

CHARTS = [
    {"id": "compare", "title": "从建议到执行", "nodes": ["GPT\n给方案", "Codex\n直接执行", "交付\n结果"], "start": 72.0, "end": 80.5, "x": "460", "y": "540", "width": 1000, "height": 320},
    {"id": "workers", "title": "多个小工并行协作", "nodes": ["检索", "处理", "校验", "汇总"], "start": 100.0, "end": 106.6, "x": "460", "y": "540", "width": 1000, "height": 320},
    {"id": "agent_flow", "title": "AGENT 连续动作", "nodes": ["打开项目", "改代码", "查资料", "部署上线"], "start": 114.0, "end": 125.7, "x": "460", "y": "540", "width": 1000, "height": 320},
    {"id": "business", "title": "工具进入真实业务", "nodes": ["内容创作", "批量处理", "电商增长", "稳定复用"], "start": 179.0, "end": 201.0, "x": "460", "y": "540", "width": 1000, "height": 320},
]

TEXT_CARDS = []

SCREEN_HIGHLIGHTS = [
    {"start": 143.4, "end": 144.9, "x": 20, "y": 110, "w": 430, "h": 790, "color": ACCENT},
    {"start": 144.9, "end": 146.3, "x": 440, "y": 110, "w": 1030, "h": 790, "color": ACCENT},
    {"start": 146.3, "end": 147.8, "x": 1460, "y": 110, "w": 440, "h": 790, "color": ACCENT},
]

SUBTITLE_KEYWORDS = [
    "AI", "OpenClaw", "Claude Code", "Codex", "GPT", "额度更高", "功能更全",
    "上手更快", "Agent", "智能体", "打开项目", "改代码", "查资料", "部署上线",
    "内容创作", "电商", "一键三连", "SOP", "普通人", "上桌",
]

BGM_VOLUME = 0.06
VOICE_VOLUME = 1.05
