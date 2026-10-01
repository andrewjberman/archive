#!/usr/bin/env bash
# MS-r-1 AC3 (AMENDMENT 1, the control: the deploy script's existing base-ref guard is unmoved by R-4):
# infra/aws/ec2/opal-gateway/tests/test_deploy_base_guard.py passes with nothing failed and at least 6 passed (6 at the
# issuance base b90073c197; 6 FAILED after MS-r-1 first merged, measured by the issuer's drain diff).
. "$(dirname "$0")/_root.sh"
out=$(cd "$G" && AUDIT_PATH="$(mktemp "${TMPDIR:-/tmp}/ms_r1_ac3.XXXXXX")" timeout 110 python -m pytest tests/test_deploy_base_guard.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '')
tail=$(printf '%s
' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
passed=$(printf '%s' "$tail" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); passed=${passed:-0}
echo "deploy base guard suite: $tail"
if [ "$failed" = 0 ] && [ "$passed" -ge 6 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
