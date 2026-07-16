from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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


def ass_time(timestamp: str) -> str:
    hours, minutes, rest = timestamp.replace(",", ".").split(":")
    seconds = float(rest)
    return f"{int(hours)}:{int(minutes):02d}:{seconds:05.2f}"


def highlight_keywords(text: str) -> str:
    safe = text.replace("{", r"\{").replace("}", r"\}")
    keywords = sorted(config.SUBTITLE_KEYWORDS, key=len, reverse=True)
    pattern = re.compile("(" + "|".join(re.escape(word) for word in keywords) + ")", re.IGNORECASE)
    return pattern.sub(
        lambda match: r"{\c&H75FF69&\b1}" + match.group(0) + r"{\c&HFFFFFF&\b0}",
        safe,
    )


def generate_ass_subtitles() -> Path:
    output = config.EDIT_DIR / "master_v2.ass"
    output.parent.mkdir(parents=True, exist_ok=True)
    blocks = re.split(r"\r?\n\r?\n", config.SUBTITLES.read_text(encoding="utf-8-sig").strip())
    events: list[str] = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or " --> " not in lines[1]:
            continue
        start, end = lines[1].split(" --> ")
        text = "".join(line.strip() for line in lines[2:])
        events.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{highlight_keywords(text)}"
        )

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Microsoft YaHei,40,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,1.5,0,2,60,60,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    output.write_text(header + "\n".join(events) + "\n", encoding="utf-8-sig")
    return output


def fit_font(path: Path, size: int, text: str, max_width: int) -> ImageFont.FreeTypeFont:
    while size >= 18:
        font = ImageFont.truetype(str(path), size)
        if font.getlength(text) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(str(path), 18)


def generate_ui_cards() -> list[dict]:
    output_dir = config.EDIT_DIR / "animations" / "ui_cards"
    output_dir.mkdir(parents=True, exist_ok=True)
    width, height = 560, 180
    generated: list[dict] = []
    for card in config.UI_CARDS:
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (2, 2, width - 3, height - 3),
            radius=16,
            fill=(16, 20, 23, 204),
            outline=(105, 255, 117, 210),
            width=2,
        )
        draw.rounded_rectangle((2, 2, 11, height - 3), radius=5, fill=(105, 255, 117, 255))
        title_font = fit_font(config.FONT_BOLD, 34, card["title"], width - 70)
        draw.text((30, 21), card["title"], font=title_font, fill=(105, 255, 117, 255))
        for index, line in enumerate(card["lines"]):
            body_font = fit_font(config.FONT_REGULAR, 27, line, width - 70)
            y = 78 + index * 42
            draw.ellipse((31, y + 9, 39, y + 17), fill=(105, 255, 117, 230))
            draw.text((50, y), line, font=body_font, fill=(244, 247, 248, 255))
        path = output_dir / f"{card['id']}.png"
        image.save(path)
        generated.append({**card, "path": path, "width": width, "kind": "image", "animated": True})
    return generated


