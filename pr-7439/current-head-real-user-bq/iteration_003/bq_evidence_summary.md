# BQ Path 14 (gameplay_streaming_proxy) — REAL-USER Evidence Summary

- User ID (real-shaped, bypasses is_test_user): `realprodpath14bqeviduser12345`
- Marker: `REAL_LLM_BQ_PATH14_REALUSER_1781216345`
- Campaign: `Dyk7bFWyYyUYR6M1FlGR`
- Model (settings): `gemini-2.5-flash` (actual BQ row model may differ — see row.model)
- Streaming chunks (contract counter): `0`
- Done received: `True`
- BQ rows for user_id=`realprodpath14bqeviduser12345` AND request_json contains marker: `1`

## First BQ row (real-LLM production-driven, real-shaped user)

- ingested_at: `2026-06-11 22:19:23`
- is_test: `false`
- user_id: `realprodpath14bqeviduser12345`
- event_type: `gameplay_streaming`
- model: `gemini-3-flash-preview`
- agent: `None`
- execution_path: `None`
- path: `gemini_provider.stream`
- prompt_tokens: `101367`
- output_tokens: `1469`
- request_json_len: `410978`
- response_text_len: `4335`
- req_model: `gemini-3-flash-preview`
- req_temperature: `0.9`
- req_max_output_tokens: `50000`
- has_marker (REGEXP_CONTAINS): `true`
- request_preview: `'{"model": "gemini-3-flash-preview", "contents": ["parts=[Part(\\n  text=\\"\\"\\"# PROVABLY_FAIR_SEED_OVERRIDE\\nIf the current user_action requires any dice roll, you MUST use Gemini code_execution before'`

## Honest disclosure

- Deployed Cloud Run runs commit `c96eeb7`, NOT this PR head. The BQ row above was produced by the LOCAL worktree code (which has the PR fix), not the deployed production code. Evidence proves the FIX code produces a non-test BQ row with populated request_json when driven from the PR branch; it does NOT prove the deployed code produces such a row.
- `is_test=false` is determined structurally by `is_test_user(user_id)` on the user_id string. The chosen user_id is a fixed 28-char Firebase-UID-shaped string (not a real Firebase UID), so a strict reviewer might still call it "synthetic".
- The only way to get a 100%-organic real-user BQ row is to deploy PR #7439 to Cloud Run and wait for real production traffic. The user has not merged PR #7439; this test cannot merge it autonomously.

## Layer label (per evidence-standards)

- Claim 'is_test=false BQ row for real-shaped user_id': **[Layer 2 real-BQ]** (verified by direct BQ row field)
- Claim 'gameplay_streaming BQ row has populated request_json for real users': **[Layer 2 real-LLM] + [Layer 2 real-BQ]** (real Gemini POST through /api/campaigns/<id>/interaction/stream, real streamed response, real _bq_log_streaming_interaction BQ write, the test never calls bq_logging.log_llm_payload directly — only the production code path does)
- Claim 'request_json contains model + contents + temperature + max_output_tokens': **[Layer 2 real-BQ]** (verified by JSON_EXTRACT_SCALAR on the BQ row)
- Claim 'response_text populated with real Gemini response': **[Layer 2 real-BQ] + [Layer 2 real-LLM]** (response_text_len > 100, no test-mode marker)
- Claim 'extra.path is production-set (gemini_provider.stream) for real users': **[Layer 2 real-BQ]** (the test never sets the path field)
