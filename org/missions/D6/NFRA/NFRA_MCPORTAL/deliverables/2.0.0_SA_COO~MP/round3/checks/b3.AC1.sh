#!/usr/bin/env bash
# MP-b-3 AC1 (row Z-S10, CTO ruling msg 26207): the writer's tests pass with nothing failed, and the named test
# test_written_item_never_carries_owner_key PASSES -- on BOTH owner-key branches (oid and sub) a WRITTEN outcome's record
# item contains the configured owner-key value in NO field, and its `who` reads "<claim name> <email>".
. "$(dirname "$0")/_root.sh"
D="$MPW_DIR/tests"
[ -d "$D" ] || { echo "$D absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$D" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
named=$(printf '%s\n' "$out" | grep -cE "::test_written_item_never_carries_owner_key(\[[^]]*\])? PASSED")
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "writer tests: $tail; test_written_item_never_carries_owner_key PASSED cases=$named"
if [ "$named" -ge 2 ] && [ "$failed" = 0 ] && [ "$passed" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
