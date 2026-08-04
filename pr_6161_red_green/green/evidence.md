# Evidence Summary: rewards_box_planning_block_e2e

## Test Results
- **Total Scenarios:** 3
- **Scenario Validation Passed:** 3
- **Scenario Validation Failed:** 0
- **Scenario Validation Pass Rate:** 100.0%
- **Raw LLM Layer Passed:** 3/3 (100.0%)

## ⚠️ Multi-Campaign Isolation Note

This evidence bundle contains **3 campaigns**:
- **0 shared campaign(s)** reused across multiple tests
- **3 independent campaign(s)** each used by one test only

**Why:** Each test uses its own campaign to prevent state bleed

**Claim Scoping:** Each scenario result below includes its `campaign_id`. Claims about
specific scenarios reference ONLY that scenario's campaign. Aggregate claims (e.g., "18/18 passed")
span all campaigns but each individual result is traceable to its campaign.

- **Post-Processing Campaign Capture Passed:** 3
- **Post-Processing Campaign Capture Failed:** 0
- **Post-Processing Campaign Capture Pass Rate:** 100.0%
## Scenario Results

### atomicity_e2e
- **Status:** ✅ PASS
- **Campaign ID:** `3GDFTAaejZ7khpU9pTIg`

### projected_level_up_button_text
- **Status:** ✅ PASS
- **Campaign ID:** `Itzj9icU4hytVBqcrPse`

### multi_level_organic_progression
- **Status:** ✅ PASS
- **Campaign ID:** `nZ3MPpvor03dOy6C5iZd`

## Provenance Chain
- **Git HEAD:** `e68239f7728465ab766df8020b86dc248a2bad06`
- **Test Timestamp:** `2026-04-09T20:57:55.875524+00:00`
- **Server PID:** `1001881`

## System Instruction Files Observed
- `prompts/master_directive.md`
- `prompts/god_mode_instruction.md`
- `prompts/game_state_instruction.md`
- `prompts/planning_protocol.md`
- `prompts/dnd_srd_instruction.md`
- `prompts/mechanics_system_instruction.md`
- `prompts/dice_system_instruction_code_execution.md`
- `prompts/character_template.md`
- `prompts/narrative_system_instruction.md`
- `prompts/living_world_instruction.md`
- `prompts/level_up_instruction.md`
- `prompts/combat_system_instruction.md`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 3/3 | run.json | scenarios[*].passed, scenarios[*].errors |
| Campaign post-processing capture passed: 3/3 | run.json | campaign_capture_status[*].status |
| MCP local server transport | http_request_responses.jsonl | http_request/http_response entries |
| Local server HTTP request/response captured | http_request_responses.jsonl | http_request/http_response entries |
| LLM request/response stream fingerprint | llm_request_responses.jsonl.sha256 | checksum + external log retention |
| Gemini HTTP transport captured | gemini_http_request_responses.jsonl | http_request/http_response/transport_error entries |
| Git provenance | metadata.json | git_provenance.git_head = `e68239f7...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| atomicity_e2e | ✅ Pass | `3GDFTAae...` |
| projected_level_up_button_text | ✅ Pass | `Itzj9icU...` |
| multi_level_organic_progression | ✅ Pass | `nZ3MPpvo...` |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use evidence-root-relative paths for portability (`sha256sum -c` compatible from evidence root)

- ⚠️ Server warnings detected (stored in uncommitted runtime logs)
- Warning: ENTITY_TRACKING_VALIDATION
- Warning: ACTION_RESOLUTION_MISSING_FIELDS
- Warning: CRITICAL_SAFEGUARD
- Warning: SYSTEM_INSTRUCTION_EMERGENCY_COMPACT
- Warning: ENTITY_TRACKING_CAPPED
- Warning: SOCIAL_HP_GUARD


## What This Evidence Does NOT Prove

- Production server behavior (tested on local server unless otherwise noted)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
