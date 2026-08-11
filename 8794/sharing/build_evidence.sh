#!/bin/bash
# Build the captioned MP4 + GIF from the three evidence frames.
# Captions are burned-in above each frame using ffmpeg drawtext with a black
# letterbox bar so the wizard DOM stays 100% unobstructed.
set -euo pipefail
EVIDENCE=/home/jleechan/projects/wt-share-takeover/evidence/8794/sharing
cd "$EVIDENCE"

# Letterbox the existing screenshots: top 64px bar with caption text, the
# wizard screenshot below. Output as 1280x964 (1280x900 + 64 letterbox).
mkdir -p captioned

ANNOTATIONS=(
    "01_wizard_prefill|Step 1 — URL-param prefill|/new-campaign?title=The Lost Spire&character=Lyra&setting=Astral Sea prefills the wizard"
    "02_shared_landing|Step 2 — /shared/<token> landing|Strict-CSP server-rendered HTML with Play-in-this-world anchor"
    "03_play_roundtrip|Step 3 — play button round-trip|Clicking Play lands on /new-campaign with prefilled fields + source attribution"
)

for entry in "${ANNOTATIONS[@]}"; do
    IFS='|' read -r slug title body <<< "$entry"
    src="${slug#0}_"  # skip leading zero
    # Source is named like after_url_param_prefill.png
    case "$slug" in
        01_wizard_prefill) src=after_url_param_prefill.png ;;
        02_shared_landing) src=after_shared_landing.png ;;
        03_play_roundtrip) src=after_play_roundtrip.png ;;
    esac
    out="captioned/${slug}.png"
    convert "$src" \
        -gravity North -background black -splice 0x80 \
        -gravity North -fill white -font DejaVu-Sans-Bold -pointsize 22 \
        -annotate +0+10 "$title" \
        -gravity North -fill '#bbbbbb' -font DejaVu-Sans -pointsize 16 \
        -annotate +0+40 "$body" \
        -gravity South -background black -splice 0x40 \
        -gravity South -fill '#bbbbbb' -font DejaVu-Sans -pointsize 14 \
        -annotate +0+10 "feat/campaign-share-url-phase1-takeover @ $(git -C /home/jleechan/projects/wt-share-takeover rev-parse --short HEAD)" \
        "$out"
done

# Build the MP4: each captioned frame held for 3s.
ffmpeg -y \
    -loop 1 -t 3 -i captioned/01_wizard_prefill.png \
    -loop 1 -t 3 -i captioned/02_shared_landing.png \
    -loop 1 -t 3 -i captioned/03_play_roundtrip.png \
    -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" \
    -map "[outv]" \
    -r 24 -pix_fmt yuv420p -c:v libx264 -preset veryfast \
    share_flow_captions.mp4

# Build the GIF: same frames, smaller, autoplayable.
ffmpeg -y \
    -loop 1 -t 2 -i captioned/01_wizard_prefill.png \
    -loop 1 -t 2 -i captioned/02_shared_landing.png \
    -loop 1 -t 2 -i captioned/03_play_roundtrip.png \
    -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0,scale=720:-1,split[a][b];[a]palettegen[p];[b][p]paletteuse" \
    -r 12 \
    share_flow_captions.gif

ls -la captioned/ share_flow_captions.mp4 share_flow_captions.gif
sha256sum captioned/*.png share_flow_captions.mp4 share_flow_captions.gif > checksums.txt
cat checksums.txt