#!/usr/bin/env bash
# MS-t-1 AC2 (the control -- the Opal-tenant asker path is unmoved): the existing asker suites (test_asker_scope.py,
# test_asker_binding.py, test_asker_nochannels.py) pass with nothing failed and at least 23 passed (23 at the cut).
. "$(dirname "$0")/_root.sh"
out=$(cd "$G" && timeout 100 python -m pytest tests/test_asker_scope.py tests/test_asker_binding.py tests/test_asker_nochannels.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "asker suites: $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 23 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
