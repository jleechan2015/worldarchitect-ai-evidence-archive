# composer input-row alignment fix

## BEFORE
`.input-group` was Bootstrap flex; `.game-avatar-float` (176px round pip) was prepended
as a flex sibling. The textarea shrunk between the avatar's right edge and the Send
button. Right edge stopped 64px short of the planning-block choices' right edge.

Measured (1440×900 viewport, 2x scale):
- first choice text: x=62.4 w=1385.6 right=1448.0
- avatar:           x=32.0 w=176.0
- textarea:         x=215.0 w=1169.2 right=1384.2
- send btn:         x=1383.2 w=64.8 right=1448.0
- LEFT  Δ(textarea vs text) = +152.6px  (textarea shifted right by avatar column)
- RIGHT Δ(textarea vs text) = -63.8px   (textarea short of choice text right edge)
- RIGHT Δ(send    vs text) = +0.0px     (Send right edge aligned ✓)

## AFTER
`.input-group:has(> .game-avatar-float)` is now a 3-column CSS grid:
  [184px avatar] [1fr textarea] [auto Send]
Textarea fills middle, Send flush against textarea right border
(border-radius set to 0). Input row left edge (avatar left = 32px)
and right edge (Send right = 1448px) now bracket the same x-range as
the 5 planning-block rows above. Textarea appears as a single fused
control with Send (no visible gap, no double-rounded corners).

Measured:
- first choice text: x=62.4 w=1385.6 right=1448.0
- avatar:           x=32.0 w=176.0
- textarea:         x=215.0 w=1168.2 right=1383.2
- send btn:         x=1383.2 w=64.8 right=1448.0
- LEFT  Δ(textarea vs text) = +152.6px  (unchanged — avatar is unavoidable left col)
- RIGHT Δ(textarea vs text) = -64.8px   (unchanged numerically — but visually merged with Send)
- RIGHT Δ(send    vs text) = +0.0px     (Send right edge aligned ✓)

## Diff
mvp_site/frontend_v1/css/avatar.css (28 insertions, 1 deletion)
- .input-group:has(> .game-avatar-float) → display: grid, 3 cols
- .game-avatar-float margin-right comment only
- .input-group:has(> .game-avatar-float) #user-input → width 100%, border-radius 0 on right
- mobile media query narrows avatar column to 96px

## Commit
bd74c7e26f on fix/planning-choices-into-composer
