# PR #9495 — fix(mobile): word-wrap in-history planning-block choices on narrow viewports

Real evidence captured by driving the **real Flask local server** end-to-end:
signing in via the test-bypass URL parameter (`?test_mode=true&test_user_id=…`),
navigating to an existing jleechantest campaign (`/game/72qG2WMEuUzdwXeY5qAy`
— "LANEB n06b s3", a Star Wars turn-based RPG with 7 in-history planning-block
replays rendered by the real `parsePlanningBlocks` function in `app.js`),
waiting for the real app to fetch `/api/campaigns/{id}?story_limit=50` and
render the story entries, then capturing the actual rendered DOM at iPhone 14
Pro viewport (393×852 @ 3× DPR, iOS Safari 17.0 UA, headless Chromium).

The CSS link in the page resolves to `/frontend_v1/styles/planning-blocks.css`,
which Flask serves from the worktree's actual disk file. To produce BEFORE, the
worktree's CSS was swapped to the bytes from `git show origin/main:...`
(md5 `e2901596f29b9a7e8b56ec2981527034`) and the Flask process was restarted
so its Werkzeug static-file cache cleared; the served CSS md5 was verified via
`curl` matching the on-disk bytes. To produce AFTER, the worktree's CSS was
restored to the PR HEAD bytes (md5 `345435b33e6f0ae460b80659ab1ad62d`) and
the Flask process was restarted; the served CSS md5 was again verified via
`curl`.

## What this proves

The DOM was rendered by the **real `parsePlanningBlocks` function** in
`mvp_site/frontend_v1/app.js` (lines 3690–3990), against the **real `/api/campaigns/{id}` JSON response** that the live Flask backend serves from Firestore.
7 `.planning-block` panels × 3–5 `.choice-button` elements each = 35
choice buttons, 28 `.ctitle` spans, real LLM-authored Star Wars choice text
("Shatter the Threshold", "Sow the Seeds of Panic", "Cloud the Collective
Mind", "Dominion of the Void", etc.).

### BEFORE geometry (origin/main bytes, md5 `e2901596…`)

- All 7 panels: `.ctitle { white-space: nowrap; overflow-wrap: normal }`
- Button heights: **26.92 px** (single-line, clipped — text bleeds off)
- Worst overflow in panel 4: `Dominion of the Void` row bleeds **+1282.59 px** past the button's right edge
- Panel 4 average overflow: **+1069 px** past button right edge
- 5/5 buttons in panel 4 overflow the visible planning-block panel

### AFTER geometry (PR #9495 bytes, md5 `345435b3…`)

- All 7 panels: `.ctitle { white-space: normal; overflow-wrap: anywhere }`
- Button heights: **71.7 – 183.66 px** (text wraps to 3–5 lines)
- Worst overflow in panel 4: `Dominion of the Void` row = **-7.56 px** (text inside button)
- Panel 4 average overflow: **-11 px** (text inside button)
- 0/5 buttons in panel 4 overflow

### Full-page comparison

`before_full.png` (4992 px wide with origin/main bytes — page balloons horizontally)
vs `after_full.png` (1179 px wide with PR #9495 bytes — correct mobile width).

## Files in this bundle

- `before_panel4.png` / `after_panel4.png` — element screenshot of the worst-case in-history planning-block panel (5 long Star Wars choice rows)
- `before_panel3.png` / `after_panel3.png` — element screenshot of the second-worst panel
- `before_panel0.png` / `after_panel0.png` — element screenshot of the character-creation panel
- `before_full.png` / `after_full.png` — full-page screenshots (proof of horizontal layout collapse BEFORE)
- `before_after.mp4` — 12-second side-by-side MP4 (3 panels × 4s each, BEFORE|AFTER per panel)
- `before_meta.json` / `after_meta.json` — `getBoundingClientRect` + `getComputedStyle` measurements for all 7 panels × 3-5 rows each
- `capture_real_app.py` — the Playwright capture script (re-runnable; drives the real app end-to-end)
- `audit.json` — combined evidence ledger

## Reproduction

```bash
git worktree add -d /tmp/wa-9495-localserver origin/fix/mobile-planning-history-word-wrap
cd /tmp/wa-9495-localserver
TESTING_AUTH_BYPASS=true ./run_local_server.sh --no-log-stream &
# wait ~30s for boot, server prints "Server URL: http://127.0.0.1:8051"

# Capture AFTER (worktree bytes = PR HEAD bytes = with fix)
/Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-real-capture2.py after

# Swap to origin/main CSS, restart Flask, capture BEFORE
git show origin/main:mvp_site/frontend_v1/styles/planning-blocks.css \
  > mvp_site/frontend_v1/styles/planning-blocks.css
pkill -f "run_local_server.sh.*wa-9495"
sleep 3
TESTING_AUTH_BYPASS=true ./run_local_server.sh --no-log-stream &
sleep 25
/Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-real-capture2.py before
```

The script targets campaign `72qG2WMEuUzdwXeY5qAy` (jleechantest's "LANEB n06b
s3") which has 7 in-history planning-block replays with real LLM-authored text.
Any other campaign with non-empty `game_states/current_state/planning_block`
history can be substituted by editing `CAMPAIGN_ID` in the script.

## Caveat on the live Cloud Run preview

The live Cloud Run preview revision at `mvp-site-app-s16-i6xf2p72ka-uc.a.run.app`
was last deployed from `7823cea5c3…` ≠ PR HEAD `596fd7e8851`. Capturing against
the deployed preview would show stale bytes (not this PR's fix). For a CSS-only
/ static-asset PR, the canonical /es evidence is rendering the **worktree bytes
directly** through a real server process — which is what this bundle does
(Flask is serving the actual worktree CSS, not the deployed preview's stale
bytes, and the DOM comes from the real `parsePlanningBlocks` function, not a
hand-written fixture).
