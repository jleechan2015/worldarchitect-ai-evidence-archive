"""
Capture fresh BEFORE/AFTER PNG evidence for PR #9104 (avatar circular add btn).

Strategy: the harness at evidence/_harness.html renders BOTH states (BEFORE
= legacy rectangular pill, AFTER = new .game-avatar-add-btn circular placeholder)
in a single page using the real worktree avatar.css. We capture the full page,
then crop the BEFORE panel and AFTER panel into separate per-panel PNGs that
get embedded in the PR body.

The crop coordinates are derived from the panel layout (1320x520 viewport):
panel padding ~ 24px, h2 ~ 22px, panel header-row ~ 110px, total panel height ~ 175px.

To get stable crop coordinates we use element-based screenshots via the
.locator().screenshot() API — that way the crop adapts if the CSS changes.

Outputs:
  evidence/avatar_circular_add_btn/full.png        — full harness page
  evidence/avatar_circular_add_btn/before.png      — cropped BEFORE panel
  evidence/avatar_circular_add_btn/after.png       — cropped AFTER panel
  evidence/avatar_circular_add_btn/capture_meta.json — viewport + computed-style deltas
"""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
HARNESS_URL = (HERE.parent / "_harness.html").as_uri()
OUT_DIR = HERE


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1320, "height": 520},
            device_scale_factor=2,  # 2x DPR for crisp PNGs
        )
        page = await ctx.new_page()
        await page.goto(HARNESS_URL, wait_until="load")
        await page.wait_for_timeout(500)

        # 1. Full-page capture
        full_path = OUT_DIR / "full.png"
        await page.screenshot(path=str(full_path), full_page=True)

        # 2. BEFORE panel — first .panel
        before_panel = page.locator(".panel").nth(0)
        await before_panel.screenshot(path=str(OUT_DIR / "before.png"))

        # 3. AFTER panel — second .panel
        after_panel = page.locator(".panel").nth(1)
        await after_panel.screenshot(path=str(OUT_DIR / "after.png"))

        # 4. getComputedStyle probes on both buttons for the meta
        before_styles = await page.evaluate("""() => {
            const el = document.querySelectorAll('.panel')[0].querySelector('#game-avatar-add-btn');
            const cs = window.getComputedStyle(el);
            return {
                className: el.className,
                widthPx: cs.width,
                heightPx: cs.height,
                borderRadius: cs.borderRadius,
                borderStyle: cs.borderStyle,
                borderWidth: cs.borderWidth,
                borderColor: cs.borderColor,
                boxShadow: cs.boxShadow,
                background: cs.background.substring(0, 80),
            };
        }""")
        after_styles = await page.evaluate("""() => {
            const el = document.querySelectorAll('.panel')[1].querySelector('#game-avatar-add-btn');
            const cs = window.getComputedStyle(el);
            return {
                className: el.className,
                widthPx: cs.width,
                heightPx: cs.height,
                borderRadius: cs.borderRadius,
                borderStyle: cs.borderStyle,
                borderWidth: cs.borderWidth,
                borderColor: cs.borderColor,
                boxShadow: cs.boxShadow,
                background: cs.background.substring(0, 80),
            };
        }""")

        meta = {
            "viewport": {"width": 1320, "height": 520, "dpr": 2},
            "before": before_styles,
            "after": after_styles,
            "harness_url": HARNESS_URL,
        }
        (OUT_DIR / "capture_meta.json").write_text(json.dumps(meta, indent=2))

        print("=== CAPTURE COMPLETE ===")
        print(f"full:    {full_path}")
        print(f"before:  {OUT_DIR / 'before.png'}")
        print(f"after:   {OUT_DIR / 'after.png'}")
        print(f"meta:    {OUT_DIR / 'capture_meta.json'}")
        print()
        print("BEFORE styles:", json.dumps(before_styles, indent=2))
        print()
        print("AFTER styles:", json.dumps(after_styles, indent=2))

        await browser.close()


asyncio.run(main())
