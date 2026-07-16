from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "02_口播视频原稿" / "视频源文件.mp4"
SCREEN_RECORDING = ROOT / "03_剪辑物料" / "录屏" / "Codex演示_界面与热点任务.mp4"
BGM = ROOT / "03_剪辑物料" / "BGM_Codex教学_v1_ToolThatLands.wav"
SUBTITLES = ROOT / "04_剪辑方案" / "字幕工作区" / "字幕_校对v1.srt"
ASSET_DIR = ROOT / "03_剪辑物料" / "剪辑素材"
OUTPUT_DIR = ROOT / "05_成片"

FPS = 30
DURATION = 229.778
DESIGN_SIZE = (1920, 1080)
FONT_REGULAR = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")

# The recording starts at its first frame. Its local 18.6s typing action aligns
# with the narration's 149.6s demonstration sentence.
SCREEN_INSERT = {
    "start": 131.0,
    "end": 154.4,
    "source_start": 0.0,
}

# Static overlays. Positions are ffmpeg expressions in the 1920x1080 design
# coordinate system so timing changes stay isolated in this file.
OVERLAYS = [
    {"file": "OpenClaw图标.png", "start": 1.9, "end": 4.8, "width": 250, "x": "90", "y": "150"},
    {"file": "claude.png", "start": 2.5, "end": 4.8, "width": 250, "x": "W-w-90", "y": "150"},
    {"file": "Codex图标.png", "start": 4.8, "end": 8.1, "width": 360, "x": "W-w-110", "y": "120"},
    {"file": "Codex图标.png", "start": 16.3, "end": 21.7, "width": 250, "x": "110", "y": "150"},
    {"file": "gpt.png", "start": 16.3, "end": 21.7, "width": 250, "x": "W-w-110", "y": "150"},
    {"file": "魔法1.png", "start": 26.5, "end": 29.2, "width": 360, "x": "100", "y": "120"},
    {"file": "白圆箭头.png", "start": 26.5, "end": 29.2, "width": 250, "x": "W-w-180", "y": "620"},
    {"file": "genji像素小人.png", "start": 30.0, "end": 41.9, "width": 330, "x": "90", "y": "520"},
    {"file": "genji账号头像.png", "start": 30.0, "end": 41.9, "width": 220, "x": "W-w-90", "y": "100"},
    {"file": "图标/OpenAI.png", "start": 43.5, "end": 46.8, "width": 300, "x": "100", "y": "140"},
    {"file": "Codex图标.png", "start": 43.5, "end": 52.5, "width": 270, "x": "W-w-100", "y": "130"},
    {"file": "图标_表格.png", "start": 48.0, "end": 50.2, "width": 230, "x": "100", "y": "570"},
    {"file": "图标_剪刀胶片剪辑.png", "start": 50.2, "end": 52.5, "width": 260, "x": "W-w-100", "y": "560"},
    {"file": "对话气泡.png", "start": 56.4, "end": 62.0, "width": 390, "x": "80", "y": "120"},
    {"file": "对话气泡.png", "start": 62.0, "end": 67.0, "width": 390, "x": "W-w-80", "y": "130"},
    {"file": "对话气泡.png", "start": 67.0, "end": 71.9, "width": 390, "x": "80", "y": "520"},
    {"file": "像素老师.png", "start": 80.5, "end": 94.8, "width": 330, "x": "90", "y": "500"},
    {"file": "豆包男老师.png", "start": 80.5, "end": 94.8, "width": 330, "x": "W-w-90", "y": "500"},
    {"file": "像素老师.png", "start": 95.4, "end": 106.6, "width": 240, "x": "55", "y": "120"},
    {"file": "豆包男老师.png", "start": 95.4, "end": 106.6, "width": 240, "x": "W-w-55", "y": "120"},
    {"file": "👂.png", "start": 98.0, "end": 106.6, "width": 150, "x": "80", "y": "650"},
    {"file": "✅.png", "start": 100.0, "end": 106.6, "width": 150, "x": "W-w-80", "y": "650"},
    {"file": "图标_打开文件夹带文档.png", "start": 110.4, "end": 125.7, "width": 235, "x": "80", "y": "150"},
    {"file": "cc  logo.png", "start": 114.0, "end": 125.7, "width": 235, "x": "340", "y": "150"},
    {"file": "图标_文件夹放大镜检索.png", "start": 117.2, "end": 125.7, "width": 235, "x": "W-w-340", "y": "150"},
    {"file": "图标_齿轮文档看板.png", "start": 120.5, "end": 125.7, "width": 235, "x": "W-w-80", "y": "150"},
    {"file": "2025年百大up主皇冠全.png", "start": 162.6, "end": 174.5, "width": 430, "x": "80", "y": "120"},
    {"file": "💰️.png", "start": 175.1, "end": 188.0, "width": 310, "x": "90", "y": "180", "kind": "animated_image"},
    {"file": "💸.png", "start": 188.0, "end": 201.0, "width": 310, "x": "W-w-90", "y": "180"},
    {"file": "一键三连-绿幕.mp4", "start": 209.4, "end": 214.4, "width": 1300, "x": "(W-w)/2+260", "y": "0", "kind": "green_video"},
    {"file": "Codex图标.png", "start": 218.6, "end": 229.1, "width": 390, "x": "W-w-120", "y": "110"},
]

