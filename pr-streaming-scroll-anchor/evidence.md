# PR #9358 — Evidence (real run, commit `12a85e3ff9`)

Verdict: **PASS** on both scroll claims; **PARTIAL** on streaming depth (provider
limitation, disclosed).

## Claim -> Artifact map

### Claim 1 — Viewport does NOT move during streaming chunk growth

What this run actually exercises is **the absence of any auto-scroll in
`streamingClient.onChunk`**.

> **Mechanism caveat (do not overclaim `overflow-anchor`).** In this run the
> reader sat at `scrollTop=431` with `clientHeight=483`, so the viewport covered
> `[431, 914]`, while all DOM growth occurred in `[1717, 2395]` — roughly 800 px
> **below the fold**. Browser scroll anchoring only compensates for content
> changes *above* the anchor, so `#story-content { overflow-anchor: none }` could
> not have been the operative mechanism here. The 0.0 px null is real and
> measured; the causal attribution to `overflow-anchor` is **not** established by
> this run. Proving that rule would need the reader positioned so growth happens
> above the viewport.

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
- **Visual**: the MP4 between the scroll-up and completion (HUD shows a constant
  `scrollTop=431px` while the story grows). Note `real_20260826_frame_02_*.png` is
  the **`2_BEFORE`** phase at `scrollTop=519px`, captured ~3 s before submit — it
  is NOT a during-stream still and must not be cited as one. No dedicated
  during-stream screenshot was captured; the per-sample JSON and the video are the
  support for this claim.

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

Summary of end-to-end `delta_ms` (LLM emit -> browser receive), n=3:
**first chunk 5.94 ms, min 1.97 ms, median 5.94 ms, max 16.61 ms**
(nearest-rank p95 = 16.61 ms, i.e. the max at this sample size).

> **n=3 caveat.** A p95 over three samples is not statistically meaningful — it
> is just a high-order order statistic. Treat min/median/max as the real summary.
> An earlier revision of this bundle printed `p95 = 5.94 ms`, which was a defect
> in the analyzer (`int(n*0.95)-1` returns the median at n=3). Corrected here and
> in `testing_ui/archive/analyze_pr9358_streaming_timing.py`.

Thresholds from the skill: `p95 <= 2000 ms`, `max <= 5000 ms` -> **PASS**.

### These hop deltas are NOT user-perceived latency

The per-hop figures above measure only the intra-process handoff of an
**already-buffered** AGY response. What the reader actually waits is:

| Measure | Value |
|---|---|
| submit -> first SSE event (`metadata`) | **1.513 s** |
| submit -> **first narrative chunk** | **28.877 s** |

28.877 s is the honest time-to-first-token for this turn, and it is consistent
with the app's own burned-in readout ("Time to first token: 28.8s") visible in
`real_20260826_frame_03_after_completion_preserved.png`. Millisecond hop deltas
must not be read as "streaming is fast".

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
- **`overflow-anchor: none` is not proven by this run** — all DOM growth was
  below the fold (see the mechanism caveat under Claim 1).
- **No runtime fix-off control.** The RED probe proves the *detector* registers
  movement; it does not show the pre-fix build yanking at runtime. The fix-off
  control that exists is Layer 1 only:
  `mvp_site/tests/test_streaming_scroll_anchor.py::test_phase_a_before_fixture_would_yank`.
- **`mvp_site/llm_providers/gemini_provider.py` is in this PR's diff but outside
  this bundle's envelope** — the run used the AGY provider, so it exercises no
  Gemini-SDK code path.
- **Measured sampling cadence, not the requested 50 ms**: n=456 intervals,
  min 60 ms, median 93 ms, p95 277 ms, **max 743 ms** (52 gaps >200 ms, 6 >500 ms).
  A transient yank-and-return inside a 743 ms blind spot would not be seen.
- **Growth was 4 discrete events, not 457**: `scrollHeight` took the values
  1717 / 1866 / 2014 / 2062 / 2395. 239 of 457 samples (52%) sit at 1717 before
  any content arrived, and 333 px of the 678 px total landed on the final render,
  observed in a single sample. The 457 figure is sampling density, not evidence density.
- Not multi-user or network-loss behavior.
- Not non-Chromium engines; this run is headless Chromium only.
- The published MP4 is trimmed to start at the first frame that shows the HUD;
  the removed lead-in is pre-navigation dead time (blank white) while the server
  booted and the campaign was created. Nothing after page load was cut.
