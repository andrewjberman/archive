#!/usr/bin/env bash
# MP-t-1 AC1 (built, both directions in one harness): the owner-gate tests pass -- the five named tests, nothing failed.
#   test_owner_page_served                    Andrew's verified identity gets / and /api/admin/whoami
#   test_non_owner_refused_page_and_handler   a verified NON-owner is refused on / and on /api/admin/whoami
#   test_missing_or_forged_header_refused     no x-amzn-oidc-data, or one failing verification, is refused
#   test_boot_refuses_extra_owner_entry       DASHBOARD_OWNER_EMAILS holding any entry beyond Andrew's refuses boot
#   test_sprint_served_to_non_owner           /sprint still serves a verified non-owner Opal account
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_owner_gate.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_owner_page_served test_non_owner_refused_page_and_handler test_missing_or_forged_header_refused test_boot_refuses_extra_owner_entry test_sprint_served_to_non_owner; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 5; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 5 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
