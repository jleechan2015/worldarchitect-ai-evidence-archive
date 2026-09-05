# Methodology: PR #9087 HTML cache-control

- Exact checkout SHA: `300878325227b2b940081305351e38326960ce29`
- Checkout ref: `codex/pr9087-evidence-preflight`
- Registered upstream: `origin/feat/html-nocache-query`
- `/health.git_commit`: `300878325227b2b940081305351e38326960ce29` (exact match)
- Layer: real-browser Playwright against the locally started server
- Viewports: desktop 1440x900 and mobile 375x812
- Scenarios: `?nocache=1`, empty `?nocache=`, `?cb=<token>`, and baseline `/`
- Browser media: fresh WebM recordings with same-run `.vtt` caption sidecars
- Post-run publication media: captioned MP4 and GIF derivatives plus VTT/SRT
  sidecars generated from those immutable same-run WebM sources; this does not
  execute the evidence scenario again.
- Node runtime preflight: `<USER_HOME>/.nvm/versions/node/v22.22.0/bin/node`
  (`v22.22.0`).
- Invocation environment explicitly removed `MOCK_SERVICES_MODE`, `TEST_MODE`,
  `USE_MOCK_FIREBASE`, `USE_MOCK_GEMINI`, `SMOKE_TOKEN`, and
  `WORLDAI_MOCK_MODE`; the harness started the real local Gunicorn server and
  real headless Chromium.
- Seal: `checksums.sha256` is generated after all reports and media exist and is
  verified before this run returns.
- Publishable JSON records `credentials_configured` only; credential paths are
  never emitted.
- Deterministic supporting command: `./venv/bin/python -m pytest -q
  testing_ui/test_pr9087_harness_contracts.py` completed 22/22 PASS at the exact
  SHA. Its asciinema cast, raw transcript, captioned GIF/MP4/VTT/SRT, and
  inspection frames are included under `artifacts/`.

The run is valid only when every scenario predicate passes, every recorded WebM
has a non-empty caption sidecar, and the aggregate checksum manifest verifies.

## Request, cache, and connection controls

- This is a behavior test, not a latency or performance measurement. There was
  no timed warm-up population; the harness waited for `/health` before the
  first scenario.
- Every scenario used a newly created Playwright browser context. Persistent
  browser-cache reuse across contexts or processes was intentionally out of
  scope.
- After the browser flow, the harness issued one independent
  `urllib.request.Request`/`urlopen(..., timeout=600)` GET for each of the four
  root URLs. The recorded responses all reported `Connection: close`; no
  keepalive or connection reuse was claimed.
- `artifacts/http_request_responses.jsonl` retains URL, status, and response
  headers only. It does not retain HTML bodies, request-method fields, or
  separate app/settings asset exchanges.
- The Settings URL/status fields in `run.json` came from Playwright's
  `page.expect_response` and the executing app script's `data-settings-src`.
  They are structured browser receipts, not standalone raw HTTP traces.
- The browser used `test_user_id=pr9087-cache-evidence` with the repository's
  test-auth bypass. Mock-service environment flags were disabled, and the flow
  performed no campaign write. This does not establish a real Firebase login.
- Headless Playwright records the page viewport, not browser chrome. The
  existing route captions are explicit, but the videos do not show an actual
  browser URL bar and therefore remain partial under the strict UI-video rule.
- A bounded visual-only remediation used Aside CLI `1.26.810.1915`: account
  transport was signed in, Aside attached to the exact local route, and local
  `/health` returned the full tested SHA. macOS CoreGraphics nevertheless
  reported every on-screen Aside window with `sharing_state=0`, while native
  `screencapture -l <window-id>` returned `could not create image from window`.
  The attempt did not rerun the four-scenario harness, call an LLM/provider, or
  synthesize browser chrome. The raw sanitized diagnostics are retained as
  `artifacts/aside_*`.

The raw Playwright recordings begin before navigation. Publication MP4/GIF
derivatives trim only the initial blank/loading frames (`0.8s` desktop, `0.4s`
mobile), then burn the scenario route/header/token/SHA captions into the pixels.
The source WebM files remain included and unchanged. Extracted first frames and
contact sheets are included for visual inspection.

See `reproduction.md` for the complete clean-computer setup and copy-paste
commands. The browser command intentionally remains a one-shot command: a
failed capture must be investigated, not silently rerun for a passing result.
