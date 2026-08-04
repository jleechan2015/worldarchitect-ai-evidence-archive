# Evidence Manifest — PR #7579

## Background

This manifest documents the functional DOM-level testing and TDD verification for the collapsible campaign filter controls and active filter count badge features (PR #7579, resolving Issue #7203). This implementation is **mobile-only**; on desktop viewports, the filters remain always expanded and the toggle button is hidden.

## Functional Validation Coverage

The test suite in `mvp_site/tests/frontend/test_enhanced_search_collapsible.js` and the browser suite in `testing_ui/test_enhanced_search_collapsible_evidence.py` validate the following behaviors:

1. **EnhancedSearch Instantiation**: Confirms the component boots and registers successfully on the global `window` object.
2. **Double Event Listener Bug Fix**: Confirms that clicking the toggle button once registers exactly one click and transitions `aria-expanded` from `'false'` to `'true'` and applies the `.expanded` class.
3. **Active Filters Badge Count**: Confirms the badge count is updated correctly to reflect only non-default filters (e.g. `2` when theme and status are active).
4. **Theme Filtering Logic**: Verifies that filtering by theme ('sci-fi') hides non-matching campaigns ('fantasy') and keeps matching ones.
5. **Status Filtering Logic**: Verifies that filtering by status ('completed') hides non-matching campaigns ('active') and keeps matching ones.
6. **app.js Dataset Integration**: Validates that `renderCampaignListUI` inside `mvp_site/frontend_v1/app.js` correctly maps `created_at`, `theme`, and `status` campaign properties to their respective HTML dataset attributes (`data-created`, `data-theme`, `data-status`).
7. **Mobile-Only Collapsible Behavior**: Verifies that collapsible states (initially collapsed, click to toggle, persistence) only apply on mobile viewports (width <= 768px).
8. **Desktop Always-Expanded Behavior**: Verifies that on desktop viewports (width > 768px), the toggle button is hidden, filters are always expanded, and the state persists after reloads.

## Artifacts

- **MANIFEST.md**: This file.
- **test_run_red.txt**: The failing test log showing the double-binding click listener failure and badge mismatch.
- **test_run_green.txt**: The passing test log verifying all functional DOM checks succeed after the fix is implemented.
- **01_filters_initially_collapsed.png**: Headless browser screenshot showing filters collapsed by default on mobile.
- **02_filters_expanded.png**: Headless browser screenshot showing filters expanded on toggle click on mobile.
- **03_filters_persist_expanded.png**: Headless browser screenshot showing expanded state persisted after page reload on mobile.
- **04_filters_persist_collapsed.png**: Headless browser screenshot showing collapsed state persisted after page reload on mobile.
- **05_filters_active_scifi.png**: Headless browser screenshot showing Theme=sci-fi filter active and badge count = 1 on mobile.
- **06_filters_active_completed.png**: Headless browser screenshot showing Status=completed filter active and badge count = 1 on mobile.
- **07_desktop_view_expanded.png**: Headless browser screenshot showing desktop view with always-expanded filters and hidden toggle button.
- **08_desktop_view_persist.png**: Headless browser screenshot showing desktop view always-expanded state persisting after page reload.
- **evidence_demo.webm**: WebM video recording of the headless browser test execution.
- **evidence_demo.vtt**: VTT subtitle track containing captioned steps synchronized with the video.

## TDD Red/Green Provenance

- **PR Branch**: `resolve-pr-7579-green`
- **Headless Browser Test**: `testing_ui/test_enhanced_search_collapsible_evidence.py`
