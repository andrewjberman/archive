#!/usr/bin/env bash
# MP-b-2 AC1 (R-2, both branches built and selected by configuration): the four named owner-key tests pass, nothing failed.
#   test_owner_key_oid_branch        MCPORTAL_OWNER_KEY_CLAIM=oid: a verified header whose oid matches is the owner
#   test_owner_key_sub_branch        MCPORTAL_OWNER_KEY_CLAIM=sub: a verified header whose sub matches is the owner
#   test_iat_absent_uses_exp         no iat: freshness is the signed exp, and an expired header is refused
#   test_no_owner_claim_refuses      a verified header carrying neither oid nor sub is refused before any store call
. "$(dirname "$0")/_root.sh"
F="$MPW_DIR/tests/test_owner_key_and_record.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_owner_key_oid_branch test_owner_key_sub_branch test_iat_absent_uses_exp test_no_owner_claim_refuses; do
  printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 4; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 4 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
