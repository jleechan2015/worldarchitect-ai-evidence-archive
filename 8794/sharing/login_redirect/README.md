# Share-link prefill — evidence

Test: `testing_ui/test_share_link_login_redirect_e2e.py` — three scenarios in
one run. Layer 3: real Chromium, real local Flask server, real Firestore, and
every source campaign is created through the real `POST /api/campaigns` path
(not a direct Firestore doc write, which would bypass the persistence this
change depends on).

```
PYTHONPATH=$PWD PORT=8181 TESTING_AUTH_BYPASS=true GOOGLE_APPLICATION_CREDENTIALS=$HOME/serviceAccountKey.json ./vpython mvp_site/main.py serve
PYTHONPATH=$PWD SHARE_TAKEOVER_BASE_URL=http://localhost:8181 GOOGLE_APPLICATION_CREDENTIALS=$HOME/serviceAccountKey.json ./vpython testing_ui/test_share_link_login_redirect_e2e.py
```

## Three claims, three proofs

### Claim 1 — a signed-out recipient lost the whole prefill at sign-in

`red/` vs `green/` is the RED/GREEN pair for the `auth.js` fix (a27907bf47).
RED was produced by reverting ONLY the two fixed files to the pre-fix commit,
restarting the server, and running the unchanged test.

| Scenario | Pre-fix (`red/`) | Post-fix (`green/`) |
|---|---|---|
| signed out -> click Play -> sign in | FAIL, 6 errors | PASS |
| already signed in -> click Play | PASS | PASS |

Only the signed-out path was broken; the signed-in scenario is the regression
check, not a second bug. `red/03_after_sign_in.png` shows the dashboard (the
bug); `green/03_after_sign_in.png` shows the prefilled wizard.

### Claim 2 — every editable wizard field now round-trips

The five editable fields in the wizard, and where each is carried:

| Wizard field | URL param | Allowlisted | Persisted at creation |
|---|---|---|---|
| campaign type radios | `type` | `campaign_type` | yes (server-derived) |
| Campaign Title | `title` | `title` | yes |
| Character you want to play | `character` | `character` | yes |
| Setting/world | `setting` | `setting` | yes |
| Campaign description prompt | `description` | `description` | yes |

Plus non-editable attribution: `source` (`source_campaign_id`) and `author`
(`author_handle`, derived server-side).

Current top-level screenshots are the post-change run.
`11_signed_in_prefilled.png` shows title, character and setting all rendered.

### Claim 3 — a DRAGON KNIGHT source campaign round-trips as Dragon Knight, not "custom"

Every scenario above (Claims 1 and 2) seeds a CUSTOM campaign. The `type`
URL param, and the `campaign_type` field it's derived from, had never been
exercised in a real browser for a real Dragon Knight source campaign — only
in a unit test. A share link that silently downgrades a Dragon Knight world
to a custom one on the recipient's wizard is exactly the class of bug that
gap could hide.

`run_dragon_knight()` creates a SECOND source campaign through the real
`POST /api/campaigns` path, but this time with the exact canonical inputs
(`mvp_site/constants.py` `DRAGON_KNIGHT_CANONICAL_*` + the bundled
`dragon_knight_canonical_description.txt`) that make
`world_logic.create_campaign_unified`'s Dragon Knight template shortcut
match — the same inputs the production wizard's Dragon Knight quick-start
card sends. Only a request that hashes to
`DRAGON_KNIGHT_CANONICAL_PROMPT_SHA256` gets `campaign_type="dragon-knight"`
persisted; anything else, including free-text that merely looks like Dragon
Knight content, is persisted as `"custom"`. Because the shortcut also skips
the opening-story LLM call, this creation is fast, not a second slow
LLM-backed campaign.

