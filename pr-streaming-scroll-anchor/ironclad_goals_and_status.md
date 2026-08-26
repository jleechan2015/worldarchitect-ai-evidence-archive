# PR #9358 — Exit criteria and status

Status: **MET** for the scroll claims; one criterion **PARTIAL** by provider
limitation, disclosed rather than papered over.

Captured at `12a85e3ff915837a6464af7d59d033072fde9bb9`.

This replaces the earlier status file, which was invalidated when its run hit
AGY quota exhaustion before any streamed chunk.

## Exit criteria

| # | Criterion | Binary test | Status |
|---|---|---|---|
| 1 | Real local server, no mock mode | server booted with `WORLDAI_DEV_MODE=true`, `TESTING=true` absent | **MET** |
| 2 | Real LLM, not a fixture | AGY CLI `Gemini 3.5 Flash (High)`; launcher fails closed if AGY disabled | **MET** |
| 3 | Real streamed turn reaches completion | SSE `done` observed | **MET** |
| 4 | Position does not move during chunk growth | `scrolltop_range_px == 0` while `scrollheight_growth_px > 0` | **MET** (0.0 px / +678 px) |
| 5 | Position preserved at completion | `after_completion.final_drift_px == 0` and not at bottom | **MET** (0.0 px, 1502 px above bottom) |
| 6 | Detector proven able to see movement | RED probe range > 0 | **MET** (1003 px) |
| 7 | Chunk timing correlation table | joined table with p50/p95/max vs thresholds | **MET** (p95 5.94 ms, max 16.61 ms) |
| 8 | Video with URL + git SHA + captions, first frame not blank | programmatic first-frame check | **MET** |
| 9 | Artifacts published to GitHub with real URLs | `gh release view` returns asset URLs | **MET** |
| 10 | Token-by-token streaming depth | many chunks per turn | **PARTIAL** — AGY yields one completed response per turn; out of reach for this provider |

## Why criterion 10 is PARTIAL, not failed

`AgyModels.generate_content_stream` (`mvp_site/llm_providers/agy_provider.py:1361-1369`)
yields a single completed response — "agy has no streaming". `testing_mcp/CLAUDE.md`
states an AGY-backed run is valid evidence for transport and narrative behavior
but explicitly **not** for token-by-token model streaming.

The scroll claims do not depend on chunk count. What triggers browser scroll
anchoring is DOM growth above the viewport, and the DOM grew 678 px in real
increments while the position held at 0.0 px. Satisfying criterion 10 would
require switching providers, which would change the path under test.

## Honest record of what went wrong first

1. A probe suggested AGY quota had reset. It had not, for the relevant model —
   the probe resolved to Claude Sonnet 4.6 from the default `$HOME`, while the
   server requests the Gemini family from `AGY_RUNTIME_HOME`. All Gemini labels
   were still exhausted. The run was delayed until the real reset.
2. A first completed run appeared to show 281 px of drift. It did not: the
   baseline had been read while the app's smooth-scroll animation was in flight,
   producing a constant offset that was identical across all 278 samples (zero
   variance — the signature of an offset, not movement). The harness was fixed
   and the run repeated, rather than the numbers being reinterpreted after the
   fact. See `methodology.md`.

Both are recorded here because a bundle that hides its false starts is harder to
trust than one that shows them.
