# Evidence Summary: pr7439-current-head-bq-path14

## Test Results
- **Total Scenarios:** 2
- **Scenario Validation Passed:** 2
- **Scenario Validation Failed:** 0
- **Scenario Validation Pass Rate:** 100.0%
- **Raw LLM Layer Passed:** 1/1 (100.0%)

- **Post-Processing Campaign Capture Passed:** 1
- **Post-Processing Campaign Capture Failed:** 0
- **Post-Processing Campaign Capture Pass Rate:** 100.0%
## Scenario Results

### path14_gameplay_streaming_proxy
- **Status:** ✅ PASS
- **Campaign ID:** `6WfwGRCs7GuO2vYK7KXo`

### EVIDENCE_SIGNATURE_GUARD
- **Status:** ✅ PASS

## Provenance Chain
- **Git HEAD:** `64321cced78af9fc253fd8b06f2a533a2598ed70`
- **Test Timestamp:** `2026-06-11T18:02:15.429716+00:00`
- **Server PID:** `61587`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 2/2 | run.json | scenarios[*].passed, scenarios[*].errors |
| Campaign post-processing capture passed: 1/1 | run.json | campaign_capture_status[*].status |
| Streaming evidence normalized | streaming_evidence.json | summary.*, scenarios[*].chunk_count_observed |
| Bundle artifact inventory | artifacts/collection_log.txt | core_files, jsonl_captures, campaigns_dir |
| MCP request/response captured | request_responses.jsonl | Full request/response pairs |
| Local server HTTP request/response captured | http_request_responses.jsonl | http_request/http_response entries |
| LLM request/response stream captured | llm_request_responses.jsonl | request/response entries (type field) |
| Gemini HTTP transport captured | gemini_http_request_responses.jsonl | http_request/http_response/transport_error entries |
| Server execution log | artifacts/server.log | Raw server output |
| Git provenance | metadata.json | git_provenance.git_head = `64321cce...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| path14_gameplay_streaming_proxy | ✅ Pass | `6WfwGRCs...` |
| EVIDENCE_SIGNATURE_GUARD | ✅ Pass | N/A |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use local basename paths so per-file verification works from each artifact directory


## What This Evidence Proves vs. Does NOT Prove

**Proves**:
- Core logic and scenario validation for pr7439-current-head-bq-path14
- Scenario execution pass rates (2/2)

**Does NOT Prove**:
- Production server behavior (tested on local server unless otherwise noted)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
