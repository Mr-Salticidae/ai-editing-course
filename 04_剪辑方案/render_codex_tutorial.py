from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import config


def ff(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def filter_path(path: Path) -> str:
    try:
        value = path.relative_to(config.ROOT).as_posix()
    except ValueError:
        value = path.as_posix()
    return value.replace("'", r"\'").replace(":", r"\:")


def drawtext_escape(value: str) -> str:
    return (
        value.replace("\\", r"\\")
        .replace("'", r"\'")
        .replace(":", r"\:")
        .replace(",", r"\,")
    )


def validate_inputs() -> None:
    required = [
        config.SOURCE,
        config.SCREEN_RECORDING,
        config.BGM,
        config.SUBTITLES,
        config.FONT_REGULAR,
        config.FONT_BOLD,
    ]
    required.extend(config.ASSET_DIR / item["file"] for item in config.OVERLAYS)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required files:\n" + "\n".join(missing))
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is not available on PATH")


def build_command(draft: bool, output: Path, encoder: str) -> tuple[list[str], str]:
    command = ["ffmpeg", "-y", "-hide_banner", "-stats", "-i", str(config.SOURCE)]
    command += ["-i", str(config.SCREEN_RECORDING)]
    command += ["-stream_loop", "-1", "-i", str(config.BGM)]

    asset_indexes: list[int] = []
    for item in config.OVERLAYS:
        duration = item["end"] - item["start"]
        path = config.ASSET_DIR / item["file"]
        kind = item.get("kind", "image")
        if kind == "image":
            command += ["-stream_loop", "-1", "-framerate", str(config.FPS), "-t", ff(duration), "-i", str(path)]
        elif kind == "animated_image":
            command += ["-stream_loop", "-1", "-t", ff(duration), "-i", str(path)]
        else:
            command += ["-stream_loop", "-1", "-t", ff(duration), "-i", str(path)]
        asset_indexes.append(len(asset_indexes) + 3)

    filters: list[str] = ["[0:v]setpts=PTS-STARTPTS,format=yuv420p[base0]"]
    screen_duration = config.SCREEN_INSERT["end"] - config.SCREEN_INSERT["start"]
    screen_source_end = config.SCREEN_INSERT["source_start"] + screen_duration
    filters.append(
        "[1:v]"
        f"trim=start={ff(config.SCREEN_INSERT['source_start'])}:end={ff(screen_source_end)},"
        f"setpts=PTS-STARTPTS+{ff(config.SCREEN_INSERT['start'])}/TB,"
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white[screen]"
    )
    filters.append(
        "[base0][screen]overlay=x=0:y=0:eof_action=pass:shortest=0:"
        f"enable='between(t,{ff(config.SCREEN_INSERT['start'])},{ff(config.SCREEN_INSERT['end'])})'[v0]"
    )

    current = "v0"
    for number, (item, index) in enumerate(zip(config.OVERLAYS, asset_indexes), start=1):
        duration = item["end"] - item["start"]
        fade = min(0.18, duration / 4)
        kind = item.get("kind", "image")
        transform = f"scale={item['width']}:-1:force_original_aspect_ratio=decrease"
        if kind == "green_video":
            transform += ",chromakey=0x00FF00:0.24:0.08"
        overlay_label = f"asset{number}"
        filters.append(
            f"[{index}:v]{transform},format=rgba,"
            f"fade=t=in:st=0:d={ff(fade)}:alpha=1,"
            f"fade=t=out:st={ff(duration - fade)}:d={ff(fade)}:alpha=1,"
            f"setpts=PTS-STARTPTS+{ff(item['start'])}/TB[{overlay_label}]"
        )
        next_label = f"v{number}"
        filters.append(
            f"[{current}][{overlay_label}]overlay=x={item['x']}:y={item['y']}:"
            f"eof_action=pass:shortest=0:enable='between(t,{ff(item['start'])},{ff(item['end'])})'"
            f"[{next_label}]"
        )
        current = next_label

    for number, card in enumerate(config.TEXT_CARDS, start=1):
        next_label = f"text{number}"
        x = card.get("x", "(w-text_w)/2")
        if isinstance(x, int):
            x = str(x)
        font = filter_path(config.FONT_BOLD)
        filters.append(
            f"[{current}]drawtext=fontfile='{font}':text='{drawtext_escape(card['text'])}':"
            "expansion=none:"
            f"fontsize={card.get('size', 74)}:fontcolor={card.get('color', '#FFFFFF')}:"
            f"x={x}:y={card['y']}:box=1:boxcolor=0x101820@0.78:boxborderw=22:"
            f"enable='between(t,{ff(card['start'])},{ff(card['end'])})'[{next_label}]"
        )
        current = next_label

    for number, box in enumerate(config.SCREEN_HIGHLIGHTS, start=1):
        next_label = f"box{number}"
        color = box["color"].lstrip("#")
        filters.append(
            f"[{current}]drawbox=x={box['x']}:y={box['y']}:w={box['w']}:h={box['h']}:"
            f"color=0x{color}@0.92:t=7:enable='between(t,{ff(box['start'])},{ff(box['end'])})'"
            f"[{next_label}]"
        )
        current = next_label

    subtitle_path = filter_path(config.SUBTITLES)
    subtitle_style = (
        "FontName=Microsoft YaHei,FontSize=50,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00101010,BorderStyle=1,Outline=3,Shadow=0,"
        "Alignment=2,MarginV=48"
    )
    filters.append(
        f"[{current}]subtitles=filename='{subtitle_path}':force_style='{subtitle_style}'[subbed]"
    )
    if draft:
        filters.append("[subbed]scale=960:540:flags=lanczos[vout]")
    else:
        filters.append("[subbed]null[vout]")

    # Voice remains the timing backbone. BGM is looped, faded and mixed at
    # roughly -22.5 dB so it supports the narration without masking it.
    filters.append(
        f"[0:a]highpass=f=70,lowpass=f=15000,volume={config.VOICE_VOLUME},"
        "acompressor=threshold=0.14:ratio=2.2:attack=15:release=180[voice]"
    )
    filters.append(
        f"[2:a]atrim=0:{ff(config.DURATION)},asetpts=PTS-STARTPTS,"
        f"volume={config.BGM_VOLUME},afade=t=in:st=0:d=1.2,"
        f"afade=t=out:st={ff(config.DURATION - 3.0)}:d=3[bgm]"
    )
    filters.append(
        "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0,"
        "loudnorm=I=-14:LRA=7:TP=-1.5,"
        "alimiter=limit=0.84:attack=5:release=50:level=0,aresample=48000[aout]"
    )

    filter_graph = ";\n".join(filters)
    command += ["-filter_complex_script", str(config.ROOT / "04_剪辑方案" / "render_filter.txt")]
    command += ["-map", "[vout]", "-map", "[aout]", "-t", ff(config.DURATION), "-r", str(config.FPS)]

    if encoder == "h264_nvenc":
        command += ["-c:v", encoder, "-preset", "p5" if not draft else "p3", "-tune", "hq", "-rc", "vbr", "-cq", "19" if not draft else "27", "-b:v", "0"]
    else:
        command += ["-c:v", "libx264", "-preset", "medium" if not draft else "ultrafast", "-crf", "18" if not draft else "28"]
    command += [
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-ar", "48000",
        "-b:a", "192k" if not draft else "128k",
        "-movflags", "+faststart",
        str(output),
    ]
    return command, filter_graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the approved Codex tutorial edit.")
    parser.add_argument("--draft", action="store_true", help="Render a 960x540 review copy.")
    parser.add_argument("--encoder", choices=("libx264", "h264_nvenc"), default="libx264")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    validate_inputs()
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = args.output or config.OUTPUT_DIR / (
        "Codex保姆级教学_审核预览_v1.mp4" if args.draft else "Codex保姆级教学_成片_v1.mp4"
    )
    output = output.resolve()
    command, filter_graph = build_command(args.draft, output, args.encoder)
    filter_file = config.ROOT / "04_剪辑方案" / "render_filter.txt"
    filter_file.write_text(filter_graph, encoding="utf-8")

    print(f"Rendering: {output}")
    print(f"Encoder: {args.encoder}")
    result = subprocess.run(command, cwd=config.ROOT)
    if result.returncode:
        return result.returncode
    print(f"Done: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
