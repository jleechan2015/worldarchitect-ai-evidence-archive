# Evidence bundle for issue #7628

## Files
- `Dragon Knight _7628-repro__ADFQD6bi.txt` — full story transcript (73.9 KB, 30 entries) of the copied campaign `ADFQD6biQFqGEHPaovde`.
- `Dragon Knight _7628-repro__ADFQD6bi_game_state.json` — current game state (58.3 KB).
- `evidence.json` — index of the bug, expected label, prompt spec, server code, screenshot.
- `checksums.txt` — sha256 checksums of the transcript and game state.
- `README.md` — this file.

## Bug evidence (from the transcript at line 806)
The level-up entry choice in `planning_block.choices` is rendered to the player as:
> "Meditate on Your Growth (Level Up) - Take a moment to fully integrate your new power before the Host arrives."

The choice id is `level_up_now` (visible in the transcript line "Player (choice: level_up_now)"). Per `mvp_site/prompts/rewards_system_instruction.md:374` and `mvp_site/rewards_engine.py:2070`, the canonical text for an entry choice with id `level_up_now` is:
> "Level Up to Level <N>"

## Repro recipe
1. Open https://mvp-site-app-s3-i6xf2p72ka-uc.a.run.app/game/7nHHkuGizNDhzgmZEcgQ
2. Replay the campaign to scene 15 — at the start of scene 15 the level-up entry choice is rendered as the long "Meditate" label.
3. After the fix is deployed, replay the same scene on dev preview and confirm the rendered label is `Level Up to Level <N>`.

## Test reference
- `mvp_site/tests/test_world_logic.py:8062-8106` — `TestLevelUpChoiceForcesCharacterCreation` — asserts `"Level Up to Level 2 - Meditate"` in the expanded model context.
- `mvp_site/tests/test_rewards_engine.py:311,403,6280` — use `"Level Up to Level 2"`.
- `mvp_site/tests/test_freeze_time_choices.py:58,262,396,410,645,1025,1033,1054,1067` — use `"Level Up to Level 5"` and `"Level Up to Level 10"`.
