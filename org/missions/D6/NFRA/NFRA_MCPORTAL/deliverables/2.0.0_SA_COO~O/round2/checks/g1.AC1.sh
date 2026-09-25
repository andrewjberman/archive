#!/usr/bin/env bash
# MP-g-1 AC1 (E1's capture): the two named claim-capture tests pass, nothing failed.
#   test_whoami_returns_claim_keys_to_owner          GET /api/admin/whoami, as the owner, returns the verified header's claim
#                                                    keys and its oid/sub values; a non-owner is refused
#   test_claim_keys_logged_once_without_other_values the OWNER-HEADER-CLAIMS line is printed once per process and carries no
#                                                    claim value other than oid and sub (a planted name/email never appears)
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_admin_round2.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_whoami_returns_claim_keys_to_owner test_claim_keys_logged_once_without_other_values; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 2; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 2 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
