# Evidence Summary: event_cascade_real_e2e

## Test Results
- **Total Scenarios:** 3
- **Scenario Validation Passed:** 3
- **Scenario Validation Failed:** 0
- **Scenario Validation Pass Rate:** 100.0%
- **Raw LLM Layer Passed:** 2/2 (100.0%)

## ⚠️ Multi-Campaign Isolation Note

This evidence bundle contains **2 campaigns**:
- **0 shared campaign(s)** reused across multiple tests
- **2 independent campaign(s)** each used by one test only

**Why:** Each test uses its own campaign to prevent state bleed

**Claim Scoping:** Each scenario result below includes its `campaign_id`. Claims about
specific scenarios reference ONLY that scenario's campaign. Aggregate claims (e.g., "18/18 passed")
span all campaigns but each individual result is traceable to its campaign.

- **Post-Processing Campaign Capture Passed:** 2
- **Post-Processing Campaign Capture Failed:** 0
- **Post-Processing Campaign Capture Pass Rate:** 100.0%
## Scenario Results

### god_mode_cascade
- **Status:** ✅ PASS
- **Campaign ID:** `ZeLNjyjKFCVdusWmNHzQ`

### regular_turn_cascade
- **Status:** ✅ PASS
- **Campaign ID:** `CwXl5hyCkc2sQSa4Mu8c`

### EVIDENCE_SIGNATURE_GUARD
- **Status:** ✅ PASS

## Provenance Chain
- **Git HEAD:** `125a12c2891747edcab8c4f1ab796dfa465f7aec`
- **Test Timestamp:** `2026-05-28T01:18:52.018055+00:00`
- **Server PID:** `81900`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 3/3 | run.json | scenarios[*].passed, scenarios[*].errors |
| Campaign post-processing capture passed: 2/2 | run.json | campaign_capture_status[*].status |
| Streaming evidence normalized | streaming_evidence.json | summary.*, scenarios[*].chunk_count_observed |
| Bundle artifact inventory | artifacts/collection_log.txt | core_files, jsonl_captures, campaigns_dir |
| MCP request/response captured | request_responses.jsonl | Full request/response pairs |
| Local server HTTP request/response captured | http_request_responses.jsonl | http_request/http_response entries |
| LLM request/response stream captured | llm_request_responses.jsonl | request/response entries (type field) |
| Gemini HTTP transport captured | gemini_http_request_responses.jsonl | http_request/http_response/transport_error entries |
| Server execution log | artifacts/server.log | Raw server output |
| Git provenance | metadata.json | git_provenance.git_head = `125a12c2...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| god_mode_cascade | ✅ Pass | `ZeLNjyjK...` |
| regular_turn_cascade | ✅ Pass | `CwXl5hyC...` |
| EVIDENCE_SIGNATURE_GUARD | ✅ Pass | N/A |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use local basename paths so per-file verification works from each artifact directory

- ⚠️ Server warnings detected (see artifacts/server.log)
- Warning: ACTION_RESOLUTION_MISSING_FIELDS
- Warning: SYSTEM_INSTRUCTION_EMERGENCY_COMPACT
- Warning: ENTITY_TRACKING_CAPPED


## What This Evidence Proves vs. Does NOT Prove

**Proves**:
- Core logic and scenario validation for event_cascade_real_e2e
- Scenario execution pass rates (3/3)

**Does NOT Prove**:
- Production server behavior (tested on local server unless otherwise noted)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
