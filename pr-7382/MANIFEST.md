# Evidence Manifest — PR #7382

## Source Campaign

- **Campaign ID:** `mppfHseT9cy44Ywro4oJ` (referenced in PR body)
- **Deployment:** dev (`mvp-site-app-dev`)
- **Audit target:** Dice audit warning rate ~12.5% of recent entries

## Replayed Rolls (`replayed_rolls.jsonl`)

The four records in `replayed_rolls.jsonl` were extracted from
campaign `mppfHseT9cy44Ywro4oJ` story entries demonstrating the
pre-fix LLM behavior (composite notation, parenthetical annotations).

| turn | notation | result | total | purpose | source entry |
|------|----------|--------|-------|---------|--------------|
| 1 | `1d20+12` | 4 | 16 | Persuasion (Marquis's Diplomacy) | `mppfHseT9cy44Ywro4oJ` story entry 1 |
| 1 | `1d12` | 8 | 8 | Bardic Inspiration (Sariel's Support) | `mppfHseT9cy44Ywro4oJ` story entry 1 |
| 2 | `1d20+12` | 3 | 15 | Persuasion (Marquis Status) | `mppfHseT9cy44Ywro4oJ` story entry 2 |
| 2 | `1d12` | 5 | 5 | Bardic Inspiration (Sariel) | `mppfHseT9cy44Ywro4oJ` story entry 2 |

Each composite pre-fix notation (e.g.,
`1d20 + 11 (CHA/PROF/Crown) + 1d10 (Inspiration)`) corresponds to TWO
post-fix `mechanics.rolls[]` entries — one per die term.

## Parser Validation

- **Parser under test:** `mvp_site.action_resolution_utils.parse_dice_notation`
- **Acceptance test cases (single-die terms):**
  - `1d20+12` → die_type=20
  - `1d12` → die_type=12
  - `1d20+11` → die_type=20
  - `2d6kh1+8` → die_type=6 (keep highest)
- **Rejection test cases (composite / inline-annotated):**
  - `1d20 + 11 (PROF/CHA/Crown) + 1d10 (Inspiration)` → die_type=None
  - `1d20+11+1d10` → die_type=None
  - `1d20 + 11 (CHA/PROF/ITEM) + 1d10 (Bardic Inspiration)` → die_type=None

See `mvp_site/tests/test_action_resolution_utils.py::test_parse_dice_notation_*`
for the canonical unit test cases demonstrating both acceptance and
rejection behavior.

## Daily Dice Audit Run

- **Audit log:** `daily_dice_audit.log` (239 lines, attached)
- **Test run log (Green state):** `test_run.log` (124 passing tests, attached)
- **Test run log (Red state):** `test_run_red.log` (3 failed / 1 passed against pre-fix source — TDD baseline)
- **Checksums:** `checksums.sha256` (6 entries, attached)

### Audit log scope clarification

The `daily_dice_audit.log` artifact audits the **full history** of the
twin-copied `EBtkR3tfdLdF9WurDvaw` campaign (549 story entries, 466
dice rolls, 215 entries with dice). The unparseable-notation warnings
at the bottom of the log (lines 203-211) correspond to **historical
pre-fix story entries** (sequence 32, 86, 250, 318, 330, 332, 342,
350, 352, 354, 368, 378, 380, 384) recorded **before** the new prompt
+ schema contract shipped. These pre-existing entries are the audit
tool's *positive control* — they prove the unparseable-notation
detection still fires for the original bug class. They are NOT new
post-fix replay output.

The PR body's "no warnings" claim scopes to the **5 new live replay
turns** at the head of the run (the post-fix prompt contract), not to
the historical pre-fix entries audited at the bottom. See the
"Live Replay Verification" section in the PR body and the
`replayed_rolls.jsonl` file for the new-turn samples.

## TDD Red/Green Provenance

- **PR head SHA:** `751fe872c5dfffe56f5934e96ed3d78d0fc9d6f3` (current HEAD; substantive code change landed in `7bb3559f22`; `292a0e4d` was a no-op Green-Gate trigger; `751fe872` is a provenance/evidence refresh)
- **Pre-fix ref used for Red capture:** `c96eeb784658acd0a84210f43645bd64a779da45` (parent of `de69aca1ff`, the first PR commit that introduced `TestDiceCompositeNotation`)
- **Red capture method:** source files (`mvp_site/prompts/game_state_instruction.md`, `mvp_site/schemas/game_state.schema.json`, `scripts/audit_dice_rolls.py`) reverted to the pre-fix content of `c96eeb7846` while keeping the new test file at PR HEAD.  The 4 `TestDiceCompositeNotation` tests then fail as captured in `test_run_red.log`.  Fix-source files were restored immediately after capture; no source code was modified.
- **Skeptic Gate 6, Gate 8a, Gate 8c evidence** (TDD Red baseline + media SHA caption) — see updated PR body section "Terminal Video Evidence".

## Prompt Schema Update

The prompt contract version for `game_state_instruction_prompt` was
bumped to **1.1.33** with sha256
`d68c7b64ec916663d1974a6dbc1a6a469c5187cf4241d7dd101d718ddef725e0`
to match the rebase-resolved file content (which embeds the new
"one die term per mechanics.rolls[] entry" prompt section).
