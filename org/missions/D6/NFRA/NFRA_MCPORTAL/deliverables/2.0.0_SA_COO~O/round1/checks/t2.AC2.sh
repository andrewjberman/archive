#!/usr/bin/env bash
# MP-t-2 AC2 (built, with its negative arms): the writer's tests in its source_dir pass -- the four named tests, nothing
# failed. The three refusals are proven BEFORE any store call (the fake store records zero calls on each).
#   test_refused_without_owner_header   test_refused_for_non_owner   test_refused_for_stale_header
#   test_owner_write_lands_with_operator_audit   (the grant revision and its operator_audit land in ONE transaction)
. "$(dirname "$0")/_root.sh"
e=$(mp_writer_entry); src=$(printf '%s\n' "$e" | sed -n 3p)
F="$src/tests/test_grant_writer.py"
[ -n "$src" ] && [ -f "$F" ] || { echo "writer tests absent (${F})"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_refused_without_owner_header test_refused_for_non_owner test_refused_for_stale_header test_owner_write_lands_with_operator_audit; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 4; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 4 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
