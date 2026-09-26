#!/usr/bin/env bash
# OA-f-1 AC1 (the client-keyed scope): the named tests in tests/test_identity_scope.py pass, nothing failed.
#   test_upload_admitted_only_for_operator_client       a client-qualified row admits its own client_id
#   test_upload_refused_for_other_client_same_identity  the same identity on ANOTHER client_id is refused
#   test_scoped_deny_by_default                         reads a FIXTURE overlay (never the live file) and passes
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_identity_scope.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_upload_admitted_only_for_operator_client test_upload_refused_for_other_client_same_identity test_scoped_deny_by_default; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 3; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
