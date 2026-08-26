# INVALID — DO NOT USE AS EVIDENCE

The described run is historical and does not substantiate the exact-head
request. The current real run was blocked by AGY quota exhaustion before a
streamed chunk and terminal completion. Its checksum sidecar is intentionally
invalidated by this withdrawal.

# Historical methodology (invalid)

## Environment
- **Server**: Real Flask backend (`python -m mvp_site.main serve`) on port `57744`
- **Browser**: Headless Chromium (Playwright), viewport 1280x800
- **Git Head**: `284539f64882ab7922efb80ca041cfbf925a4c75`
- **PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/9358

## Procedure
1. Boot real Flask server on isolated localhost port `57744` with `TESTING_AUTH_BYPASS=true`.
2. Load route `/game/cBCSrw17eBrpCos2n9SR?test_mode=true&test_user_id=test-user-123`.
3. Overlay HUD banner with visible URL, Git SHA, and test identifier.
4. Position scroll to read Chapter 2 (`scrollTop=150px`).
5. Stream 9 sequential narrative chunks into `#story-content`.
6. Assert `scrollTop` drift remains 0.0px during chunk insertion (`overflow-anchor: none;`).
7. Trigger `streamingClient.onComplete` and verify guarded `scrollToBottom` preserves `scrollTop=150px`.
8. Record continuous video, burn in subtitles, and emit bundle checksums.
