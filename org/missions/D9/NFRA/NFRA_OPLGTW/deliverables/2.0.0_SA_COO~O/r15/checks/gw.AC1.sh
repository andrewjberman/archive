#!/usr/bin/env bash
# OPLGTW OG-gw-1 AC1 (analysis round 14 R1): the three named tests in the grant writer's
# tests/test_build_input_pinned.py pass -- build_package.py stages its closure from EC2_MANIFEST.json
# services.opal-gateway.deployed_commit, never from the working checkout -- and the run leaves no tracked file dirty.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
L="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
[ -f "$L/tests/test_build_input_pinned.py" ] || { echo "$L/tests/test_build_input_pinned.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$L" && timeout 300 python -m pytest tests/test_build_input_pinned.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_oggw1_ac01 test_oggw1_ac02 test_oggw1_ac03; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
f=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 3; failed/error lines $f"
dirty=$(git status --porcelain --untracked-files=no -- "$L" | grep -c .)
echo "tracked files dirty under the grant writer after the run: $dirty"
[ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$f" = 0 ] && [ "$dirty" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
