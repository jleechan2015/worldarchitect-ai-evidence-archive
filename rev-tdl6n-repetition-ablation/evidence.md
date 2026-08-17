# Evidence — rev-tdl6n / rev-ac8vk (PR #8985)

**Original capture head SHA**: `15192a1eda65d241d10057f81ab71a88d261e60b`
**Post-/advice-fixup head SHA**: `1199380237a1bfc1aab08900b9aab49e89333543`
**Branch**: `fix/gemini-code-exec-safety-rev-ac8vk-tdl6n`
**Date**: 2026-08-17

## Addendum — post-/advice-fixup re-verification

An independent `/advice` second-opinion review (see PR discussion) found two
untouched divider-bordered templates in `combat_system_instruction.md`
(Action Economy State Tracking, and the higher-risk MANDATORY-every-round
Combat Status Display with a centered, padding-requiring "ROUND 3" line)
plus an empirically-too-tight `CODE_EXECUTION_WALL_CLOCK_DEADLINE_SECONDS`
(45.0s — below 2 of this bundle's own 11 clean trials at 46.55s/47.07s).
Both fixed at head `1199380237a1bfc1aab08900b9aab49e89333543` (see that
commit message for full detail). Per evidence-standards staleness rules,
a production change re-stales prior evidence — re-verified with 5 fresh
real-API trials against the updated prompt:

`results_postfix_confirmation.jsonl` — 5/5 `FinishReason.STOP`,
`max_consecutive_line_repeat` = 2 in all 5, 6,043-7,887 chars. Consistent
with the original 11-trial result. `CombatAgent().build_system_instructions()`
re-scanned at the new head: 0 banned box-drawing chars, 653,433 chars
(vs 653,491 pre-fixup — the two divider blocks shrank slightly, no other
change). Local gate scripts and the 251-test scoped pytest suite re-run
clean at the new head (see methodology.md).

## Claims under test

1. **rev-tdl6n (root cause, prompt layer)**: removing the ASCII box-drawing
   templates from `mvp_site/prompts/combat_system_instruction.md` and
   `mvp_site/prompts/shared/mechanics_leveling_rewards_body.md` stops the
   narrative repetition-loop pathology confirmed live on dev (2026-08-16/17):
   `gemini-3-flash-preview` under `CombatAgent` repeated an empty ASCII box
   border line ~3,700 times, reaching `FinishReason.MAX_TOKENS` at 49,656
   output tokens / 157,458 chars.
2. **rev-ac8vk (backstop, defense in depth)**: `code_execution_circuit_breaker.py`
   (iteration/wall-clock/tool-token/char bounds) and `repetition_guard.py`
   (20-consecutive-identical-line detector) exist as a deterministic
   backstop, wired into `gemini_provider.generate_content_stream_sync`'s
   streaming loop, so a *future* vendor regression degrades predictably
   instead of relying solely on Gemini's own ceiling.

**Operator directive (verbatim)**: "circuit breaker is ok but shuldnt be the
only thing we rely on." The breaker stays as defense in depth, but claim 1
must be proven with the breaker **out of the path**, so it cannot mask a
residual, smaller-scale recurrence of the same defect.

## Claim → Artifact map

| Claim | Artifact | Key field | Layer |
|---|---|---|---|
| Prompt fix eliminates the repetition loop, breaker fully out of the call path | `results.jsonl` (11 rows) + `README.md` | `max_consecutive_line_repeat` (2-3 across all 11 trials, vs ~3,700 baseline), `finish_reason` (`FinishReason.STOP` in 11/11, vs `MAX_TOKENS` baseline) | Layer 2 real-LLM |
| Real production system instruction (post-fix) contains 0 banned double-line box-drawing chars | `ablate_repetition_loop.py` stdout (`Banned double-line box-drawing chars present: NONE`), reproduced inline below | direct char-set scan of `CombatAgent().build_system_instructions()` output (653,491 chars) | Layer 1 (static content check on real production assembly code) |
| Real local server + real Gemini call through the actual MCP/CombatAgent code path also shows 0 banned box-drawing chars | `server_e2e_supplementary/raw_mcp_responses.jsonl` (7 real MCP calls) | scanned every response body for `║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬` — 0 found | Layer 2 real-LLM, real server |
| Backstop bounds exist and trip correctly on synthetic input (unit-level, in-scope for this PR's own new code) | `mvp_site/tests/test_code_execution_circuit_breaker.py`, `test_code_execution_circuit_breakers.py`, `test_repetition_guard.py`, `test_gemini_provider_circuit_breaker_wiring.py` — all pass locally | pytest exit 0 | Layer 1 unit (acceptable: backstop-bound logic is a pure function, not an LLM-behavior claim, and is <100 delta lines on its own) |
| Real local gate scripts pass at this HEAD | see `methodology.md` | exit 0 for all three | N/A (static/CI mirror) |

## Primary result: 11 real-API trials, breaker never in the call path

`ablate_repetition_loop.py` calls `google.genai` directly — it does **not**
import or call `gemini_provider.generate_content_stream_sync`, so
`code_execution_circuit_breaker.py` and `repetition_guard.py` are never
invoked; there is no code path by which they could intervene. System
instruction is the real string `CombatAgent().build_system_instructions()`
returns in production. Model is `gemini-3-flash-preview` (the incident
model), `code_execution` enabled, `max_output_tokens=65536` (the model's real
ceiling — high enough that a residual loop would hit `MAX_TOKENS`, not be
truncated early).

| trial | finish_reason | text_chars | max_consecutive_line_repeat |
|---|---|---|---|
| 1-11 | STOP (11/11) | 6,361-8,944 | 2-3 (11/11) |

Full per-trial data: `results.jsonl`. Full method and rationale: `README.md`.

Baseline (pre-fix, live incident): `FinishReason.MAX_TOKENS`, ~3,700 repeats,
157,458 chars.

## Supplementary: real local server + real Gemini through the production MCP path

`server_e2e_supplementary/` — `testing_mcp/test_combat_agent_real_e2e.py` run
against a real local server (`./vpython mvp_site/main.py serve`,
`WORLDAI_DEV_MODE=true`, real `GOOGLE_APPLICATION_CREDENTIALS`, real
`GEMINI_API_KEY`) at head SHA `15192a1eda6`. 7 real MCP `tools/call` requests
captured in `raw_mcp_responses.jsonl` (campaign creation, 4x `process_action`,
`get_campaign_state`, quick-combat execution). `combat_agent_e2e_test.json`
carries full provenance (`git_head`, `merge_base`, `diff_stat_vs_main`,
server PID/cmdline/env).

**What this run proves**: the real server boots on this branch, real MCP
calls reach `world_logic`/`CombatAgent`-eligible code with the updated
prompt files in place, `combat_state.in_combat` flips `true` on the second
turn, and every captured response body is free of the banned box-drawing
character set.

**What this run does NOT prove**: it did not reach a full combat-victory /
milestone narrative — the test's scripted character was still in the
"CHARACTER CREATION - Review" gate when combat markers appeared, a
pre-existing test/gameplay interaction gap unrelated to this PR (the seeded
character in `test_combat_agent_real_e2e.py` is a freeform `create_campaign`
character, not a pre-finalized template; the test's own strict-mode
pass/fail criteria — `combat_summary` populated, XP awarded — are about the
combat-rewards pipeline, not the box-drawing prohibition). It is included as
supplementary real-server-liveness evidence, not as the primary proof of
claim 1 — the primary proof is the 11-trial ablation above, which uses the
byte-identical real production system instruction and deliberately baits the
exact three formerly-boxed templates into firing.

## Local gate scripts (see methodology.md for exact commands and output)

- `scripts/validate_prompt_tool_contracts.py` — PASS
- `scripts/check_function_loc_ratchet.py` — PASS
- `scripts/check_schema_coverage.py --fail-under 100` — PASS (168/168, 100.0%)

## What this evidence does NOT prove

- It does not prove the pathology can **never** recur under any input —
  it proves the specific incident scenario (and a deliberately harder,
  multi-template-baiting variant of it) is clean across 11 independent real
  calls plus 7 more through the real server. `repetition_guard.py` remains
  as a backstop for inputs this evidence didn't cover.
- It does not re-validate every other CombatAgent behavior (dice rolls,
  XP math, loot tables) — those are unchanged by this PR and out of scope.
- The supplementary server run did not exercise a full multi-round combat to
  natural victory (see limitation above); it exercises the real request path
  up to the point combat state activates.
- CI shard results for this exact HEAD were still queued/running on the
  self-hosted fleet at evidence-capture time; this bundle documents local
  gate-script mirrors per the operator's backlog directive, not a
  substitute for the CI checks completing.
