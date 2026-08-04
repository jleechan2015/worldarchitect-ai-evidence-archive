# Evidence Package: pr7439-current-head-bq-path14

## Package Manifest
- **Test Name:** pr7439-current-head-bq-path14
- **Run ID:** `pr7439-current-head-bq-path14-001-20260611T180215`
- **Iteration:** 1
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-06-11T18:02:15.429716+00:00
- **Repository:** worldarchitect.ai
- **Branch:** worktree_bq_loggin
- **Commit:** 64321cced78af9fc253fd8b06f2a533a2598ed70
- **Merge Base:** a556c41022782bfba88464eaef6339f517cba6d4
- **Commits Ahead of Main:** 31

## Git Provenance
```
mvp_site/bq_logging.py                             |  88 +-
 mvp_site/llm_parser.py                             | 117 ++-
 mvp_site/llm_providers/cerebras_provider.py        |  29 +
 mvp_site/llm_providers/gemini_provider.py          | 488 ++++++++---
 .../openai_compatible_provider_core.py             |  69 +-
 mvp_site/llm_providers/openclaw_provider.py        | 104 ++-
 mvp_site/llm_providers/openrouter_provider.py      |  89 ++
 mvp_site/llm_service.py                            | 347 ++++++--
 mvp_site/main.py                                   | 158 +++-
 mvp_site/tests/fake_services.py                    |  24 +-
 mvp_site/tests/test_always_json_mode.py            |  76 +-
 mvp_site/tests/test_bq_logging.py                  |  45 +
 .../test_cerebras_provider_bq_codepath_coverage.py |  97 +++
 mvp_site/tests/test_client_diagnostic_log.py       |  13 +-
 mvp_site/tests/test_debug_info_trimming.py         |  43 +
 mvp_site/tests/test_fake_services_cleanup.py       |  45 +
 mvp_site/tests/test_game_state.py                  |  47 +-
 mvp_site/tests/test_gemini_provider_bq_logging.py  | 369 ++++++++
 .../tests/test_initial_story_cache_hit_bq_guard.py | 247 ++++++
 .../tests/test_level_up_session_architecture.py    |   2 -
 mvp_site/tests/test_llm_service_error_handling.py  |  34 +-
 .../test_openai_compatible_providers_bq_logging.py | 320 +++++++
 mvp_site/tests/test_openai_inference_proxy.py      | 124 +++
 .../tests/test_openai_proxy_nonstream_bq_path8.py  | 103 +++
 .../tests/test_openclaw_provider_streaming_bq.py   | 280 ++++++
 mvp_site/tests/test_streaming_orchestrator.py      | 286 ++++++
 mvp_site/tests/test_world_logic.py                 | 151 +++-
 mvp_site/world_logic.py                            | 154 +++-
 run_local_server.sh                                |  20 +-
 scripts/CLAUDE.md                                  |  16 +
 scripts/archive/verify_bq_logging.sh               | 279 ++++++
 scripts/test_determine_smoke_mode.sh               |   0
 .../test_bq_logging_real_llm_real_user_e2e.py      | 969 +++++++++++++++++++++
 .../test_bq_path14_gameplay_streaming_proxy_e2e.py | 421 +++++++++
 .../test_openrouter_nonstreaming_bq_path10.py      | 187 ++++
 35 files changed, 5510 insertions(+), 331 deletions(-)
```

## Server Runtime
- **Port:** 8049
- **PID:** 61587
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
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/pr7439-current-head-bq-path14/iteration_001/llm_request_responses_1781200848363.jsonl
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/pr7439-current-head-bq-path14/iteration_001/http_request_responses_1781200848363.jsonl
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/pr7439-current-head-bq-path14/iteration_001/gemini_http_request_responses_1781200848363.jsonl
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_bq_loggin/pr7439-current-head-bq-path14/iteration_001/provider_http_request_responses_1781200848363.jsonl

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
