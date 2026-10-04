#!/usr/bin/env bash
# OPLGTW OG-ts-1 AC1 (row Z-W26-S4): the grant writer's test suite runs against the PINNED staged closure
# (build_package.py output from the manifest's deployed_commit), not HEAD's gateway tree: the named test proves the
# imported app.config / app.data_entitlement / contract are the staged bytes, and the whole suite passes.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
L="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
[ -f "$L/tests/test_closure_under_test.py" ] || { echo "$L/tests/test_closure_under_test.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$L" && timeout 400 python -m pytest tests -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=$(printf '%s\n' "$out" | grep -cE "::test_ogts1_ac01(\[.*\])? PASSED")
f=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
dirty=$(git status --porcelain --untracked-files=no -- "$L" "infra/aws/ec2/opal-gateway" | grep -c .)
echo "suite rc=$rc; test_ogts1_ac01 passed $p of 1; failed/error lines $f; tracked files dirty after the run $dirty ($(printf '%s\n' "$out" | tail -1))"
[ "$rc" = 0 ] && [ "$p" = 1 ] && [ "$f" = 0 ] && [ "$dirty" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
