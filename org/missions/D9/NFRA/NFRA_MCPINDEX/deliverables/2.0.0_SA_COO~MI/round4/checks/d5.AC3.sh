#!/usr/bin/env bash
# MX-d-5 AC3 (recall guard): of the harness's dataset asks (expected is not NOT_CATALOGUED), >= 2 of 3 still route to their dataset first.
. "$(dirname "$0")/_root.sh"
H="$GW/tests/routing/run_routing.py"; a=$(timeout 300 python "$H" 2>&1 | tr -d '\r'); ra=$?
ds=$(printf '%s\n' "$a" | grep -E '^Q[0-9]+ ' | grep -vE 'expected=NOT_CATALOGUED '); n=$(printf '%s\n' "$ds" | grep -cE '^Q[0-9]+ '); k=$(printf '%s\n' "$ds" | grep -cE ' HIT ')
echo "harness rc=$ra; dataset asks routed first $k of $n"
rc=1; [ "$ra" = 0 ] && [ "$n" -ge 3 ] && [ "$k" -ge 2 ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
