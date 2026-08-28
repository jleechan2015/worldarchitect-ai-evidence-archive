# Methodology

The runner started the repository-owned testing_ui local stack from the clean
worktree at exact commit `8151005e282e3aa4337df9aafe50338f1ca0e7f0`. It used a
minted test identity, created and persisted a real Firestore campaign, and
submitted one real streaming turn through AGY.

The prompt requested a long narrative, one fixture-known sentence in the
middle, structured debug information, and exactly four actionable choices.
After the sentence appeared inside the tall active `.streaming-entry`, a real
Playwright mouse-wheel action stopped bottom-following and centered the
sentence. The oracle re-resolved that literal sentence using a DOM Range in the
tagged active entry on every animation frame through completion and 1.4 seconds
of settling.

The pass conditions were no stream errors, one sentence match, all resolved
samples within 2px, four choices, visible debug UI, and AGY streaming metadata.
The served `app.js` hash was compared with `git show HEAD:mvp_site/frontend_v1/app.js`.

The WebM is a headless/page-only Playwright recording with the exact-head badge;
it does not contain browser chrome or a URL bar and is therefore supplemental
visual evidence. The MP4 is a captioned derivative of that recording.

The selected frame files are extracted directly from the same raw MP4: page
load at approximately 72s, reading with the anchor visible at approximately
150.5s, completion at approximately 151.5s, and settled completion at 152.0s.
The provider-reported streaming digest is retained with `signed: false`; no
independent cryptographic signature claim is made. Raw intermediate SSE chunks
were not captured, so the HTTP trace records the final done payload only.
