# PR #9358 — Methodology (real run, commit `12a85e3ff9`)

## Environment

| Item | Value |
|---|---|
| Server | real local Flask via `testing_mcp` launcher, port `50015` |
| Server env | `TESTING_AUTH_BYPASS=true`, `WORLDAI_DEV_MODE=true` (NOT `TESTING=true`) |
| LLM provider | real AGY CLI, model `Gemini 3.5 Flash (High)` |
| `AGY_RUNTIME_HOME` | `~/.cache/worldai/agy-clean-home-v1` |
| Datastore | real Firestore (`~/serviceAccountKey.json`) |
| Browser | headless Chromium (Playwright), viewport 1280x720 |
| Campaign | `bD4qaarukZ06zY6zyABq` |
| Commit | `12a85e3ff915837a6464af7d59d033072fde9bb9` |

## Procedure

1. Boot the real server on an isolated free port. Provider selection is asserted
   by the launcher (`_assert_agy_provider_enabled`), which fails closed if AGY
   is disabled — so a silent fallback to the Gemini SDK cannot happen.
2. Create a story-ready campaign through the real MCP/API path and complete
   character creation in the browser.
3. Run warm-up streamed turns only until `maxScroll >= 400 px`, so the reader can
   actually sit away from the bottom. This run needed **1** warm-up turn
   (final `maxScroll` = 1039 px). Warm-ups are capped to conserve LLM quota.
4. Settle the scroll: poll until `scrollTop` and `scrollHeight` both stop
   changing. **This step matters** — the app runs a custom rAF smooth-scroll, and
   sampling a baseline while that animation is in flight yields a stale baseline
   that later reads as a large constant phantom offset (see "Correction" below).
5. Scroll to a mid-story reading position and settle again -> baseline 519 px.
6. Submit a real streamed turn.
7. **1.2 s after submit**, scroll UP to ~35% of `maxScroll` and re-baseline to the
   position the reader actually chose (431 px). This is the real user story:
   reading history while the turn streams.
8. Sample every 50 ms until the SSE `done` event: record `scrollTop`,
   `scrollHeight`, `clientHeight`, `.streaming-text` length, SSE event count and
   whether a `.streaming-entry` is active.
9. After completion, record the final position and the container bottom.
10. **RED probe**: repeat with an external `+3px/40ms` scroll injected during the
    stream, to prove the detector registers movement.
11. Post-process the three chunk timelines into a joined table.

## Correction applied during this session (disclosed)

An earlier attempt reported "281 px drift". That number was an artifact of the
harness, not app behavior: `scroll_story_to_middle()` set `scrollTop=220` while
the app's smooth-scroll animation was still running, which carried the container
to 501 px before sampling began. Every sample then computed
`drift = 501 - 220 = 281`, **identical across all 278 samples with zero
variance** — the signature of a constant offset, not of movement.

Rather than reinterpret that run's numbers after the fact, the harness was fixed
(settle-before-baseline, re-read the true pre-action position at submit time) and
the run was repeated. The primary metric was also changed to a
baseline-independent one — `scrolltop_range_px`, the spread of `scrollTop` across
the stream — which cannot be fooled by a stale baseline at all.

## Reproduce

```bash
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/serviceAccountKey.json
export WORLDAI_DEV_MODE=true TEST_RECORD_VIDEO=true TEST_BROWSER_SLOWMO_MS=120

./vpython testing_ui/archive/capture_streaming_scroll_pr9358_evidence.py /tmp/pr9358_out
./vpython testing_ui/archive/analyze_pr9358_streaming_timing.py  /tmp/pr9358_out
```

Then convert and verify the video (a blank first frame is invalid evidence):

```bash
ffmpeg -y -i /tmp/pr9358_out/video/page@*.webm -c:v libx264 -pix_fmt yuv420p out.mp4
ffmpeg -y -i out.mp4 -vf "select=eq(n\,0)" -vframes 1 frame1.png   # must NOT be blank
```

## Video / first-frame verification

Playwright begins recording at browser-context creation, so the raw `.webm`
opens with ~64 s of blank white while the server boots and the campaign is
created. Per `~/.claude/skills/ui-video-evidence/SKILL.md` a blank first frame is
invalid, so the published MP4 is trimmed to the first frame that shows the HUD.

Verified programmatically before publishing:

- raw first frame: **1 unique color, 100 % white -> INVALID**
- published first frame: **13,747 unique colors, HUD text present -> VALID**

The published first frame shows the URL bar contents, the git SHA, PR #9358, the
UTC stamp, the phase and the live `scrollTop` — satisfying the URL, before-state
and git-linkage mandatory frames simultaneously.

## Provider-quota note

The prior withdrawn attempt failed on `agy quota exhausted`. A probe run in a
plain shell appeared to show the quota had reset, but that probe resolved its
model from `$HOME/.gemini` (default **Claude Sonnet 4.6 (Thinking)**), a
different quota bucket from the **Gemini** family the evidence server requests
via `AGY_RUNTIME_HOME`. All Gemini labels were still exhausted at that moment.
This run was executed after the Gemini-family quota genuinely reset.

**When probing AGY quota for an evidence run, always probe with
`HOME=$AGY_RUNTIME_HOME` and the exact `--model` label the server will request.**
