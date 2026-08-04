# Notes: rewards_box_planning_block_e2e

## Run Information
- **Run ID:** `rewards_box_planning_block_e2e-001-20260409T213008`
- **Iteration:** 1
- **Bundle Version:** 1.2.0
- **Timestamp:** 2026-04-09T21:30:08.927668+00:00

## Evidence Integrity
- All files in this bundle have corresponding `.sha256` checksum files
- Checksums use evidence-root-relative paths for portability (`sha256sum -c` compatible from evidence root)

## Scenario Summary
- **Total:** 3
- **Passed:** 1
- **Failed:** 2

## Post-Processing Capture Summary
- **Campaigns with capture status:** 3
- **Capture Passed:** 3
- **Capture Failed:** 0

## Warning/Error Summary
- **Server Warnings:** 232 warnings in server.log
- **Warning Parser:** line-level regex `\bWARNING\b|SYSTEM WARNING:` (one count per matching line)
- **Key Warning Categories:**
  - CODE_EXEC_NO_RNG
  - ENTITY_TRACKING_VALIDATION
  - ACTION_RESOLUTION_MISSING_FIELDS
  - CRITICAL_SAFEGUARD
  - SYSTEM_INSTRUCTION_EMERGENCY_COMPACT
  - ENTITY_TRACKING_CAPPED

## Failed Scenarios

### projected_level_up_button_text
- Projected pending state did not return rewards_box.level_up_available=true
- Projected pending state did not return canonical level-up planning choices
- Projected pending state missing level_up_now button text

### multi_level_organic_progression
- level_up_to_2: level_up_modal_enter_target_2: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_2: level_up_modal_enter_target_2: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_enter_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_enter_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_1_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_1_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_2_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_2_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_3_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_3_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_4_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_4_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_5_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_5_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_6_target_3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: level_up_modal_step_6_target_3: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_3: Did not reach finish_level_up_return_to_game for level 3 within modal step budget; transcript=[{'step': 'enter_level_up', 'action': 'CHOICE:level_up_now', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_1', 'action': 'CHOICE:choose_champion', 'choice_ids': ['level_up_now', 'adjust_archetype', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_2', 'action': 'CHOICE:adjust_archetype', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_3', 'action': 'CHOICE:choose_champion', 'choice_ids': ['level_up_now', 'adjust_archetype', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_4', 'action': 'CHOICE:adjust_archetype', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_5', 'action': 'CHOICE:choose_champion', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_6', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'choose_champion', 'choose_battle_master', 'choose_eldritch_knight', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}]
- level_up_to_4: level_up_modal_enter_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_enter_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_1_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_1_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_2_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_2_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_3_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_3_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_4_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_4_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_5_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_5_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_6_target_4: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: level_up_modal_step_6_target_4: polled campaign state has level-up planning choices without a paired rewards_box.level_up_available=true
- level_up_to_4: Did not reach finish_level_up_return_to_game for level 4 within modal step budget; transcript=[{'step': 'enter_level_up', 'action': 'CHOICE:level_up_now', 'choice_ids': ['level_up_now', 'apply_asi_str', 'apply_asi_con', 'apply_feat_gwm', 'apply_feat_sentinel', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_1', 'action': 'CHOICE:apply_asi_str', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_2', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'apply_asi_str', 'apply_asi_con', 'apply_feat_sentinel', 'apply_feat_tough', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_3', 'action': 'CHOICE:apply_asi_str', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_4', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'apply_asi_str_20', 'apply_asi_dex_14', 'choose_feat_gwm', 'choose_feat_sentinel', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_5', 'action': 'CHOICE:apply_asi_str_20', 'choice_ids': ['level_up_now', 'adjust_level_up_choices', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}, {'step': 'level_up_step_6', 'action': 'CHOICE:adjust_level_up_choices', 'choice_ids': ['level_up_now', 'apply_asi_str', 'apply_asi_con', 'choose_feat_gwm', 'choose_feat_sentinel', 'continue_adventuring', 'finish_level_up_return_to_game'], 'has_planning_block': True}]

## Follow-up Items
<!-- Add any follow-up items, TODOs, or observations here -->

## Additional Context
<!-- Add any additional context that helps understand this test run -->
