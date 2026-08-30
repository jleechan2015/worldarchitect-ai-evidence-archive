"""Capture BEFORE / AFTER screenshots + side-by-side MP4 for PR #9495 /es evidence.

Reads the worktree's actual planning-blocks.css bytes (no mock). Before = the same
CSS with the @media (max-width: 576px) wrap rules stripped (simulates origin/main).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

EVIDENCE_DIR = Path("/tmp/wa-evidence-9495")
OUT_DIR = EVIDENCE_DIR / "evidence"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BEFORE_URL = "http://127.0.0.1:8765/harness-before.html"
AFTER_URL = "http://127.0.0.1:8765/harness-after.html"

IPHONE = {"width": 393, "height": 852}
DPR = 3

# iOS Safari 17.0 UA
SAFARI_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

OVERFLOW_THRESHOLD_PX = 4  # pixels of ctitle-right past button-right = overflow


def measure(page, label: str) -> dict:
    """Read each choice button's getBoundingClientRect for the wrap audit."""
    data = page.evaluate(
        """() => {
            const buttons = Array.from(document.querySelectorAll('.choice-button'));
            return buttons.map((btn, i) => {
                const btnRect = btn.getBoundingClientRect();
                const ctitle = btn.querySelector('.ctitle');
                const ctitleRect = ctitle ? ctitle.getBoundingClientRect() : null;
                const ctitleStyle = ctitle ? getComputedStyle(ctitle) : null;
                return {
                    i: i,
                    btn_left: btnRect.left,
                    btn_right: btnRect.right,
                    btn_width: btnRect.width,
                    ctitle_left: ctitleRect ? ctitleRect.left : null,
                    ctitle_right: ctitleRect ? ctitleRect.right : null,
                    ctitle_width: ctitleRect ? ctitleRect.width : null,
                    white_space: ctitleStyle ? ctitleStyle.whiteSpace : null,
                    overflow: ctitleStyle ? ctitleStyle.overflow : null,
                    text_overflow: ctitleStyle ? ctitleStyle.textOverflow : null,
                    overflow_wrap: ctitleStyle ? ctitleStyle.overflowWrap : null,
                    word_break: ctitleStyle ? ctitleStyle.wordBreak : null,
                };
            });
        }"""
    )
    overflow_count = 0
    for r in data:
        if r["ctitle_right"] is not None and r["btn_right"] is not None:
            if r["ctitle_right"] > r["btn_right"] + OVERFLOW_THRESHOLD_PX:
                overflow_count += 1
    audit = {
        "label": label,
        "buttons": data,
        "overflow_count": overflow_count,
        "button_count": len(data),
    }
    print(f"  [{label}] {overflow_count}/{len(data)} buttons overflow")
    for r in data:
        flag = "OVERFLOW" if (r["ctitle_right"] and r["btn_right"] and r["ctitle_right"] > r["btn_right"] + OVERFLOW_THRESHOLD_PX) else "ok"
        print(
            f"    btn[{r['i']}]: btn.right={r['btn_right']:.0f} ctitle.right={r['ctitle_right']:.0f} "
            f"white-space={r['white_space']} overflow-wrap={r['overflow_wrap']} word-break={r['word_break']} [{flag}]"
        )
    return audit


