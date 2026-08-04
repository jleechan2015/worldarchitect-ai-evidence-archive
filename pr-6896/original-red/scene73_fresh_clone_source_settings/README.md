# PR #6896 Original Scene 73 Red Repro

This directory contains the real red repro for the original user-visible bug in PR #6896: old-turn/stale-input narrative contamination at Scene 73.

## Source and clone

- Source campaign: `7KeJUkLioKDFBJiAgCks` (`jleechan@gmail.com`)
- Test UID: `0wf6sCREyLcgynidU5LjyZEfm7D2` (`jleechantest@gmail.com`)
- Fresh repro clone: `8rWDIkXDgGdG1DZaffPT`
- Generated bad replay doc: `iMIHO17SCaRIUNf6NYLq`
- Remote app: `https://mvp-site-app-dev-i6xf2p72ka-uc.a.run.app`

## Matched source conditions

- `llm_provider=gemini`
- `gemini_model=gemini-3.5-flash`
- `pre_spicy_model=gemini-3.5-flash`
- `spicy_mode=false`
- `mode=character`
- Agent/model observed in result: `DialogAgent`, `gemini-3.5-flash`, streaming path

## Replayed input

```text
have someone keep tailing grog mar, assess prisoners to see if any breeders, then do this Return to the Silvershield Annex: Escort Duke Ravengard back to your safehouse to finalize and sign the Joint Defense Pact in absolute security.
```

## Failure reproduced

The replay generated doc `iMIHO17SCaRIUNf6NYLq` with stale structured input:

```text
tie up prisoners, fully loot them, draft treaty now and use my full cha and beauty and bardic insp for treaty, requisition contraband
```

The narrative follows that stale prior-turn thread by focusing on scows/contraband, fully looting prisoners, and inventing a viable quartermaster breeder. It omits the requested Grog-Mar tailing flow and contradicts the requested prisoner assessment.

## Artifacts

- `run.json` - summarized repro metadata and pass/fail analysis.
- `raw/remote_replay_result.json` - raw stream/done payload, including raw model response text.
- `raw/pre_replay_firestore_snapshot.json` - Firestore snapshot before replay.
- `raw/post_replay_firestore_snapshot.json` - Firestore snapshot after replay.
- `campaigns/original_red_repro_campaign_8rWDIkXD.txt` - full human-readable campaign export.
- `campaigns/original_red_repro_campaign_8rWDIkXD.md` - same full campaign export wrapped as Markdown.
- `campaigns/original_red_repro_campaign_8rWDIkXD_game_state.json` - exported game state after replay.

## Boundary

This proves the original red failure. It does not prove the current PR fixes it. A green run for this exact reproduced scenario is still required before PR #6896 can claim to fix the original old-scene/stale-input bug.
