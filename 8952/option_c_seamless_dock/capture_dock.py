#!/usr/bin/env python3
"""Real-server, real-Firestore, real-browser capture of the planning-block
composer for PR #8952 (Option C seamless dock). Reuses the exact quick-start
+ TESTING_AUTH_BYPASS pattern from testing_ui/capture_quick_start_evidence_pr8422.py:
Quick Start's Dragon Knight template seeds a REAL .planning-block with ZERO
LLM calls, so this needs no GEMINI_API_KEY.

Usage:
    python3 capture_dock.py <base_url> <out_png_path> <label>
"""
import sys
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = sys.argv[1]
OUT_PNG = Path(sys.argv[2])
LABEL = sys.argv[3]
TEST_USER_ID = f"pr8952-dock-{LABEL}-{int(time.time())}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 900, "height": 700})
    context.add_init_script(
        f"""
        window._testModeParams = {{
            enabled: true,
            userId: {json.dumps(TEST_USER_ID)},
            email: {json.dumps(TEST_USER_ID + "@worldai.test")}
        }};
        window.testAuthBypass = window._testModeParams;
        window.__ALLOW_TEST_MODE__ = true;
        """
    )
    page = context.new_page()
    console_errors = []
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

    url = f"{BASE_URL}/?test_mode=true&test_user_id={TEST_USER_ID}&skip_redirect=true"
    page.goto(url)
    page.wait_for_load_state("networkidle", timeout=180000)
    page.wait_for_selector("#dashboard-view.active-view", timeout=180000)

    btn = page.locator("#quick-start-btn")
    btn.wait_for(state="visible", timeout=180000)
    btn.click()

    page.wait_for_url("**/game/*", timeout=180000)
    page.wait_for_load_state("networkidle", timeout=180000)
    page.wait_for_selector(".planning-block", state="visible", timeout=180000)
    # The composer is the feature under test: give renderComposerChoices time
    # to promote the turn's choices above #user-input.
    page.wait_for_selector("#composer-choices .choice-button", state="visible", timeout=30000)
    page.wait_for_timeout(800)

    # Scroll the composer into view so the screenshot frames choices+textarea together.
    page.locator("#composer-stack, #composer-choices").first.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    campaign_id = page.url.split("/game/")[1].split("?")[0]
    choice_count = page.locator("#composer-choices .choice-button").count()
    has_stack = page.evaluate("() => !!document.getElementById('composer-stack')")
    stack_classes = page.evaluate(
        "() => document.getElementById('composer-stack')?.className || null"
    )
    placeholder = page.evaluate(
        "() => document.getElementById('user-input')?.placeholder || null"
    )
    custom_action_in_composer = page.evaluate(
        "() => !!document.querySelector('#composer-choices .custom-action-button')"
    )

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(OUT_PNG))

    result = {
        "label": LABEL,
        "base_url": BASE_URL,
        "campaign_id": campaign_id,
        "composer_choice_count": choice_count,
        "has_composer_stack": has_stack,
        "composer_stack_classes": stack_classes,
        "user_input_placeholder": placeholder,
        "custom_action_button_in_composer": custom_action_in_composer,
        "console_errors": console_errors,
        "png": str(OUT_PNG),
    }
    print(json.dumps(result, indent=2))
    (OUT_PNG.parent / f"{LABEL}_meta.json").write_text(json.dumps(result, indent=2))

    context.close()
    browser.close()
