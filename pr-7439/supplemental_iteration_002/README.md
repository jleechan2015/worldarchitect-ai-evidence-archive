# PR 7439 Supplemental Evidence - Iteration 002

Collected at 2026-06-11T19:15:39Z for commit `417ec77d278e9de2837d10505220dba66e8153da`.

## Purpose

This supplemental bundle addresses the current-head skeptic evidence blockers from [issue comment 4683970675](https://github.com/jleechanorg/worldarchitect.ai/pull/7439#issuecomment-4683970675):

- Gate 8a: goals proof gap for OpenRouter, OpenClaw, and OpenAI-compatible proxy behavioral goals.
- Gate 8c: red/green provenance gap.

## Files

- `provenance.env` - git/environment provenance for this evidence collection.
- `queries/red_prior_gap_query.sql` and `queries/red_prior_gap_query_result.json` - current BQ readback query for empty `request_json` rows on `gameplay_streaming_proxy`.
- `test_outputs/openrouter_path10_real_bq_adc_attempt.txt` - real OpenRouter call plus real BigQuery insert proof for `extra.path=openrouter_provider.generate_content`; exits 0 and prints `VERDICT: GREEN`.
- `openrouter_path10_real_bq_adc_attempt/result_intermediate.json` - machine-readable OpenRouter path 10 before/after BQ count and sample row.
- `test_outputs/openrouter_path10_real_bq_service_account_attempt.txt` - service-account write attempt; kept as red/provenance because the provider call succeeded but BQ write was denied under that credential.
- `test_outputs/openai_proxy_path8_pytest.txt` - hermetic integration proof for `main.openai_chat_completions` request/response/tokens/user context BQ helper call.
- `test_outputs/openclaw_streaming_bq_pytest.txt` - hermetic integration proof for OpenClaw streaming assembled response text, request payload, suppression, and fail-soft behavior.
- `test_outputs/openai_compatible_providers_bq_pytest.txt` - shared helper/provider proof for OpenRouter/Cerebras/OpenClaw OpenAI-compatible logging fields and suppression.

## Red/Green Notes

Red evidence used for the PR review loop:

- [Current-head skeptic FAIL for this commit](https://github.com/jleechanorg/worldarchitect.ai/pull/7439#issuecomment-4683970675) documents the exact evidence goals that were still failing before this supplemental bundle.
- [Earlier evidence review comment](https://github.com/jleechanorg/worldarchitect.ai/pull/7439#issuecomment-4678107753) documented the original BQ gap: `gameplay_streaming_proxy` rows with populated `response_text` but empty `request_json`.
- `test_outputs/openrouter_path10_real_bq_service_account_attempt.txt` records a red environment attempt where the provider call succeeded but BigQuery insert failed under the local service account.

Green evidence in this bundle:

- OpenRouter real provider + real BQ insert: `test_outputs/openrouter_path10_real_bq_adc_attempt.txt` and `openrouter_path10_real_bq_adc_attempt/result_intermediate.json`.
- OpenAI-compatible proxy path: `test_outputs/openai_proxy_path8_pytest.txt`.
- OpenClaw streaming path: `test_outputs/openclaw_streaming_bq_pytest.txt`.
- Shared OpenAI-compatible provider helper path: `test_outputs/openai_compatible_providers_bq_pytest.txt`.

## Limits

OpenClaw gateway credentials are not set in this environment, so OpenClaw proof is hermetic at the provider seam with network behavior patched. The OpenRouter path has real external provider and real BigQuery proof via local ADC credentials.
