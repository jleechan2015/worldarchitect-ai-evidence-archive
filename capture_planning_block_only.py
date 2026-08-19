#!/usr/bin/env python3
"""Capture before/after screenshots of the risk-tinted planning block.

Renders the planning block in a standalone HTML page that INLINES the real
planning-blocks.css contents (no file:// vs http:// mismatch, no CSS
cross-origin issues with Playwright/Chromium).

Output:
  evidence/before_planning_block.png  (CSS override disables risk-tint)
  evidence/after_planning_block.png   (CSS live, all 4 risk levels resolved)
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path("/tmp/wt-risk-d4")
CSS_FILE = REPO_ROOT / "mvp_site/frontend_v1/styles/planning-blocks.css"
OUT_DIR = REPO_ROOT / "evidence"
LABEL = sys.argv[1] if len(sys.argv) > 1 else "after"

# Read the real CSS so the harness applies the EXACT rule from the repo.
CSS_CONTENTS = CSS_FILE.read_text()

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Risk-tinted planning block — standalone harness</title>
<style>
{css_contents}

body {{
  background: #1a1530;
  color: #f0ecff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  margin: 0;
  padding: 32px;
}}
.harness-banner {{
  background: #2a2545;
  border-left: 3px solid #6a5acd;
  padding: 8px 16px;
  font-size: 12px;
  margin-bottom: 24px;
  color: #b0a8d0;
}}
.planning-block-choices {{
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 720px;
}}
.choice-row {{
  border-radius: 6px;
  padding: 12px 14px;
}}
.choice-head {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.choice-button {{
  background: #2a2545;
  border: 1px solid #3d3560;
  color: #f0ecff;
  padding: 10px 14px;
  border-radius: 4px;
  width: 100%;
  text-align: left;
  font-size: 1rem;
  cursor: pointer;
}}
.ctitle {{ font-size: 1rem; }}

/* BEFORE-only override disables the new risk-tint rules so the screenshot
   shows the pre-merge state. */
{before_override}
</style>
</head>
<body>
  <div class="harness-banner">
    Risk-tinted planning block — standalone harness — label=<strong>{label}</strong><br>
    Real <code>planning-blocks.css</code> inlined below &lt;style&gt; block;
    4 <code>.choice-row[data-risk]</code> rows matching
    <code>parsePlanningBlocksJson</code> emission shape (app.js:2859, 2885).
  </div>

  <div class="planning-block-choices">
    <div class="choice-row" data-risk="safe">
      <div class="choice-head">
        <button class="choice-button choice-select risk-safe" data-choice-id="safe_row">
          <span class="ctitle">Kneel and request a private audience with the queen</span>
        </button>
      </div>
    </div>
    <div class="choice-row" data-risk="low">
      <div class="choice-head">
        <button class="choice-button choice-select risk-low" data-choice-id="low_row">
          <span class="ctitle">Present the royal decree at the morning court</span>
        </button>
      </div>
    </div>
    <div class="choice-row" data-risk="medium">
      <div class="choice-head">
        <button class="choice-button choice-select risk-medium" data-choice-id="medium_row">
          <span class="ctitle">Invoke the saintly revelation from the chapel crypt</span>
        </button>
      </div>
    </div>
    <div class="choice-row" data-risk="high">
      <div class="choice-head">
        <button class="choice-button choice-select risk-high" data-choice-id="high_row">
          <span class="ctitle">Draw the cursed blade and strike the herald down</span>
        </button>
      </div>
    </div>
  </div>
</body>
</html>
"""

BEFORE_OVERRIDE_CSS = """.choice-row[data-risk] {
  border-left: none !important;
  background-color: transparent !important;
}"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    label = LABEL
    before_override = BEFORE_OVERRIDE_CSS if label == "before" else ""
    html = HTML_TEMPLATE.format(
        css_contents=CSS_CONTENTS, label=label, before_override=before_override
    )
    html_path = OUT_DIR / f"_harness_{label}.html"
    html_path.write_text(html)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 760, "height": 540})
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle", timeout=15000)
        page.wait_for_selector(".choice-row[data-risk]", timeout=10000)
        probe = page.evaluate(
            """() => {
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
              const root = getComputedStyle(document.documentElement);
              const tokens = {
                safe: root.getPropertyValue('--risk-safe').trim(),
                risky: root.getPropertyValue('--risk-risky').trim(),
                dangerous: root.getPropertyValue('--risk-dangerous').trim(),
              };
              return { tokens, rows };
            }"""
        )
        png_path = OUT_DIR / f"{label}_planning_block.png"
        page.screenshot(path=str(png_path))
        meta = {
            "label": label,
            "harness": str(html_path),
            "png": str(png_path),
            "css_source": str(CSS_FILE),
            "css_size_bytes": len(CSS_CONTENTS),
            "computed_style_probe": probe,
        }
        (OUT_DIR / f"{label}_planning_block_meta.json").write_text(
            json.dumps(meta, indent=2)
        )
        print(json.dumps(meta, indent=2))
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
