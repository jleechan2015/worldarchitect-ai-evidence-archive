# Methodology: banned-names-always-on

## Test Type
Real API test against MCP server (not mock mode).

## Test Mode
- **TESTING env var:** None
- **MOCK_SERVICES_MODE env var:** not set (default: false = real)
- **Mode:** Real API calls via MCP HTTP JSON-RPC

## Execution Environment
- **Mode:** External remote server (no local process — lsof/ps not applicable)
- **Target port in provenance:** 64121
- **Note:** No server.log, lsof_output, or ps_output; all evidence comes from
  HTTP request/response traces in http_request_responses.jsonl and artifacts/http_scenario_responses.json.

## Evidence Capture
- Git provenance captured at test start

## Evidence Mode
- System instruction capture: filenames + char_count (lightweight). Raw LLM request/response payloads captured in request_responses.jsonl when raw payload capture is enabled.


## Validation Criteria
Test scenarios validate that:
1. The remote API endpoint responds correctly to HTTP requests
2. Authentication (generate/use/revoke key lifecycle) behaves as expected
3. Error responses (e.g. 401 after revocation) are returned correctly

**Note:** No local server.log is available for this run (external server mode).
Check artifacts/http_scenario_responses.json for full request/response traces.
