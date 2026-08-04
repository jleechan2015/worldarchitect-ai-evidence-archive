# Methodology: Combat Rewards Level-Up Test

## Test Type
Real API test against MCP server (not mock mode).

## Purpose
Validates that when combat ends and XP is awarded, the LLM:
1. Sets combat_summary with xp_earned
2. Detects that XP crosses level threshold
3. Offers level-up to the player

This is the PRIMARY path for level-up detection - LLM should handle this
directly without needing server-side fallback.

## Test Steps
1. Seed character at level 1 with 250 XP (50 below level 2 threshold of 300)
2. Initiate combat against weak enemy (goblin = ~50 XP)
3. Continue combat until enemy defeated
4. Verify combat_summary.xp_earned is set
5. Verify level-up is offered (rewards_pending or narrative)

## Pass Criteria
- Combat ended successfully
- XP was awarded (in combat_summary, narrative, or state)
- Level-up was detected (rewards_pending.level_up_available, narrative mention, or level increased)
