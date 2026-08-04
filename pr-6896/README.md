# Evidence Package: schema_migration_flow_real_api

## Package Manifest
- **Test Name:** schema_migration_flow_real_api
- **Run ID:** `schema_migration_flow_real_api-003-20260523T073045`
- **Iteration:** 3
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-05-23T07:30:45.566026+00:00
- **Repository:** worldarchitect.ai
- **Branch:** worktree_sync_location
- **Commit:** fd68b6b6d5113b57c5085f37238a9e8905d09a1a
- **Merge Base:** unknown
- **Commits Ahead of Main:** 0

## Git Provenance
```
No diff available
```

## Server Runtime
- **Port:** 8098
- **PID:** 96975
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:8098 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 50 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** None
- **MOCK_SERVICES_MODE:** false
- **GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **WORLDAI_GOOGLE_APPLICATION_CREDENTIALS:** [SET - file:serviceAccountKey.json]
- **FIRESTORE_EMULATOR_HOST:** None
- **PORT:** 8098
- **FIREBASE_PROJECT_ID:** worldarchitecture-ai
- **GEMINI_API_KEY:** [SET - 39 chars]
- **LLM_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_sync_location/schema_migration_flow_real_api/iteration_003/llm_request_responses_1779521297519.jsonl
- **HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_sync_location/schema_migration_flow_real_api/iteration_003/http_request_responses_1779521297519.jsonl
- **GEMINI_HTTP_REQUEST_RESPONSE_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_sync_location/schema_migration_flow_real_api/iteration_003/gemini_http_request_responses_1779521297519.jsonl
- **MCP_TEST_PROVIDER_HTTP_CAPTURE_PATH:** /tmp/worldarchitect.ai/worktree_sync_location/schema_migration_flow_real_api/iteration_003/provider_http_request_responses_1779521297519.jsonl

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
