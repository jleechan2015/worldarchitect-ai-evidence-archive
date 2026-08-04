
Single lifecycle scenario `campaign_upgrade_lifecycle_streaming` exercises the
real /interaction/stream endpoint across three sequential turns:
  1. Enter ceremony via choice routing → expect CampaignUpgradeAgent and
     custom_campaign_state.campaign_upgrade_in_progress=True.
  2. Respond to ceremony → expect lock cleared (in_progress=False), agent
     returns to StoryModeAgent (lock-exit transition).
  3. Follow-up action after ceremony with stale campaign_upgrade_completed_tier
     left in state → stale-flag guard must prevent CampaignUpgradeAgent
     re-routing (StoryModeAgent expected).
Each streaming turn emits SSE chunks captured into scenario["details"] so
streaming_evidence.json is populated by the evidence builder.
