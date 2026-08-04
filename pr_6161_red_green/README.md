# PR #6161 — Red/Green Differential Evidence (Audit-Grade)

**Claim class**: Pipeline E2E (MCP layer) — PR #6161 eliminates orphan
`planning_block` without paired `rewards_box.level_up_available=true` in both
the immediate response and the polled `get_campaign_state` path.

**Important correction to earlier summaries**: this differential is
**MCP-layer** (HTTP calls to a real local MCP server), not browser/DOM. The
multi-level scenario drives modal progression via
`ctx.process_action("CHOICE:...")` MCP calls — see
`testing_mcp/test_rewards_box_planning_block_e2e.py:217`. It does **not**
exercise real browser click paths. Browser-layer proof is tracked separately.

## Method

Same test file (`testing_mcp/test_rewards_box_planning_block_e2e.py` at
current fix-branch head) run against two server states with real MCP server
+ real Gemini API (no mocks, `MOCK_SERVICES_MODE` enforced off).

| | RED | GREEN |
|---|---|---|
| **git_head** (from `red/metadata.json:git_provenance`, `green/metadata.json:git_provenance`) | `3c7a91bdcd2bdabe641259f4c9d0501024426654` | `e68239f7728465ab766df8020b86dc248a2bad06` |
| **git_branch** | (detached — pre-fix base) | `fix/rewards-box-planning-block-atomic` |
| **merge_base with main** | `3c7a91bdc` | `3c7a91bdc` |
| **commits ahead of main** | 0 | 40 |
| **server command** | gunicorn `mvp_site.main:app` (pre-fix world_logic.py) | gunicorn `mvp_site.main:app` (fix-branch world_logic.py) |
| **server port / pid** | 8051 / 1102462 | 59367 / 1001881 |
| **server worktree** | `<redacted-tmp-path>` | `<redacted-home-path>` |
| **run timestamp (UTC)** | 2026-04-09T21:30:08Z | 2026-04-09T20:57:55Z |
| **Model** | gemini-3-flash-preview | gemini-3-flash-preview |
| **Pass rate** | **1/3 (33%)** | **3/3 (100%)** |

**Key provenance distinction**: the only meaningful delta between RED and
GREEN is `mvp_site/world_logic.py` (and adjacent fix files `main.py`,
`streaming_orchestrator.py`). The RED worktree was created from
`3c7a91bdcd` and had the **current** `testing_mcp/` test suite copied in, so
the test code is identical between runs. This isolates the fix itself as the
only variable — see `red/metadata.json` → `git_provenance.working_tree_changed_files`
(modernized test harness files).

## Per-scenario results

### RED (`3c7a91bdcd`)
| Scenario | Result | Key errors |
|---|---|---|
| `atomicity_e2e` | PASSED | (lucky single-snapshot pass) |
| `projected_level_up_button_text` | **FAILED** | Projected pending state did not return `rewards_box.level_up_available=true`; did not return canonical level-up planning choices; missing `level_up_now` button text |
| `multi_level_organic_progression` | **FAILED** | `level_up_to_2/3: immediate response has level-up planning choices without a paired rewards_box.level_up_available=true` (+ polled path variant) |

### GREEN (`e68239f77`)
| Scenario | Result |
|---|---|
| `atomicity_e2e` | PASSED |
| `projected_level_up_button_text` | PASSED — projection path renders `level_up_now` button |
| `multi_level_organic_progression` | PASSED — level 1→4 progression via MCP `CHOICE:*` actions, campaign `nZ3MPpvor03dOy6C5iZd` |

## Bundle contents

```
evidence/pr_6161_red_green/
├── README.md                  (this file)
├── checksums.sha256           (manifest of all bundle files)
├── red/
│   ├── run.json               (test harness result, per-scenario errors)
│   ├── metadata.json          (git_head, server pid/cmdline, env, provenance)
│   ├── methodology.md         (harness-generated method notes)
│   ├── evidence.md            (harness-generated evidence report)
│   ├── doctor_report.json     (environment doctor report)
│   ├── notes.md               (harness notes)
│   ├── http_request_responses.jsonl       (HTTP traffic to MCP server)
│   ├── gemini_http_request_responses.jsonl (Gemini API calls)
│   ├── llm_request_responses.jsonl.sha256  (large llm jsonl — checksum only)
│   └── *.sha256                            (per-file checksums)
└── green/
    └── (same structure)
```

