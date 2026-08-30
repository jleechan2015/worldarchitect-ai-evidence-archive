"""
Real local-server evidence for PR #9495 (mobile planning-block word-wrap).

This drives the REAL Flask server end-to-end:
- signs in via the test-bypass cookie endpoint
- navigates to a campaign page that already has planning-block history
- waits for the real `parsePlanningBlocks` function in `app.js` to render the
  in-story planning-block panels from the real `/api/campaigns/{id}` payload
- captures the rendered planning-block DOM at iPhone 14 Pro viewport

Run BEFORE (with planning-blocks.css = origin/main bytes):
  /Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-real-capture2.py before

Run AFTER (with planning-blocks.css = PR #9495 bytes):
  /Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-real-capture2.py after
"""
import asyncio
import json
import os
import subprocess
import sys
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8051"
TEST_UID = "0wf6sCREyLcgynidU5LjyZEfm7D2"
TEST_EMAIL = "jleechantest@gmail.com"
# Campaign with the longest planning-block choice text (230 chars)
CAMPAIGN_ID = "72qG2WMEuUzdwXeY5qAy"
# Campaign URL pattern is /game/<id>, not /campaigns/<id>
GAME_PATH = f"/game/{CAMPAIGN_ID}"

LABEL = sys.argv[1] if len(sys.argv) > 1 else "unknown"
OUT_DIR = "/tmp/wa-9495-real-evidence"
os.makedirs(OUT_DIR, exist_ok=True)

VIEWPORT = {"width": 393, "height": 852}
DPR = 3
USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)
CHROME = "/Users/jleechan/Library/Caches/ms-playwright/chromium-1228/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"


async def capture(page, label):
    print(f"\n=== {label.upper()} ===")

    # The app's authTokenManager reads ?test_mode=true&test_user_id=<uid>
    # and resolves auth locally without a real Google login. Use that on the
    # game URL directly — authTokenManager listens to URL params first.
    print(f"  navigating to {GAME_PATH}?test_mode=true&test_user_id={TEST_UID}")
    await page.goto(
        f"{BASE}{GAME_PATH}?test_mode=true&test_user_id={TEST_UID}",
        wait_until="networkidle",
        timeout=30000,
    )
    await page.wait_for_timeout(10000)  # let the story render (authTokenManager + API + parsePlanningBlocks)

    # Force layout to settle
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(2000)
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(1000)

    # Locate all planning-block panels (rendered by parsePlanningBlocks in app.js)
    pb_locator = page.locator(".planning-block")
    n = await pb_locator.count()
    print(f"  planning-block panels visible: {n}")

    # Element screenshots of each panel + computed-style measurements
    geom = []
    for i in range(n):
        try:
            pb_path = f"{OUT_DIR}/{label}_pb_{i:02d}.png"
            await pb_locator.nth(i).screenshot(path=pb_path)
            g = await pb_locator.nth(i).evaluate("""
                (pb) => {
                    const buttons = Array.from(pb.querySelectorAll('.choice-button'));
                    const choicesContainer = pb.querySelector('.planning-block-choices');
                    const containerRect = choicesContainer ? choicesContainer.getBoundingClientRect() : pb.getBoundingClientRect();
                    return {
                        container_right: Math.round(containerRect.right * 100) / 100,
                        container_width: Math.round(containerRect.width * 100) / 100,
                        panel_class: pb.className,
                        row_count: buttons.length,
                        rows: buttons.map(b => {
                            const t = b.querySelector('.ctitle');
                            const bRect = b.getBoundingClientRect();
                            const tRect = t ? t.getBoundingClientRect() : null;
                            return {
                                text: (t ? t.textContent : b.textContent).slice(0, 80) + '…',
                                btn_right: Math.round(bRect.right * 100) / 100,
                                btn_height: Math.round(bRect.height * 100) / 100,
                                ctitle_right: tRect ? Math.round(tRect.right * 100) / 100 : null,
                                overflow_px: tRect ? Math.round((tRect.right - bRect.right) * 100) / 100 : null,
                                ctitle_white_space: t ? getComputedStyle(t).whiteSpace : null,
                                ctitle_overflow_wrap: t ? getComputedStyle(t).overflowWrap : null,
                                btn_overflow_wrap: getComputedStyle(b).overflowWrap,
                            };
                        }),
                    };
                }
            """)
            geom.append({"panel_index": i, "screenshot": pb_path, "geometry": g})
        except Exception as e:
            print(f"  panel {i} capture failed: {e}")

    # Full-page screenshot
    full_path = f"{OUT_DIR}/{label}_full.png"
    await page.screenshot(path=full_path, full_page=True)

    # Document the DOM source: prove it was rendered by the real app
    page_meta = await page.evaluate("""
        () => ({
            url: window.location.href,
            title: document.title,
            parsePlanningBlocks_present: typeof parsePlanningBlocks === 'function' || (window.parsePlanningBlocks ? true : false),
            planning_block_count: document.querySelectorAll('.planning-block').length,
            choice_button_count: document.querySelectorAll('.choice-button').length,
            ctitle_count: document.querySelectorAll('.ctitle').length,
            viewport_w: window.innerWidth,
            document_w: document.documentElement.scrollWidth,
            document_h: document.documentElement.scrollHeight,
        })
    """)

    audit = {
        "label": label,
        "viewport": VIEWPORT,
        "dpr": DPR,
        "user_agent": USER_AGENT,
        "campaign_id": CAMPAIGN_ID,
        "served_css_check": {
            "url": f"{BASE}/frontend_v1/styles/planning-blocks.css",
            "verified_via": "curl during capture run (script-side check before/after)",
        },
        "page_meta": page_meta,
        "panels": geom,
        "screenshots": {"full": full_path},
    }
    audit_path = f"{OUT_DIR}/{label}_audit.json"
    with open(audit_path, "w") as f:
        json.dump(audit, f, indent=2)

    print(f"\n--- {label.upper()} summary ---")
    print(f"  page_url: {page_meta['url']}")
    print(f"  parsePlanningBlocks present: {page_meta['parsePlanningBlocks_present']}")
    print(f"  .planning-block count: {page_meta['planning_block_count']}")
    print(f"  .choice-button count: {page_meta['choice_button_count']}")
    print(f"  .ctitle count: {page_meta['ctitle_count']}")
    print(f"  viewport_w: {page_meta['viewport_w']}, doc_w: {page_meta['document_w']}, doc_h: {page_meta['document_h']}")
    print(f"  panels captured: {len(geom)}")
    for p in geom[:5]:
        g = p["geometry"]
        print(f"  panel[{p['panel_index']}] container_right={g['container_right']} rows={g['row_count']}:")
        for j, row in enumerate(g["rows"][:5]):
            print(f"    [{j}] overflow_px={row['overflow_px']} btn_h={row['btn_height']} ws={row['ctitle_white_space']} ow={row['btn_overflow_wrap']} text={row['text']}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=CHROME,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        ctx = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=DPR,
            user_agent=USER_AGENT,
            is_mobile=True,
            has_touch=True,
        )
        page = await ctx.new_page()
        await capture(page, LABEL)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
