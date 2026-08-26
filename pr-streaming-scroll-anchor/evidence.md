# PR #9358 — Evidence (real run, commit `12a85e3ff9`)

Verdict: **PASS** on both scroll claims; **PARTIAL** on streaming depth (provider
limitation, disclosed).

## Claim -> Artifact map

### Claim 1 — Viewport does NOT move during streaming chunk growth

`#story-content { overflow-anchor: none }` plus the deliberate absence of
auto-scroll in `streamingClient.onChunk`.

- **Metric**: `scrollTop` min == max == **431 px** across **457 samples**
  (range **0.0 px**), while `scrollHeight` grew **1717 -> 2395 px** and
  `.streaming-text` grew **16 -> 732 chars**.
- **Raw**: `run_data/measured_turn_scroll_samples.json` — every sample carries
  `scrollTop`, `scrollHeight`, `streaming_text_len`, `sse_event_count`,
  `streaming_active`.
- **Key fields**: `run_data/capture_record.json` ->
  `measured_turn.scrolltop_range_px` (0.0),
  `measured_turn.scrollheight_growth_px` (678),
  `measured_turn.sample_count` (457).
- **Visual**: frame 2 (`real_20260826_frame_02_before_reading_position.png`)
  and the MP4 between the scroll-up and completion.

### Claim 2 — Stream completion preserves the reading position

`shouldAutoScrollStreamingEntry` guard in `onComplete`, with follow-intent
captured before the final render grows `scrollHeight`.

- **Metric**: after `done`, `scrollTop` = **431 px**, drift from the mid-stream
  reading position = **0.0 px**. Bottom was **1933 px**, so the reader remained
  **1502 px above the bottom** — not yanked.
- **Key fields**: `run_data/capture_record.json` -> `after_completion.metrics.scrollTop`,
  `after_completion.final_drift_px`, `after_completion.bottom_scrollTop_px`.
- **Visual**: `real_20260826_frame_03_after_completion_preserved.png`.

### Claim 3 — The detector is not blind (RED control)

A null result is only meaningful if the instrument can register movement.

- **Metric**: with externally induced +3px/40ms scrolling during a real streamed
  turn, the same detector recorded a `scrollTop` range of **1003 px**
  (max abs drift 2111 px) over 228 samples.
- **Key fields**: `run_data/capture_record.json` -> `red_probe.scrolltop_range_px`.
- **Visual**: `real_20260826_frame_04_red_probe_detector_works.png`.

Claim 1's 0.0 px is therefore a measured null, not an unarmed instrument.

### Claim 4 — Real server, real LLM, real streamed delivery

- **Real LLM I/O**: https://github.com/jleechanorg/worldarchitect.ai/releases/download/evidence-pr-9358/llm_request_responses.jsonl
- **Real HTTP + SSE**: https://github.com/jleechanorg/worldarchitect.ai/releases/download/evidence-pr-9358/http_request_responses.jsonl (`sse_event` records)
- **Server log**: https://github.com/jleechanorg/worldarchitect.ai/releases/download/evidence-pr-9358/server.log
- **Console**: https://github.com/jleechanorg/worldarchitect.ai/releases/download/evidence-pr-9358/console.log
- **Git linkage**: burned into every video frame; also `capture_record.json.git_sha`.

## Chunk timing correlation (streaming-evidence-standards)

Three hops, joined on `request_id` + `sequence`
(`run_data/joined_3hop_chunk_timing.csv`):

| request_id (campaign `bD4qaarukZ06zY6zyABq`) | seq | llm_ts_utc | flask_yield_ts_utc | browser_recv_ts_utc | llm->flask ms | flask->browser ms | **llm->browser ms** |
|---|---|---|---|---|---|---|---|
| `..._3dd6de56ed18412baafea9639441682a` | 0 | 06:56:04.843055 | 06:56:04.846209 | 06:56:04.849 | 3.15 | 2.79 | **5.94** |
| `..._d81c2e2915e64fa78dfbbab3fc675d38` | 0 | 06:57:01.214388 | 06:57:01.220012 | 06:57:01.231 | 5.62 | 10.99 | **16.61** |
| `..._2007b473024046bba4146516a74b50d6` | 0 | 06:58:03.955032 | 06:58:03.955745 | 06:58:03.957 | 0.71 | 1.26 | **1.97** |

Summary of end-to-end `delta_ms` (LLM emit -> browser receive):
**first 1.97 ms, p50 5.94 ms, p95 5.94 ms, max 16.61 ms** (n=3).

Thresholds from the skill: `p95 <= 2000 ms`, `max <= 5000 ms` -> **PASS**
by three orders of magnitude.

- LLM side: `run_data/llm_chunk_log_bD4qaarukZ06zY6zyABq_*.csv`
  (from `mvp_site/streaming_chunk_logger.py`)
- Flask-yield side: `run_data/flask_sse_chunk_log.csv`
- Browser-receive side: `run_data/browser_sse_chunk_log.csv`
- Joined + summary: `run_data/joined_3hop_chunk_timing.csv`,
  `run_data/timing_correlation.json`

The middle row (`..._d81c2e29`) is the measured scroll turn.

## What this evidence does NOT prove

- **Not** token-by-token model streaming. AGY yields one completed response per
  turn (`agy_provider.py:1361-1369`), so only `sequence=0` and `sequence=1`
  exist per turn and the joined table has 3 rows, not hundreds.
- Only `sequence=0` rows join all three hops: the phase-2 `sequence=1` chunk is
  emitted without a `request_id` (`mvp_site/llm_service.py:11466`), so it cannot
  be correlated end-to-end. This is a pre-existing instrumentation gap, not a
  gap introduced by this PR.
- Not multi-user or network-loss behavior.
- Not non-Chromium engines; this run is headless Chromium only.
- The published MP4 is trimmed to start at the first frame that shows the HUD;
  the removed lead-in is pre-navigation dead time (blank white) while the server
  booted and the campaign was created. Nothing after page load was cut.
