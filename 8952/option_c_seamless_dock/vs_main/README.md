# PR #8952 — Option C vs true `origin/main` (the actual diff base)

Found by adversarial review: the sibling `../before.png` compares against commit
`928af5efc9` (Option E, an intermediate state pushed to this branch mid-session while the
operator was still deciding between designs), not against `origin/main`. That comparison is
real and kept for the design-evolution record, but reviewers evaluating this PR's diff need
a comparison against what `main` actually looks like today — that's this directory.

Both frames captured against a real gunicorn server + real Firestore + real headless
Chromium, Quick Start's Dragon Knight template (zero LLM calls needed), then scrolled to
the bottom of the story feed and screenshotted. Script: `capture_vs_main.py`.

- `before_main.png` / `before_main_meta.json` — `origin/main` @ `c4ba6ab063` (verified via
  `git rev-parse HEAD` in a detached checkout immediately before capture).
- `after.png` / `after_meta.json` — this branch @ `946c3017d4`. Two design-fidelity
  corrections landed after the first capture, both caught by the operator comparing the live
  screenshot against the approved Claude Design mock:
  1. `3e73e37398` — dock border used `--accent-color` (gold); every version of the mock used
     `--border-color` / `rgba(168,85,247,.35)` (purple) for it. Gold was only ever the
     pencil-icon/hover accent, and `themes/fantasy.css` states the rule outright: "Gold for
     text/links. Purple for borders, glows, button bg."
  2. `946c3017d4` — the 176px character portrait was mounted inside `.input-group`, i.e.
     *inside* the dock's border. The mock puts only choices + textarea + Send in that single
     bordered surface, with a small portrait on the mode-radio row beneath it. The avatar now
     mounts into `#composer-avatar-slot` at the mock's 34px size.

  Earlier captures at `d7d4b8df83` / `3e73e37398` are superseded.

SHA-256 of both PNGs in `checksums.sha256` — distinct, not the same image shown twice.

## What the probes prove

| | before_main (origin/main) | after (this branch) |
|---|---|---|
| `has_composer_stack` | `false` | `true` |
| `composer_stack_classes` | `null` | `composer-stack composer-stack--has-choices` |
| `composer_choice_count` | `0` | `4` |
| `composer_choice_ids` | `[]` | `confirm_template, customize_character, custom_class_design, finish_character_creation_start_game` — **no `custom_action`**, confirming the C1 fix live in the real DOM, not just in the test suite |
| `story_choice_count` | `5` | `5` |
| `user_input_placeholder` | `"What do you do?"` | `"Or describe your own action…"` |

`story_choice_count` staying `5` on both sides is expected and correct: `main`'s 5 choices
include a real "Custom Action" button (visible in `before_main.png`, inside the purple story
block); this branch's composer shows only the 4 real choices (the free-form option is the
textarea itself), while history — not shown in this screenshot, scrolled past — still keeps
all 5 as real clickable buttons per the "old planning blocks stay clickable" requirement.
