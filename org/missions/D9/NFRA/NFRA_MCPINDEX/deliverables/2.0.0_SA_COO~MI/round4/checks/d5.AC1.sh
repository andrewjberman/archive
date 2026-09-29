#!/usr/bin/env bash
# MX-d-5 AC1 (Z-W10-S1): the MX-v-6 harness plain run exits 0 with ROUTING >= 25 of 27.
. "$(dirname "$0")/_root.sh"
H="$GW/tests/routing/run_routing.py"; [ -f "$H" ] || { echo "$H absent"; echo "RESULT: FAIL"; exit 1; }
a=$(timeout 300 python "$H" 2>&1 | tr -d '\r'); ra=$?
k=$(printf '%s\n' "$a" | sed -n 's/^ROUTING: \([0-9]*\) of \([0-9]*\) .*/\1/p' | tail -1); n=$(printf '%s\n' "$a" | sed -n 's/^ROUTING: [0-9]* of \([0-9]*\) .*/\1/p' | tail -1)
echo "plain run rc=$ra ROUTING ${k:-?} of ${n:-?}"
rc=1; [ "$ra" = 0 ] && [ "$n" = 27 ] && [ -n "$k" ] && [ "$k" -ge 25 ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
