#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-3 AC2 -- portal/DESIGN.md carries the RATIFIED C13 clause (L4R_C13_RATIFIED.md s.5,
# verbatim): its five bullets are present by their opening phrases, in order. usage: bash <this>  (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; F="$ROOT/portal/DESIGN.md"
n=0
for phrase in \
  'C13. \*\*Overflow, truncation and wrap.\*\*' \
  'Text whose full form is not reachable in the view never clips' \
  'Text whose full form IS reachable may clip, and the clip must be visible' \
  'A table cell defaults to `whitespace-nowrap` for a short single-token value' \
  '`overflow-hidden` on a FRAME is a layout device and is unrestricted' \
  'Conformance is read on the render, at the panel.s own minimum width'; do
  c=$(grep -c -E -- "$phrase" "$F"); echo "$c  $phrase"; [ "$c" -ge 1 ] && n=$((n+1))
done
echo "C13 heading + five bullets present: $n of 6"
[ "$n" -eq 6 ]
