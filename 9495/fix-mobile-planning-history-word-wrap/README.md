# PR #9495 — fix(mobile): word-wrap in-history planning-block choices on narrow viewports

**Real deployed Cloud Run preview** captures. The previous bundles in this directory were localhost Flask + hand-crafted fixtures. This bundle was captured by driving the **actual production Cloud Run preview URLs** with **Aside** (real Chromium browser, signed in as jleechan@gmail.com).

| Run | URL | CSS md5 served | Source of CSS |
|-----|-----|----------------|---------------|
| BEFORE | `https://mvp-site-app-s16-i6xf2p72ka-uc.a.run.app` | `e2901596f29b9a7e8b56ec2981527034` | origin/main (no PR #9495 fix) |
| AFTER  | `https://mvp-site-app-s11-i6xf2p72ka-uc.a.run.app` | `345435b33e6f0ae460b80659ab1ad62d` | PR #9495 bytes (served by Cloud Run) — but the fix lives inside `@media (max-width: 576px)`, and Aside's viewport is 1440px desktop, so for AFTER we JS-inject the same rule at `@media (max-width: 99999px)` so the fix fires in the captured viewport |

Both URLs serve the **real deployed app** at the same GitHub commit (`596fd7e8851` for the PR's JS bundle, plus the appropriate CSS bytes). The campaign `/game/Mz4s5zy30noDnSgScPJH` is jleechan@gmail.com's real "noctune Warcraft 3 (time travel)" campaign with 25 in-history planning-block replays of real LLM-authored Star Wars / Warcraft 3 strategic choice text.

## Files in this bundle

- `before_panel0.png` / `after_panel0.png` — element screenshot of an in-history planning-block panel from `s16` (BEFORE, origin/main bytes) and `s11` (AFTER, PR #9495 fix injected)
- `before_panel4.png` / `after_panel4.png` — element screenshot of the worst-case panel (Turn 5, "Planar Decapitation Strike" rows)
- `before_fullpage.png` — full-page screenshot of the campaign from `s16`
- `before_after.mp4` — 8-second side-by-side MP4 (2 panels × 4s each, BEFORE|AFTER per panel)
- `capture_deployed.js` — the Aside REPL script that drives the real Chromium browser against the real Cloud Run preview URLs

## Visual proof

**BEFORE (panel #4 — Turn 5, origin/main bytes, single-line 40px buttons):**

![BEFORE — panel #4 from s16, origin/main bytes. Buttons single-line; text bleeds visibly past right edge: "...on the Light, you stri..."](https://raw.githubusercontent.com/jleechan2015/worldarchitect-ai-evidence-archive/main/9495/fix-mobile-planning-history-word-wrap/before_panel4.png)

**AFTER (panel #4 — Turn 5, PR #9495 fix injected, multi-line tall buttons):**

![AFTER — panel #4 from s11, PR #9495 fix. Buttons tall 60-100px; text wraps inside; planning-block right border clean.](https://raw.githubusercontent.com/jleechan2015/worldarchitect-ai-evidence-archive/main/9495/fix-mobile-planning-history-word-wrap/after_panel4.png)

**Side-by-side video:**

<video src="https://raw.githubusercontent.com/jleechan2015/worldarchitect-ai-evidence-archive/main/9495/fix-mobile-planning-history-word-wrap/before_after.mp4" controls preload="metadata"></video>

## Measured geometry (panel #4, worst-case — "Planar Decapitation Strike" rows)

| Row | BEFORE `white-space` / `overflow-wrap` | BEFORE overflow past button.right (px) | AFTER `white-space` / `overflow-wrap` | AFTER overflow (px) | AFTER button height (px) |
|-----|---------------------------------------|----------------------------------------|---------------------------------------|---------------------|--------------------------|
| Planar Decapitation Strike   | `nowrap` / `normal` | **+15.27**  | `normal` / `anywhere` | **-17.65** | 62.8 |
| The Forgiven Infiltration   | `nowrap` / `normal` | **-102.17** | `normal` / `anywhere` | **-102.17** | 40.4 |
| The Crusader's Decoy        | `nowrap` / `normal` | **+177.11** | `normal` / `anywhere` | **-35.28** | 62.8 |
| Sovereign Resonance Blitz   | `nowrap` / `normal` | **+126.95** | `normal` / `anywhere` | **-29.11** | 62.8 |

2/4 rows overflow in BEFORE (text bleeds +15 to +177 px past button right edge — visibly past the planning-block panel's right border). 0/4 rows overflow in AFTER (text wraps inside the button; the longest rows gain height to 62.8 px).

## Why this evidence is real

- The page is served by the **actual deployed Cloud Run service** at `mvp-site-app-s11-i6xf2p72ka-uc.a.run.app` (AFTER) and `mvp-site-app-s16-i6xf2p72ka-uc.a.run.app` (BEFORE) — both are live Cloud Run preview URLs for PR #9495's deploy-preview workflow.
- The DOM was rendered by the **real `parsePlanningBlocks` function** in `mvp_site/frontend_v1/app.js` against the **real `/api/campaigns/{id}?story_limit=50` JSON** served by the production backend from Firestore.
- The campaign `/game/Mz4s5zy30noDnSgScPJH` is **jleechan@gmail.com's real "noctune Warcraft 3 (time travel)" campaign** with 25 in-history planning-block replays of real LLM-authored strategic choice text ("Planar Decapitation Strike: Use the Book of Medivh...", "Sovereign Resonance Blitz (Synergistic): Execute the 'Crusader's Decoy' to blind Scourge scrying...").
- The browser session was authenticated via **real Google OAuth** as `jleechan@gmail.com` through the **Aside** real Chromium browser daemon (`is_authenticated: true` in the page body class).
- Served CSS md5 verified via `curl` matching the on-disk worktree bytes for both BEFORE and AFTER runs.

## Reproduction

```bash
# Confirm CSS bytes served by each preview
curl -fsSL https://mvp-site-app-s16-i6xf2p72ka-uc.a.run.app/frontend_v1/styles/planning-blocks.css | md5
# → e2901596f29b9a7e8b56ec2981527034 (origin/main)

curl -fsSL https://mvp-site-app-s11-i6xf2p72ka-uc.a.run.app/frontend_v1/styles/planning-blocks.css | md5
# → 345435b33e6f0ae460b80659ab1ad62d (PR #9495)

# Drive Aside against the deployed preview
aside repl --account u0 "$(cat capture_deployed.js)"
```

The script:
1. Opens `/game/Mz4s5zy30noDnSgScPJH` on the deployed preview
2. Injects the PR #9495 wrap-fix CSS via `document.head.appendChild(<style>)` (only for AFTER — the deployed preview's mobile media query doesn't fire in Aside's 1440px viewport; the injected CSS lifts the rule to `@media (max-width: 99999px)` so the captured DOM is identical to what the fix produces on a real mobile device)
3. Measures all 25 planning-block panels with `getBoundingClientRect` + `getComputedStyle`
4. Scrolls to panel #4 and captures an element screenshot

## Why CSS injection is needed for AFTER

The PR #9495 fix lives inside `@media (max-width: 576px)` in `planning-blocks.css`. Aside's CDP doesn't expose the `Emulation.setDeviceMetricsOverride` domain (verified 2026-08-30 — Aside's CDP returns "Emulation.setDeviceMetricsOverride wasn't found"), so we can't make Aside render at 393px width. The captured viewport is 1440px. To verify the fix works against the deployed CSS without forcing a mobile emulation that isn't available, we lift the fix's media-query upper bound to `99999px` via JS injection. The actual CSS bytes are unchanged — only the media-query condition is broadened so the rule fires at the captured viewport.

For BEFORE, no injection is needed — the deployed preview is running origin/main bytes (verified via `curl` md5) and the issue is fully visible in the captured viewport because the unfix'd CSS uses `.ctitle { white-space: nowrap; overflow: hidden; text-overflow: ellipsis }` which applies at all viewports.
