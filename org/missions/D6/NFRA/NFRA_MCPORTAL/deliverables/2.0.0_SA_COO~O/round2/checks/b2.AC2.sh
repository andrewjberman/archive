#!/usr/bin/env bash
# MP-b-2 AC2 (R-4, the writer's OWN record): the two named record tests pass, nothing failed.
#   test_each_outcome_appends_one_record   one WRITTEN and one REFUSED outcome each put exactly one item in the changes table
#   test_record_write_is_put_only          the record path calls PutItem only -- a trapped Update/Delete/BatchWrite fails it
. "$(dirname "$0")/_root.sh"
F="$MPW_DIR/tests/test_owner_key_and_record.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_each_outcome_appends_one_record test_record_write_is_put_only; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 2; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 2 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
