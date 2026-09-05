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

The run is valid only when every scenario predicate passes, every recorded WebM
has a non-empty caption sidecar, and the aggregate checksum manifest verifies.

The raw Playwright recordings begin before navigation. Publication MP4/GIF
derivatives trim only the initial blank/loading frames (`0.8s` desktop, `0.4s`
mobile), then burn the scenario route/header/token/SHA captions into the pixels.
The source WebM files remain included and unchanged. Extracted first frames and
contact sheets are included for visual inspection.
