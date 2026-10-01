#!/usr/bin/env bash
# MS-w-1 AC2 (the control -- the existing writer is unmoved): every OTHER test file in the writer's tests/ passes with
# nothing failed (narrow, widen, revoke, the owner key and the record, as they stood at the cut).
. "$(dirname "$0")/_root.sh"
files=$(cd "$MPW_DIR" && ls tests/test_*.py 2>/dev/null | grep -v 'test_register_tenant\.py' | tr '\n' ' ')
[ -n "$files" ] || { echo "no existing writer tests"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$MPW_DIR" && timeout 100 python -m pytest $files -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "existing writer tests ($files): $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