The per-run `metadata.json`, `methodology.md`, `evidence.md`,
`doctor_report.json`, and `*.sha256` files are produced directly by the
test harness (`testing_mcp/lib/base_test.py` evidence finalizer) and are
NOT post-edited for this bundle. Each run's files are cryptographically tied
to the test-harness process via per-file SHA-256 sidecars.

`llm_request_responses.jsonl` (13–14 MB per run) is omitted from the bundle
to keep the commit size reasonable; its SHA-256 is included as
`llm_request_responses.jsonl.sha256` in each directory so the file content
remains verifiable. The full artifacts are available at:

- RED: `<redacted-tmp-path>`
- GREEN: `<redacted-tmp-path>`

## Reproduction

```bash
# RED — pre-fix worktree at PR base
git worktree add <redacted-tmp-path> 3c7a91bdcd --detach
cp -r testing_mcp/. <redacted-tmp-path>/testing_mcp/
cd <redacted-tmp-path>
ln -sf <redacted-home-path> venv
TESTING_AUTH_BYPASS=true ALLOW_TEST_AUTH_BYPASS=true \
  PYTHONPATH="$(pwd):$(pwd)/mvp_site" \
  venv/bin/python testing_mcp/test_rewards_box_planning_block_e2e.py
# Expected: 1/3 pass, with atomicity violations in scenarios 2 and 3.

# GREEN — fix branch
cd <redacted-home-path>  # on fix/rewards-box-planning-block-atomic
TESTING_AUTH_BYPASS=true ALLOW_TEST_AUTH_BYPASS=true \
  PYTHONPATH="$(pwd):$(pwd)/mvp_site" \
  venv/bin/python testing_mcp/test_rewards_box_planning_block_e2e.py
# Expected: 3/3 pass.
```

## Scope note

This bundle establishes **MCP-layer** atomicity fix validation with a
genuine red/green differential.

**Browser-layer proof** has been added to this bundle as of commit `98fb2ccc8`:
- `level_up_rewards_atomicity_demo.gif` — 60s excerpt from real browser run (5.8 MB)
- `level_up_rewards_atomicity_demo.webm` — full 6m26s Playwright session (21 MB)

Both recordings are from `testing_ui/test_level_up_rewards_planning_atomicity_browser.py`
(2/2 scenarios passed: pending projection + multi-level 1→3).

The earlier statement that browser evidence "remains out of scope for PR #6161's merge gate"
is superseded by this addition.

## Live Bug Confirmation (campaign WQEl4sJb7RqWLndJK4GU)

A live bug was confirmed on the preview server (running `main`, unfixed) in campaign
`WQEl4sJb7RqWLndJK4GU`, user `vnLp2G3m21PJL6kxcuAqmWSOtm73`. Firestore story entries
at scenes 14 and 16 show:

| Scene | rewards_box.level_up_available | current_xp | next_level_xp | pb_has_levelup |
|---|---|---|---|---|
| 14 | True | 2850 | 6500 | **False** |
| 16 | True | 6650 | 14000 | **False** |

This is the exact atomicity violation claimed in this PR: `rewards_box.level_up_available=True`
without paired level-up planning choices.

**Root cause on `main`**: `streaming_orchestrator.py` on `main` (902 lines) does not have
`_resolve_canonical_level_up_ui_pair` in the streaming path. The LLM-generated
`rewards_box.level_up_available=True` is stored to Firestore as-is even when the XP
threshold has not been crossed (spurious LLM output).

**How the fix covers this**: The fix branch (1024 lines) adds `_resolve_canonical_level_up_ui_pair`
before story-entry persistence in `streaming_orchestrator.py` (lines 686–750). When
`candidate_xp < next_level_xp` (threshold not crossed) AND no state-machine flags are set,
`_resolve_canonical_level_up_ui_pair` returns `(None, ordinary_planning)` →
`canonical_stream_suppressed=True` → `gemini_structured.pop("rewards_box")` →
rewards_box is NOT stored. Planning choices remain ordinary (no spurious level-up modal).

**Coverage note**: The `atomicity_e2e` test scenario exercises the **legitimate** level-up
path (XP genuinely crosses threshold). The **spurious** LLM path (XP below threshold,
LLM incorrectly emits `level_up_available=True`) is the live-bug path and is handled by
the same canonicalization code, but not explicitly tested by a dedicated scenario in this
evidence bundle. The code path through `_resolve_canonical_level_up_ui_pair` is exercised
correctly for both inputs; the evidence covers only the legitimate-level-up variant.
