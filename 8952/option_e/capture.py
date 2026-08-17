"""
Capture BEFORE/AFTER screenshots of the planning-block composer (Option E).

What it does:
  1. Build a JSDOM-free static HTML harness that re-renders #composer-choices
     using the REAL parsePlanningBlocks from production app.js.
  2. Render TWO VERSIONS of the same data:
        BEFORE = origin/main's parsePlanningBlocks (the heavy card-style UI)
        AFTER  = this PR's parsePlanningBlocks (numbered compact rows)
     Both produced by the SAME renderer function — only app.js differs.
  3. Save PNGs and report paths + dimensions + row counts.

The harness runs app.js into a `Function` scope (no globals leak), extracts the
two render functions, calls them with the SAME PLANNING_BLOCK fixture, and
writes the generated innerHTML into a host page styled to match the production
composer area (dark theme, #interaction-form with textarea below).
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from playwright.async_api import async_playwright

WT = Path("/Users/jleechan/projects/worktree_ui_planningb")
MAIN_APP = WT  # current branch already has the AFTER; use git to swap for BEFORE
OUT = Path("/tmp/option_e_proof")
OUT.mkdir(parents=True, exist_ok=True)

PLANNING_BLOCK = {
    "thinking": "The campaign template provides a complete character build for Ser Arion.",
    "choices": {
        "finish_cc": {"text": "Finish Character Creation and Start Game",
                      "description": "accept the provided build.",
                      "risk_level": "low"},
        "edit_cc":   {"text": "Edit Character",
                      "description": "modify stats, skills, or equipment.",
                      "risk_level": "low"},
        "custom_class": {"text": "Custom Class",
                         "description": "design a unique class for Arion.",
                         "risk_level": "low"},
    },
}


def extract_functions(app_js_path: Path):
    """Mirror the test harness extraction: slice parsePlanningBlocks* and helpers."""
    src = app_js_path.read_text("utf8")
    names = ["decodeHtmlEntities", "sanitizeHtml", "escapeHtmlAttribute",
             "sanitizeIdentifier", "parsePlanningBlocksJson", "parsePlanningBlocks"]
    parts = []
    for n in names:
        for pat in (f"const {n} = (", f"const {n} = async ("):
            i = src.find(pat)
            if i != -1:
                start = i
                break
        else:
            raise RuntimeError(f"could not find function {n}")
        # find opening brace (the one after `=>`)
        bs = src.find("{", src.find("=>", start))
        depth = 0
        for j in range(bs, len(src)):
            if src[j] == "{":
                depth += 1
            elif src[j] == "}":
                depth -= 1
                if depth == 0:
                    parts.append(src[start:j + 1] + ";")
                    break
    return "\n".join(parts)


HTML_HEAD = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html, body { background: #1f1d2e; color: #e2d9f3; margin: 0; padding: 0;
               font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  #wrap { max-width: 720px; margin: 60px auto; padding: 0 16px; }
  .label { font-size: 12px; color: rgba(226,217,243,0.6); margin: 0 0 6px 4px; }
  .composer-choices { margin-bottom: 0.35rem; }
  .input-group { display: flex; align-items: stretch; position: relative; }
  .input-group textarea {
    flex: 1 1 auto; background: #181623; color: #e2d9f3;
    border: 1px solid rgba(155, 89, 255, 0.55); border-radius: 6px;
    padding: 10px 14px; font: inherit; min-height: 44px; resize: none;
  }
  .input-group .btn-send {
    background: #9b59ff; color: white; border: 0; border-radius: 6px;
    padding: 0 22px; font-weight: 600; margin-left: 8px; cursor: pointer;
  }
  .composer-promoted-note { font-size:11px; opacity:0.6; margin-top:4px; }
</style>
__EXTRA_CSS__
</head>"""

