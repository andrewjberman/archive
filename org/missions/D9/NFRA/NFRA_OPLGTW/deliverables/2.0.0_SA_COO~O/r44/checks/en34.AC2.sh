#!/usr/bin/env bash
# OPLGTW OG-en-34 AC2 (round 44): the listener's two test files still pass after the comment correction (a control: the comment change moved no behaviour).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 110 python -m pytest -q -p no:cacheprovider --color=no tests/test_og_pr1.py tests/test_og_pr5.py 2>&1 | tr -d '\r'); rc=$?
last=$(printf '%s\n' "$out" | tail -1)
p=$(printf '%s\n' "$last" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); f=$(printf '%s\n' "$last" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
restore_audit
echo "test_og_pr1.py and test_og_pr5.py together: passed ${p:-0}; failed ${f:-0}; pytest rc=$rc"
[ "$rc" = 0 ] && [ "${p:-0}" -ge 1 ] && [ "${f:-0}" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
