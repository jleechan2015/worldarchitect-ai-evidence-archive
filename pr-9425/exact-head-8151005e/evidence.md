# PR #9425 exact-head real AGY evidence

Verdict: **PASS for the covered real-local-stack active-entry completion
invariant.**

| Claim | Artifact | Result |
|---|---|---|
| Exact application and served asset | `artifacts/exact-head.txt`, `artifacts/git_app_asset_sha256.txt`, `artifacts/real_agy_anchor_result.json` | HEAD `8151005e...`; served and Git app.js both `c3dddce9...` |
| Sentence stays fixed through completion | `artifacts/real_agy_anchor_result.json`, `artifacts/streaming_execution_trace.json` | 470/470 resolved rAF samples; max/final drift 0.0625px |
| Structured completion rendered | `artifacts/anchor_metrics.json` | Four choices, debug visible, no event errors |
| Real provider and persistence path | `artifacts/response_provenance.json`, `artifacts/raw_request_payload.json`, `artifacts/raw_response_text.txt`, `artifacts/llm_request_responses.jsonl`, `artifacts/request_responses.jsonl`, `artifacts/server-proof.log` | AGY streaming, test-auth Firestore campaign, full captured request/response payloads |
| Visual continuity | `artifacts/exact_head_real_agy.mp4`, `.webm`, `.vtt`, and `artifacts/video_frames/` | Exact-head badge, timestamped page-load, reading, completion, and settled frames |
| Requested cmux terminal surface | `artifacts/cmux-terminal-proof.txt` | Literal `cmux capture-pane --surface surface:79 --scrollback`; runner exit 0; transcript retained as supplemental terminal evidence |

## Scope boundary

This bundle proves one real local-stack headless Chromium scenario. It does not
claim production deployment or cross-browser behavior. The page-only recording
does not include a browser URL bar and is supplemental rather than strict
URL-bar visual evidence.

The provider response contains `streaming_response_signature.signed: false`.
The digest is preserved as server-reported metadata, not presented as an
independently verified cryptographic signature. The HTTP trace captures the
complete final done payload; raw intermediate SSE chunk bytes were not retained.
