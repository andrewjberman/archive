#!/usr/bin/env bash
# MX-d-3 AC2 (row Z-W2-S8, the defect itself): of the harness questions whose EXPECTED tool is a dataset (expected is not
# NOT_CATALOGUED), at least 2 of 3 route to that dataset FIRST. Read from the harness's own per-question lines.
. "$(dirname "$0")/_root.sh"
H="$GW/tests/routing/run_routing.py"
[ -f "$H" ] || { echo "$H absent"; echo "RESULT: FAIL"; exit 1; }
a=$(timeout 110 python "$H" 2>&1 | tr -d '\r'); ra=$?
ds=$(printf '%s\n' "$a" | grep -E '^Q[0-9]+ ' | grep -vE 'expected=NOT_CATALOGUED ')
n=$(printf '%s\n' "$ds" | grep -cE '^Q[0-9]+ ')
k=$(printf '%s\n' "$ds" | grep -cE ' HIT ')
echo "harness rc=$ra; dataset asks routed first $k of $n: $(printf '%s\n' "$ds" | awk '{v="MISS"; for(i=1;i<=NF;i++) if($i=="HIT") v="HIT"; printf "%s:%s ", $1, v}')"
if [ "$ra" = 0 ] && [ "$n" = 3 ] && [ "$k" -ge 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
