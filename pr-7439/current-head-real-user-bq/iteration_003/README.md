# Evidence Package: bq_path14_real_user_e2e

## Package Manifest
- **Test Name:** bq_path14_real_user_e2e
- **Run ID:** `bq_path14_real_user_e2e-003-20260611T221945`
- **Iteration:** 3
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-06-11T22:19:45.575908+00:00
- **Repository:** worldarchitect.ai
- **Branch:** worktree_bq_loggin
- **Commit:** e8180f690f07d6ed71893925a3a12bed9381f45a
- **Merge Base:** a556c41022782bfba88464eaef6339f517cba6d4
- **Commits Ahead of Main:** 57

## Git Provenance
```
.github/workflows/mcp-smoke-tests.yml              |   1 -
 .github/workflows/test.yml                         |   2 -
 .../current-head-bq-path14/iteration_001/README.md |  88 ++
 .../iteration_001/README.md.sha256                 |   1 +
 .../iteration_001/bq_evidence_summary.md           |  35 +
 .../iteration_001/bq_query_result.json             |  24 +
 .../campaigns/6WfwGRCs7GuO2vYK7KXo.json            | 289 ++++++
 .../campaigns/6WfwGRCs7GuO2vYK7KXo.json.sha256     |   1 +
 ...ath14 Gameplay Streaming Proxy E2E_6WfwGRCs.txt |  42 +
 ...ay Streaming Proxy E2E_6WfwGRCs_game_state.json | 213 +++++
 .../iteration_001/evidence.md                      |  65 ++
 .../iteration_001/evidence.md.sha256               |   1 +
 .../gemini_http_request_responses.jsonl            |   4 +
 .../gemini_http_request_responses.jsonl.sha256     |   1 +
 ...mini_http_request_responses_1781200848363.jsonl |   4 +
 .../iteration_001/http_request_responses.jsonl     |  66 ++
 .../http_request_responses.jsonl.sha256            |   1 +
 .../http_request_responses_1781200848363.jsonl     |  66 ++
 .../iteration_001/llm_request_responses.jsonl      |   2 +
 .../llm_request_responses.jsonl.sha256             |   1 +
 .../llm_request_responses_1781200848363.jsonl      |   2 +
 .../iteration_001/metadata.json                    | 116 +++
 .../iteration_001/metadata.json.sha256             |   1 +
 .../iteration_001/methodology.md                   |  38 +
 .../iteration_001/methodology.md.sha256            |   1 +
 .../current-head-bq-path14/iteration_001/notes.md  |  31 +
 .../iteration_001/notes.md.sha256                  |   1 +
 .../pr7439-current-head-bq-path14.cast             |   2 +
 ...ash-preview_path14_gameplay_streaming_proxy.txt |  93 ++
 ...view_path14_gameplay_streaming_proxy.txt.sha256 |   1 +
 .../raw_unknown_model_evidence_signature_guard.txt |   1 +
 ...known_model_evidence_signature_guard.txt.sha256 |   1 +
 .../replay_fixture_source_manifest.json            |  66 ++
 .../iteration_001/request_responses.jsonl          |   2 +
 .../iteration_001/request_responses.jsonl.sha256   |   1 +
 .../current-head-bq-path14/iteration_001/run.json  |  49 ++
 .../iteration_001/run.json.sha256                  |   1 +
 .../iteration_001/scenario_results_checkpoint.json |   1 +
 .../scenario_results_checkpoint.json.sha256        |   1 +
 .../iteration_001/streaming_evidence.json          |  27 +
 .../iteration_001/streaming_evidence.json.sha256   |   1 +
 .../iteration_001/test_console_output.txt          |  86 ++
 .../iteration_001/test_console_output.txt.sha256   |   1 +
 .../current-head-bq-path14/iteration_003/README.md | 162 ++++
 .../iteration_003/README.md.sha256                 |   1 +
 .../iteration_003/bq_evidence_summary.md           |  35 +
 .../bq_path14_gameplay_streaming_proxy_e2e.cast    |   2 +
 .../iteration_003/bq_query_result.json             |  24 +
 ...ath14 Gameplay Streaming Proxy E2E_zXDOGgAL.txt |  45 +
 ...ay Streaming Proxy E2E_zXDOGgAL_game_state.json | 196 +++++
 .../campaigns/zXDOGgALmEJOUaGl96m8.json            | 251 ++++++
 .../campaigns/zXDOGgALmEJOUaGl96m8.json.sha256     |   1 +
 .../iteration_003/evidence.md                      |  65 ++
 .../iteration_003/evidence.md.sha256               |   1 +
 .../gemini_http_request_responses.jsonl            |   4 +
 .../gemini_http_request_responses.jsonl.sha256     |   1 +
 ...mini_http_request_responses_1781209204025.jsonl |   4 +
 .../iteration_003/http_request_responses.jsonl     |  62 ++
 .../http_request_responses.jsonl.sha256            |   1 +
 .../http_request_responses_1781209204025.jsonl     |  62 ++
 .../iteration_003/llm_request_responses.jsonl      |   2 +
 .../llm_request_responses.jsonl.sha256             |   1 +
 .../llm_request_responses_1781209204025.jsonl      |   2 +
 .../iteration_003/metadata.json                    | 103 +++
 .../iteration_003/metadata.json.sha256             |   1 +
 .../iteration_003/methodology.md                   |  38 +
 .../iteration_003/methodology.md.sha256            |   1 +
 .../current-head-bq-path14/iteration_003/notes.md  |  31 +
 .../iteration_003/notes.md.sha256                  |   1 +
 ...ash-preview_path14_gameplay_streaming_proxy.txt |  84 ++
 ...view_path14_gameplay_streaming_proxy.txt.sha256 |   1 +
 .../raw_unknown_model_evidence_signature_guard.txt |   1 +
 ...known_model_evidence_signature_guard.txt.sha256 |   1 +
 .../replay_fixture_source_manifest.json            |  66 ++
 .../iteration_003/request_responses.jsonl          |   2 +
 .../iteration_003/request_responses.jsonl.sha256   |   1 +
 .../current-head-bq-path14/iteration_003/run.json  |  49 ++
 .../iteration_003/run.json.sha256                  |   1 +
 .../iteration_003/scenario_results_checkpoint.json |   1 +
 .../scenario_results_checkpoint.json.sha256        |   1 +
 .../iteration_003/streaming_evidence.json          |  27 +
 .../iteration_003/streaming_evidence.json.sha256   |   1 +
 .../iteration_003/test_console_output.txt          |  87 ++
 .../iteration_003/test_console_output.txt.sha256   |   1 +
 .../pr-7439/supplemental_iteration_002/README.md   |  40 +
 .../supplemental_iteration_002/README.md.sha256    |   1 +
 .../supplemental_iteration_002/checksums.sha256    |  26 +
 .../result_intermediate.json                       |  24 +
 .../result_intermediate.json.sha256                |   1 +
 .../result_intermediate.json                       |  24 +
 .../result_intermediate.json.sha256                |   1 +
 .../supplemental_iteration_002/provenance.env      |   7 +
 .../provenance.env.sha256                          |   1 +
 .../queries/red_prior_gap_query.sql                |  14 +
 .../queries/red_prior_gap_query.sql.sha256         |   1 +
 .../queries/red_prior_gap_query_result.json        |   1 +
 .../queries/red_prior_gap_query_result.json.sha256 |   1 +
 .../openai_compatible_providers_bq_pytest.txt      |   4 +
 ...penai_compatible_providers_bq_pytest.txt.sha256 |   1 +
 .../test_outputs/openai_proxy_path8_pytest.txt     |  12 +
 .../openai_proxy_path8_pytest.txt.sha256           |   1 +
 .../test_outputs/openclaw_streaming_bq_pytest.txt  |   4 +
 .../openclaw_streaming_bq_pytest.txt.sha256        |   1 +
 .../openrouter_path10_real_bq_adc_attempt.exitcode |   1 +
 ...uter_path10_real_bq_adc_attempt.exitcode.sha256 |   1 +
 .../openrouter_path10_real_bq_adc_attempt.txt      |  17 +
 ...penrouter_path10_real_bq_adc_attempt.txt.sha256 |   1 +
 ...path10_real_bq_service_account_attempt.exitcode |   1 +
 ...real_bq_service_account_attempt.exitcode.sha256 |   1 +
 ...uter_path10_real_bq_service_account_attempt.txt |  46 +
 ...th10_real_bq_service_account_attempt.txt.sha256 |   1 +
 mvp_site/bq_logging.py                             |  88 +-
 mvp_site/llm_parser.py                             | 117 ++-
 mvp_site/llm_providers/cerebras_provider.py        | 125 ++-
 mvp_site/llm_providers/gemini_provider.py          | 541 +++++++++---
 .../openai_compatible_provider_core.py             |  69 +-
 mvp_site/llm_providers/openclaw_provider.py        | 104 ++-
 mvp_site/llm_providers/openrouter_provider.py      | 191 +++-
 mvp_site/llm_service.py                            | 418 +++++++--
 mvp_site/main.py                                   | 158 +++-
 mvp_site/tests/fake_services.py                    |  24 +-
 mvp_site/tests/test_always_json_mode.py            |  76 +-
 mvp_site/tests/test_bq_logging.py                  |  45 +
 .../tests/test_cerebras_native_tools_bq_path19.py  | 202 +++++
 .../test_cerebras_provider_bq_codepath_coverage.py |  97 +++
 .../tests/test_cerebras_tool_requests_bq_path16.py | 164 ++++
 mvp_site/tests/test_client_diagnostic_log.py       |  13 +-
 mvp_site/tests/test_debug_info_trimming.py         |  46 +-
 mvp_site/tests/test_fake_services_cleanup.py       |  45 +
 mvp_site/tests/test_game_state.py                  |  47 +-
 mvp_site/tests/test_gemini_provider_bq_logging.py  | 440 ++++++++++
 .../test_gemini_provider_code_execution_bq.py      | 160 ++++
 ...est_gemini_provider_code_execution_bq_reallm.py | 136 +++
 .../tests/test_initial_story_cache_hit_bq_guard.py | 247 ++++++
 .../tests/test_level_up_session_architecture.py    |   2 -
 mvp_site/tests/test_llm_service_error_handling.py  |  34 +-
 ..._llm_service_log_raw_llm_data_nonstream_path.py | 228 +++++
 ...est_llm_service_log_raw_llm_data_stream_path.py | 228 +++++
 .../test_openai_compatible_providers_bq_logging.py | 331 +++++++
 mvp_site/tests/test_openai_inference_proxy.py      | 124 +++
 .../tests/test_openai_proxy_nonstream_bq_path8.py  | 103 +++
 .../tests/test_openclaw_provider_streaming_bq.py   | 280 ++++++
 .../tests/test_openclaw_tool_requests_bq_path17.py | 227 +++++
 .../test_openrouter_native_tools_bq_path18.py      | 389 +++++++++
 mvp_site/tests/test_provider_tool_requests.py      | 140 +++
 mvp_site/tests/test_streaming_orchestrator.py      | 286 ++++++
 mvp_site/tests/test_world_logic.py                 | 235 ++++-
 mvp_site/world_logic.py                            | 155 +++-
 run_local_server.sh                                |  20 +-
 scripts/CLAUDE.md                                  |  16 +
 scripts/archive/verify_bq_logging.sh               | 279 ++++++
 .../evidence_openrouter_nonstreaming_bq_path10.py  | 190 ++++
 scripts/test_determine_smoke_mode.sh               |   0
 .../test_bq_logging_real_llm_real_user_e2e.py      | 969 +++++++++++++++++++++
 .../test_bq_path14_gameplay_streaming_proxy_e2e.py | 421 +++++++++
 .../streaming/test_bq_path14_real_user_e2e.py      | 504 +++++++++++
 156 files changed, 11411 insertions(+), 389 deletions(-)
```

