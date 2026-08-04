# Evidence bundle for PR #7658

This directory contains terminal recording evidence for PR #7658, showing the initial failing state and the final passing state of the frontend_v1 JS unit tests.

## Files
- `red.cast` — Terminal asciicast recording showing the test failures in `settings_listeners.test.js` before the fix is applied.
- `green.cast` — Terminal asciicast recording showing the 132 successful test runs (including the fixed settings listener and the new auth persistence tests) after the fix is applied.
- `checksums.txt` — SHA256 checksums of the cast files.
- `README.md` — This file.

## Proof & Repro
To verify the tests:
1. Run all frontend unit tests locally:
   ```bash
   node --test mvp_site/frontend_v1/tests/*.test.js
   ```
2. Verify that all 132 tests pass successfully.
