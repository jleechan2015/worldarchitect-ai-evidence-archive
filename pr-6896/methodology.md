# Methodology: schema_migration_flow_real_api

## Test Type
Real API test against MCP server (not mock mode).

## Test Mode
- **TESTING env var:** None
- **MOCK_SERVICES_MODE env var:** false
- **Mode:** Real API calls via MCP HTTP JSON-RPC

## Execution Environment
- Server running at port 8098
- Process: /opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m gunicorn mvp_site.main:app --bind 0.0.0.0:8098 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 50 --access-logfile - --error-logfile - --log-level info

## Evidence Capture
- Git provenance captured at test start
- Raw request/response payloads captured for each MCP call
- Server runtime info captured via lsof/ps
- Streaming evidence normalized into streaming_evidence.json
- Raw local-server HTTP request/response payloads captured in http_request_responses.jsonl
- Raw LLM request/response payloads captured in llm_request_responses.jsonl
- Raw Gemini HTTP transport payloads captured in gemini_http_request_responses.jsonl
- Raw LLM response text captured in server.log (artifacts/server.log)

## Evidence Mode
- System instruction capture: filenames + char_count (lightweight). Raw LLM request/response payloads captured in request_responses.jsonl when raw payload capture is enabled.


## Validation Criteria
Test scenarios validate that:
1. MCP server processes actions correctly
2. State updates are returned as expected
3. Server processes all requests successfully (validation warnings may be logged but requests succeed)

**Note:** Server warnings (e.g., validation, entity tracking) may appear in logs.
Check artifacts/server.log for full server output.

Warning parser for notes: counts each log line matching `\bWARNING\b|SYSTEM WARNING:` once.
