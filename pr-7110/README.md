# Evidence Package: event_cascade_real_e2e

## Package Manifest
- **Test Name:** event_cascade_real_e2e
- **Run ID:** `event_cascade_real_e2e-054-20260528T011852`
- **Iteration:** 54
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-05-28T01:18:52.018055+00:00
- **Repository:** worldarchitect.ai
- **Branch:** investigate-reaper-stale-living-world
- **Commit:** 125a12c2891747edcab8c4f1ab796dfa465f7aec
- **Merge Base:** b247c9297a0475f7030f8a008ce2add5c0c54683
- **Commits Ahead of Main:** 133

## Git Provenance
```
.beads/issues.jsonl                                |   9 +-
 .github/scripts/skeptic-evaluate.sh                |  43 +-
 .github/workflows/green-gate.yml                   | 619 ++++++++++++++-------
 .github/workflows/test-deployment.yml              |  22 +-
 evidence/pr-7110/README.md                         | 135 +++++
 evidence/pr-7110/README.md.sha256                  |   1 +
 .../Event Cascade Test - GodMode_q1fJIBcx.txt      | 179 ++++++
 ...Cascade Test - GodMode_q1fJIBcx_game_state.json | 205 +++++++
 .../Event Cascade Test - RegularTurn_LebCoush.txt  | 193 +++++++
 ...ade Test - RegularTurn_LebCoush_game_state.json | 228 ++++++++
 .../pr-7110/campaigns/LebCoushqOhoGurZGbUu.json    | 277 +++++++++
 .../campaigns/LebCoushqOhoGurZGbUu.json.sha256     |   1 +
 .../pr-7110/campaigns/q1fJIBcxagf0ZiIHBST8.json    | 248 +++++++++
 .../campaigns/q1fJIBcxagf0ZiIHBST8.json.sha256     |   1 +
 evidence/pr-7110/event_cascade_real_e2e.cast       |   2 +
 evidence/pr-7110/evidence.md                       |  88 +++
 evidence/pr-7110/evidence.md.sha256                |   1 +
 .../pr-7110/gemini_http_request_responses.jsonl    |  16 +
 .../gemini_http_request_responses.jsonl.sha256     |   1 +
 ...mini_http_request_responses_1779924084806.jsonl |  16 +
 evidence/pr-7110/http_request_responses.jsonl      | 355 ++++++++++++
 .../pr-7110/http_request_responses.jsonl.sha256    |   1 +
 .../http_request_responses_1779924084806.jsonl     | 355 ++++++++++++
 evidence/pr-7110/llm_request_responses.jsonl       |  16 +
 .../pr-7110/llm_request_responses.jsonl.sha256     |   1 +
 .../llm_request_responses_1779924084806.jsonl      |  16 +
 evidence/pr-7110/metadata.json                     | 103 ++++
 evidence/pr-7110/metadata.json.sha256              |   1 +
 evidence/pr-7110/methodology.md                    |  51 ++
 evidence/pr-7110/methodology.md.sha256             |   1 +
 evidence/pr-7110/notes.md                          |  88 +++
 evidence/pr-7110/notes.md.sha256                   |   1 +
 ...raw_gemini-3-flash-preview_god_mode_cascade.txt |  57 ++
 ...ini-3-flash-preview_god_mode_cascade.txt.sha256 |   1 +
 ...gemini-3-flash-preview_regular_turn_cascade.txt |  80 +++
 ...3-flash-preview_regular_turn_cascade.txt.sha256 |   1 +
 .../raw_unknown_model_evidence_signature_guard.txt |   1 +
 ...known_model_evidence_signature_guard.txt.sha256 |   1 +
 .../pr-7110/replay_fixture_source_manifest.json    |  66 +++
 evidence/pr-7110/request_responses.jsonl           |  10 +
 evidence/pr-7110/request_responses.jsonl.sha256    |   1 +
 evidence/pr-7110/run.json                          |  91 +++
 evidence/pr-7110/run.json.sha256                   |   1 +
 evidence/pr-7110/scenario_results_checkpoint.json  |   1 +
 .../scenario_results_checkpoint.json.sha256        |   1 +
 evidence/pr-7110/streaming_evidence.json           |  39 ++
 evidence/pr-7110/streaming_evidence.json.sha256    |   1 +
 evidence/pr-7110/test_console_output.txt           | 111 ++++
 evidence/pr-7110/test_console_output.txt.sha256    |   1 +
 mvp_site/backend_adjustment_registry.py            |  93 +---
 mvp_site/backend_adjustment_specs.py               |  91 ++-
 mvp_site/backend_adjustment_types.py               |  41 +-
 mvp_site/firestore_service.py                      | 104 +++-
 mvp_site/llm_request.py                            |  29 +
 mvp_site/llm_service.py                            | 180 +++++-
 mvp_site/narrative_response_schema.py              |  28 +-
 mvp_site/prompts/god_mode_instruction.md           |  33 +-
 mvp_site/prompts/living_world_instruction.md       |  33 +-
 mvp_site/schemas/prompt_tool_contracts.json        |   4 +-
 .../tests/frontend/test_scroll_video_evidence.py   |  21 +-
 mvp_site/tests/test_backend_adjustment_registry.py | 102 +++-
 mvp_site/tests/test_llm_service_cache_import.py    |   1 +
 mvp_site/tests/test_llm_service_context.py         |  30 +
 mvp_site/tests/test_merge_background_events.py     | 211 +++++++
 mvp_site/tests/test_prompts.py                     |  52 +-
 testing_mcp/test_cache_cross_run_savings.py        |  51 +-
 testing_mcp/test_event_cascade_real_e2e.py         | 371 ++++++++++++
 tests/scripts/test_pr_autonomy_metrics.py          |   4 +-
 tests/test_mcp_global_installation.py              |  32 +-
 69 files changed, 4803 insertions(+), 446 deletions(-)
```

## Server Runtime
- **Port:** 8045
- **PID:** 81900
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:8045 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 1000 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** None
- **MOCK_SERVICES_MODE:** false
- **GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **WORLDAI_GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **FIRESTORE_EMULATOR_HOST:** None
- **PORT:** 8045
- **FIREBASE_PROJECT_ID:** worldarchitecture-ai
- **GEMINI_API_KEY:** [SET - 39 chars]
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/investigate-reaper-stale-living-world/event_cascade_real_e2e/iteration_054/llm_request_responses_1779930892225.jsonl
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/investigate-reaper-stale-living-world/event_cascade_real_e2e/iteration_054/http_request_responses_1779930892225.jsonl
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/investigate-reaper-stale-living-world/event_cascade_real_e2e/iteration_054/gemini_http_request_responses_1779930892225.jsonl
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** /tmp/worldarchitect.ai/investigate-reaper-stale-living-world/event_cascade_real_e2e/iteration_054/provider_http_request_responses_1779930892225.jsonl

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
