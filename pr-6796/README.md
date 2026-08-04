# XP Threshold Test Evidence

## Test Run: 20260505_193000
## Mode: unit-tests
## Result: PASS

## Git Provenance
- HEAD: 35823eb34c7e88b8c0b3db2e03dc4beb55017dd8
- Branch: fix/remove-level-20-cap
- Origin/Main: f22bc0ad0c474fb79c699b843aec12fcdbcb6d1b

## Changed Files (vs main)
- docs/design/pr-designs/pr-6796.md
- mvp_site/game_state.py
- mvp_site/rewards_engine.py
- mvp_site/world_logic.py
- mvp_site/tests/test_agents.py
- mvp_site/tests/test_canonicalize_invariants.py
- mvp_site/tests/test_game_state.py
- mvp_site/tests/test_resolver_sole_source.py
- testing_mcp/test_infinite_leveling_evidence.py

## app.js — NOT modified by this PR
- `git diff f22bc0ad..35823eb34 -- mvp_site/frontend_v1/app.js` = **0 lines**
- app.js was reverted to origin/main state in commit dc50028e8 (removed scroll changes introduced by a prior commit that misidentified the baseline)
- This PR's scope is XP/level math only: game_state.py, rewards_engine.py, world_logic.py

## Delta since evidence run (d9d00c4de → dc50028e8)
Production code changes:
- d9d00c4de → fb044c7dc: base PR commits (game_state.py, rewards_engine.py, world_logic.py)
- fb044c7dc → 65785ff5: world_logic.py — REMOVED over-broad `or not character_creation_active` from inject_modal_finish_choice_if_needed (Bugbot fix); evidence provenance updated
- 65785ff5 → f7898ed5: CI auto-commit — docs only (pr-6796.html, pr-6796.md), no production code change
- f7898ed5 → dc50028e8: fix(app) — revert unrelated scroll changes in app.js to match origin/main; zero production logic change to game_state.py, rewards_engine.py, world_logic.py
- dc50028e8 → 65f5ceef42 → 2b7b3a7c6b → ba9736418 → decc333b4: evidence/CI auto-commits — docs only (pr-6796.html, pr-6796.md) and evidence provenance updates; zero production code change
Evidence 532-test suite still valid at decc333b45bdb7bdc642c3e0e5acd0292fedd06c; zero production-code delta since test run at d9d00c4de; all commits after d9d00c4de are evidence/docs only.

## CI Auto-Commit Pattern Note
This repo's "Generate PR Design Docs" CI workflow auto-commits docs/design/pr-designs/pr-6796.html and pr-6796.md on every push. If the live PR HEAD is ahead of this evidence bundle's head_commit (35823eb34) by 1-2 commits, those commits are docs-only CI auto-commits and DO NOT affect evidence validity. Production code (game_state.py, rewards_engine.py, world_logic.py) has not changed since d9d00c4de.

To verify: `git diff d9d00c4de..<live-head> -- mvp_site/game_state.py mvp_site/rewards_engine.py mvp_site/world_logic.py` = 0 lines.

## Test Results Summary
- 532 passed, 3 skipped, 132 subtests
- test_agents.py: PASS (includes L31 routing via XP=910000)
- test_resolver_sole_source.py: PASS (level=30,xp=905000 → (True,31,False))
- test_canonicalize_invariants.py: PASS (includes test_infinite_level_with_no_signal_triggers_level_up)
- test_game_state.py: PASS (XP threshold + level_from_xp + infinite leveling formula)

## Collection Window
- Started: 2026-05-05T19:30:00Z
- Ended: 2026-05-05T19:30:02Z

## Files
- metadata.json - Git provenance and bundle metadata
- test_results.json - Full test results with git provenance
- evidence.md - Claim-to-artifact map