## Server Runtime
- **Port:** 8049
- **PID:** 58903
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:8049 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 1000 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** None
- **MOCK_SERVICES_MODE:** false
- **GOOGLE_APPLICATION_CREDENTIALS:** None
- **WORLDAI_GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **FIRESTORE_EMULATOR_HOST:** None
- **PORT:** 8049
- **FIREBASE_PROJECT_ID:** worldarchitecture-ai
- **GEMINI_API_KEY:** [SET - 39 chars]
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/bq_path14_real_user_e2e/iteration_003/llm_request_responses_1781216293840.jsonl
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/bq_path14_real_user_e2e/iteration_003/http_request_responses_1781216293840.jsonl
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/bq_path14_real_user_e2e/iteration_003/gemini_http_request_responses_1781216293840.jsonl
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/bq_path14_real_user_e2e/iteration_003/provider_http_request_responses_1781216293840.jsonl

## Files in This Bundle
- `README.md` - This manifest
- `methodology.md` - Testing methodology
- `evidence.md` - Evidence summary with Claim→Artifact Map and Coverage Matrix
- `notes.md` - Additional context, TODOs, follow-ups
- `metadata.json` - Machine-readable metadata
- `assertions.json` - Strict before/after parity assertions (if present)
- `run.json` - Test results
    - `streaming_evidence.json` - Normalized streaming evidence summary
    - `request_responses.jsonl` - Raw MCP request/response payloads (if present)
    - `llm_request_responses.jsonl` - Raw LLM request/response payloads (if present)
    - `http_request_responses.jsonl` - Raw local-server HTTP request/response payloads (if present)
    - `gemini_http_request_responses.jsonl` - Raw Gemini transport HTTP traces (if present)
    - `artifacts/` - Additional evidence files
