# Evidence Package: cleanup-defeated-enemies

## Package Manifest
- **Test Name:** cleanup-defeated-enemies
- **Run ID:** `cleanup-defeated-enemies-002-20260531T195215`
- **Iteration:** 2
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-05-31T19:52:15.370447+00:00
- **Repository:** worldarchitect.ai
- **Branch:** fix/dead-npc-hallucination-v2
- **Commit:** 612960be3f63bb2b8dcc7bd33dac774a96e894da
- **Merge Base:** 7394f3b51563641dab261dcbca916b971ddac625
- **Commits Ahead of Main:** 22

## Git Provenance
```
.beads/issues.jsonl                                |  12 +-
 mvp_site/backend_adjustment_registry.py            |   2 +
 mvp_site/backend_adjustment_specs.py               |  87 +++++
 mvp_site/constants.py                              |  41 +++
 .../evidence/dead_npc_hallucination/proof.json     |  30 ++
 .../evidence/dead_npc_hallucination/proof.sha256   |   1 +
 mvp_site/firestore_service.py                      |   2 -
 mvp_site/game_state.py                             |  29 +-
 mvp_site/game_state_mixins.py                      | 361 +++++++++++++------
 mvp_site/prompts/game_state_instruction.md         |  14 +
 mvp_site/prompts/god_mode_instruction.md           |  12 +
 mvp_site/schemas/prompt_tool_contracts.json        |   4 +-
 mvp_site/tests/test_game_state.py                  | 368 +++++++++++++-------
 mvp_site/tests/test_npc_death_state_persistence.py | 387 ++++++++++++++++++++-
 mvp_site/world_logic.py                            |  29 +-
 15 files changed, 1093 insertions(+), 286 deletions(-)
```

## Server Runtime
- **Port:** 8045
- **PID:** 95989
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:8045 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 1000 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** None
- **MOCK_SERVICES_MODE:** false
- **GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **WORLDAI_GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **FIRESTORE_EMULATOR_HOST:** None
- **PORT:** 8045
- **FIREBASE_PROJECT_ID:** None
- **GEMINI_API_KEY:** [SET - 39 chars]
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix_dead-npc-hallucination-v2/cleanup-defeated-enemies/iteration_002/llm_request_responses_1780257090614.jsonl
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix_dead-npc-hallucination-v2/cleanup-defeated-enemies/iteration_002/http_request_responses_1780257090614.jsonl
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix_dead-npc-hallucination-v2/cleanup-defeated-enemies/iteration_002/gemini_http_request_responses_1780257090614.jsonl
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** /tmp/worldarchitect.ai/fix_dead-npc-hallucination-v2/cleanup-defeated-enemies/iteration_002/provider_http_request_responses_1780257090614.jsonl

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
