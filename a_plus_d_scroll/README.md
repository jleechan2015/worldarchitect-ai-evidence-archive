# A+D Evidence — `rev-9me4j`

Scroll-driven auto-collapse / auto-expand for `#composer-choices` panel, as shipped in PR #9240 (`evaluateScrollCollapseExpand`, `initComposerScrollGate`, `resetComposerTurnTracking` in `mvp_site/frontend_v1/app.js`). This bundle does not describe the earlier, closed/unmerged PR #9126 design (accumulator + `dDebounceTimer`/`SCROLL_DEBOUNCE_MS`) — see `docs/user_stories/composer_planning_and_header_avatar.md`'s "User Story 4" section for the full history of why the design changed.

## Captioned Video Evidence (Real Campaign Walkthrough)

All video evidence is recorded against the real application running locally via `./vpython mvp_site/main.py serve`, with full normal Quick Start campaign generation (real narrative and strategic planning-block choices). No synthetic HTML, no forced UI states, and no mock submit events are used.

Captions are burned into the video stream via `testing_ui/lib/video_caption.py` (`ffmpeg drawtext`), featuring a persistent top banner anchored to the branch and commit SHA, plus timestamped bottom action labels for each phase:

- **Desktop Walkthrough (1440x900)**: [`a_plus_d_scroll_real_campaign.mp4`](file:///Users/jleechan/projects/worktree_planningb_scroll/evidence/a_plus_d_scroll/a_plus_d_scroll_real_campaign.mp4) (and animated preview [`a_plus_d_scroll_real_campaign.gif`](file:///Users/jleechan/projects/worktree_planningb_scroll/evidence/a_plus_d_scroll/a_plus_d_scroll_real_campaign.gif))
- **Mobile Walkthrough (375x812)**: [`a_plus_d_scroll_real_campaign_mobile.mp4`](file:///Users/jleechan/projects/worktree_planningb_scroll/evidence/a_plus_d_scroll/a_plus_d_scroll_real_campaign_mobile.mp4)

### Walkthrough Phases
1. **Frame 1 (0-3s)**: Initial load at bottom of narrative -> `#composer-choices` is **expanded** (choices visible)
2. **Frame 2 (3-6s)**: User scrolls UP into narrative history (`pctRaw < DEEP_SCROLL_PCT`, 80%) -> auto-**collapsed** (peek strip shows "Tap to expand")
3. **Frame 3 (6-10s)**: User scrolls back DOWN to bottom (`pctRaw >= 80%`) -> auto-**expanded** (choices ready)
4. **Frame 4 (10-15s)**: User clicks Choice 1 button -> real submit -> `isTurnStreaming` lock forces collapsed during narrative streaming -> turn finishes, choices render, lock clears, and it auto-**expands**
5. **Frame 5 (15-18s)**: User scrolls UP into narrative history (`pctRaw < 80%`) -> auto-**collapsed**
6. **Frame 6 (18-22s)**: User taps peek strip manually -> `manualChoicesOverride` latch set -> **expanded** via manual tap override

### Key Captured Screenshots
- `01_initial_expanded_bottom.png` — Real app initial load at bottom: `#composer-choices` is **expanded**
- `02_scrolled_up_collapsed.png` — Scrolled UP into story history (`pctRaw < 80%`), auto-**collapsed**
- `03_scrolled_down_expanded.png` — Scrolled back DOWN to bottom (`pctRaw >= 80%`), auto-**expanded**
- `04_turn_completed_expanded.png` — Turn completes streaming at bottom, **expanded** with next turn choices
- `05_scrolled_up_collapsed.png` — Scrolled UP into history again, auto-**collapsed**
- `06_tap_to_expand.png` — Tapped peek strip manually while scrolled up, **expanded** (manual tap override)

## Reproduction

Run the automated evidence capture script using `./vpython`:
```bash
./vpython testing_ui/capture_a_plus_d_real_evidence.py
```

## Test evidence

```bash
$ NODE_PATH=mvp_site/node_modules node --test mvp_site/frontend_v1/tests/composer_scroll_collapse_expand.test.js mvp_site/frontend_v1/tests/planning_composer_dom.test.js
# tests 21
# suites 0
# pass 21
# fail 0
# cancelled 0
# skipped 0
# todo 0
```

Coverage:
- **Absolute scroll-depth threshold** (`pctRaw = 100 * scrollTop / (scrollHeight - clientHeight)` vs `DEEP_SCROLL_PCT = 80`): expand at `>= 80%`, collapse below it — no accumulator, no direction-delta tracking.
- **`isTurnStreaming` lock**: set on form submit, short-circuits `evaluateScrollCollapseExpand` to force collapsed regardless of scroll position, cleared when the next turn's choices render (not by a timer).
- **`manualChoicesOverride` latch**: set on peek-strip tap, holds the expanded state until scroll naturally crosses back over the threshold, then self-clears.
- **`resetComposerTurnTracking()`**: campaign reset clears `isTurnStreaming`, `manualChoicesOverride`, and all other turn-tracking state together.
- **Placement and DOM integration** (`planning_composer_dom.test.js`): verified with 0 uncaught errors.

## Code references

- `mvp_site/frontend_v1/app.js`: `evaluateScrollCollapseExpand()`, `initComposerScrollGate()`, `resetComposerTurnTracking()`, and the scroll listener on `#story-content`
- `mvp_site/frontend_v1/tests/composer_scroll_collapse_expand.test.js`: unit tests against the real extracted `evaluateScrollCollapseExpand` closure
- `mvp_site/frontend_v1/tests/planning_composer_dom.test.js`: DOM placement tests with complete constants and state declarations
- `testing_ui/capture_a_plus_d_real_evidence.py`: automated Playwright harness capturing SHA-tied real application evidence via `./vpython`

## Bead

- `rev-9me4j` (composer scroll-driven auto-collapse / auto-expand)