HTML_BODY = r"""<body>
<div id="wrap">
  <div class="label">composer-choices (current turn mirrored here)</div>
  <div id="composer-choices" class="composer-choices"></div>
  <div class="input-group">
    <textarea placeholder="What do you do?" rows="1"></textarea>
    <button type="submit" class="btn-send">Send</button>
  </div>
  <div class="composer-promoted-note" id="diag"></div>
</div>
<script>
  const PLANNING_BLOCK = __PB_JSON__;
  const helpers = `__HELPERS_JS__`;
  const fn = new Function(helpers + "\nreturn parsePlanningBlocks;");
  const parsePlanningBlocks = fn();
  const html = parsePlanningBlocks(PLANNING_BLOCK, { interactiveOnly: true });
  document.getElementById("composer-choices").innerHTML = html;
  const buttons = document.querySelectorAll("#composer-choices .choice-button").length;
  const badges  = document.querySelectorAll("#composer-choices .choice-index").length;
  document.getElementById("diag").textContent =
    buttons + " choice-button / " + badges + " choice-index / " + html.length + "B html";
</script>
</body></html>
"""


def build_page(app_js_path: Path, label: str, extra_css_html: str = ""):
    helpers = extract_functions(app_js_path)
    helpers = helpers.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    head = HTML_HEAD.replace("__EXTRA_CSS__", extra_css_html)
    body = HTML_BODY.replace("__PB_JSON__", json.dumps(PLANNING_BLOCK).replace("</", "<\\/"))
    body = body.replace("__HELPERS_JS__", helpers)
    page = OUT / f"page_{label}.html"
    page.write_text(head + body, "utf8")
    return page


async def capture(page_path: Path, out_png: Path, viewport=(720, 360)):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": viewport[0], "height": viewport[1]},
                                        device_scale_factor=2)
        page = await ctx.new_page()
        await page.goto(f"file://{page_path}", wait_until="domcontentloaded", timeout=10000)
        await page.wait_for_function('document.querySelectorAll("#composer-choices .choice-button").length > 0', timeout=10000)
        await page.wait_for_timeout(200)
        await page.screenshot(path=str(out_png), full_page=False)
        diag = await page.locator("#diag").inner_text()
        button_count = await page.locator("#composer-choices .choice-button").count()
        index_count = await page.locator("#composer-choices .choice-index").count()
        await browser.close()
        return {"diag": diag, "buttons": button_count, "indexes": index_count}


async def main():
    # BEFORE = origin/main app.js (extract from git show). AFTER = current branch.
    import subprocess
    before_app = OUT / "app_BEFORE.js"
    after_app = WT / "mvp_site/frontend_v1/app.js"
    print("[1/3] Writing BEFORE app.js from origin/main...")
    before_src = subprocess.check_output(
        ["git", "-C", str(WT), "show", "origin/main:mvp_site/frontend_v1/app.js"],
        text=True,
    )
    before_app.write_text(before_src, "utf8")
    print(f"  before bytes: {len(before_src)}, after bytes: {after_app.stat().st_size}")

    print("[2/3] Building harness pages...")
    # BEFORE: origin/main app.js + origin/main planning-blocks.css (faithful prod).
    before_css = OUT / "planning-blocks.css.BEFORE"
    if not before_css.exists():
        before_css.write_text(subprocess.check_output(
            ["git", "-C", str(WT), "show", "origin/main:mvp_site/frontend_v1/styles/planning-blocks.css"],
            text=True,
        ), "utf8")
    extra_before = (
        f'<link rel="stylesheet" href="{before_css}">'
        f'<link rel="stylesheet" href="{WT}/mvp_site/frontend_v1/style.css">'
    )
    extra_after = (
        f'<link rel="stylesheet" href="{WT}/mvp_site/frontend_v1/styles/planning-blocks.css">'
        f'<link rel="stylesheet" href="{WT}/mvp_site/frontend_v1/style.css">'
    )
    page_before = build_page(before_app, "before", extra_css_html=extra_before)
    page_after  = build_page(after_app,  "after",  extra_css_html=extra_after)
    print(f"  page BEFORE: {page_before}")
    print(f"  page AFTER : {page_after}")

    print("[3/3] Capturing screenshots...")
    png_before = OUT / "before.png"
    png_after  = OUT / "after.png"
    res_before = await capture(page_before, png_before)
    res_after  = await capture(page_after,  png_after)
    print(f"  BEFORE: {res_before} → {png_before}")
    print(f"  AFTER : {res_after} → {png_after}")

    # Sanity: AFTER should have ≥1 choice-index badge for the numbered rows.
    assert res_after["indexes"] >= 3, f"AFTER missing numbered badges: {res_after}"
    print("\nDONE")


if __name__ == "__main__":
    asyncio.run(main())
