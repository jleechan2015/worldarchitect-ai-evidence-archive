# PR #6896 Original Bug Repro Criteria - Awaiting Human Sign-off

## GOAL

Define the exact pass/fail criteria for reproducing the original Scene 73 bug before running any more repro attempts.

## MODIFICATION

This document records the required observable phenotype, required artifacts, falsifiers, and non-qualifying related failures for the original bug.

## NECESSITY

The previous evidence was mislabeled: it showed related stale-input/stale-context behavior, but not the original obvious repeated-narrative symptom. This criteria file prevents another weaker artifact from being called the original repro.

## INTEGRATION PROOF

Future `/repro` evidence for PR #6896 must reference this file and fill out the verdict table below before claiming success.

## Source bug

- Source campaign: `7KeJUkLioKDFBJiAgCks`
- Source account: `jleechan@gmail.com`
- User-visible bug scene: Scene 73
- Original bad AI doc: `ETxMDfWxYLzVSacRQYnk`
- Immediate Scene 73 user input:

```text
have someone keep tailing grog mar, assess prisoners to see if any breeders, then do this Return to the Silvershield Annex: Escort Duke Ravengard back to your safehouse to finalize and sign the Joint Defense Pact in absolute security.
```

## Required original phenotype

A successful red repro must occur in a newly copied campaign, not the original source campaign, and must show obvious repeated old narrative in the newly generated Scene 73-equivalent AI response.

Required visible symptoms:

- The new copied campaign has a newly generated AI response after the replayed Scene 73 input.
- The new response visibly repeats substantial narrative text from earlier campaign scenes.
- The repeated text is traceable to earlier source/copy story docs by doc ID and matching text spans.
- The repeated narrative is user-visible in the full human-readable campaign export.
- The repeated narrative causes the turn to fail to cleanly advance from the replayed Scene 73 input.

Known original repeated narrative anchors:

- Prior Annex/Ravengard arrival block from doc `y25jgAkHrBJMFzCSCTZy`, visible again in original bad doc `ETxMDfWxYLzVSacRQYnk`.
- Prior dockworker/Grog-Mar block from doc `D1OVbe5UUx7ThFjV2ynJ`, visible again in original bad doc `ETxMDfWxYLzVSacRQYnk`.

## Required setup

- Copy source campaign `7KeJUkLioKDFBJiAgCks` to `jleechantest@gmail.com` / UID `0wf6sCREyLcgynidU5LjyZEfm7D2`.
- Use a fresh test clone for each serious attempt, or prove the test clone was restored to the exact pre-Scene-73 boundary.
- Do not mutate the read-only baseline clone.
- Align source-relevant runtime settings unless deliberately testing a mismatch:
  - `llm_provider=gemini`
  - `gemini_model=gemini-3.5-flash`
  - `pre_spicy_model=gemini-3.5-flash`
  - `spicy_mode=false`
  - `mode=character`
- Replay the exact Scene 73 input above.

## Required artifacts

- New copied campaign ID.
- New generated AI doc ID.
- Full human-readable campaign export for the copied campaign.
- Raw request/response or stream result for the replay.
- Firestore pre/post snapshots for the copied campaign.
- Prior source/copy doc IDs that contain the repeated text.
- Matching-span evidence showing repeated narrative text from earlier docs appears in the new generated response.
- Verdict table completed with `REPRO`, `RELATED`, or `NON-REPRO`.

## Falsifiers

Any of these means the original repeated-narrative bug was not reproduced:

- The new response is fresh prose with no substantial repeated old narrative.
- Only `action_resolution.player_input` is stale.
- Only location, planning block, or game state is stale.
- The response follows the wrong old action thread but does not visibly repeat prior narrative text.
- The repeated text is found only in the original source campaign, not in the new copied campaign response.
- The evidence does not identify earlier doc IDs and matching spans.

## Related but insufficient findings

These are useful debugging signals but do not satisfy the original repro:

- Stale `action_resolution.player_input`.
- Fresh prose generated from stale prior context.
- Wrong thread continuation, such as tie/loot/requisition instead of Grog-Mar tailing.
- Contradicting the user input by inventing a breeder prisoner.
- Location mismatch or location concatenation.

## Verdict table template

| Original required symptom | New copied-run observation | Evidence file / doc ID | Verdict |
|---------------------------|----------------------------|------------------------|---------|
| New copied campaign, not source | | | |
| Exact Scene 73 input replayed | | | |
| New AI response generated after replay | | | |
| Visible repeated old narrative appears | | | |
| Repeated text mapped to earlier doc IDs | | | |
| Full human-readable export shows the repeat | | | |
| Raw captures/snapshots attached | | | |

## Human sign-off

Do not run another repro attempt until Jeffrey signs off on these criteria or edits them.
