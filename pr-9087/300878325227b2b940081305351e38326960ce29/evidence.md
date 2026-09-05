# Evidence Summary: PR #9087 Page-Level Cache Bust

## Claim -> Artifact Map

| Claim | Evidence Layer | Artifact | Verification Result |
| :--- | :--- | :--- | :--- |
| `?nocache=1` returns HTTP 200 with `no-store, must-revalidate` and `Pragma: no-cache` | [Layer 2 real HTTP] | `artifacts/http_request_responses.jsonl` line 1 | **PASS** (raw root-response headers) |
| `?cb=1788320000` returns HTTP 200 with `no-store, must-revalidate` and `Pragma: no-cache` | [Layer 2 real HTTP] | `artifacts/http_request_responses.jsonl` line 3 | **PASS** (raw root-response headers) |
| Empty `?nocache=` and baseline return HTTP 200 without `no-store` | [Layer 2 real HTTP] | `artifacts/http_request_responses.jsonl` lines 2 and 4 | **PASS** (raw root-response headers) |
| The browser observed the expected executing `app.js?v=` token and one matching Settings-script HTTP 200 response for each scenario | [Layer 2 real-browser receipt] | `run.json` (`asset_url`, `asset_token_match`, `settings_script`) | **PASS WITH LIMIT** (structured Playwright response/DOM receipt; not a standalone raw asset trace) |
| Desktop and mobile Settings transitions are visually reviewable | [Layer 2 real-browser] | `artifacts/desktop-captioned.{mp4,gif,vtt,srt}` and `artifacts/mobile-captioned.{mp4,gif,vtt,srt}` | **PARTIAL** (before/action/after and full SHA are visible, but the headless recording has no browser URL bar) |
| A bounded Aside-first recapture could automate the exact-head local route, but the OS capture layer could not capture genuine browser chrome | [Capture-environment diagnostic] | `artifacts/aside_account_list.txt`, `artifacts/aside_version.txt`, `artifacts/aside_tabs.txt`, `artifacts/aside_health.json`, `artifacts/aside_window_server.txt`, `artifacts/aside_screencapture_errors.txt` | **BLOCKED** (Aside is signed in and the exact route is attached; each on-screen Aside window reports `sharing_state=0`, and native window capture fails) |
| The recorded server process used Gunicorn for `mvp_site.main:app` at the scenario port | [Recorded local process provenance] | `metadata.json`, `artifacts/server_provenance.json`, `artifacts/collection_log.txt` | **PASS WITH LIMIT** (PID/cmdline/ps receipt and listener attestation are present; raw lsof and raw `/health` response files were not retained) |
| Exact-head deterministic focused validation is independently replayable | [Layer 1 deterministic] | `artifacts/terminal.cast`, `artifacts/terminal-transcript.txt`, and `artifacts/terminal-captioned.{gif,mp4,vtt,srt}` | **PASS** (22/22 harness-contract tests; pre/post SHA exact; checkout clean) |
| Published files match the sealed source bytes | [Artifact transport/integrity] | `checksums.sha256` plus sibling `.sha256` files | **PASS** (47/47 substantive files) |

## What This Evidence Proves

1. A real local Gunicorn response returned the recorded active/inactive cache-control headers for the four tested root URLs.
2. Real headless Chromium rendered the campaign page and completed the visible Settings transition at desktop and mobile viewports.
3. The Playwright scenario receipts recorded the expected app token and exact Settings-script URL/status for those four runs.
4. The focused deterministic harness-contract command passed 22 tests at the exact SHA and left the checkout clean.

## What This Evidence Does NOT Prove

1. The raw HTTP artifact does not retain HTML bodies, request methods, or separate app/settings asset exchanges. App and Settings token/status fields are Playwright-derived structured receipts in `run.json`, not independent raw wire rows.
2. It does not prove token sanitization/length-capping, container fallback selection, content-hashed asset handling, or foreign/wrong-path rejection in a real-server scenario.
3. It does not include raw output for the separate Settings-loader Node suite.
4. The browser videos do not include an actual browser URL bar. Route captions are visible but do not satisfy that strict visual invariant. A bounded Aside-first attempt reached the exact-head route, but macOS reported every on-screen Aside window as non-shareable (`sharing_state=0`) and `screencapture` returned `could not create image from window`; no chrome was synthesized.
5. It does not prove CDN, reverse-proxy, persistent cross-process browser cache, deployed Cloud Run edge-cache, campaign, LLM, Firebase-write, or primary-account behavior.
6. The flow uses a dedicated localhost test ID under the repository's test-auth bypass; it does not prove a real Firebase-authenticated user session.
