# PR #9358 — Current-head gate report

**PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/9358
**Branch**: `fix/streaming-scroll-anchor-keep-position`
**Head SHA at capture**: `12a85e3ff915837a6464af7d59d033072fde9bb9`
**Timestamp**: 2026-08-26 (UTC)

This replaces the earlier gate report, which was marked invalid because its
run never reached a streamed chunk (AGY quota exhaustion).

---

## 1. Scoped test execution at current head

```
./vpython -m pytest -q mvp_site/tests/test_streaming_scroll_anchor.py \
                       mvp_site/tests/frontend/test_scroll_disabled.py
```

Result: **10 passed** in 88.10s (exit 0).

## 2. Real runtime evidence at current head

| Gate | Result |
|---|---|
| Real local server (not mock, not `TESTING=true`) | PASS — port 50015, `WORLDAI_DEV_MODE=true` |
| Real LLM provider | PASS — AGY CLI, `Gemini 3.5 Flash (High)` |
| Real streamed SSE delivery | PASS — `done` event reached; per-chunk `sse_event` records captured |
| Position stable during chunk growth | PASS — `scrollTop` range **0.0 px** over 457 samples, `scrollHeight` +678 px |
| Position preserved at completion | PASS — drift **0.0 px**, **1502 px** above bottom |
| RED control (detector not blind) | PASS — induced drift produced a **1003 px** range |
| Chunk timing correlation | PASS — end-to-end p95 **5.94 ms**, max **16.61 ms** (thresholds 2000/5000 ms) |
| Video first frame not blank | PASS — 13,747 unique colors, HUD present (raw webm's blank lead-in trimmed) |
| Git SHA visible in video | PASS — burned into every frame |

## 3. Production bytes under test

`app.js` / `style.css` are byte-identical from `f083a8c9d3` through the branch
head; the commits in between touch beads, evidence and capture scripts only.

```
62881794ae6329ef13f146d4587138e211e8a85210e9e3930d67ad07617d2399  mvp_site/frontend_v1/app.js
6d5f6e0ae6fb5ec5127bd125a96a0854943892b68d26ff0981bc028841f71f23  mvp_site/frontend_v1/style.css
```

## 4. Disclosed gaps

- AGY is not a token-streaming provider, so the joined timing table has 3 rows
  (one phase-1 chunk per turn), not hundreds. Not evidence for token-by-token
  streaming.
- Only `sequence=0` correlates across all three hops; phase-2 `sequence=1` is
  emitted without a `request_id` (`mvp_site/llm_service.py:11466`) — a
  pre-existing instrumentation gap.
- Headless Chromium only; no other engines, no multi-user or lossy-network runs.

## 5. Not claimed

This report does **not** assert `/green`. CI status at head is not evaluated
here; this covers scoped tests plus real runtime evidence only.