**A customized Dragon Knight campaign sharing as `type=custom` is INTENDED
behavior, confirmed by the product owner (2026-08-10) — do not "fix" it.**
`dragon-knight` denotes the canonical template campaign specifically. Once a
user edits the prompt away from the canonical text, the campaign genuinely is
a custom world that started from the Dragon Knight template, and the
destination wizard should open it as Custom rather than re-applying Dragon
Knight defaults over the user's own edits. The hash gate is the mechanism
that draws that line, not a bug in it.

`20_dragon_knight_landing.png` shows the public share landing page for "The
Knight of Two Suns". `21_dragon_knight_prefilled.png` shows the destination
wizard with the **Dragon Knight Campaign** card selected (highlighted) and
**Custom Campaign** NOT selected, with title/character/setting all
prefilled from the shared world. The test additionally expands the
description textarea (same click-based pattern as Claim 2) and asserts its
full text, and asserts `source_campaign_id` / `author_handle` attribution.

| Field | Assertion |
|---|---|
| `wizard-dragon-knight-campaign` radio | checked = True |
| `wizard-customCampaign` radio | checked = False |
| title / character / setting / description | equal to the canonical Dragon Knight values, visible |
| `source_campaign_id` | equals the Dragon Knight campaign's own ID |
| `author_handle` | equals the Dragon Knight campaign owner's derived handle |

## Fake-audit (Job 2)

Every non-production-path element left in the test file, and why:

