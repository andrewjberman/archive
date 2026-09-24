#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-4 AC1 -- the ANCESTOR-AWARE clip arm sees what the leaf-only arm cannot: on a static
# fixture reproducing the pre-rm-5 clip (flex-shrink-0 + flexbox's implicit min-width:auto, the cut at an ancestor
# frame, NO overflow/clip/ellipsis on the leaf), ui-measure.mjs --self-test prints ONE line of the form
#   ANCESTOR-CLIP leafOnly=<a> ancestorAware=<b>
# with a == 0 and b >= 1. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
FX=src/pages/SecurityAnalysis/__harness__/tests/uiClipFixture.html
[ -s "$FX" ] || { echo "fixture absent: $FX"; exit 1; }
node scripts/ui-measure.mjs --self-test --fixture "$FX" > .scratch.rn4.selftest.txt 2>&1; rc=$?
cat .scratch.rn4.selftest.txt
line=$(grep -E '^ANCESTOR-CLIP leafOnly=[0-9]+ ancestorAware=[0-9]+' .scratch.rn4.selftest.txt | head -1); rm -f .scratch.rn4.selftest.txt
[ -n "$line" ] || { echo "no ANCESTOR-CLIP line (self-test rc=$rc)"; exit 1; }
a=${line#*leafOnly=}; a=${a%% *}; b=${line#*ancestorAware=}; b=${b%% *}
echo "leafOnly=$a ancestorAware=$b (self-test rc=$rc)"
[ "$a" -eq 0 ] && [ "$b" -ge 1 ]
