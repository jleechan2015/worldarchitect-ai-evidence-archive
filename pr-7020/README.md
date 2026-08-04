# Evidence Package: test_campaign_upgrade_modal_lock_red_green

## Package Manifest
- **Test Name:** test_campaign_upgrade_modal_lock_red_green
- **Run ID:** `test_campaign_upgrade_modal_lock_red_green-007-20260529T065632`
- **Iteration:** 7
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-05-29T06:56:32.889542+00:00
- **Repository:** worldarchitect.ai
- **Branch:** fix-campaign-upgrade-hang
- **Commit:** 7187d915335039dda194c266a6c2e6ad3c222115
- **Merge Base:** 02bc02e9736306521eb2ea2dfc295701e65958cd
- **Commits Ahead of Main:** 28

## Git Provenance
```
.github/workflows/test.yml                         |   2 +-
 evidence/pr-7020/README.md                         | 112 +++
 evidence/pr-7020/README.md.sha256                  |   1 +
 .../pr-7020/campaigns/B5bEx6v09MtBnKQtVGYZ.json    | 286 ++++++++
 .../campaigns/B5bEx6v09MtBnKQtVGYZ.json.sha256     |   1 +
 ...grade Lifecycle Streaming Evidence_B5bEx6v0.txt |  92 +++
 ...cle Streaming Evidence_B5bEx6v0_game_state.json | 221 ++++++
 evidence/pr-7020/evidence.md                       |  68 ++
 evidence/pr-7020/evidence.md.sha256                |   1 +
 .../pr-7020/gemini_http_request_responses.jsonl    |   8 +
 .../gemini_http_request_responses.jsonl.sha256     |   1 +
 ...mini_http_request_responses_1780028778629.jsonl |   8 +
 evidence/pr-7020/http_request_responses.jsonl      | 168 +++++
 .../pr-7020/http_request_responses.jsonl.sha256    |   1 +
 .../http_request_responses_1780028778629.jsonl     | 168 +++++
 evidence/pr-7020/llm_request_responses.jsonl       |   8 +
 .../pr-7020/llm_request_responses.jsonl.sha256     |   1 +
 .../llm_request_responses_1780028778629.jsonl      |   8 +
 evidence/pr-7020/metadata.json                     | 109 +++
 evidence/pr-7020/metadata.json.sha256              |   1 +
 evidence/pr-7020/methodology.md                    |  12 +
 evidence/pr-7020/methodology.md.sha256             |   1 +
 evidence/pr-7020/notes.md                          |  33 +
 evidence/pr-7020/notes.md.sha256                   |   1 +
 ..._model_campaign_upgrade_lifecycle_streaming.txt |   1 +
 ...campaign_upgrade_lifecycle_streaming.txt.sha256 |   1 +
 .../raw_unknown_model_evidence_signature_guard.txt |   1 +
 ...known_model_evidence_signature_guard.txt.sha256 |   1 +
 .../pr-7020/replay_fixture_source_manifest.json    |  69 ++
 evidence/pr-7020/request_responses.jsonl           |  14 +
 evidence/pr-7020/request_responses.jsonl.sha256    |   1 +
 evidence/pr-7020/run.json                          | 757 +++++++++++++++++++++
 evidence/pr-7020/run.json.sha256                   |   1 +
 evidence/pr-7020/scenario_results_checkpoint.json  |   1 +
 .../scenario_results_checkpoint.json.sha256        |   1 +
 evidence/pr-7020/streaming_evidence.json           |  27 +
 evidence/pr-7020/streaming_evidence.json.sha256    |   1 +
 ...test_campaign_upgrade_modal_lock_red_green.cast |   2 +
 evidence/pr-7020/test_console_output.txt           |  94 +++
 evidence/pr-7020/test_console_output.txt.sha256    |   1 +
 mvp_site/agents.py                                 |  81 ++-
 mvp_site/campaign_upgrade.py                       | 168 ++++-
 mvp_site/llm_parser.py                             |   5 +
 mvp_site/tests/test_agents.py                      |  45 ++
 ..._level_up_server_generated_invariant_end2end.py |   4 +-
 mvp_site/tests/test_world_logic.py                 | 221 +++++-
 mvp_site/world_logic.py                            |  57 ++
 .../test_campaign_upgrade_modal_lock_red_green.py  | 358 ++++++++++
 48 files changed, 3183 insertions(+), 41 deletions(-)
```

## Server Runtime
- **Port:** 8083
- **PID:** 28119
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:8083 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 1000 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** None
- **MOCK_SERVICES_MODE:** false
- **GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **WORLDAI_GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **FIRESTORE_EMULATOR_HOST:** None
- **PORT:** 8083
- **FIREBASE_PROJECT_ID:** worldarchitecture-ai
- **GEMINI_API_KEY:** [SET - 39 chars]
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix-campaign-upgrade-hang/test_campaign_upgrade_modal_lock_red_green/iteration_007/llm_request_responses_1780037674376.jsonl
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix-campaign-upgrade-hang/test_campaign_upgrade_modal_lock_red_green/iteration_007/http_request_responses_1780037674376.jsonl
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix-campaign-upgrade-hang/test_campaign_upgrade_modal_lock_red_green/iteration_007/gemini_http_request_responses_1780037674376.jsonl
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix-campaign-upgrade-hang/test_campaign_upgrade_modal_lock_red_green/iteration_007/provider_http_request_responses_1780037674376.jsonl

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