def generate_charts() -> list[dict]:
    output_dir = config.EDIT_DIR / "animations" / "charts"
    output_dir.mkdir(parents=True, exist_ok=True)
    generated: list[dict] = []
    for chart in config.CHARTS:
        width, height = chart["width"], chart["height"]
        nodes = chart["nodes"]
        stage_duration = (chart["end"] - chart["start"]) / len(nodes)
        for stage in range(1, len(nodes) + 1):
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle(
                (2, 2, width - 3, height - 3),
                radius=20,
                fill=(16, 20, 23, 204),
                outline=(105, 255, 117, 210),
                width=2,
            )
            title_font = fit_font(config.FONT_BOLD, 34, chart["title"], width - 70)
            draw.text((32, 22), chart["title"], font=title_font, fill=(105, 255, 117, 255))

            count = len(nodes)
            node_width = min(190, (width - 100 - (count - 1) * 40) // count)
            node_height = 105
            gap = (width - 80 - count * node_width) / max(count - 1, 1)
            top = 120
            centers: list[tuple[float, float]] = []
            for index in range(count):
                left = 40 + index * (node_width + gap)
                centers.append((left + node_width / 2, top + node_height / 2))

            for index in range(stage - 1):
                x1, y1 = centers[index]
                x2, y2 = centers[index + 1]
                draw.line((x1 + node_width / 2, y1, x2 - node_width / 2, y2), fill=(105, 255, 117, 220), width=5)
                draw.polygon(
                    [(x2 - node_width / 2, y2), (x2 - node_width / 2 - 13, y2 - 8), (x2 - node_width / 2 - 13, y2 + 8)],
                    fill=(105, 255, 117, 235),
                )

            for index in range(stage):
                center_x, center_y = centers[index]
                longest_line = max(nodes[index].splitlines(), key=len)
                node_font = fit_font(
                    config.FONT_BOLD, 25, longest_line, node_width - 16
                )
                box = (
                    int(center_x - node_width / 2),
                    int(center_y - node_height / 2),
                    int(center_x + node_width / 2),
                    int(center_y + node_height / 2),
                )
                draw.rounded_rectangle(box, radius=14, fill=(32, 64, 40, 235), outline=(105, 255, 117, 255), width=3)
                text_box = draw.multiline_textbbox((0, 0), nodes[index], font=node_font, spacing=4, align="center")
                text_width = text_box[2] - text_box[0]
                text_height = text_box[3] - text_box[1]
                draw.multiline_text(
                    (center_x - text_width / 2, center_y - text_height / 2 - 2),
                    nodes[index],
                    font=node_font,
                    fill=(246, 249, 247, 255),
                    spacing=4,
                    align="center",
                )

            progress_width = int((width - 64) * stage / count)
            draw.rounded_rectangle((32, height - 24, width - 32, height - 16), radius=4, fill=(55, 63, 60, 190))
            draw.rounded_rectangle((32, height - 24, 32 + progress_width, height - 16), radius=4, fill=(105, 255, 117, 255))

            path = output_dir / f"{chart['id']}_{stage}.png"
            image.save(path)
            start = chart["start"] + (stage - 1) * stage_duration
            end = chart["start"] + stage * stage_duration
            generated.append(
                {
                    "id": f"{chart['id']}_{stage}",
                    "path": path,
                    "start": start,
                    "end": end,
                    "x": chart["x"],
                    "y": chart["y"],
                    "width": width,
                    "kind": "image",
                    "animated": True,
                }
            )
    return generated


def generate_progress_assets() -> list[dict]:
    output_dir = config.EDIT_DIR / "animations" / "progress"
    output_dir.mkdir(parents=True, exist_ok=True)
    width, height = 1640, 56
    rail_left, rail_right, rail_y = 20, width - 20, 10
    label_font = ImageFont.truetype(str(config.FONT_BOLD), 28)
    generated: list[dict] = []

    for active_index, section in enumerate(config.PROGRESS_SECTIONS):
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        for index, item in enumerate(config.PROGRESS_SECTIONS):
            segment_left = rail_left + (rail_right - rail_left) * item["start"] / config.DURATION
            segment_right = rail_left + (rail_right - rail_left) * item["end"] / config.DURATION
            x = round(segment_left)
            active = index == active_index
            passed = index < active_index
            fill = (
                (105, 255, 117, 255)
                if active
                else ((105, 255, 117, 215) if passed else (92, 101, 98, 230))
            )
            radius = 8 if active else 6
            draw.ellipse(
                (x - radius, rail_y - radius, x + radius, rail_y + radius),
                fill=fill,
            )
            label = item["label"]
            box = draw.textbbox((0, 0), label, font=label_font)
            text_width = box[2] - box[0]
            label_center = (segment_left + segment_right) / 2
            text_x = max(0, min(width - text_width, label_center - text_width / 2))
            text_fill = (105, 255, 117, 255) if active else (246, 249, 248, 245)
            draw.text(
                (text_x, 23),
                label,
                font=label_font,
                fill=text_fill,
                stroke_width=3,
                stroke_fill=(10, 14, 13, 235),
            )

        end_x = rail_right
        end_active = active_index == len(config.PROGRESS_SECTIONS) - 1
        end_radius = 8 if end_active else 6
        draw.ellipse(
            (
                end_x - end_radius,
                rail_y - end_radius,
                end_x + end_radius,
                rail_y + end_radius,
            ),
            fill=(105, 255, 117, 255) if end_active else (92, 101, 98, 230),
        )

        path = output_dir / f"section_{active_index + 1}_{section['id']}.png"
        image.save(path)
        generated.append(
            {
                "id": f"progress_{section['id']}",
                "path": path,
                "start": section["start"],
                "end": section["end"],
                "x": "140",
                "y": "1004",
                "width": width,
                "kind": "image",
            }
        )

    generated.append(
        {
            "id": "progress_genji",
            "path": config.PROGRESS_ICON,
            "start": 0.0,
            "end": config.DURATION,
            "x": f"'160+(1600-w)*min(t,{ff(config.DURATION)})/{ff(config.DURATION)}'",
            "y": "'937-3*abs(sin(PI*t*2))'",
            "width": 64,
            "kind": "image",
        }
    )
    return generated


def generate_screen_freeze() -> Path:
    output = config.EDIT_DIR / "animations" / "screen_freeze.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            "13.0",
            "-i",
            str(config.SCREEN_RECORDING),
            "-frames:v",
            "1",
            str(output),
        ],
        check=True,
    )
    return output


