# Evidence Package: combat_rewards_level_up

## Package Manifest
- **Test Name:** combat_rewards_level_up
- **Run ID:** `combat_rewards_level_up-001-20260524T095319`
- **Iteration:** 1
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-05-24T09:53:19.528492+00:00
- **Repository:** worldarchitect.ai
- **Branch:** claude/vigilant-ritchie-GbMPa
- **Commit:** 80690b8b2736d07735cc07dd38bed862a0a1792c
- **Merge Base:** 25cee34d6ff9f966eb9ba190e40efbd6eec3a5b9
- **Commits Ahead of Main:** 8

## Git Provenance
```
mvp_site/prompts/combat_system_instruction.md      | 52 +++++++++-----
 mvp_site/prompts/deferred_rewards_instruction.md   | 34 +++++++--
 mvp_site/prompts/faction_minigame_instruction.md   | 30 ++++----
 mvp_site/prompts/god_mode_instruction.md           |  8 +++
 .../prompts/narrative_lite_system_instruction.md   |  6 ++
 mvp_site/prompts/narrative_system_instruction.md   | 38 ++++++----
 mvp_site/prompts/rewards_system_instruction.md     | 84 +++++++++++++++++++++-
 scripts/validate_beads_issues_jsonl.py             |  2 +-
 8 files changed, 202 insertions(+), 52 deletions(-)
```

## Server Runtime
- **Port:** 55724
- **PID:** 45659
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:55724 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 1000 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** false
- **MOCK_SERVICES_MODE:** false
- **GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **WORLDAI_GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **FIRESTORE_EMULATOR_HOST:** None
- **PORT:** None
- **FIREBASE_PROJECT_ID:** worldarchitecture-ai
- **GEMINI_API_KEY:** [SET - 39 chars]
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** None
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** None
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** None
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** None

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
