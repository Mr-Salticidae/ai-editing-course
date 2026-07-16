# 口播原片字幕识别：faster-whisper 词级时间戳 → JSON + SRT
import json, os, sys
from pathlib import Path

# Windows 下 ctranslate2 GPU 依赖 pip 装的 nvidia 运行库。ctranslate2 用
# LoadLibraryA 按文件名懒加载 cublas/cudnn，不走 add_dll_directory，只认 PATH。
_dll_dirs = [str(Path(sys.prefix) / "Lib" / "site-packages" / "nvidia" / sub / "bin")
             for sub in ("cublas", "cudnn")]
os.environ["PATH"] = os.pathsep.join(_dll_dirs + [os.environ.get("PATH", "")])
for d in _dll_dirs:
    if Path(d).is_dir():
        os.add_dll_directory(d)

WORK = Path(r"E:\ai-editing-course\04_剪辑方案\字幕工作区")
AUDIO = WORK / "源音频_16k.wav"

from faster_whisper import WhisperModel

def load_model():
    for device, compute, name in [("cuda", "float16", "large-v3"),
                                  ("cpu", "int8", "medium")]:
        try:
            m = WhisperModel(name, device=device, compute_type=compute)
            print(f"model={name} device={device}", flush=True)
            return m
        except Exception as e:
            print(f"[{device}/{name}] failed: {e}", file=sys.stderr, flush=True)
    raise RuntimeError("no model could be loaded")

model = load_model()
segments, info = model.transcribe(
    str(AUDIO), language="zh", word_timestamps=True,
    vad_filter=True, initial_prompt="以下是B站科技区UP主Genji关于Codex的口播教学视频，简体中文。")

def fmt_ts(t):
    h, rem = divmod(t, 3600); m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"

segs, srt_lines = [], []
for i, seg in enumerate(segments, 1):
    words = [{"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3)} for w in (seg.words or [])]
    segs.append({"id": i, "start": round(seg.start, 3), "end": round(seg.end, 3),
                 "text": seg.text.strip(), "words": words})
    srt_lines += [str(i), f"{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}", seg.text.strip(), ""]
    print(f"[{seg.start:7.2f} - {seg.end:7.2f}] {seg.text.strip()}", flush=True)

(WORK / "识别结果_词级.json").write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
(WORK / "识别结果.srt").write_text("\n".join(srt_lines), encoding="utf-8")
print(f"\nsegments={len(segs)} duration={info.duration:.1f}s -> 识别结果_词级.json / 识别结果.srt", flush=True)
