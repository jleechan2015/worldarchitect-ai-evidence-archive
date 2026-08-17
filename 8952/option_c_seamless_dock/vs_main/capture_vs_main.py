#!/usr/bin/env python3
"""Real-server, real-Firestore capture that works against BOTH true origin/main
(no composer exists) and this branch's HEAD (seamless dock composer exists).
Uses a baseline-agnostic wait (any visible .choice-button), then probes whichever
structure is actually present.
"""
import sys, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL, OUT_PNG, LABEL = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
uid = f"pr8952-recap-{LABEL}-{int(time.time())}"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    ctx.add_init_script(f"""
        window._testModeParams = {{enabled:true, userId:{json.dumps(uid)},
                                   email:{json.dumps(uid+'@worldai.test')}}};
        window.testAuthBypass = window._testModeParams;
        window.__ALLOW_TEST_MODE__ = true;""")
    pg = ctx.new_page()
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(f"{BASE_URL}/?test_mode=true&test_user_id={uid}", wait_until="networkidle", timeout=180000)
    pg.wait_for_selector("#dashboard-view.active-view", timeout=180000)
    pg.wait_for_selector("#quick-start-btn", state="visible", timeout=180000)
    pg.click("#quick-start-btn")
    pg.wait_for_url("**/game/*", timeout=180000)
    pg.wait_for_selector(".choice-button:visible", timeout=180000)
    pg.wait_for_timeout(1500)

    probe = pg.evaluate("""() => {
        const stack = document.querySelector('.composer-stack');
        const composerBtns = [...document.querySelectorAll('#composer-choices .choice-button')];
        const storyBtns = [...document.querySelectorAll('#story-content .choice-button')];
        return {
            has_composer_stack: !!stack,
            composer_stack_classes: stack ? stack.className : null,
            composer_choice_count: composerBtns.length,
            composer_choice_ids: composerBtns.map(b => b.getAttribute('data-choice-id')),
            story_choice_count: storyBtns.length,
            user_input_placeholder: document.getElementById('user-input')?.placeholder || null,
            campaign_id: location.pathname.split('/game/')[1] || null,
        };
    }""")
    (OUT_PNG.parent / f"{LABEL}_probe.json").write_text(json.dumps(probe, indent=2))
    print(f"[{LABEL}] {json.dumps(probe)}")
    if errs:
        print(f"[{LABEL}] console errors: {errs}")
    # Scroll the story feed to the bottom so the latest turn's choices/composer
    # (the whole point of this screenshot) are actually in frame.
    pg.evaluate("""() => { const c=document.getElementById('story-content');
                            if (c) c.scrollTop = c.scrollHeight; }""")
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(OUT_PNG))
    print(f"[{LABEL}] screenshot -> {OUT_PNG}")
    b.close()
