#!/usr/bin/env bash
# MS-t-1 AC2 (AMENDMENT 1 -- the Opal-tenant asker path is unmoved AND the adapter agrees with its contract): the
# existing asker suites (test_asker_scope.py, test_asker_binding.py, test_asker_nochannels.py) and the adapter's own
# suites (test_access_state.py, test_email_deny.py) pass with nothing failed and at least 41 passed (40 passed +
# test_ogd1_ac03 red at the amendment, the contract-vs-adapter gap this cell closes).
. "$(dirname "$0")/_root.sh"
out=$(cd "$G" && timeout 110 python -m pytest tests/test_asker_scope.py tests/test_asker_binding.py tests/test_asker_nochannels.py tests/test_access_state.py tests/test_email_deny.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "asker + adapter suites: $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 41 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
