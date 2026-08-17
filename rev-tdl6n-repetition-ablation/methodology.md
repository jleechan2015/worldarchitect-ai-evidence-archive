# Methodology

## Environment

- Repo: `jleechanorg/worldarchitect.ai`
- Branch: `fix/gemini-code-exec-safety-rev-ac8vk-tdl6n`
- Head SHA: `15192a1eda65d241d10057f81ab71a88d261e60b`
- Python venv: repo-shared venv (`./venv` symlink), `python3 --version` → 3.13.7 (dev harness), server runs under repo's pinned interpreter via `./vpython`
- `GEMINI_API_KEY`: fetched fresh via `gcloud secrets versions access latest --secret=gemini-api-key --project=worldarchitecture-ai` (the env var itself was revoked/rotated 2026-08-17 after a prior leak report — never hardcode it)
- `GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json`, `WORLDAI_DEV_MODE=true` (required — omitting it makes `world_logic.py`'s module-level `clock_skew_credentials.validate_deployment_config()` raise, which the stdlib `LazyLoader` background-warmup thread silently swallows and leaves the module in a broken half-initialized state for the rest of the process's life; every MCP call then fails with `AttributeError: '_LazyModule' object has no attribute ...`)

## Ablation script (primary evidence, breaker OUT of the path)

```bash
export GEMINI_API_KEY=$(gcloud secrets versions access latest \
    --secret=gemini-api-key --project=worldarchitecture-ai)
python3 evidence/rev-tdl6n-repetition-ablation/ablate_repetition_loop.py \
    --reps 11 --out /tmp/rev-tdl6n-ablation.jsonl
```

Ran in 3 batches (1 + 6 + 2 + 2 = 11 total trials across separate invocations
while iterating) — all merged into `results.jsonl`. Each trial is an
independent real HTTP POST to
`https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:streamGenerateContent`.

## Real local server + real MCP evidence (supplementary)

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json
export GEMINI_API_KEY=$(gcloud secrets versions access latest \
    --secret=gemini-api-key --project=worldarchitecture-ai)
export WORLDAI_DEV_MODE=true
export CAPTURE_SYSTEM_INSTRUCTION_MAX_CHARS=15000
export PORT=8018
./vpython mvp_site/main.py serve &
# server healthy at http://localhost:8018

export BASE_URL=http://localhost:8018
python3 testing_mcp/test_combat_agent_real_e2e.py
```

Server PID recorded in `combat_agent_e2e_test.json.provenance.server`; killed
by exact recorded PID after capture (not by pattern), per the evidence-standards
cleanup-discipline rule.

## Local gate-script mirrors (operator directive: local runs satisfy Gate 1
## when the self-hosted CI fleet is backlogged, provided they mirror the
## workflow's actual command)

```bash
$ python3 scripts/validate_prompt_tool_contracts.py
prompt/tool contracts validated
$ echo $?
0

$ python3 scripts/check_function_loc_ratchet.py
function LOC ratchet check passed (no tracked function grew)
$ echo $?
0

$ python3 scripts/check_schema_coverage.py --fail-under 100 \
    --waived-paths-file mvp_site/schemas/game_state_schema_coverage_waivers.txt
Schema coverage check
- code paths: 168
- covered:    168
- missing:    0
- coverage:   100.0%
$ echo $?
0
```

These three scripts are the actual non-advisory CI gates for this PR's file
scope (`mvp_site/prompts/**` → prompt-tool-contract validation and schema
coverage; ruff/mypy are advisory per operator confirmation 2026-08-17).

## Scoped pytest (the specific CI failure this PR fixed, plus this PR's new
## test files)

```bash
$ python3 -m pytest \
    mvp_site/tests/test_code_execution_circuit_breaker.py \
    mvp_site/tests/test_code_execution_circuit_breakers.py \
    mvp_site/tests/test_repetition_guard.py \
    mvp_site/tests/test_gemini_provider_circuit_breaker_wiring.py \
    mvp_site/tests/test_prompts.py \
    mvp_site/tests/test_llm_provider_latency_logging.py -q
Pytest: 251 passed
```

`test_llm_provider_latency_logging.py::TestGeminiLatencyLogging::test_llm_call_logged_on_error`
was the one CI failure on the pre-rebase HEAD (core-mvp-2 shard,
`github.com/.../actions/runs/31999311944/job/95303236395`) — its
blanket-patched `gemini_provider.time` mock didn't configure
`perf_counter.return_value`, so the new circuit-breaker's
`elapsed_seconds = time.perf_counter() - t_request_sent` compared an
unconfigured `MagicMock` against a float and raised `TypeError` before the
test's injected `RuntimeError` ever reached the assertion. Fixed by
configuring `mock_time.perf_counter.return_value = 1.0`, matching the
pattern the file's other (already-passing) tests use.

## Post-/advice-fixup re-verification (head `1199380237a1bfc1aab08900b9aab49e89333543`)

```bash
$ python3 -m pytest \
    mvp_site/tests/test_code_execution_circuit_breaker.py \
    mvp_site/tests/test_code_execution_circuit_breakers.py \
    mvp_site/tests/test_repetition_guard.py \
    mvp_site/tests/test_gemini_provider_circuit_breaker_wiring.py \
    mvp_site/tests/test_prompts.py \
    mvp_site/tests/test_llm_provider_latency_logging.py -q
Pytest: 251 passed

$ python3 scripts/validate_prompt_tool_contracts.py && echo OK
prompt/tool contracts validated
OK
$ python3 scripts/check_function_loc_ratchet.py && echo OK
function LOC ratchet check passed (no tracked function grew)
OK
$ python3 scripts/check_schema_coverage.py --fail-under 100 \
    --waived-paths-file mvp_site/schemas/game_state_schema_coverage_waivers.txt
coverage: 100.0%

$ python3 evidence/rev-tdl6n-repetition-ablation/ablate_repetition_loop.py \
    --reps 5 --out /tmp/rev-tdl6n-ablation-postfix.jsonl
# 5/5 FinishReason.STOP, max_consecutive_line_repeat=2 in all 5
# saved to results_postfix_confirmation.jsonl in this directory
```

## Cross-worktree caveat (transparency)

An earlier local full-suite run (`./run_tests.sh --test-dirs=mvp_site
--parallel --exclude-integration --exclude-mcp --include-end2end`) collided
with a second, independently-started instance of the same command in the
same worktree (both bound to worktree-derived ports/temp dirs) and produced
a false "0.0% success rate / 590 failed / all-timeout" result. That result is
discarded — it is a resource-contention artifact (confirmed by every failure
reading `(timeout)`, not a real assertion failure), not a signal about this
branch. The scoped pytest run above (clean, single-process) is the trustworthy
local signal; CI's own sharded run is the authoritative full-suite signal.
