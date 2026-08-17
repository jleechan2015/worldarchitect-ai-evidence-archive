# PR #8952 — Option C seamless dock + C1 (real server / real Firestore / real browser)

Real evidence, not a static render: `capture_dock.py` boots the real Flask app
(`mvp_site/main.py serve`, `TESTING_AUTH_BYPASS=true`,
`GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json`), drives headless
Playwright through the real Quick Start button, and screenshots the real
`/game/<id>` page. Quick Start's Dragon Knight template seeds a real
`.planning_block` in real Firestore with **zero LLM calls** (pre-cached
template), so no `GEMINI_API_KEY` is needed for this capture — the same
technique `testing_ui/capture_quick_start_evidence_pr8422.py` uses.

- `before.png` / `before_meta.json` — commit `928af5efc9` (Option E, numbered
  compact rows), the state a different agent had pushed to this branch while
  the operator was still deciding between designs. Server on `:9242`, run
  from a throwaway `git worktree add --detach 928af5efc9`.
- `after.png` / `after_meta.json` — commit `d7d4b8df83` (Option C + C1, with
  the backend-`custom_action` follow-up fix below), server on `:9244`, run
  from this checkout.

## Follow-up fix reflected in this capture

The first version of `after.png` (captured at `90c1f92ebb`) still showed a
"Custom Action: decide whatever you want to do" row in the composer, because
the Dragon Knight template supplies its own **backend** `custom_action` choice
and the original C1 change only suppressed the **frontend's own synthesized**
`__custom_action__` fallback — a different code path. `agy-coder-pr8952-capture`
caught this by reading that exact capture (adversarial review, not the test
suite) and landed the fix in `d7d4b8df83`. This README's `after.png` was
re-captured against that corrected HEAD: **4** choice rows now, no
`custom_action` button anywhere in the composer, `composer_choice_count`
dropped from 5 to 4.

## What the metadata proves

- `composer_stack_classes`: `null` in before (no `#composer-stack` element
  existed yet) vs `"composer-stack composer-stack--has-choices"` in after —
  proves the new wrapper renders and its has-choices class toggles on.
- `user_input_placeholder`: `"What do you do?"` (unchanged/default) in before
  vs `"Or describe your own action…"` in after — proves
  `syncComposerPlaceholder()` fires for real, in a real browser, against a
  real rendered turn.
- `custom_action_button_in_composer`: `false` in both, but now for the SAME
  reason in both — no `custom_action`/`__custom_action__` choice-id ever
  reaches the composer, backend-supplied or frontend-synthesized.
- `composer_choice_count`: `5` (before, Option E: 4 real choices + the
  template's own custom_action row, still shown) vs `4` (after: the same 4
  real choices, backend custom_action correctly suppressed).
- `console_errors`: `[]` in both — no JS errors introduced.

## Visual diff (read the PNGs, don't take this on faith)

- before.png: choices float with no shared border; each row carries a small
  purple numbered badge (1..5, the 5th being the un-suppressed Custom Action
  row); avatar and textarea have a visible gap (predates `bd74c7e26f`'s
  alignment fix, which landed after this Option E commit).
- after.png: **4** choices + avatar + textarea share ONE rounded bordered
  surface; hairline dividers between rows; no numbers, no Custom Action row;
  pencil-glyph gutter inside the textarea; Send sits flush against the
  textarea's right edge.

## Reproduce

```bash
GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json TESTING_AUTH_BYPASS=true \
  PORT=9241 PYTHONPATH=. venv/bin/python mvp_site/main.py serve &
venv/bin/python evidence/8952/option_c_seamless_dock/capture_dock.py \
  http://localhost:9241 /tmp/after.png after
```
