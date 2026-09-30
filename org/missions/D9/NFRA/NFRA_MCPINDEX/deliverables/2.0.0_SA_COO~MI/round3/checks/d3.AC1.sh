#!/usr/bin/env bash
# MX-d-3 AC1 (no regression on the MX-v-6 harness): the plain run of run_routing.py over the 27 real asks exits 0 and
# scores ROUTING >= 21 of 27 (the round-2 baseline).
. "$(dirname "$0")/_root.sh"
H="$GW/tests/routing/run_routing.py"
[ -f "$H" ] || { echo "$H absent"; echo "RESULT: FAIL"; exit 1; }
a=$(timeout 110 python "$H" 2>&1 | tr -d '\r'); ra=$?
k=$(printf '%s\n' "$a" | sed -n 's/^ROUTING: \([0-9]*\) of \([0-9]*\) .*/\1/p' | tail -1)
n=$(printf '%s\n' "$a" | sed -n 's/^ROUTING: [0-9]* of \([0-9]*\) .*/\1/p' | tail -1)
echo "plain run rc=$ra ROUTING ${k:-?} of ${n:-?}"
if [ "$ra" = 0 ] && [ -n "$k" ] && [ "$n" = 27 ] && [ "$k" -ge 21 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
