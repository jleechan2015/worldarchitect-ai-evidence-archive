# INVALID — DO NOT USE AS EVIDENCE

The requested real server/browser replay at
`10b17f7a599452feaed5191f31ca7776ef5e9d85` failed closed before a provider
chunk or SSE completion: `agy_provider: agy quota exhausted; wait for quota reset before proof`.
The checksum sidecar is intentionally invalidated by this withdrawal. The
historical claims below are not publishable evidence.

# Historical evidence (invalid)

## Claim → Artifact Map
- **Claim 1**: Viewport position does NOT shift during streaming chunk growth (`overflow-anchor: none;`).
  - **Artifact**: `artifacts/02_during_streaming_stable_position.png` (drift: 0.0px across 9 chunks)
  - **Key Field**: `metadata.json` -> `verification_results.samples[*].drift` (all 0.0)
- **Claim 2**: Stream completion preserves reader position when scrolled up (`shouldAutoScrollStreamingEntry` guard in `onComplete`).
  - **Artifact**: `artifacts/03_after_stream_completion_preserved.png` (final scrollTop: 150px, drift: 0px)
  - **Key Field**: `metadata.json` -> `verification_results.reading_position_preserved` (true)
- **Claim 3**: Real server & browser callstack exercised with visible SHA linkage.
  - **Artifact**: `artifacts/streaming_scroll_real_server.mp4` (burned-in captions, URL bar, Git SHA `284539f648`)
  - **Artifact**: `artifacts/streaming_scroll_real_server.gif` (animated preview)
  - **Artifact**: `artifacts/server.log` (real Flask runtime log)

## What This Evidence Does NOT Prove
- Does not prove multi-user concurrent WebSocket streaming under network packet loss (covered by backend soak suite).
- Does not prove legacy IE/Safari 12 scroll behavior (focus is modern evergreen Chromium/WebKit/Firefox).
