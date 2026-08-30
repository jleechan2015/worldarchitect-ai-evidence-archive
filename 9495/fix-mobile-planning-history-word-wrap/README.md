# PR #9495 — fix(mobile): word-wrap in-history planning-block choices on narrow viewports

Mobile CSS fix only; no backend / LLM / Firestore impact. Real evidence
captured by Playwright headless Chromium against the **actual worktree CSS
bytes** at PR HEAD `596fd7e8851` — `before_planning.png` is rendered against
the same CSS with the new `@media (max-width: 576px)` block stripped (i.e.
the same CSS that exists on `origin/main`).

## What this proves

- `before_planning.png` — 5/5 choice buttons overflow their container by
  476..566 px at iPhone 14 Pro viewport (393×852 @ 3× DPR, iOS Safari 17.0
  UA). Text bleeds visibly past the planning-block's right border.
- `after_planning.png` — 0/5 overflow. The same 5 buttons wrap cleanly
  inside their containers (`ctitle.right ≤ button.right` for every row).
- `before_after.mp4` / `before_after.gif` — side-by-side animation, captioned
  with the BEFORE/AFTER counts and the PR head SHA, framed at 393 px wide.

## Caveat on the live preview

`gcloud run revisions list --service=mvp-site-app-s16` reports the live
revision is at commit `7823cea5c32e360a3f92347d7bacf973446d4493`, NOT the PR
head `596fd7e8851`. The deployed preview is **stale** (a different commit
on the same branch). Per `.claude/skills/repo-agents-evidence-contract`, we
fell back to the source-of-truth: render the worktree CSS bytes directly
through Playwright. The PR's fix lives in `mvp_site/frontend_v1/styles/
planning-blocks.css` lines 695-720 (the `@media (max-width: 576px)`
override). What you see in `after_planning.png` is those exact bytes.

## Reproduce

```bash
# From the worktree at PR HEAD
cd ~/repos/jleechanorg/worldarchitect.ai
git worktree add -d /tmp/wa-evidence-9495 596fd7e8851

# 1. Stand up a static harness on :8765 with BEFORE / AFTER CSS files
mkdir -p /tmp/wa-evidence-9495/styles
cp /tmp/wa-evidence-9495/capture.py /tmp/wa-evidence-9495/

# (See capture_mobile_wrap.py — it builds both harness pages, a tiny
# http.server, runs Playwright Chromium headless iPhone 14 Pro, and writes
# the audit JSON.)

python3 /tmp/wa-evidence-9495/capture_mobile_wrap.py

# Output PNG/MP4/GIF land in /tmp/wa-evidence-9495/evidence/
```

## What the metadata proves

- `overflow_count`: 5 in `before_meta.json` vs 0 in `after_meta.json` — the
  PR's CSS override eliminates every overflow row.
- `ctitle.right - btn.right`: 476..566 px past the right edge in BEFORE;
  ≤0 in AFTER for every row.
- `getComputedStyle` `.ctitle {white-space, overflow-wrap, word-break}` —
  `nowrap / normal / normal` in BEFORE; `normal / anywhere / break-word` in
  AFTER. That matches the PR's override block byte-for-byte.
- Viewport / DPR / UA match the iPhone 14 Pro device profile; static-file
  harness reads the worktree CSS bytes verbatim — no production-server
  dependency, no mock-mode artifact.
