# Evidence Report: PR #8961 Share Token Lifecycle & Provenance Guard

## Overview

- **PR:** #8961 (`fix/share-token-lifecycle-and-provenance-guard`)
- **Scope & Addressed Beads:**
  1. `rev-ecsha`: Token expiration lifecycle (`expires_in_seconds`, `expires_at`, and fail-closed validation).
  2. `rev-y1t37`: PATCH `/api/campaigns/<id>` provenance & identity overwrite protection (`source_campaign_id`, `author_handle`, `owner_id`, `share_token`, `user_id`).
  3. `rev-rov5j`: Author handle derivation from user profile document (`display_name`, `custom_handle`, `handle`, `author_handle`).
  4. `rev-0pd0k`: `build_share_play_url` raising `ValueError("invalid_share_token")` for invalid token syntax.
  5. `rev-usmzq`: `render_shared_landing_page` rendering 500 error page for URL budget/alias issues instead of conflating with 404 missing/revoked.
  6. `rev-vzjno`: Layer 2 composed integration test covering `mint → share → fork → forgery-attempt → rejection → expiry` in a single unified flow (`mvp_site/tests/test_share_lifecycle_composed_integration.py`).
  7. `rev-d7piq` & `rev-eblin`: Authentic real-server subprocess and real GCP Firestore (`worldarchitecture-ai`) integration test execution trace and checksum bundle.

## Layer 1 & Route Pytest Suite Execution

Executed all 11 unit, route, and Layer 2 composed integration test suites in a single combined process:

```bash
./vpython -m pytest -v \
  mvp_site/tests/test_share_token.py \
  mvp_site/tests/test_share_token_lifecycle_contract.py \
  mvp_site/tests/test_share_lifecycle_composed_integration.py \
  mvp_site/tests/test_share_routes.py \
  mvp_site/tests/test_share_provenance_security.py \
  mvp_site/tests/test_share_attribution_persisted.py \
  mvp_site/tests/test_share_url_origin.py \
  mvp_site/tests/test_share_large_wiki_campaign.py \
  mvp_site/tests/test_share_legacy_prompt_fallback.py \
  mvp_site/tests/test_share_dragon_knight_custom_type.py \
  mvp_site/tests/test_share_provenance_server_bound.py
```

### Pytest Result Summary

- **Total Tests Collected:** 156
- **Passed:** 156
- **Failed:** 0
- **Execution Time:** 2.90s
- **Trace Output File:** `pytest_output.txt`
- **SHA-256 Checksum:** `ab3ee81a4432812d355879c494b2ba7ed6c00cbf0065ceb8ee882b7da218e5e7`

## Real-Server Subprocess + Real GCP Firestore Execution (`rev-d7piq`, `rev-vzjno`, `rev-eblin`)

Executed `testing_mcp/test_share_lifecycle_composed_real_server.py` launching a real local Gunicorn server connected to the live `worldarchitecture-ai` Firestore project with no mocks:

```bash
WORLDAI_DEV_MODE=true python3 testing_mcp/test_share_lifecycle_composed_real_server.py
```

### Real-Server Execution Artifacts & Checksums

- **Server Test Output:** `real_server_test_output.txt` (SHA-256: `41e8bc3e50cc4d36192c4f668116e7478e4bd626c01365d2f3d7e85930ecd3ec`)
- **HTTP Request/Response Trace:** `real_server_evidence/http_request_responses.jsonl` (SHA-256: `de9a60fba3dc680b4ee1b1c38c2d0d21b200a3bb2ce110b6b81454588333a4bc`)
- **Execution Summary:** `real_server_evidence/test_summary.json` (SHA-256: `338e60e094ba5d53c92e5ddd0db66c1aa8d85b24e29f316695a1da8ae33ce17f`)

### Real-Server Verification Matrix

1. **Step 1 (User Profile Seeding & Custom Handle Resolution - `rev-rov5j`):**
   - Seeded `users/test-creator-9038498b` with `display_name="Aria_9038498b"` and `custom_handle="ArchmageAria_9038498b"` directly in Firestore.
2. **Step 2 (Campaign Creation via Real Server):**
   - Creator called `POST /api/campaigns` through real HTTP on port 56066 $\rightarrow$ created campaign `DKlTGMUmm3icHnBIjuNt`.
3. **Step 3 (Mint with Expiry TTL - `rev-ecsha`):**
   - Creator called `POST /api/campaigns/DKlTGMUmm3icHnBIjuNt/share-token` with `expires_in_seconds=3600`.
   - Verified that `expires_at: 2026-08-17T08:01:49.752794+00:00` was persisted to `shared_links/G-nND3K82BAHNiLG3YQ4O9UV-b7OxSEs-BJ4D7AkEqI` and returned in the HTTP response.
4. **Step 4 (Public Read & Handle Resolution - `rev-rov5j`):**
   - Public read `GET /api/shared/G-nND3K82BAHNiLG3YQ4O9UV-b7OxSEs-BJ4D7AkEqI` returned HTTP 200.
   - Verified `author_handle` resolved to `ArchmageAria_9038498b` without leaking creator email or UID.
5. **Step 5 (Recipient Campaign Fork with Server Provenance):**
   - Recipient `test-player-9038498b` called `POST /api/campaigns` carrying `share_token` and forged provenance parameters.
   - Created forked campaign `393iTkUV97i5tNeA8b4i` under recipient.
   - Verified Firestore persistence of `source_campaign_id="DKlTGMUmm3icHnBIjuNt"` and `author_handle="ArchmageAria_9038498b"`, rejecting forged creation values.
6. **Step 6 (Attacker PATCH Forgery Rejection - `rev-y1t37`):**
   - Recipient/attacker attempted `PATCH /api/campaigns/393iTkUV97i5tNeA8b4i` supplying forged `source_campaign_id`, `author_handle`, `owner_id`, `share_token`, `user_id`.
   - Verified HTTP 200 returned and mutable `title` updated in Firestore, while all immutable provenance and ownership fields remained strictly preserved.
7. **Step 7 (Expiry Fail-Closed - `rev-ecsha`):**
   - Timestamp advanced to the past (`2020-01-01T00:00:00+00:00`).
   - Verified `GET /api/shared/<token>` returned HTTP 404 (`not_found`).
8. **Step 8 (Automated Teardown & Deletion Verification):**
   - Deleted all created test campaigns (`DKlTGMUmm3icHnBIjuNt`, `393iTkUV97i5tNeA8b4i`), tokens, and user records from live Firestore, confirming complete cleanup.
