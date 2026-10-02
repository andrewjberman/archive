#!/usr/bin/env bash
# MX-f-1 AC2 (CTO 3a Z-S74 part 1): the weekly trading-day-frontier rule -- FRESH on a day after the weekly producer ran;
# STALE only past the next scheduled weekly production day; the positive control is a write one week past. Offline fixtures
# (no held config read; COMP_FRESHNESS_PIPELINE is never set by this test).
. "$(dirname "$0")/_root.sh"
t=".tools/tests/test_comp_freshness_weekly.py"
[ -f "$t" ] || { echo "$t absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$t" -q -rA -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
