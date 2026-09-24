#!/usr/bin/env bash
# MP-t-4 AC1 (built): the admin grant handler tests pass -- the four named tests, nothing failed.
#   test_get_grant_reads_store                          GET /api/admin/grants/{tid}/{oid} returns the profile + active data grant
#   test_narrow_invokes_writer_with_forwarded_header    POST .../narrow invokes the writer with the request's x-amzn-oidc-data
#   test_gateway_never_writes_policy                    no handler reaches the store's write API (a trapped write fails the test)
#   test_changes_newest_first                           GET /api/admin/changes lists the writer's audit rows newest first, before + after
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_admin_grants.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_get_grant_reads_store test_narrow_invokes_writer_with_forwarded_header test_gateway_never_writes_policy test_changes_newest_first; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 4; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 4 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
