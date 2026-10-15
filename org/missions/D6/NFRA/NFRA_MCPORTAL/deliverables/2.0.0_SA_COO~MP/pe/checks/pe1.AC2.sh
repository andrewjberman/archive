#!/usr/bin/env bash
# MP-pe-1 AC2 (the bound and the seam; decomposition PE.2): the whole gateway admin suite still passes. Base (measured 2026-10-15 ~16:5xZ): 93 passed, 0 failed.
# A BOUND, so it passes at the base: the run must read 0 failed and at least the base 93 passed (the new tests of AC1 only add to it). This includes test_person_holdings_equal_breakdown_holders in
# tests/test_admin_people.py: the People view reuses the breakdown's helpers, and its seam to the breakdown must still hold after the regrouping.
. "$(dirname "$0")/../../pd/checks/_root.sh"
out=$(cd "$GW" && timeout 115 python -m pytest tests/test_admin*.py tests/test_owner_gate.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
pass=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' | head -1); pass=${pass:-0}
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
seam=$(printf '%s\n' "$out" | grep -c 'FAILED.*test_person_holdings_equal_breakdown_holders')
echo "admin suite: $tail; passed=$pass failed=$failed; seam test failures=$seam"
if [ "$failed" = 0 ] && [ "$seam" = 0 ] && [ "$pass" -ge 93 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
