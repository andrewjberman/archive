#!/usr/bin/env bash
# OA-f-14 AC2 (nothing else moved): the four suites that already hold the /login admit rule, the identity allowlist and
# the tier scope-minting still read exactly their BASE result -- every test that passed at the cut still passes, and no
# test fails that did not fail at the cut. The base failed set is measured at the cut and pinned below.
. "$(dirname "$0")/_root.sh"
G=infra/aws/ec2/opal-gateway
SUITES="tests/test_login_admit_r24.py tests/test_identity_scope.py tests/test_tier_principal.py tests/test_principal_cutover.py"
BASE_PASSED=36
BASE_FAILED=""
out=$(cd "$G" && timeout 280 python -m pytest $SUITES -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -v '^[[:space:]]*$')
passed=$(printf '%s\n' "$out" | grep -cE '^PASSED ')
failed_set=$(printf '%s\n' "$out" | grep -E '^(FAILED|ERROR) ' | awk '{print $2}' | sort | tr '\n' ' ' | sed 's/ $//')
summ=$(printf '%s\n' "$out" | tail -1)
echo "passed $passed (base $BASE_PASSED); failed=[$failed_set] (base [$BASE_FAILED]); summary: $summ"
if [ "$passed" -ge "$BASE_PASSED" ] && [ "$failed_set" = "$BASE_FAILED" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
