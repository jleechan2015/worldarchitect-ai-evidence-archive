# rev-tdl6n repetition-loop ablation — breaker OUT of the path

## Claim under test

Does removing the ASCII box-drawing templates from
`mvp_site/prompts/combat_system_instruction.md` and
`mvp_site/prompts/shared/mechanics_leveling_rewards_body.md` (commit
`2b60f65401`) stop the narrative repetition-loop pathology confirmed live on
dev 2026-08-16/17 (bead rev-tdl6n: `gemini-3-flash-preview` repeated an empty
ASCII box border line ~3,700 times, reaching `MAX_TOKENS` at 49,656 output
tokens / 157,458 chars)?

Per operator directive ("circuit breaker is ok but shuldnt be the only thing
we rely on"), the circuit breaker (`mvp_site/code_execution_circuit_breaker.py`)
and repetition guard (`mvp_site/repetition_guard.py`) MUST NOT be in the path
for this proof — otherwise a residual loop that the breaker aborts early
(e.g. at chunk N) would be indistinguishable from a fix that prevents the
loop from starting at all.

## Method

`ablate_repetition_loop.py` calls the real Gemini API directly via
`google.genai` — it never imports or calls
`gemini_provider.generate_content_stream_sync`, so
`code_execution_circuit_breaker.py` / `repetition_guard.py` are never
invoked. There is no code path by which they could intervene.

- **System instruction**: the REAL production string returned by
  `CombatAgent().build_system_instructions()` (653,491 chars) — the exact
  prompt CombatAgent assembles in production, with the rev-tdl6n fix
  applied. Verified 0 banned double-line box-drawing characters
  (`║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬`) present.
- **Model**: `gemini-3-flash-preview` (the incident model).
- **`code_execution`**: enabled (`types.Tool(code_execution={})`), matching
  production for this model.
- **`max_output_tokens`**: 65536 — the model's real ceiling, same order of
  magnitude as the incident's MAX_TOKENS stop, so a residual loop would not
  be masked by an artificially low cap.
- **User turn**: deliberately adversarial — baits all three formerly-boxed
  templates ("COMBAT VICTORY!", "ENEMY STAT BLOCK", "MILESTONE ACHIEVED!")
  into a single response by asking for enemy stat blocks + combat victory
  summary + quest milestone completion in one turn.
- **Measurement**: `max_consecutive_line_repeat()` — the identical
  line-repeat signal `repetition_guard.detect_pathological_repetition` uses,
  but reimplemented here to report the actual max run length (a count), not
  a boolean threshold trip, so a smaller-scale recurrence of the pathology
  (e.g. 19 repeats instead of 3,700) would be visible rather than hidden.

## Results — 11 independent real-API trials

| trial | finish_reason | text_chars | max_consecutive_line_repeat | code_execution_iterations | elapsed_s |
|---|---|---|---|---|---|
| 1 | STOP | 8,944 | 3 | 1 | 34.82 |
| 2 | STOP | 8,171 | 2 | 2 | 38.90 |
| 3 | STOP | 8,100 | 2 | 2 | 34.50 |
| 4 | STOP | 7,105 | 2 | 2 | 33.66 |
| 5 | STOP | 8,345 | 2 | 2 | 47.07 |
| 6 | STOP | 8,308 | 2 | 1 | 36.89 |
| 7 | STOP | 7,177 | 2 | 2 | 31.24 |
| 8 | STOP | 6,937 | 2 | 2 | 35.44 |
| 9 | STOP | 7,640 | 3 | 2 | 46.55 |
| 10 | STOP | 7,749 | 2 | 1 | 33.54 |
| 11 | STOP | 6,361 | 2 | 1 | 29.16 |

**11/11 trials: clean `FinishReason.STOP`, max consecutive identical line
repeat of 2-3 (normal narrative variance — e.g. two duplicate loot-line
entries), 6,361-8,944 output chars.**

Baseline incident (pre-fix, live 2026-08-16): `FinishReason.MAX_TOKENS`,
~3,700 consecutive repeats, 157,458 chars.

No trial came anywhere close to `repetition_guard.py`'s own trip threshold
(`DEFAULT_MAX_CONSECUTIVE_LINE_REPEATS = 20`) — the worst observed run (3)
is 6.7x below the threshold that would even engage the backstop, with the
breaker never in the call path at all.

## Raw data

`results.jsonl` — one JSON record per trial (model, finish_reason,
text_chars, max_consecutive_line_repeat, code_execution_iterations,
elapsed_s, token counts).

## Reproduce

```bash
export GEMINI_API_KEY=$(gcloud secrets versions access latest \
    --secret=gemini-api-key --project=worldarchitecture-ai)
python3 evidence/rev-tdl6n-repetition-ablation/ablate_repetition_loop.py \
    --reps 11 --out /tmp/rev-tdl6n-ablation.jsonl
```
