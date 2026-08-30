"""
Capture BEFORE/AFTER screenshots of the in-history planning-block-choices
on iPhone 14 Pro viewport (393x852 @ 3x DPR, iOS Safari 17.0 UA) against
the REAL Flask local server (http://127.0.0.1:8051).

The fixture HTML is at /tmp/wa-9495-localserver/mvp_site/frontend_v1/_local_evidence_9495.html
and links the worktree's actual planning-blocks.css.

Usage:
    /Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-capture.py before
    /Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-capture.py after
"""
import sys
import os
import json
from playwright.sync_api import sync_playwright

LABEL = sys.argv[1] if len(sys.argv) > 1 else "unknown"
OUT_DIR = "/tmp/wa-9495-evidence"
os.makedirs(OUT_DIR, exist_ok=True)

URL = "http://127.0.0.1:8051/frontend_v1/_local_evidence_9495.html"

# iPhone 14 Pro viewport: 393x852 logical, devicePixelRatio=3, iOS Safari 17.0 UA
VIEWPORT = {"width": 393, "height": 852}
DEVICE_SCALE_FACTOR = 3
USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)

CHROME = "/Users/jleechan/Library/Caches/ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROME,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )
        ctx = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=DEVICE_SCALE_FACTOR,
            user_agent=USER_AGENT,
            is_mobile=True,
            has_touch=True,
        )
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(500)  # let layout settle

        # Element-level screenshot of the .planning-block so BEFORE/AFTER frames
        # have identical crop region (required for ffmpeg hstack; full-page
        # heights differ when text wraps vs bleeds, breaking the side-by-side).
        pb = page.locator(".planning-block").first
        pb.wait_for(state="visible", timeout=5000)

        # Compute geometry for verification.
        geom = page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('.choice-button'));
                const planning = document.querySelector('.planning-block-choices');
                const planningRect = planning.getBoundingClientRect();
                const rows = buttons.map(b => {
                    const t = b.querySelector('.ctitle');
                    const bRect = b.getBoundingClientRect();
                    const tRect = t ? t.getBoundingClientRect() : null;
                    return {
                        text: (t ? t.textContent : b.textContent).slice(0, 60) + '…',
                        btn_right: Math.round(bRect.right * 100) / 100,
                        ctitle_right: tRect ? Math.round(tRect.right * 100) / 100 : null,
                        overflow_px: tRect ? Math.round((tRect.right - bRect.right) * 100) / 100 : null,
                        btn_height: Math.round(bRect.height * 100) / 100,
                        ctitle_white_space: t ? getComputedStyle(t).whiteSpace : null,
                        ctitle_overflow_wrap: t ? getComputedStyle(t).overflowWrap : null,
                        btn_overflow_wrap: getComputedStyle(b).overflowWrap,
                        planning_right: Math.round(planningRect.right * 100) / 100,
                        planning_width: Math.round(planningRect.width * 100) / 100,
                    };
                });
                return { rows, viewport_w: window.innerWidth, planning_right: Math.round(planningRect.right * 100) / 100 };
            }
        """)

        # Element screenshot (just the .planning-block element).
        element_path = f"{OUT_DIR}/{LABEL}_planning_block.png"
        pb.screenshot(path=element_path)
        # Also a full-page screenshot for context.
        full_path = f"{OUT_DIR}/{LABEL}_full.png"
        page.screenshot(path=full_path, full_page=True)

        out = {
            "label": LABEL,
            "viewport": VIEWPORT,
            "device_scale_factor": DEVICE_SCALE_FACTOR,
            "user_agent": USER_AGENT,
            "url": URL,
            "geometry": geom,
            "element_screenshot": element_path,
            "full_screenshot": full_path,
        }
        with open(f"{OUT_DIR}/{LABEL}_audit.json", "w") as f:
            json.dump(out, f, indent=2)

        # Pretty print the geometry table to stdout.
        print(f"\n=== {LABEL.upper()} geometry ===")
        print(f"viewport_w: {geom['viewport_w']}")
        print(f"planning-block right edge: {geom['planning_right']}")
        print(f"{'#':<3}{'overflow_px':<13}{'btn_h':<8}{'white-space':<13}{'btn_ow':<10}{'text'}")
        for i, r in enumerate(geom["rows"]):
            ov = r["overflow_px"]
            print(f"{i:<3}{str(ov):<13}{r['btn_height']:<8}{str(r['ctitle_white_space']):<13}{str(r['btn_overflow_wrap']):<10}{r['text']}")

        browser.close()

if __name__ == "__main__":
    main()
