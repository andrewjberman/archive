#!/usr/bin/env bash
# MX-c-10 AC3 (answer time, EVERY measured row): discover(row, exact) answers each measured row with the same depth,
# claim measured, read at answer time. Instrument c12_depth.py answer.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 600 python "$(native "$H/c12_depth.py")" answer "$(native "$(pwd)/$GW")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | grep -E '^(ANSWER)|Error|Traceback' | cut -c1-200 | tail -16
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