TEXT_CARDS = [
    {"text": "额度更高", "start": 8.3, "end": 9.7, "y": 70, "color": "#7DE2D1"},
    {"text": "功能更全", "start": 9.7, "end": 11.1, "y": 70, "color": "#FFD166"},
    {"text": "上手更快", "start": 11.1, "end": 12.5, "y": 70, "color": "#FF8C69"},
    {"text": "不怕封号", "start": 12.5, "end": 13.8, "y": 70, "color": "#FFFFFF"},
    {"text": "下载  →  登录  →  开始用", "start": 16.3, "end": 21.7, "y": 580, "size": 64, "color": "#FFFFFF"},
    {"text": "评论区置顶", "start": 26.5, "end": 29.2, "y": 620, "size": 58, "color": "#FFD166"},
    {"text": "PPT", "start": 46.8, "end": 48.0, "y": 170, "color": "#7DE2D1"},
    {"text": "Excel", "start": 48.0, "end": 49.2, "y": 170, "color": "#7DE2D1"},
    {"text": "操作浏览器", "start": 49.2, "end": 50.5, "y": 170, "color": "#7DE2D1"},
    {"text": "剪视频", "start": 50.5, "end": 52.5, "y": 170, "color": "#FFD166"},
    {"text": "GPT：告诉你怎么做", "start": 53.7, "end": 71.9, "y": 110, "size": 58, "color": "#FFFFFF", "x": 600},
    {"text": "Codex：直接把活干完", "start": 80.5, "end": 94.8, "y": 110, "size": 62, "color": "#7DE2D1"},
    {"text": "多个小工，并行开工", "start": 95.4, "end": 106.6, "y": 115, "size": 58, "color": "#FFD166"},
    {"text": "打开项目  →  改代码  →  查资料  →  部署", "start": 110.4, "end": 125.7, "y": 500, "size": 54, "color": "#FFFFFF"},
    {"text": "AGENT", "start": 125.7, "end": 127.9, "y": 160, "size": 108, "color": "#7DE2D1"},
    {"text": "官网下载 · 安装 · 登录", "start": 128.3, "end": 131.0, "y": 150, "size": 66, "color": "#FFFFFF"},
    {"text": "左：任务列表", "start": 143.4, "end": 144.9, "x": 90, "y": 130, "size": 46, "color": "#FF5F57"},
    {"text": "中：对话区", "start": 144.9, "end": 146.3, "y": 130, "size": 46, "color": "#FFD166"},
    {"text": "右：多功能区", "start": 146.3, "end": 147.8, "x": 1370, "y": 130, "size": 46, "color": "#28C840"},
    {"text": "2025 百大讲师", "start": 162.6, "end": 174.5, "x": 1110, "y": 160, "size": 64, "color": "#FFD166"},
    {"text": "内容创作", "start": 175.1, "end": 188.0, "x": 1150, "y": 180, "size": 72, "color": "#7DE2D1"},
    {"text": "电商增长", "start": 188.0, "end": 201.0, "x": 120, "y": 180, "size": 72, "color": "#FF8C69"},
    {"text": "现在上桌", "start": 218.6, "end": 229.1, "x": 120, "y": 170, "size": 92, "color": "#FFD166"},
]

SCREEN_HIGHLIGHTS = [
    {"start": 143.4, "end": 144.9, "x": 20, "y": 110, "w": 430, "h": 900, "color": "#FF5F57"},
    {"start": 144.9, "end": 146.3, "x": 440, "y": 110, "w": 1030, "h": 900, "color": "#FFD166"},
    {"start": 146.3, "end": 147.8, "x": 1460, "y": 110, "w": 440, "h": 900, "color": "#28C840"},
]

BGM_VOLUME = 0.075
VOICE_VOLUME = 1.05
