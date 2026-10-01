#!/usr/bin/env bash
# MX-x-4 AC3 (row Z-W21-S7): the catalog emitter takes its census and portal inputs as declared arguments and REFUSES when
# the census is absent, never writing "NONE -- uncensused" over a row.
. "$(dirname "$0")/_root.sh"
t=workflows/atom_decomposition/tests/test_emit_declared_inputs.py
[ -f "$t" ] || { echo "$t absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$t" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