def main() -> int:
    audits = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = browser.new_context(
            viewport=IPHONE,
            device_scale_factor=DPR,
            user_agent=SAFARI_UA,
            is_mobile=True,
            has_touch=True,
            color_scheme="light",
        )
        page = ctx.new_page()

        # BEFORE — element-screenshot of the planning block (same crop for both states)
        page.goto(BEFORE_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        before_png = OUT_DIR / "before_planning.png"
        planning = page.query_selector(".planning-block")
        planning.screenshot(path=str(before_png))
        audits.append(measure(page, "BEFORE"))
        print(f"  saved {before_png} ({os.path.getsize(before_png)} bytes)")

        # AFTER — same element crop
        page.goto(AFTER_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(300)
        after_png = OUT_DIR / "after_planning.png"
        planning = page.query_selector(".planning-block")
        planning.screenshot(path=str(after_png))
        audits.append(measure(page, "AFTER"))
        print(f"  saved {after_png} ({os.path.getsize(after_png)} bytes)")

        # Full-page captures (for completeness, not the side-by-side)
        page.goto(BEFORE_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUT_DIR / "before_full.png"), full_page=True)
        page.goto(AFTER_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUT_DIR / "after_full.png"), full_page=True)

        ctx.close()
        browser.close()

    # Save audits
    with open(OUT_DIR / "audit.json", "w") as f:
        json.dump({"viewport": IPHONE, "dpr": DPR, "ua": SAFARI_UA, "audits": audits}, f, indent=2)
    print(f"\n  summary: BEFORE={audits[0]['overflow_count']}/{audits[0]['button_count']} overflow, AFTER={audits[1]['overflow_count']}/{audits[1]['button_count']} overflow")

    # Generate captioned side-by-side MP4 (BEFORE | AFTER) using ffmpeg.
    # Force both frames to identical height (max of the two) before stacking so
    # the side-by-side doesn't get rejected for height mismatch.
    mp4_path = OUT_DIR / "before_after.mp4"
    r = subprocess.run(
        [
            "ffmpeg", "-y",
            "-loop", "1", "-t", "3", "-i", str(OUT_DIR / "before_planning.png"),
            "-loop", "1", "-t", "3", "-i", str(OUT_DIR / "after_planning.png"),
            "-filter_complex",
            "[0:v]scale=540:-2:flags=lanczos,pad=iw:max(ih\\,1620):(ow-iw)/2:(oh-ih)/2:color=white[v0];"
            "[1:v]scale=540:-2:flags=lanczos,pad=iw:max(ih\\,1620):(ow-iw)/2:(oh-ih)/2:color=white[v1];"
            "[v0]drawtext=text='BEFORE origin/main — 5/5 buttons overflow':fontcolor=white:fontsize=18:box=1:boxcolor=red@0.75:boxborderw=14:x=(w-text_w)/2:y=20[v0t];"
            "[v1]drawtext=text='AFTER PR #9495 @ 596fd7e8 — 0/5 overflow':fontcolor=white:fontsize=18:box=1:boxcolor=green@0.75:boxborderw=14:x=(w-text_w)/2:y=20[v1t];"
            "[v0t][v1t]hstack=inputs=2:shortest=1,pad=iw:ih+40:0:0:color=black[stacked];"
            "[stacked]drawtext=text='iPhone 14 Pro 393x852 @ 3x DPR — iOS Safari 17.0 — PR #9495 / 596fd7e8851':fontcolor=white:fontsize=14:box=1:boxcolor=black@0.7:boxborderw=8:x=(w-text_w)/2:y=h-th-12[v]",
            "-map", "[v]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "23",
            "-movflags", "+faststart",
            str(mp4_path),
        ],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"FFMPEG MP4 FAIL: {r.stderr[-2500:]}", file=sys.stderr)
    else:
        print(f"  saved {mp4_path} ({os.path.getsize(mp4_path)} bytes)")

    # GIF (autoplays in PR markdown)
    gif_path = OUT_DIR / "before_after.gif"
    r = subprocess.run(
        [
            "ffmpeg", "-y",
            "-loop", "1", "-t", "3", "-i", str(OUT_DIR / "before_planning.png"),
            "-loop", "1", "-t", "3", "-i", str(OUT_DIR / "after_planning.png"),
            "-filter_complex",
            "[0:v]scale=480:-2:flags=lanczos,pad=iw:max(ih\\,1440):(ow-iw)/2:(oh-ih)/2:color=white[v0];"
            "[1:v]scale=480:-2:flags=lanczos,pad=iw:max(ih\\,1440):(ow-iw)/2:(oh-ih)/2:color=white[v1];"
            "[v0][v1]hstack=inputs=2:shortest=1[stacked];"
            "[stacked]split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-t", "6",
            str(gif_path),
        ],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"GIF FAIL: {r.stderr[-2000:]}", file=sys.stderr)
    else:
        print(f"  saved {gif_path} ({os.path.getsize(gif_path)} bytes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
