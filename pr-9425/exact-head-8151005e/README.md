# PR #9425 exact-head real AGY anchor evidence

This bundle records one real local-stack browser run at exact commit
`8151005e282e3aa4337df9aafe50338f1ca0e7f0`.

## Claim

A uniquely identified sentence remains in place while a tall active streaming
entry completes into structured debug information and exactly four choices.

## Environment

- Repository: `jleechanorg/worldarchitect.ai`, PR #9425
- Worktree: `/Users/jleechan/projects/worktree_misc_p0`
- Server: testing_ui local server on an automatically selected free port
- Browser: headless Chromium 149.0.7827.55, 1280x720
- Persistence: real Firestore through the repository test-auth path
- Generation: real AGY provider (`gemini-3-flash-preview`)
- Network/API mocking: none
- Execution path: streaming

## Result

- rAF samples: 470; resolved samples: 470
- Maximum and final sentence drift: 0.0625px (limit 2px)
- Unique sentence match count: 1
- Final choices: 4; debug UI: visible
- Stream errors: none
- Served `app.js` SHA-256: `c3dddce95d1869c6741b4a7417e3f0aab6e5ca501ddcd5909ae98788fd20d701`
- Git `HEAD:mvp_site/frontend_v1/app.js` SHA-256: same value

## Files

`artifacts/real_agy_anchor_result.json` is the primary machine result.
`artifacts/streaming_execution_trace.json` contains every captured frame sample.
`artifacts/raw_request_payload.json` and `artifacts/raw_response_text.txt`
preserve the provider request/response captured by the harness.
`artifacts/llm_request_responses.jsonl` and `artifacts/request_responses.jsonl`
index those same full payloads as machine-readable LLM and local HTTP pairs.
`artifacts/exact_head_real_agy.mp4` is the captioned derivative and
`artifacts/exact_head_real_agy.webm` is the Playwright source recording;
`artifacts/exact_head_real_agy.vtt` is the subtitle sidecar. The recording is
headless/page-only and has an on-page exact-head badge; it does not include
browser chrome or a URL bar, so it is supplemental visual evidence rather than
strict URL-bar evidence.

The single checksum manifest is `checksums.sha256` at the bundle root.

The reported streaming digest has `signed: false`; this bundle does not claim
cryptographic signature verification. The HTTP pair contains the final done
payload, while raw intermediate SSE chunk bytes were not captured.
