# Evidence Summary: PR #9087 Page-Level Cache Bust

## Claim -> Artifact Map

| Claim | Evidence Layer | Artifact | Verification Result |
| :--- | :--- | :--- | :--- |
| `?nocache=1` sets `no-store` on HTML and rewrites anchored app.js | [Layer 2 real-browser] | `run.json` (`desktop_nocache_flag_headers_and_render`) | **PASS** (status=200, token='pr9087-evidence-revision') |
| `?nocache=1` renders desktop viewport | [Layer 2 real-browser] | `artifacts/ui_nocache_desktop_1440x900.png` | **PASS** (1440x900 screenshot captured) |
| `?nocache=` (empty value) is inactive | [Layer 2 real-browser] | `run.json` (`desktop_empty_nocache_inactive`) | **PASS** (`no-store` absent, default caching preserved) |
| `?cb=<token>` rewrites anchored app.js and sets `no-store` | [Layer 2 real-browser] | `run.json` (`mobile_cb_token_headers_and_dom_rewrite`) | **PASS** (`?v=1788320000` expected `1788320000`, `no-store` confirmed) |
| `?cb=<token>` renders mobile viewport | [Layer 2 real-browser] | `artifacts/ui_cb_mobile_375x812.png` | **PASS** (375x812 screenshot captured) |
| Baseline `/` does not set `no-store` | [Layer 2 real-browser] | `run.json` (`desktop_baseline_no_cache_bust`) | **PASS** (`no-store` absent, un-busted request) |
| Harness server command, ps receipt, and listener ownership | [Local process provenance] | `artifacts/server_provenance.json` | **PASS** (Gunicorn app/bind command and port listener tied to PID after `/health`) |
| SPA settings action loads the executing app's same-origin settings asset | [Layer 2 real-browser] | `run.json` (`settings_script`) | **PASS** (HTTP 200, exact declared asset URL, no foreign/duplicate response) |
| Desktop and mobile before/action/after transitions are publicly reviewable | [Layer 2 real-browser] | `artifacts/desktop-captioned.{mp4,gif,vtt,srt}` and `artifacts/mobile-captioned.{mp4,gif,vtt,srt}` | **PASS** (same-run WebM derivatives, route/header/token/SHA captions, non-blank first frames) |
| The one-shot driver execution is preserved without credentials or host paths | [Local execution provenance] | `artifacts/collection_log.txt` | **PASS** (sanitized stdout/stderr; 4/4 final result) |

## What This Evidence Proves
1. Real Playwright headless Chromium against the live running server receives `Cache-Control: no-store, must-revalidate` and `Pragma: no-cache` when `?nocache=1` or `?cb=<token>` is passed.
2. The anchored `/frontend_v1/app.js` DOM asset has the expected `?v=` token for both cache-bust modes.
3. An empty `?nocache=` query parameter is strictly treated as inactive and does not bust cache.
4. Standard requests without `?cb=` or `?nocache=` remain untouched (no regression to default caching).
5. Visual rendering across desktop (1440x900) and mobile (375x812) viewports is completely intact and functional.
6. Every desktop/mobile claim includes a before/action/after ledger with the
   exact checkout SHA, SPA `/settings` URL, and fresh screenshot/video
   artifacts with caption sidecars.

The result above is a claim only for scenarios whose recorded predicate is
`PASS`; stale media is removed before each run.

## What This Evidence Does NOT Prove

1. It does not prove CDN, reverse-proxy, browser-cache persistence across
   separate processes, or deployed Cloud Run edge-cache behavior.
2. It does not prove behavior for query values beyond the four recorded
   scenarios: `nocache=1`, empty `nocache=`, `cb=1788320000`, and baseline.
3. It does not prove campaign, LLM, Firebase-write, or primary-account behavior;
   this cache-control flow uses a dedicated localhost test identity and performs
   no campaign mutation.
