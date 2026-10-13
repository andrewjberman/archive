#!/usr/bin/env bash
# MP-n-5 AC1 (C17 round-1 analysis E2): .tools/tests/test_safe_ec2_deploy_manifest.py passes with 0 failed, and the two new
# arms PASS:
#   test_new_commit_moves_previous_deployed_commit    commit A then commit B -> previous_deployed_commit == A
#   test_equal_commit_leaves_previous_unchanged       B then B -> previous_deployed_commit unchanged
# (the file's existing arms keep escape style, key order and newline convention byte-equal outside the moved fields)
. "$(dirname "$0")/../../cp2/checks/_root.sh"
TF=.tools/tests/test_safe_ec2_deploy_manifest.py
out=$(timeout 110 python -m pytest "$TF" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
n=0; for t in test_new_commit_moves_previous_deployed_commit test_equal_commit_leaves_previous_unchanged; do
  printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
echo "manifest helper tests: $tail; named tests PASSED $n of 2"
if [ "$n" = 2 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
