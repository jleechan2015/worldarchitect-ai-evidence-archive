# A+D Evidence — `rev-9me4j`

Scroll-driven auto-collapse / auto-expand for `#composer-choices` panel.
Replaces the R2a scroll-depth trigger removed in `rev-f9kno.15.9`.

## Captioned Video Evidence (Real Campaign Walkthrough)

All video evidence is recorded against the real application running locally via `./vpython mvp_site/main.py serve`, with full normal Quick Start campaign generation (real narrative and strategic planning-block choices). No synthetic HTML, no forced UI states, and no mock submit events are used.

Captions are burned into the video stream via `testing_ui/lib/video_caption.py` (`ffmpeg drawtext`), featuring a persistent top banner anchored to the branch and commit SHA (`feat/composer-scroll-driven-expand@9e2f524bf98a`), plus timestamped bottom action labels for each phase:

- **Desktop Walkthrough (1440x900)**: [`a_plus_d_scroll_real_campaign.mp4`](file:///Users/jleechan/projects/worktree_planningb_scroll/evidence/a_plus_d_scroll/a_plus_d_scroll_real_campaign.mp4) (and animated preview [`a_plus_d_scroll_real_campaign.gif`](file:///Users/jleechan/projects/worktree_planningb_scroll/evidence/a_plus_d_scroll/a_plus_d_scroll_real_campaign.gif))
- **Mobile Walkthrough (375x812)**: [`a_plus_d_scroll_real_campaign_mobile.mp4`](file:///Users/jleechan/projects/worktree_planningb_scroll/evidence/a_plus_d_scroll/a_plus_d_scroll_real_campaign_mobile.mp4)

### Walkthrough Phases
1. **Frame 1 (0-3s)**: Initial load at bottom of narrative -> `#composer-choices` is **expanded** (choices visible)
2. **Frame 2 (3-6s)**: User scrolls UP into narrative history (<80% scroll depth) -> auto-**collapsed** (peek strip shows "Tap to expand")
3. **Frame 3 (6-10s)**: User scrolls back DOWN to bottom (>=80% scroll depth) -> auto-**expanded** (choices ready)
4. **Frame 4 (10-15s)**: User clicks Choice 1 button -> real submit -> collapsed during narrative streaming -> turn finishes at bottom and auto-**expands**
5. **Frame 5 (15-18s)**: User scrolls UP into narrative history (<80%) -> auto-**collapsed**
6. **Frame 6 (18-22s)**: User taps peek strip manually -> **expanded** via manual tap override

### Key Captured Screenshots
- `01_initial_expanded_bottom.png` — Real app initial load at bottom: `#composer-choices` is **expanded**
- `02_scrolled_up_collapsed.png` — Scrolled UP into story history (<80% scroll depth), auto-**collapsed**
- `03_scrolled_down_expanded.png` — Scrolled back DOWN to bottom (>=80%), auto-**expanded**
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
$ ~/.nvm/versions/node/v22.22.0/bin/node --test mvp_site/frontend_v1/tests/composer_scroll_collapse_expand.test.js mvp_site/frontend_v1/tests/planning_composer_dom.test.js
# tests 18
# suites 0
# pass 18
# fail 0
# cancelled 0
# skipped 0
# todo 0
```

Coverage:
- **Exact 2.5s boundary regression test** (Tests 3b, 15, 16): verifies that at exactly `now - lastSubmitForCollapseAt === 2500`, Option D fires (`>= SCROLL_DEBOUNCE_MS`), while at 2499ms it does not.
- **Direction-aware upward accumulator with seeded baseline** (Tests 9, 10, 11, 12, 13, 14): non-tautological verification that the first scroll event after listener attachment does not treat autoscroll-at-rest as a downward wipe, and upward scroll delta accumulates accurately.
- **Debounce timer lifecycle** (Tests 15-19): submit → idle → 2500ms (timer fires D), scroll-within-debounce + idle, manual peek-expand cancellation, and campaign reset cancellation (`resetComposerTurnTracking`).
- **Placement and DOM integration** (10 tests in `planning_composer_dom.test.js`): verified with 0 uncaught errors.

## Code references

- `mvp_site/frontend_v1/app.js`: `evaluateScrollCollapseExpand()`, `dDebounceTimer`, `scheduleDDebounce()`, `resetComposerTurnTracking()`, and scroll listener on `#story-content`
- `mvp_site/frontend_v1/tests/composer_scroll_collapse_expand.test.js`: 20 unit tests with deterministic FakeClock and real DOM extraction
- `mvp_site/frontend_v1/tests/planning_composer_dom.test.js`: 10 DOM placement tests with complete constants and state declarations
- `testing_ui/capture_a_plus_d_real_evidence.py`: automated Playwright harness capturing SHA-tied real application evidence via `./vpython`

## Bead

- `rev-9me4j` (composer scroll-driven auto-collapse / auto-expand)