#!/usr/bin/env bash
# OA-g-1 AC3 (the operator path; AMENDED on row Z-W9-S1 to add the owner read-back): ops/schwab_entitlement_admin.py validates a portal-only candidate against the amended contract, and rejects one naming a channel the catalog does not hold.
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_portal_grant.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
grep -q "moto" "$F" && { echo "$F imports moto (must run on site Z)"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_admin_accepts_portal_only_candidate test_admin_rejects_unknown_portal_channel test_admin_readback_shows_portal_channels; do
  printf "%s\n" "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf "%s\n" "$out" | grep -cE " FAILED| ERROR")
echo "pytest rc=$rc; named tests passed $p of 3; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 3 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
