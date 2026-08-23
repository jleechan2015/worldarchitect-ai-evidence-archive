"""Capture BEFORE/AFTER Step 2 wizard screenshots.

Reads a SHA string env var so the same script can stamp both captures.
"""
import asyncio
import os
import sys

from playwright.async_api import async_playwright


async def capture(base: str, label: str, out_path: str):
    print(f"[{label}] capture -> {out_path}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1400, "height": 1100})
        page = await ctx.new_page()
        page.on("console", lambda msg: print(f"  [{label}][{msg.type}] {msg.text[:140]}"))
        page.on("pageerror", lambda err: print(f"  [{label}][error] {err}"))

        await page.goto(
            f"{base}/new-campaign?test_mode=true&test_user_id=visualproof",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        await page.wait_for_timeout(3000)

        # Pick the "Custom" campaign type card so step 1 fields show
        try:
            await page.wait_for_selector(
                'div.campaign-type-card[data-type="custom"]', timeout=10000
            )
            await page.click('div.campaign-type-card[data-type="custom"]')
            await page.wait_for_timeout(800)
        except Exception as e:
            print(f"  [{label}] type-card not found: {e}")

        # Fill in a few inputs so the preview cards have content to display
        try:
            await page.fill("#wizard-campaign-title", "Astarion ascended")
            await page.fill("#wizard-character-input", "Astarion")
            await page.fill("#wizard-setting-input", "Baldur's Gate 3, the Shadow Curse")
        except Exception as e:
            print(f"  [{label}] fill skipped: {e}")
        await page.wait_for_timeout(800)

        # Click Next to advance to Step 2
        for attempt in range(3):
            try:
                btn = page.locator("button:has-text('Next')").first
                if await btn.is_visible(timeout=2000):
                    await btn.click()
                    await page.wait_for_timeout(900)
                else:
                    break
            except Exception:
                break
        await page.wait_for_timeout(1500)

        # Scroll to bottom so the Campaign Summary card is fully visible.
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(700)

        # Capture full page
        await page.screenshot(path=out_path, full_page=True)

        # DOM probe: list every preview item
        rows = await page.locator(".preview-item").count()
        print(f"  [{label}] preview-item count = {rows}")
        for i in range(rows):
            try:
                txt = await page.locator(".preview-item").nth(i).inner_text()
            except Exception:
                txt = "(unreadable)"
            print(f"  [{label}] row {i}: {txt[:120]}")
        # Step indicator
        try:
            step_text = await page.locator(".step-counter").first.inner_text()
            print(f"  [{label}] step-counter: {step_text}")
        except Exception as e:
            print(f"  [{label}] step-counter read err: {e}")

        await browser.close()


if __name__ == "__main__":
    label = sys.argv[1]
    out_path = sys.argv[2]
    base = os.environ.get("BASE_URL", "http://127.0.0.1:8081")
    asyncio.run(capture(base, label, out_path))
