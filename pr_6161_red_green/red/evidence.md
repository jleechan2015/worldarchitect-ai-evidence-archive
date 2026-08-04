# Evidence Summary: rewards_box_planning_block_e2e

## Test Results
- **Total Scenarios:** 3
- **Scenario Validation Passed:** 1
- **Scenario Validation Failed:** 2
- **Scenario Validation Pass Rate:** 33.3%
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
- **Campaign ID:** `SQYV3wvYNXcPdaiWxsK0`

### projected_level_up_button_text
- **Status:** ❌ FAIL
- **Campaign ID:** `dL5LR8w2kqsqb4Xqc2SK`
- **Errors:** ['Projected pending state did not return rewards_box.level_up_available=true', 'Projected pending state did not return canonical level-up planning choices', 'Projected pending state missing level_up_now button text']

### multi_level_organic_progression
- **Status:** ❌ FAIL
- **Campaign ID:** `AIZ3QHXnz3T1FlgyagjR`
- **Errors:** ['level_up_to_2: level_up_modal_enter_target_2: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_2: level_up_modal_enter_target_2: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_enter_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_enter_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_1_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_1_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_2_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_2_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_3_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_3_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_4_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_4_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_5_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_5_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_6_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_3: level_up_modal_step_6_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', "level_up_to_3: Did not reach finish_level_up_return_to_game for level 3 within modal step budget; transcript=[{'step': 'enter_level_up', 'action': 'CHOICE:level_up_now', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_1', 'action': 'CHOICE:choose_champion', 'choice_ids': ['level_up_now', 'adjust_archetype', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_2', 'action': 'CHOICE:adjust_archetype', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_3', 'action': 'CHOICE:choose_champion', 'choice_ids': ['level_up_now', 'adjust_archetype', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_4', 'action': 'CHOICE:adjust_archetype', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_5', 'action': 'CHOICE:choose_champion', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_6', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}]", 'level_up_to_4: level_up_modal_enter_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_enter_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_1_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_1_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_2_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_2_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_3_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_3_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_4_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_4_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_5_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_5_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_6_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true', 'level_up_to_4: level_up_modal_step_6_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true', "level_up_to_4: Did not reach finish_level_up_return_to_game for level 4 within modal step budget; transcript=[{'step': 'enter_level_up', 'action': 'CHOICE:level_up_now', 'choice_ids': ['level_up_now', 'apply_asi_str', 'apply_asi_con', 'apply_feat_gwm', 'apply_feat_sentinel', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_1', 'action': 'CHOICE:apply_asi_str', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_2', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'apply_asi_str', 'apply_asi_con', 'apply_feat_sentinel', 'apply_feat_tough', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_3', 'action': 'CHOICE:apply_asi_str', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_4', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'apply_asi_str_20', 'apply_asi_dex_14', 'choose_feat_gwm', 'choose_feat_sentinel', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_5', 'action': 'CHOICE:apply_asi_str_20', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_6', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'apply_asi_str', 'apply_asi_con', 'choose_feat_gwm', 'choose_feat_sentinel', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}]"]

## Provenance Chain
- **Git HEAD:** `3c7a91bdcd2bdabe641259f4c9d0501024426654`
- **Test Timestamp:** `2026-04-09T21:30:08.927668+00:00`
- **Server PID:** `1102462`

## System Instruction Files Observed
- `prompts/master_directive.md`
- `prompts/god_mode_instruction.md`
- `prompts/game_state_instruction.md`
- `prompts/planning_protocol.md`
- `prompts/dnd_srd_instruction.md`
- `prompts/mechanics_system_instruction.md`
- `prompts/dice_system_instruction_code_execution.md`
- `prompts/combat_system_instruction.md`
- `prompts/narrative_system_instruction.md`
- `prompts/living_world_instruction.md`
- `prompts/level_up_instruction.md`
- `prompts/character_template.md`


## Claim → Artifact Map

| Claim | File | Key Field(s) |
|-------|------|--------------|
| Scenario validation passed: 1/3 | run.json | scenarios[*].passed, scenarios[*].errors |
| Campaign post-processing capture passed: 3/3 | run.json | campaign_capture_status[*].status |
| MCP local server transport | http_request_responses.jsonl | http_request/http_response entries |
| Local server HTTP request/response captured | http_request_responses.jsonl | http_request/http_response entries |
| LLM request/response stream fingerprint | llm_request_responses.jsonl.sha256 | checksum + external log retention |
| Gemini HTTP transport captured | gemini_http_request_responses.jsonl | http_request/http_response/transport_error entries |
| Git provenance | metadata.json | git_provenance.git_head = `3c7a91bd...` |

## Coverage Matrix

| Scenario | Status | Campaign ID |
|----------|--------|-------------|
| atomicity_e2e | ✅ Pass | `SQYV3wvY...` |
| projected_level_up_button_text | ❌ Fail | `dL5LR8w2...` |
| multi_level_organic_progression | ❌ Fail | `AIZ3QHXn...` |

## Evidence Integrity

- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use evidence-root-relative paths for portability (`sha256sum -c` compatible from evidence root)

- ⚠️ Server warnings detected (stored in uncommitted runtime logs)
- Warning: CODE_EXEC_NO_RNG
- Warning: ENTITY_TRACKING_VALIDATION
- Warning: ACTION_RESOLUTION_MISSING_FIELDS
- Warning: CRITICAL_SAFEGUARD
- Warning: SYSTEM_INSTRUCTION_EMERGENCY_COMPACT
- Warning: ENTITY_TRACKING_CAPPED


## What This Evidence Does NOT Prove

- Production server behavior (tested on local server unless otherwise noted)
- Performance under load (single-request tests)
- Edge cases not covered by scenarios
