# Share-link field round-trip — testing_mcp real-server evidence

**PR:** #8794 (feat/campaign-share-url-phase1)
**Test:** `testing_mcp/test_share_token_real_e2e.py`
**Git SHA at capture time:** `268d228768a1580915720e50eef867ec6dae2a71` (final
verification run, after `ruff format` was applied to the test file; the
`b4c777cb23` parent SHA is where the same 12-step PASS was first captured
byte-for-byte, before formatting)
**Captured:** 2026-08-10T06:58:06Z final run (first successful capture:
2026-08-09 23:48 local / 2026-08-10T06:49:35Z)
**Result:** PASS — all 12 steps, zero mocking, reproduced twice.

## What this proves

Commit `d31c833c53` made `firestore_service.create_campaign()` persist
`character`, `setting`, `description`, and a server-derived `campaign_type`
onto the campaign doc. This bundle proves the *entire* chain end-to-end
against real services, for **both** campaign types the server can produce:

1. Real `POST /api/campaigns` (real Firebase auth bypass headers, real
   Firestore, real LLM for the custom campaign) creates the campaign.
2. A **read-only** Firestore Admin SDK `get()` (never a write) confirms
   `character`/`setting`/`description`/`campaign_type` were persisted
   verbatim by that exact code path.
3. Real `POST /api/campaigns/<id>/share-token` mints a token.
4. Real `GET /api/shared/<token>` returns the whitelisted public payload —
   the shared fields are present and correct, and
   `owner_id`/`owner_email`/`user_id`/`initial_prompt`/`selected_prompts`
   are absent.
