# Evidence Summary: banned-names-always-on

## Test Results
- **Total Scenarios:** 1
- **Scenario Validation Passed:** 1
- **Scenario Validation Failed:** 0
- **Scenario Validation Pass Rate:** 100.0%
- **Raw LLM Layer Passed:** 0/1 (0.0%)

## Scenario Results

### banned_names_injection_check
- **Status:** ✅ PASS
- **Campaign ID:** `KtdzQjJ8EqDYum6sTODt`

## Provenance Chain
- **Git HEAD:** `unknown`
- **Test Timestamp:** `2026-06-13T04:41:24.641542+00:00`
- **Server PID:** `27236`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 1/1 | run.json | scenarios[*].passed, scenarios[*].errors |
| Streaming evidence normalized | streaming_evidence.json | summary.*, scenarios[*].chunk_count_observed |
| Bundle artifact inventory | artifacts/collection_log.txt | core_files, jsonl_captures, campaigns_dir |
| Git provenance | metadata.json | git_provenance.git_head = `unknown...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| banned_names_injection_check | ✅ Pass | `KtdzQjJ8...` |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use local basename paths so per-file verification works from each artifact directory


## What This Evidence Proves vs. Does NOT Prove

**Proves**:
- Core logic and scenario validation for banned-names-always-on
- Scenario execution pass rates (1/1)

**Does NOT Prove**:
- Production server behavior (tested on external preview server — not local)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
