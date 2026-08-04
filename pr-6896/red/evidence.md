# Evidence Summary: schema_migration_flow_real_api

## Test Results
- **Total Scenarios:** 2
- **Scenario Validation Passed:** 1
- **Scenario Validation Failed:** 1
- **Scenario Validation Pass Rate:** 50.0%
- **Raw LLM Layer Passed:** 1/1 (100.0%)

## ⚠️ Post-Processing Detected Additional Issues

- **Raw Layer Pass Rate:** 1/1 (100.0%)
- **Post-Processing Pass Rate (raw-validated scenarios):** 0/1 (0.0%)

Post-processing detected issues (dm_notes, core_memories, state mutations) that
the raw narrative validation missed. See `errors` in individual scenario files.

- **Post-Processing Campaign Capture Passed:** 1
- **Post-Processing Campaign Capture Failed:** 0
- **Post-Processing Campaign Capture Pass Rate:** 100.0%
## Scenario Results

### one_time_schema_migration_and_strict_post_migration_validation
- **Status:** ❌ FAIL
- **Campaign ID:** `d7yEeRhRsTouGUX8Avo6`
- **Errors:** ["Expected current_location_name to be one of {'Legacy Crypt of Shadows', 'Regression Testing Chamber'}, got 'Regression Testing Chamber (Legacy Crypt of Shadows)'"]

### EVIDENCE_SIGNATURE_GUARD
- **Status:** ✅ PASS

## Provenance Chain
- **Git HEAD:** `9ea6062636c6405a7e439fdb32748617db91bb4f`
- **Test Timestamp:** `2026-05-22T09:40:36.495570+00:00`
- **Server PID:** `9931`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 1/2 | run.json | scenarios[*].passed, scenarios[*].errors |
| Campaign post-processing capture passed: 1/1 | run.json | campaign_capture_status[*].status |
| Streaming evidence normalized | streaming_evidence.json | summary.*, scenarios[*].chunk_count_observed |
| Bundle artifact inventory | artifacts/collection_log.txt | core_files, jsonl_captures, campaigns_dir |
| MCP request/response captured | request_responses.jsonl | Full request/response pairs |
| Local server HTTP request/response captured | http_request_responses.jsonl | http_request/http_response entries |
| LLM request/response stream captured | llm_request_responses.jsonl | request/response entries (type field) |
| Gemini HTTP transport captured | gemini_http_request_responses.jsonl | http_request/http_response/transport_error entries |
| Server execution log | artifacts/server.log | Raw server output |
| Git provenance | metadata.json | git_provenance.git_head = `9ea60626...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| one_time_schema_migration_and_strict_post_migration_validation | ❌ Fail | `d7yEeRhR...` |
| EVIDENCE_SIGNATURE_GUARD | ✅ Pass | N/A |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use local basename paths so per-file verification works from each artifact directory

- ⚠️ Server warnings detected (see artifacts/server.log)
- Warning: CRITICAL_SAFEGUARD


## What This Evidence Proves vs. Does NOT Prove

**Proves**:
- Core logic and scenario validation for schema_migration_flow_real_api
- Scenario execution pass rates (1/2)

**Does NOT Prove**:
- Production server behavior (tested on local server unless otherwise noted)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
