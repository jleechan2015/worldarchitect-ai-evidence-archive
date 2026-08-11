#!/usr/bin/env python3
"""Build captioned MP4 + GIF for the share-flow evidence bundle.

Uses PIL for the letterboxed annotated frames, then ffmpeg for the
concat + GIF palette pass. Output goes under
`/home/jleechan/projects/wt-share-takeover/evidence/8794/sharing/`.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EVIDENCE = Path(__file__).resolve().parent
WORKTREE = EVIDENCE.parent.parent.parent
CAPTIONED = EVIDENCE / "captioned"
CAPTIONED.mkdir(parents=True, exist_ok=True)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def annotate(src: Path, title: str, body: str, out: Path, commit_sha: str) -> None:
    base = Image.open(src).convert("RGB")
    width, height = base.size
    bar_top = 80
    bar_bottom = 40
    canvas_h = height + bar_top + bar_bottom
    canvas = Image.new("RGB", (width, canvas_h), "black")
    canvas.paste(base, (0, bar_top))

    draw = ImageDraw.Draw(canvas)
    f_title = _font(22)
    f_body = _font(15)
    f_foot = _font(13)
    draw.text((20, 10), title, fill="white", font=f_title)
    draw.text((20, 44), body, fill="#bbbbbb", font=f_body)
    foot = f"feat/campaign-share-url-phase1-takeover @ {commit_sha} · real local server · TESTING_AUTH_BYPASS=true"
    draw.text((20, canvas_h - bar_bottom + 8), foot, fill="#888888", font=f_foot)
    canvas.save(out, "PNG")


def main() -> int:
    sha = subprocess.check_output(
        ["git", "-C", str(WORKTREE), "rev-parse", "--short", "HEAD"],
        text=True,
    ).strip()

    steps = [
        ("01_wizard_prefill", "after_url_param_prefill.png", "Step 1 — URL-param prefill", "/new-campaign?title=…&character=…&setting=…&source=…&author=… prefills the wizard"),
        ("02_shared_landing", "after_shared_landing.png", "Step 2 — /shared/<token> landing", "Strict-CSP server-rendered HTML with Play-in-this-world anchor"),
        ("03_play_roundtrip", "after_play_roundtrip.png", "Step 3 — play button round-trip", "Clicking Play lands on /new-campaign with prefilled fields + source attribution"),
    ]
    for slug, src_name, title, body in steps:
        src = EVIDENCE / src_name
        out = CAPTIONED / f"{slug}.png"
        annotate(src, title, body, out, sha)

    mp4 = EVIDENCE / "share_flow_captions.mp4"
    gif = EVIDENCE / "share_flow_captions.gif"

    ffmpeg_inputs = []
    for slug, *_ in steps:
        ffmpeg_inputs += ["-loop", "1", "-t", "3", "-i", str(CAPTIONED / f"{slug}.png")]

    # MP4
    cmd = ["ffmpeg", "-y", *ffmpeg_inputs,
           "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]",
           "-map", "[outv]",
           "-r", "24", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "veryfast",
           str(mp4)]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # GIF (faster 2s per frame, downscaled)
    gif_inputs = []
    for slug, *_ in steps:
        gif_inputs += ["-loop", "1", "-t", "2", "-i", str(CAPTIONED / f"{slug}.png")]
    cmd = ["ffmpeg", "-y", *gif_inputs,
           "-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=720:-1,split[a][b];[a]palettegen[p];[b][p]paletteuse",
           "-r", "12",
           str(gif)]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    artifacts = sorted([*CAPTIONED.glob("*.png"), mp4, gif])
    rows = []
    for a in artifacts:
        size = a.stat().st_size
        sha256 = hashlib.sha256(a.read_bytes()).hexdigest()[:16]
        rows.append((a.relative_to(EVIDENCE), size, sha256))
    print("Generated:")
    for rel, size, sha16 in rows:
        print(f"  {rel}  size={size:>7}  sha256[:16]={sha16}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())