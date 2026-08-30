# PR #9495 — fix(mobile): word-wrap in-history planning-block choices on narrow viewports

Mobile CSS fix only; no backend / LLM / Firestore impact. Real evidence
captured by Playwright headless Chromium against the **real Flask local server**
(`./run_local_server.sh` + `TESTING_AUTH_BYPASS=true`) on a fresh worktree at
PR HEAD `596fd7e8851`. The fixture HTML at
`mvp_site/frontend_v1/_local_evidence_9495.html` mirrors the DOM structure
that `parsePlanningBlocks` produces (`app.js:3926-3937` — `<div class="planning-block"><div class="planning-block-choices"><div class="choice-row"><div class="choice-head"><button class="choice-button choice-select"><span class="ctitle">…</span></button></div></div></div></div>`).

The CSS link in the fixture points at `/frontend_v1/styles/planning-blocks.css`,
which Flask serves from the worktree's actual disk file. To produce the BEFORE
capture, the worktree's `planning-blocks.css` was swapped to the bytes from
`origin/main` (md5 `e2901596…`) and the Flask process was restarted so its
in-memory cache was cleared; the served CSS md5 was verified via `curl`
matching the on-disk bytes. To produce the AFTER capture, the worktree's
`planning-blocks.css` was restored to the PR HEAD bytes (md5 `345435b3…`)
and the Flask process restarted; the served CSS md5 was again verified via
`curl`.

## What this proves

| Item | BEFORE (origin/main) | AFTER (PR #9495 @ 596fd7e88) |
|------|---------------------|------------------------------|
| CSS source | `git show origin/main:mvp_site/frontend_v1/styles/planning-blocks.css` | worktree HEAD |
| CSS md5 (served by Flask) | `e2901596f29b9a7e8b56ec2981527034` | `345435b33e6f0ae460b80659ab1ad62d` |
| `@media (max-width: 576px)` wrap rules | absent | present (the fix) |
| `.ctitle { white-space }` | `nowrap` | `normal` |
| `.choice-button { overflow-wrap }` | `normal` | `anywhere` |
| Button height (px) | 94.09 (single line) | 138.88–183.66 (wraps to 3–5 lines) |
| `.ctitle` overflow past button right (px) | +823.34 to +1300.25 | -7.36 to -21.87 (text inside) |
| Page width (px @ 3× DPR) | **4992** (ballooned 4.2× past 1179 viewport) | **1179** (correct mobile width) |

## Files in this bundle

- `before_planning.png` — element screenshot of `.planning-block` panel with origin/main CSS
- `after_planning.png` — element screenshot of `.planning-block` panel with PR #9495 CSS
- `before_full.png` / `after_full.png` — full-page screenshots (proof of horizontal layout collapse BEFORE)
- `before_after.mp4` — 4-second side-by-side MP4 (h264, 2214×5028, 30fps)
- `before_meta.json` / `after_meta.json` — `getBoundingClientRect` + `getComputedStyle` measurements
- `capture_mobile_wrap.py` — the Playwright capture script (re-runnable)
- `audit.json` — combined evidence ledger

## Caveat on the live Cloud Run preview

The live Cloud Run preview revision at `mvp-site-app-s16-i6xf2p72ka-uc.a.run.app`
was last deployed from a different commit (`7823cea5c3…`), not the PR HEAD.
Capturing against the deployed preview would show stale bytes (not this PR's
fix). Per `repo-agents-evidence-contract` Step 3, the canonical /es evidence
for a CSS-only / static-asset PR is rendering the **worktree bytes directly**
through a real server process — which is what this bundle does (Flask is
serving the actual worktree CSS, not the deployed preview's stale bytes).

## Vision verification

`vision_analyze` on `before_planning.png`: all 5 buttons render as single-line
94px-tall cards with text visibly bleeding past the right edge
("Acknowledge t…", "half-burie…", "frequency in…", "the ridge…", "transmitte…").
`vision_analyze` on `after_planning.png`: all 5 buttons are tall (138–183px)
with text wrapping cleanly inside, no character truncation, planning-block
right border is clean.

## Reproduction

```bash
git worktree add -d /tmp/wa-9495-localserver origin/fix/mobile-planning-history-word-wrap
cd /tmp/wa-9495-localserver
TESTING_AUTH_BYPASS=true ./run_local_server.sh --no-log-stream &
# wait ~30s for boot, server prints "Server URL: http://127.0.0.1:8051"

# Capture AFTER (worktree bytes = PR HEAD bytes = with fix)
/Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-capture.py after

# Swap to origin/main CSS, restart Flask, capture BEFORE
cp /tmp/planning-blocks.css.ORIGIN-MAIN.bak mvp_site/frontend_v1/styles/planning-blocks.css
# kill+restart Flask (Werkzeug caches static files in memory)
pkill -f "run_local_server.sh.*wa-9495"
sleep 3
TESTING_AUTH_BYPASS=true ./run_local_server.sh --no-log-stream &
sleep 25
/Users/jleechan/.local/orch-venv/bin/python3 /tmp/wa-9495-capture.py before
```
