#!/usr/bin/env bash
# OPLGTW OG-bi-4 AC1 (row Z-W28-S27): tests/test_deploy_base_guard.py is green again on a tree that carries the bun
# cache pre-check, and it now also proves the pre-check sits in front of the upload. The whole file passes with 0
# failed; among its tests are two named ones: (01) `test_ogbi4_ac01` -- with the rig's dashboard stub carrying a
# lockfile whose entries are all in the rig's stub cache, the deploy script reaches the step the base-guard tests
# need (the rig's upload stub is called); (02) `test_ogbi4_ac02` NEGATIVE CONTROL -- with one lockfile entry absent
# from the stub cache the script stops with `ERROR: bun cache miss` and the rig's upload stub is NEVER called.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
f="tests/test_deploy_base_guard.py"
[ -f "$GW/$f" ] || { echo "$GW/$f absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$GW" && timeout 280 python -m pytest "$f" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ogbi4_ac01 test_ogbi4_ac02; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
passed=$(printf '%s\n' "$out" | grep -cE ' PASSED')
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 2; file passed $passed; failed/error lines $failed"
restore_audit
[ "$rc" = 0 ] && [ "$p" = 2 ] && [ "$failed" = 0 ] && [ "$passed" -ge 8 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
