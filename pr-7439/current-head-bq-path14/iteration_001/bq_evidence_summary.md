# BQ Path 14 (gameplay_streaming_proxy) — Evidence Summary

- Marker: `REAL_LLM_BQ_PATH14_1781200900`
- Campaign: `6WfwGRCs7GuO2vYK7KXo`
- User: `test-bq_path14_gameplay_streaming_proxy_e2e-1781200848`
- Model (settings): `gemini-2.5-flash` (actual BQ row model may differ — see row.model)
- Streaming chunks (contract counter): `0`
- Done received: `True`
- BQ rows matching event_type='gameplay_streaming' AND request_json contains marker: `1`

## First BQ row (real-LLM production-driven)

- ingested_at: `2026-06-11 18:01:57`
- event_type: `gameplay_streaming`
- model: `gemini-3-flash-preview`
- agent: `None`
- execution_path: `None`
- path: `gemini_provider.stream`
- prompt_tokens: `100463`
- output_tokens: `1405`
- request_json_len: `406911`
- response_text_len: `4133`
- req_model: `gemini-3-flash-preview`
- req_temperature: `None`
- req_max_output_tokens: `None`
- has_contents (REGEXP_CONTAINS): `true`
- has_marker (REGEXP_CONTAINS): `true`
- request_preview: `'{"model": "gemini-3-flash-preview", "contents": ["parts=[Part(\\n  text=\\"\\"\\"# PROVABLY_FAIR_SEED_OVERRIDE\\nIf the current user_action requires any dice roll, you MUST use Gemini code_execution before'`

## Layer label (per evidence-standards)

- Claim 'gameplay_streaming BQ row has populated request_json': **[Layer 2 real-LLM] + [Layer 2 real-BQ]** (real Gemini POST through /api/campaigns/<id>/interaction/stream, real streamed response, real _bq_log_streaming_interaction BQ write, the test never calls bq_logging.log_llm_payload directly — only the production code path does)
- Claim 'request_json contains model + contents + temperature + max_output_tokens': **[Layer 2 real-BQ]** (verified by JSON_EXTRACT_SCALAR on the BQ row)
- Claim 'response_text populated with real Gemini response': **[Layer 2 real-BQ] + [Layer 2 real-LLM]** (response_text_len > 0, no test-mode marker)
- Claim 'extra.path is production-set (gemini_provider.stream)': **[Layer 2 real-BQ]** (the test never sets the path field)