def validate_inputs() -> None:
    required = [
        config.SOURCE,
        config.SCREEN_RECORDING,
        config.BGM,
        config.SUBTITLES,
        config.FONT_REGULAR,
        config.FONT_BOLD,
        config.PROGRESS_ICON,
    ]
    required.extend(config.ASSET_DIR / item["file"] for item in config.OVERLAYS)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required files:\n" + "\n".join(missing))
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is not available on PATH")


def build_command(
    draft: bool,
    output: Path,
    encoder: str,
    subtitles: Path,
    ui_cards: list[dict],
    charts: list[dict],
    progress_assets: list[dict],
    screen_freeze: Path,
) -> tuple[list[str], str]:
    command = ["ffmpeg", "-y", "-hide_banner", "-stats", "-i", str(config.SOURCE)]
    command += ["-i", str(config.SCREEN_RECORDING)]
    command += ["-stream_loop", "-1", "-i", str(config.BGM)]
    freeze_start = config.SCREEN_HIGHLIGHTS[0]["start"]
    freeze_end = config.SCREEN_HIGHLIGHTS[-1]["end"]
    command += [
        "-loop",
        "1",
        "-framerate",
        str(config.FPS),
        "-t",
        ff(freeze_end - freeze_start),
        "-i",
        str(screen_freeze),
    ]

    overlays = [
        {**item, "path": config.ASSET_DIR / item["file"]}
        for item in config.OVERLAYS
    ] + ui_cards + charts + progress_assets
    asset_indexes: list[int] = []
    for item in overlays:
        duration = item["end"] - item["start"]
        path = item["path"]
        command += [
            "-stream_loop", "-1", "-framerate", str(config.FPS),
            "-t", ff(duration), "-i", str(path),
        ]
        asset_indexes.append(len(asset_indexes) + 4)

    filters: list[str] = [
        "[0:v]scale=2048:1152:flags=lanczos,"
        "crop=1920:1080:(iw-ow)/2:(ih-oh)/2,setsar=1,"
        "setpts=PTS-STARTPTS,format=yuv420p[base0]"
    ]
    screen_duration = config.SCREEN_INSERT["end"] - config.SCREEN_INSERT["start"]
    skip_duration = config.SCREEN_GLITCH_SKIP["end"] - config.SCREEN_GLITCH_SKIP["start"]
    screen_source_end = (
        config.SCREEN_INSERT["source_start"] + screen_duration + skip_duration
    )
    filters.append("[1:v]split=2[screen_a_src][screen_b_src]")
    filters.append(
        "[screen_a_src]"
        f"trim=start={ff(config.SCREEN_INSERT['source_start'])}:"
        f"end={ff(config.SCREEN_GLITCH_SKIP['start'])},"
        "setpts=PTS-STARTPTS[screen_a]"
    )
    filters.append(
        "[screen_b_src]"
        f"trim=start={ff(config.SCREEN_GLITCH_SKIP['end'])}:"
        f"end={ff(screen_source_end)},"
        "setpts=PTS-STARTPTS[screen_b]"
    )
    filters.append(
        "[screen_a][screen_b]concat=n=2:v=1:a=0,"
        f"setpts=PTS-STARTPTS+{ff(config.SCREEN_INSERT['start'])}/TB,"
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white[screen]"
    )
    filters.append(
        "[3:v]"
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=white,"
        f"setpts=PTS-STARTPTS+{ff(freeze_start)}/TB[screen_freeze]"
    )
    filters.append(
        "[base0][screen]overlay=x=0:y=0:eof_action=pass:shortest=0:"
        f"enable='between(t,{ff(config.SCREEN_INSERT['start'])},{ff(config.SCREEN_INSERT['end'])})'[screened_live]"
    )
    filters.append(
        "[screened_live][screen_freeze]overlay=x=0:y=0:eof_action=pass:shortest=0:"
        f"enable='between(t,{ff(freeze_start)},{ff(freeze_end)})'[screened]"
    )

    # Benchmark-style speaker picture-in-picture for the full-screen demo.
    filters.append(
        "[0:v]"
        f"trim=start={ff(config.SCREEN_INSERT['start'])}:end={ff(config.SCREEN_INSERT['end'])},"
        "crop=700:700:610:40,scale=250:250,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(lte(hypot(X-W/2,Y-H/2),W/2),255,0)',"
        f"setpts=PTS-STARTPTS+{ff(config.SCREEN_INSERT['start'])}/TB[pip]"
    )
    filters.append(
        f"color=c=0x69FF75:s=270x270:d={ff(screen_duration)}:r={config.FPS},"
        "format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(lte(hypot(X-W/2,Y-H/2),W/2),255,0)',"
        f"setpts=PTS-STARTPTS+{ff(config.SCREEN_INSERT['start'])}/TB[ring]"
    )
    filters.append(
        "[screened][ring]overlay=x=55:y=625:eof_action=pass:shortest=0:"
        f"enable='between(t,{ff(config.SCREEN_INSERT['start'])},{ff(config.SCREEN_INSERT['end'])})'[ringed]"
    )
    filters.append(
        "[ringed][pip]overlay=x=65:y=635:eof_action=pass:shortest=0:"
        f"enable='between(t,{ff(config.SCREEN_INSERT['start'])},{ff(config.SCREEN_INSERT['end'])})'[v0]"
    )

    filters.append(
        "[v0]drawbox=x=160:y=1014:w=1600:h=6:"
        "color=0x454D4A@0.88:t=fill[progressrail]"
    )
    filters.append(
        f"color=c=0x69FF75:s=1600x6:d={ff(config.DURATION)}:r={config.FPS},"
        "format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        f"a='if(lte(X,1600*T/{ff(config.DURATION)}),245,0)'[progressbar]"
    )
    filters.append(
        "[progressrail][progressbar]overlay=x=160:y=1014:"
        "eof_action=pass:shortest=0[progressfill]"
    )
    current = "progressfill"
    for number, (item, index) in enumerate(zip(overlays, asset_indexes), start=1):
        duration = item["end"] - item["start"]
        fade = min(0.22, duration / 4)
        overlay_label = f"asset{number}"
        filters.append(
            f"[{index}:v]scale={item['width']}:-1:force_original_aspect_ratio=decrease,format=rgba,"
            f"fade=t=in:st=0:d={ff(fade)}:alpha=1,"
            f"fade=t=out:st={ff(duration - fade)}:d={ff(fade)}:alpha=1,"
            f"setpts=PTS-STARTPTS+{ff(item['start'])}/TB[{overlay_label}]"
        )
        next_label = f"v{number}"
        y_expression = str(item["y"])
        if item.get("animated"):
            y_expression = (
                f"'{item['y']}+if(lt(t,{ff(item['start'] + 0.42)}),"
                f"24*pow(1-(t-{ff(item['start'])})/0.42,3),0)'"
            )
        filters.append(
            f"[{current}][{overlay_label}]overlay=x={item['x']}:y={y_expression}:"
            f"eof_action=pass:shortest=0:enable='between(t,{ff(item['start'])},{ff(item['end'])})'"
            f"[{next_label}]"
        )
        current = next_label

    for number, card in enumerate(config.TEXT_CARDS, start=1):
        next_label = f"text{number}"
        x = str(card.get("x", "(w-text_w)/2"))
        filters.append(
            f"[{current}]drawtext=fontfile='{filter_path(config.FONT_BOLD)}':"
            f"text='{drawtext_escape(card['text'])}':expansion=none:"
            f"fontsize={card.get('size', 56)}:fontcolor={card.get('color', config.ACCENT)}:"
            f"x={x}:y={card['y']}:enable='between(t,{ff(card['start'])},{ff(card['end'])})'"
            f"[{next_label}]"
        )
        current = next_label

    for number, box in enumerate(config.SCREEN_HIGHLIGHTS, start=1):
        next_label = f"box{number}"
        filters.append(
            f"[{current}]drawbox=x={box['x']}:y={box['y']}:w={box['w']}:h={box['h']}:"
            f"color=0x{box['color'].lstrip('#')}@0.92:t=5:"
            f"enable='between(t,{ff(box['start'])},{ff(box['end'])})'[{next_label}]"
        )
        current = next_label

    # ASS captions stay last so no overlay can obscure them.
    filters.append(f"[{current}]subtitles=filename='{filter_path(subtitles)}'[subbed]")
    filters.append("[subbed]scale=960:540:flags=lanczos[vout]" if draft else "[subbed]null[vout]")

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
        command += [
            "-c:v", encoder, "-preset", "p5" if not draft else "p3", "-tune", "hq",
            "-rc", "vbr", "-cq", "19" if not draft else "27", "-b:v", "0",
        ]
    else:
        command += [
            "-c:v", "libx264", "-preset", "medium" if not draft else "ultrafast",
            "-crf", "18" if not draft else "28",
        ]
    command += [
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000",
        "-b:a", "192k" if not draft else "128k", "-movflags", "+faststart", str(output),
    ]
    return command, filter_graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the benchmark-aligned Codex tutorial edit.")
    parser.add_argument("--draft", action="store_true", help="Render a 960x540 review copy.")
    parser.add_argument("--encoder", choices=("libx264", "h264_nvenc"), default="libx264")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    validate_inputs()
    subtitles = generate_ass_subtitles()
    ui_cards = generate_ui_cards()
    charts = generate_charts()
    progress_assets = generate_progress_assets()
    screen_freeze = generate_screen_freeze()
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = args.output or config.OUTPUT_DIR / (
        "Codex保姆级教学_审核预览_v2.4.1.mp4"
        if args.draft
        else "Codex保姆级教学_成片_v2.4.1.mp4"
    )
    output = output.resolve()
    command, filter_graph = build_command(
        args.draft,
        output,
        args.encoder,
        subtitles,
        ui_cards,
        charts,
        progress_assets,
        screen_freeze,
    )
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
