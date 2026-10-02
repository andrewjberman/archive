#!/usr/bin/env bash
# MX-x-5 AC2 (packet 6.5): proof-of-spec-check WARNS, naming the rows, when an instance re-committed after its first commit still
# carries PENDING-THIS-COMMIT rows (both arms: pending rows warned; all rows pinned, silent).
. "$(dirname "$0")/_root.sh"
t=".tools/tests/test_pos_recommit_warning.py"
[ -f "$t" ] || { echo "$t absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$t" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