5. Real `GET /shared/<token>` HTML landing page — the "Play in this world"
   anchor's `/new-campaign?...` query string is parsed (after HTML-unescaping
   `&amp;` → `&`, since `markupsafe.escape()` encodes the href) and carries
   title/character/setting/description/source/author/**type**.
6. Real `GET /new-campaign?...` + the `campaign-wizard.js` bundle confirm the
   play link is actually consumable by the wizard page
   (`applyUrlParams`/`URLSearchParams` wiring present).

**Both campaign types are covered end-to-end**, not just unit-tested:

| | Campaign A | Campaign B |
|---|---|---|
| Character | "Lyra the Wayfarer" | "Ser Arion" (canonical) |
| Setting | "Astral Sea — a haunted floating citadel" | canonical Dragon Knight setting |
| Path taken | Real LLM opening-story generation (via AGY CLI provider, `gemini-3.6-flash-high`) | Production Dragon Knight template fast path (`get_dragon_knight_template_opening_if_applicable`) — skips the redundant LLM call because the request byte-for-byte matches the canonical template's `selected_prompts`/`custom_options`/prompt hash. This is a production optimization, not a test shortcut: it still runs the full real `POST /api/campaigns` → `create_campaign_unified` → `firestore_service.create_campaign` code path. |
| `campaign_type` persisted | `"custom"` | `"dragon-knight"` |
| Play URL `type=` | `custom` | `dragon-knight` |

Server log confirms the real LLM call for Campaign A
(`Calling LLM API: 341291 characters (~85322 tokens)`, `AGY_PROVIDER_ENABLED
active - using agy CLI provider client`) and confirms Campaign B took the
template fast path (`Using pre-generated Dragon Knight template opening
(skipping get_initial_story LLM)`) — see `server_log_excerpt.txt` in this
directory.

## A real bug this test found (and fixed) in the pre-existing coverage

The pre-existing version of `test_share_token_real_e2e.py`:
1. Wrote the source campaign directly to Firestore via `doc.set()`, bypassing
   `firestore_service.create_campaign()` entirely — it could not prove the
   thing that actually broke (the persistence added in `d31c833c53`).
2. Checked the public payload against a `safe_fields` set that did **not**
   include `"campaign_type"`. Once `campaign_type` started being persisted
   and returned, that check would have false-flagged it as a **leaked
   forbidden field** and failed the test — the exact opposite of what the
   feature intends. Fixed here by adding `"campaign_type"` to `safe_fields`
   and asserting its value explicitly for both campaign types.

## Files in this bundle

- `http_request_responses.jsonl` — every real HTTP request/response pair
  (method, URL, request headers minus content-type, request body, status,
  response body) captured in call order. 12 real HTTP calls: 2×
  `POST /api/campaigns` (201), 3× `POST .../share-token` (200, 200, 403),
  2× `GET /api/shared/<token>` (200), 2× `GET /shared/<token>` HTML (200),
  1× `GET /new-campaign?...` (200), 1× `GET /frontend_v1/js/campaign-wizard.js` (200).
- `firestore_readback.json` — the real Firestore doc read-back for both
  campaigns (`character`/`setting`/`description`/`campaign_type`), fetched
  via a read-only Admin SDK `get()` against `worldarchitecture-ai`.
- `play_url_analysis.json` — the parsed (HTML-unescaped) query params from
  each campaign's "Play in this world" href.
- `summary.json` — pass/fail + step list, same as stdout.
- `server_log_excerpt.txt` — the real local-server log lines proving
  Campaign A took the real AGY-provider LLM path and Campaign B took the
  Dragon Knight template fast path (see "What this proves" above).

## Exact commands (reproduce)

```bash
# Source the AGY runtime env (mandatory default LLM provider per
# testing_mcp/CLAUDE.md — never Gemini-SDK direct, never mocked).
source "$HOME/.cache/worldai/agy-clean-home-v1/worldai-agy.env"

# Start the real local server on the port dedicated to this lane (8182 —
# never 8181/8183, which belong to the sibling testing_ui lane's takeover
# session on this same branch). WORLDAI_USE_RELOADER=false is required —
# see Limitations below.
PYTHONPATH="$(pwd):$(pwd)/mvp_site" \
PORT=8182 TESTING_AUTH_BYPASS=true ALLOW_TEST_AUTH_BYPASS=true \
WORLDAI_USE_RELOADER=false \
GOOGLE_APPLICATION_CREDENTIALS="$HOME/serviceAccountKey.json" \
python3 mvp_site/main.py serve

# In another shell, run the test:
source "$HOME/.cache/worldai/agy-clean-home-v1/worldai-agy.env"
PYTHONPATH="$(pwd):$(pwd)/mvp_site" \
MCP_SHARE_ROUNDTRIP_BASE_URL="http://localhost:8182" \
WORLDAI_GOOGLE_APPLICATION_CREDENTIALS="$HOME/serviceAccountKey.json" \
python3 testing_mcp/test_share_token_real_e2e.py
```

Observed output:

```json
{
  "passed": true,
  "errors": [],
  "steps": [
    "create_campaign_a_custom_real_llm",
    "create_campaign_b_dragon_knight_fast_path",
    "firestore_readback_verified_both_types",
    "mint_token_a",
    "remint_a_returns_same_token",
    "cross_owner_rejected",
    "public_payload_a_whitelisted_and_typed",
    "play_url_a_type_custom_verified",
    "mint_token_b",
    "public_payload_b_typed_dragon_knight",
    "play_url_b_type_dragon_knight_verified",
    "wizard_html_consumes_play_url"
  ]
}
```

## Limitations / honest gaps

- **No streaming claim.** `POST /api/campaigns` has no streaming variant in
  production — the opening-story generation is a single-shot call, not the
  `/interaction/stream` gameplay-turn endpoint the repo's "streaming is
  primary" policy targets. That policy is N/A here by design, not skipped.
- **`WORLDAI_USE_RELOADER=false` was required, not optional.** The first run
  attempt (reloader left at its `true` default) failed with
  `RemoteDisconnected('Remote end closed connection without response')`
  mid-LLM-call. Root cause, confirmed in the server log: Flask's debug
  auto-reloader watches the *entire* repository tree, including
  `testing_ui/`; a concurrent edit by the sibling lane
  (`testing_ui/test_share_link_login_redirect_e2e.py`) triggered
  `Detected change in ... reloading`, which killed the in-flight request.
  This is an operational finding about running a dev server with the
  default reloader inside a shared, concurrently-edited worktree — not a
  bug in the share-link feature itself, and not a workaround that touches
  any mock/test-mode flag.
- **Two `AGY_PROVIDER_ENABLED active` log lines appear for one LLM call.**
  Gemini's function-calling flow makes two round trips (tool-call turn +
  final-response turn) within the single Campaign A creation request; this
  is normal AGY/Gemini tool-calling behavior, not two separate LLM calls or
  two campaigns hitting the LLM (Campaign B's log line confirms it took the
  template fast path and never called `get_initial_story`).
- **`campaign_type` is asserted for exactly the two values the server
  currently derives** (`"custom"`, `"dragon-knight"`) — there is no third
  type in the current implementation to cover.
- **The real AGY LLM call is contention-sensitive on a busy host.** A
  formatting-only rerun (after `ruff format`, no logic change — confirmed
  via `py_compile` + `ruff check`) hit `TimeoutError('timed out')` at the
  240s timeout then in effect, because 6+ other `agy.real` CLI processes
  from unrelated concurrent sessions were competing for CPU on this
  machine at the time (`ps aux | grep agy` at the time of the failure
  showed 6 long-running `agy.real` processes from other sessions). The
  request was not stuck — the AGY subprocess was still alive and working
  server-side when the client gave up. Fixed by raising the default
  `_create_campaign_via_api` timeout to 500s (still under the repo's
  documented 600s request-timeout standard) and rerunning; the third run
  passed all 12 steps and is the evidence bundle currently on disk. This is
  a documented, load-dependent characteristic of the AGY CLI provider
  (`.claude/CLAUDE.md` already notes 60-90s subprocess overhead per call
  even uncontended), not a defect in the code under test.
