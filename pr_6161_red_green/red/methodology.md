# Methodology: rewards_box_planning_block_e2e

## Test Type
Real API test against MCP server (not mock mode).

## Test Mode
- **TESTING env var:** None
- **MOCK_SERVICES_MODE env var:** false
- **Mode:** Real API calls via MCP HTTP JSON-RPC

## Execution Environment
- Server running at port 8051
- Process: <redacted-tmp-path> -m gunicorn mvp_site.main:app --bind 0.0.0.0:8051 --workers 1 --worker-class gthread --threads 4 --timeout 600 --max-requests 0 --access-logfile - --error-logfile - --log-level info

## Test Isolation Design

**Multi-campaign architecture is BY DESIGN for test isolation.**

- **Total Campaigns:** 3
- **Shared Campaigns:** 0 (used by multiple scenarios)
- **Independent Campaigns:** 3 (single-scenario campaigns)
- **Isolated Tests:** 0 (explicit `isolated: True` scenarios)
- **Rationale:** Each test uses its own campaign to prevent state bleed

No scenarios in this run were marked `isolated: True`; campaign usage still follows multi-campaign separation to avoid state bleed.
Campaign separation in this run still prevents state bleed across scenarios that use different campaign IDs.

## Evidence Capture
- Git provenance captured at test start
- Raw request/response payloads captured for each MCP call
- Server runtime info captured via lsof/ps
- Streaming normalization artifacts were generated during capture; full stream text is not persisted in this bundle.
- Raw local-server HTTP request/response payloads captured in http_request_responses.jsonl
- LLM request/response payloads were captured during run, but `llm_request_responses.jsonl` is not included in this committed bundle (checksum file retained).
- Raw Gemini HTTP transport payloads captured in gemini_http_request_responses.jsonl
- Run logs are retained externally and are not included in this committed bundle.

## Evidence Mode
- System instruction capture: filenames + char_count (lightweight).


## Validation Criteria
Test scenarios validate that:
1. MCP server processes actions correctly
2. State updates are returned as expected
3. Server processes all requests successfully (validation warnings may be logged but requests succeed)

**Note:** Server warnings (e.g., validation, entity tracking) may appear in full run logs.

Warning parser for notes: counts each log line matching `\bWARNING\b|SYSTEM WARNING:` once.
