#!/usr/bin/env bash
# OPLGTW OG-da-1 AC1 (CTO~Z ruling msg 32354, dell2 row TCKT_VNEXT-D2-W6-S2): the data_refresh admission is FAIL-CLOSED.
# Five named tests in infra/aws/lambda/data_refresh/test_admission_gate.py (pytest), offline:
#   (01) a Lambda-authorizer context with userType 'Dev' is admitted (positive control);
#   (02) an Opal-internal principal (firm opal-capital, as the authorizer context carries it) with a non-Dev userType is
#        admitted;
#   (03) an EMPTY, missing or 'null' userType with no Opal-internal firm is REFUSED (was admitted: lambda_function.py
#        "if not user_type or user_type == 'Dev': return True");
#   (04) the JWT-claims path follows the same rule (Dev or Opal-internal admitted; empty refused);
#   (05) no authorizer context at all is REFUSED (the old "development fallback" admitted it as dev@test.com).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="infra/aws/lambda/data_refresh"
[ -f "$D/test_admission_gate.py" ] || { echo "$D/test_admission_gate.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$D" && timeout 100 python -m pytest test_admission_gate.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ogda1_ac01 test_ogda1_ac02 test_ogda1_ac03 test_ogda1_ac04 test_ogda1_ac05; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
fl=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 5; failed/error lines $fl"
[ "$rc" = 0 ] && [ "$p" = 5 ] && [ "$fl" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
