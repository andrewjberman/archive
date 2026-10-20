#!/usr/bin/env bash
# OPLGTW OG-sz-2 AC1 (round 47): tests/test_og_rv2.py passes in full (4 of 4, including test_ogrv2_ac01) on the merged trunk. At the base it fails one test, test_ogrv2_ac01, whose 120 wide rows no longer fit 50 KB
# now that harvest_typed measures the answer as served (indent=2, order OG-sz-1): the narrowed rows come back truncated.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
cd "$GW" || { echo "ERROR: gateway folder absent"; echo "RESULT: FAIL"; exit 9; }
out=$(timeout 120 python3 -I -m pytest tests/test_og_rv2.py -q -rf --color=no -p no:cacheprovider 2>&1 | tr -d '\r')
p=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | tail -1 | grep -oE '[0-9]+'); f=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | tail -1 | grep -oE '[0-9]+')
echo "tests/test_og_rv2.py: ${p:-0} passed, ${f:-0} failed (want 4 passed, 0 failed); test_ogrv2_ac01 $(printf '%s\n' "$out" | grep -q 'FAILED.*test_ogrv2_ac01' && echo FAILS || echo passes)"
[ "${p:-0}" = 4 ] && [ "${f:-0}" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
