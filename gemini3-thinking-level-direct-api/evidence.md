# Direct Gemini API Per-Model Thinking Level Evidence (PR #9167)

- **Git HEAD**: `c6d0730fa10b2ad764f36d82945cb4c3f7606c1c`
- **Date**: 2026-08-21T17:50:25.512509+00:00
- **Target Models**: `gemini-3.6-flash`, `gemini-3.7-flash`, `gemini-3-flash-preview` (control)
- **Evidence Class**: Layer 2 (real `https://generativelanguage.googleapis.com/...` direct SDK calls)

## Executive Summary

12/12 live direct API calls passed with matching observed wire configuration.
Each cell records the observed outgoing HTTP body and is failed closed when transport capture is unavailable, malformed, or differs from the expected thinking configuration.

## Claim -> Artifact Map

| Claim | Verification Layer | Artifact | Key Proof Field |
|---|---|---|---|
| `gemini-3.6-flash` thinking level low on direct JSON API | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cell 1) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.matches_expected: true` |
| `gemini-3.6-flash` thinking level low on direct Streaming API | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cell 2) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.matches_expected: true` |
| `gemini-3.6-flash` code execution suppresses thinking | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cells 3, 4) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.observed_thinking_levels: [null]` |
| `gemini-3.7-flash` thinking level low on direct JSON API | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cell 5) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.matches_expected: true` |
| `gemini-3.7-flash` thinking level low on direct Streaming API | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cell 6) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.matches_expected: true` |
| `gemini-3.7-flash` code execution suppresses thinking | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cells 7, 8) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.observed_thinking_levels: [null]` |
| Control unmapped model untouched | Layer 2 real-LLM | `thinking_level_probe.jsonl` (cells 9-12) + `gemini_wire_capture.jsonl` | `success: true`, `wire_observation.observed_thinking_levels: [null]` |

## What This Evidence Does NOT Prove

1. Does NOT prove AGY CLI behavior (AGY provider thinking config was handled separately in PR #9166).
2. Does NOT prove unmapped models (e.g. `gemini-2.5-pro`) use thinking config.
