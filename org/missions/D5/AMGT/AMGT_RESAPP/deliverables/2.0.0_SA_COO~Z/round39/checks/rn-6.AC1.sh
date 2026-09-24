#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-6 AC1 -- the sidebar under the contract: App.tsx's class census reads weight=0 radius=0
# shadow=0 size=0 (C1 weights within {400,700}, C11 radii within {2,3,4,pill}, shadows 0 outside the focus ring, no size
# below 11). usage: bash <this>   (from the repo root; no server)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
line=$(node scripts/ui-class-census.mjs src/App.tsx 2>&1 | grep -E '^src/App\.tsx ')
echo "$line"
ok=1; for k in size weight radius shadow; do v=${line#*$k=}; v=${v%% *}; [ "$v" = "0" ] || ok=0; done
[ "$ok" -eq 1 ]
