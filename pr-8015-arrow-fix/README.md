# GH-8015 — Mobile Scroll Indicator Chevron (Arrow UI) Visual Proof

Captured at 390×844 viewport (iPhone 14 mobile preset) against the live local server.

## Bug

1. When the mobile wizard was opened, `.wizard-scroll-indicator` was missing / trapped inside ancestors with `transform` / `backdrop-filter`, causing the indicator to either fail to render or be misplaced far below the viewport.
2. In single-scroll-context mode on mobile, `updateScrollIndicator()` checked only internal scroll instead of checking below-the-fold content in the viewport, leaving the indicator hidden (`display: none`).

## Fix

- **Escape Containing-Block Traps**: On mobile viewport, `setupScrollIndicator()` moves `.wizard-scroll-indicator` to `document.body` and styles it with `position: fixed; bottom: 0; left: 0; right: 0; z-index: 40;`, ensuring it floats at the true bottom of the viewport with its gradient mask.
- **Scroll Position Detection**: `updateScrollIndicator()` evaluates whether below-the-fold content exists in the mobile viewport, automatically adding `.is-visible` when the user is at the top/middle of step 1, and smoothly removing `.is-visible` as soon as the user scrolls to the bottom near the Next button.
- **Step 1 Navigation**: `#wizard-prev` uses `visibility: hidden` on step 1 to preserve layout geometry without visual distraction.
- **Cleanup**: `restoreOriginalForm()` unbinds listeners and removes the indicator from `document.body` on unmount.

## Captioned Visual Evidence

### 1. Before (Bug Baseline) — Missing Scroll Indicator
`before-broken-baseline-no-indicator.png` (390×844)
> **Caption**: On step 1 mobile view, extensive campaign fields and the Next button lie below the fold, but no scroll cue is visible to indicate more content exists.

### 2. After (Top of Step 1) — Animated "Scroll for more" Chevron Visible
`after-mobile-wizard-top.png` (390×844)
> **Caption**: Upon loading step 1 on mobile, the "SCROLL FOR MORE" affordance with its animated bouncing downward chevron floats cleanly at the bottom of the viewport with a gradient fade, signaling to the user that more form content exists below.

### 3. After (Middle of Step 1) — Affordance Stays Visible While Scrolling
`after-mobile-wizard-middle.png` (390×844)
> **Caption**: As the user scrolls down through the campaign cards and title input, the chevron remains visible while additional interactive fields remain below the fold.

### 4. After (Bottom of Step 1) — Automatic Fade-Out & Clean Navigation
`after-mobile-wizard-bottom.png` (390×844)
> **Caption**: Once the user reaches the bottom of step 1, the scroll indicator automatically hides, displaying the Next button and Step 1 of 2 indicator with no layout shift and no overlapping controls.

### 5. Interaction Demo (Animation & Video)
- `scroll-indicator-demo.gif` — Animated GIF showing the complete scroll lifecycle (initial appearance, scroll down, automatic fade-out at bottom, and reappearance upon scrolling back to top).
- `scroll-indicator-demo.mp4` — MP4 recording of the mobile scroll interaction at 390×844.