# Evidence for PR #7372 (BigQuery LLM Call-Sites Wiring)

## Current-Head Real-Service Evidence (2026-06-12)

PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7372

Commit: `f1847a8ac5e3455235e004e14d192b0e0761a933`

Worktree: `/Users/jleechan/.gemini/antigravity-cli/brain/de73e324-1703-43de-b447-568c174f117b/.system_generated/worktrees/subagent-PR-7372-Fixer-PR-7372-Fixer-f2699cb1`

Evidence bundle: `/tmp/worldarchitect.ai/fix_bq-logging-wire-call-sites/bq_logging_real_llm_real_user_e2e/iteration_003`

Temporary BigQuery dataset: `worldarchitecture-ai.llm_forensics_pr7372_evidence_20260612`

Dataset TTL: 1 day

### What Was Proven

This evidence replaces the prior mock/disk-mirror-only evidence. It used:

- live Flask server at `http://127.0.0.1:9417`
- real `/api/campaigns` create route
- real `/api/campaigns/<campaign_id>/interaction` route
- real Gemini provider path (`gemini-3-flash-preview`)
- real BigQuery REST `insertAll` rows in `worldarchitecture-ai`

The scenario passed:

- HTTP create campaign: `201`
- HTTP interaction: `200`
- BigQuery `llm_payloads` rows found: `3`
- BigQuery `log_events` rows found: `1`
- campaign id: `gRvdqQ65gOyfU0ddDn4M`
- evidence user id: `pr7372-real-bq-user-20260612`

### Key Bundle Files

- `metadata.json` records git SHA, server PID/process command, dataset, and env.
- `run.json` records the scenario result and BigQuery row summaries.
- `bq_query_results.json` contains the BigQuery query result excerpts.
- `http_request_responses.jsonl` contains the local route request/response evidence.
- `.sha256` files verify every artifact.

### Local Verification Commands

```bash
TESTING_AUTH_BYPASS=true ALLOW_TEST_AUTH_BYPASS=true \
  BQ_LOGGING_PROJECT=worldarchitecture-ai \
  BQ_LOGGING_DATASET=llm_forensics_pr7372_evidence_20260612 \
  BQ_LOGGING_TTL_DAYS=1 \
  PORT=9417 \
  python -m mvp_site.main serve
```

The evidence driver then created a campaign, sent one interaction, and queried:

```sql
SELECT ingested_at, campaign_id, user_id, is_test, agent, model, finish_reason,
       LENGTH(request_json) AS request_json_len,
       LENGTH(response_text) AS response_text_len,
       SUBSTR(response_text, 1, 500) AS response_excerpt
FROM `worldarchitecture-ai.llm_forensics_pr7372_evidence_20260612.llm_payloads`
WHERE campaign_id = @campaign_id OR user_id = @user_id
ORDER BY ingested_at DESC
LIMIT 20;
```

```sql
SELECT ingested_at, campaign_id, event_type, level, SUBSTR(message, 1, 500) AS message_excerpt
FROM `worldarchitecture-ai.llm_forensics_pr7372_evidence_20260612.log_events`
WHERE campaign_id = @campaign_id OR fields_json LIKE @campaign_like
ORDER BY ingested_at DESC
LIMIT 20;
```

### Supporting Unit/Integration Checks

The earlier local pytest checks remain supporting evidence only. They are not the primary `/es` proof:

```bash
python3 -m pytest mvp_site/tests/test_bq_logging.py mvp_site/tests/test_bq_logging_integration.py -q
python3 -m ruff check mvp_site/bq_logging.py mvp_site/llm_parser.py mvp_site/llm_service.py mvp_site/world_logic.py mvp_site/tests/test_bq_logging.py mvp_site/tests/test_bq_logging_integration.py
```
