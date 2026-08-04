# Evidence Package: banned-names-always-on

## Package Manifest
- **Test Name:** banned-names-always-on
- **Run ID:** `banned-names-always-on-001-20260613T044124`
- **Iteration:** 1
- **Bundle Version:** 1.2.0
- **Collected At (UTC):** 2026-06-13T04:41:24.641542+00:00
- **Repository:** worldarchitect.ai
- **Branch:** unknown
- **Commit:** unknown
- **Merge Base:** unknown
- **Commits Ahead of Main:** 0

## Git Provenance
```
No diff available
```

## Server Runtime
- **Port:** 64121
- **PID:** 27236
- **Command:** /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:64121 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 1000 --access-logfile - --error-logfile - --log-level info

## Environment Variables
- **WORLDAI_DEV_MODE:** true
- **TESTING:** None
- **MOCK_SERVICES_MODE:** None
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
