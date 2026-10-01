#!/usr/bin/env bash
# MS-t-5 AC2 (the control -- the existing admin surface is unmoved): tests/test_admin_grants.py and
# tests/test_admin_round2.py pass with nothing failed.
. "$(dirname "$0")/_root.sh"
out=$(cd "$G" && timeout 100 python -m pytest tests/test_admin_grants.py tests/test_admin_round2.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "admin suites: $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
