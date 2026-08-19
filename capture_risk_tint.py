#!/usr/bin/env python3
"""Capture before/after screenshots of the risk-tinted planning block (Direction 4).

Strategy:
  1. Boot Playwright against the real local dev server with the
     X-Test-Bypass-Auth init script (matches the testing_ui/capture_quick_start_evidence*
     pattern that has shipped this kind of screenshot for the last several PRs).
  2. Click Quick Start so the dashboard issues POST /api/campaigns/quick-start
     and the Dragon Knight template seeds a REAL .planning-block with ZERO LLM
     calls. Default risk_level is "low" (yellow). For visual proof of all four
     levels we inject a 4-row synthetic planning block via page.evaluate so the
     screenshot shows safe/risky/risky/dangerous side by side.
  3. Capture before.png — with the risk-tint CSS temporarily disabled
     (display:none on the rule's envelope plus an inline override style block).
  4. Capture after.png — with the CSS restored.

Run:
    venv/bin/python evidence/capture_risk_tint.py before
    venv/bin/python evidence/capture_risk_tint.py after
"""
import os
import sys
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("RISK_TINT_BASE_URL", "http://localhost:8190")
LABEL = sys.argv[1] if len(sys.argv) > 1 else "screenshot"
OUT_PNG = Path(f"/tmp/wt-risk-d4/evidence/{LABEL}.png")
TEST_USER_ID = f"risk-tint-direction-4-{int(time.time())}"

# Synthetic planning block matching the real parsePlanningBlocksJson output
# shape, with one row per risk_level so the screenshot frames all four cues
# (safe + low + medium + high) side by side.
INJECTED_HTML = """
<div class="choice-row" data-risk="safe">
  <div class="choice-head">
    <button class="choice-button choice-select risk-safe" data-choice-id="safe_row">
      <span class="ctitle">Kneel and request a private audience</span>
    </button>
  </div>
</div>
<div class="choice-row" data-risk="low">
  <div class="choice-head">
    <button class="choice-button choice-select risk-low" data-choice-id="low_row">
      <span class="ctitle">Present the royal decree</span>
    </button>
  </div>
</div>
<div class="choice-row" data-risk="medium">
  <div class="choice-head">
    <button class="choice-button choice-select risk-medium" data-choice-id="medium_row">
      <span class="ctitle">Invoke the saintly revelation</span>
    </button>
  </div>
</div>
<div class="choice-row" data-risk="high">
  <div class="choice-head">
    <button class="choice-button choice-select risk-high" data-choice-id="high_row">
      <span class="ctitle">Draw the cursed blade and strike the herald</span>
    </button>
  </div>
</div>
"""

# CSS to disable the risk-tint rules so the "before" screenshot shows the
# pre-merge state. Loaded via page.add_style_tag inside the script.
BEFORE_OVERRIDE_CSS = """
.choice-row[data-risk] {
  border-left: none !important;
  background-color: transparent !important;
}
"""


def add_test_mode_init(context):
    # The dev server's CORS config (main.py:356) only whitelists
    # X-Test-Bypass-Auth as a preflight-allowed header. Sending
    # X-Test-User-ID / X-Test-User-Email blocks the OPTIONS preflight,
    # which causes the API call to 401 even though TESTING_AUTH_BYPASS=*** is set.
    # Send ONLY X-Test-Bypass-Auth; user identity is read from the
    # test_user_id query param (server-side, main.py:1629).
    context.set_extra_http_headers({"X-Test-Bypass-Auth": "true"})
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


def probe_planning_block(page):
    """Computed-style probe for the spec's verification step.

    Returns the resolved border-left, background-color, and gap tokens for
    every data-risk row plus the :root token values. The contract test pins
    the byte-level source; this probe verifies the LIVE browser actually
    applies the rule after CSS load.
    """
    return page.evaluate(
        """
        () => {
          const root = getComputedStyle(document.documentElement);
          const tokens = {
            safe: root.getPropertyValue('--risk-safe').trim(),
            risky: root.getPropertyValue('--risk-risky').trim(),
            dangerous: root.getPropertyValue('--risk-dangerous').trim(),
          };
          const risks = ['safe', 'low', 'medium', 'high'];
          const rows = {};
          for (const r of risks) {
            const el = document.querySelector(`.choice-row[data-risk="${r}"]`);
            if (!el) { rows[r] = null; continue; }
            const cs = getComputedStyle(el);
            rows[r] = {
              borderLeftWidth: cs.borderLeftWidth,
              borderLeftColor: cs.borderLeftColor,
              backgroundColor: cs.backgroundColor,
            };
          }
          return { tokens, rows };
        }
        """
    )


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 900, "height": 700})
        add_test_mode_init(context)
        page = context.new_page()
        console_errors = []
        page.on(
            "console",
            lambda m: console_errors.append(m.text) if m.type == "error" else None,
        )

        url = f"{BASE_URL}/?test_mode=true&test_user_id={TEST_USER_ID}&skip_redirect=true"
        page.goto(url)
        page.wait_for_load_state("networkidle", timeout=180000)
        page.wait_for_selector("#dashboard-view.active-view", timeout=180000)

        # Quick Start -> /game/<id> with planning block seeded.
        page.locator("#quick-start-btn").wait_for(state="visible", timeout=180000)
        page.locator("#quick-start-btn").click()
        page.wait_for_url("**/game/*", timeout=180000)
        page.wait_for_load_state("networkidle", timeout=180000)
        page.wait_for_selector(".planning-block", timeout=180000)

        # Inject the 4-row synthetic planning block so the screenshot
        # shows safe + low + medium + high side by side. The new rows are
        # appended after the seeded choices so the composer is still
        # interactive.
        page.evaluate(
            """
            (html) => {
              const choices = document.querySelector('.planning-block-choices');
              if (!choices) return 'no .planning-block-choices';
              const tmp = document.createElement('div');
              tmp.innerHTML = html;
              while (tmp.firstChild) choices.appendChild(tmp.firstChild);
              return 'ok';
            }
            """,
            INJECTED_HTML,
        )

        # For the "before" label, override the new CSS rules so the rows
        # render untinted. For "after", the file-system CSS already does
        # the work.
        if LABEL == "before":
            page.add_style_tag(content=BEFORE_OVERRIDE_CSS)
        elif LABEL != "after":
            print(
                f"unknown LABEL={LABEL!r}; expected 'before' or 'after'",
                file=sys.stderr,
            )
            sys.exit(2)

        # Wait for layout to settle after the style tag insertion.
        page.wait_for_timeout(300)

        # Find the row container that actually has our injected rows. The
        # planning-block-choices container may be hidden inside the
        # composer's docked stack which sits BELOW the story history; we
        # locate the NEWEST .choice-row[data-risk] (last in DOM order) and
        # scroll THAT into view so the screenshot frames all four rows.
        try:
            rows = page.locator(".choice-row[data-risk]")
            count = rows.count()
            if count > 0:
                rows.nth(count - 1).scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(200)
        except Exception as exc:  # noqa: BLE001
            print(f"scroll fallback: {exc}", file=sys.stderr)

        # Computed-style probe for the spec.
        probe = probe_planning_block(page)

        # Capture the screenshot.
        OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(OUT_PNG))

        meta = {
            "label": LABEL,
            "base_url": BASE_URL,
            "test_user_id": TEST_USER_ID,
            "png": str(OUT_PNG),
            "computed_style_probe": probe,
            "console_errors": console_errors,
        }
        print(json.dumps(meta, indent=2))
        (OUT_PNG.parent / f"{LABEL}_meta.json").write_text(json.dumps(meta, indent=2))

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