- **`?test_mode=true` URL auth path** (used once, in `run()`'s sign-in step)
  — KEPT. Real Google OAuth cannot run headlessly in CI/local Playwright.
  This is the dev-only bypass the app itself ships
  (`mvp_site/frontend_v1/auth.js`), gated behind `TESTING_AUTH_BYPASS`, not a
  test-side mock. **What this weakens:** the test proves the app's own
  post-auth redirect-restoration logic (the `redirect_after_login`
  localStorage key and its consumption), but does NOT exercise the real
  Google OAuth popup/redirect-URI/third-party-cookie path — a regression
  specific to that OAuth wiring would not be caught here.
- **`window._testModeParams` init script** (used in `run_signed_in()` and
  `run_dragon_knight()`) — KEPT, same reasoning as above: the dev-only
  test_mode shim is captured by `auth.js` from the URL at module load and
  does not survive a full page navigation, unlike a real persisted Firebase
  session in IndexedDB. Seeding it via `context.add_init_script()` (runs
  before page scripts on every navigation) is the closest faithful stand-in
  for "already signed in" available without a real OAuth session.
- **Direct Firestore `doc.set()` seeding** — REMOVED already, before this
  pass (see `_create_campaign_via_real_api`'s docstring); confirmed absent
  by grep across the file. All three scenarios seed campaigns exclusively
  through `POST /api/campaigns`.
- **`page.evaluate()` DOM mutation to force an assertion to pass** — NONE
  FOUND. Every `page.evaluate()` call in the file (`VISIBILITY_PROBE` and
  the two description-textarea readers) only reads
  `getBoundingClientRect()` / `getComputedStyle()` / element `.value`; none
  of them set a value, toggle a checkbox, or change `display`/`visibility`.
  The description textarea is revealed the same way a human does it: a real
  `page.click()` on `#wizard-toggle-description`.

## Limitations, stated plainly

- **Backfill gap.** `character` / `setting` / `description` / `campaign_type`
  are written by `firestore_service.create_campaign()` going forward. Campaigns
  created BEFORE this change do not carry them, so sharing an older campaign
  still yields empty params for those fields. `type` falls back to `custom`.
  There is no backfill and no `initial_prompt` re-parse.
- **Sign-in is simulated** with the dev-only `?test_mode=true` path; real Google
  OAuth cannot run headlessly. What is proven is the pending-redirect mechanism:
  the browser arrives at `/` with NO share params in the URL, and only the
  stored redirect can restore the prefill.
- **The signed-in and Dragon Knight scenarios seed `window._testModeParams`**
  via an init script, because the test_mode shim is in-memory per page load
  while a real Firebase session persists in IndexedDB. See "Fake-audit
  (Job 2)" above for the full list of non-production elements and why each
  is kept.
- **`use_default_world` is not a gap.** The `use-default-world` checkbox lives
  in the legacy `new-campaign-form` (`index.html:248`), which the wizard hides.
  It is not reachable in any mode: `interface-manager.js` hardcodes
  `currentMode = 'modern'` ("Always use modern mode"), and the live wizard's
  `collectFormData()` (`campaign-wizard.js:1701`) hardcodes
  `useDefaultWorld = isDragonKnight` rather than reading any checkbox. So the
  value is derived from campaign type, which DOES round-trip. Same applies to
  the legacy `selected_prompts` / companions checkboxes. If classic mode is
  ever revived, this becomes a real gap.
- **The avatar file input is not shareable** — a file upload cannot be a URL
  parameter.
- Assertions read `getBoundingClientRect` + computed style, so a value hidden
  from the user fails. The test never force-shows an element; it clicks the
  "Expand" control a human clicks.

## CI state at the time of this bundle

Verified at head `9c64de2abd`. Failures remaining on the PR, and why each is
not a defect in this change:

- **Directory tests (core-mvp-1/2/3)** — all three shards fail on the single
  test `mvp_site/tests/test_canonicalize_invariants.py` (success rate 99.5%).
  Pre-existing: it was added to `testing_config/pytest_quarantine.txt` by
  commit `5f22925a3b` ("add 6 more pre-existing failing tests") BEFORE any of
  this work, the test file is byte-identical to that commit, and this branch
  never touches `rewards_engine.py` / `level_up_session.py` / `llm_parser.py`
  / `game_state.py`. Reproduced locally: 2 failed, 56 passed.
- **Light/Fantasy Compliance Gate** — the fantasy `02_dashboard` screen scores
  0.0 because the theme smoke seeds its campaign through
  `POST /api/campaigns`, which cannot succeed in that workflow
  (`GOOGLE_APPLICATION_CREDENTIALS: /dev/null`); an empty dashboard then
  redirects to `/new-campaign`, so the dashboard selector is never present.
  The gate is also failing on unrelated branches against a tight 92.0
  threshold (`feat/quick-start-rebuilt` scored 91.18).
  The light-theme half of this gate WAS a real regression from this branch and
  is fixed: `02_dashboard` went 0.0 -> 99.3 after the redirect-write guard.
- **Evidence Gate** — Check 7 compares the gist's declared head to the PR head,
  so every push invalidates the previously published bundle. The gist above is
  republished at the final head; this commit is deliberately docs-only so no
  behavioral file changes between the capture head and the new head.

### Fantasy-theme dashboard: resolved

The `Light/Fantasy Compliance Gate` fantasy `02_dashboard` score of 0.0 was a
genuine two-file interaction in this PR, not a CI-environment artifact as an
earlier note in this file claimed. The harness appends `?test_theme=fantasy`
to every navigation in the fantasy run only; the pending-redirect write guard
treated that as state worth restoring, and the `worldai-auth-ready` consumer
replayed it via `history.replaceState` on top of a URL carrying
`test_mode`/`skip_redirect`, dropping those and re-enabling the zero-campaign
auto-redirect. Fixed by ignoring debug-only query params when storing the
redirect. Gate now scores 92.38 against the 92.00 threshold, with fantasy
`02_dashboard` at 89.93 (an unaffected branch scores 89.7), and the gate
reports SUCCESS in CI at head `73508fed05`.

### Post-merge note (2026-08-10)

Head `78b99b028a` is a clean merge of `origin/main` (`b519e1cf71`) with ZERO
file overlap against this branch's changes; no share-feature file changed.
The previously-blocking `test_canonicalize_invariants.py` now reports
`61 passed, 1 xfailed` after main's rewards_engine repair (#8832) landed.
