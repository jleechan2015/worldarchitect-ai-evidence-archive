# Evidence Summary: combat_rewards_level_up

## Test Results
- **Total Scenarios:** 1
- **Scenario Validation Passed:** 1
- **Scenario Validation Failed:** 0
- **Scenario Validation Pass Rate:** 100.0%
- **Raw LLM Layer Passed:** 0/1 (0.0%)

## Scenario Results

### Combat Rewards Level-Up Test
- **Status:** ✅ PASS
- **Campaign ID:** `431zSTZtjP900pO6oP1v`

## Provenance Chain
- **Git HEAD:** `80690b8b2736d07735cc07dd38bed862a0a1792c`
- **Test Timestamp:** `2026-05-24T09:53:19.528492+00:00`
- **Server PID:** `45659`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 1/1 | run.json | scenarios[*].passed, scenarios[*].errors |
| Streaming evidence normalized | streaming_evidence.json | summary.*, scenarios[*].chunk_count_observed |
| Bundle artifact inventory | artifacts/collection_log.txt | core_files, jsonl_captures, campaigns_dir |
| MCP request/response captured | request_responses.jsonl | Full request/response pairs |
| Git provenance | metadata.json | git_provenance.git_head = `80690b8b...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| Combat Rewards Level-Up Test | ✅ Pass | `431zSTZt...` |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use local basename paths so per-file verification works from each artifact directory


## What This Evidence Proves vs. Does NOT Prove

**Proves**:
- Core logic and scenario validation for combat_rewards_level_up
- Scenario execution pass rates (1/1)

**Does NOT Prove**:
- Production server behavior (tested on external preview server — not local)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
