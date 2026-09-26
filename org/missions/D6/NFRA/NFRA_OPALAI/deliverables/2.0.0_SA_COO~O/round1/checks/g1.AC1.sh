#!/usr/bin/env bash
# OA-g-1 AC1 (the grammar): a grant may carry zero Schwab masters ONLY with a non-empty portal_channels scope; zero of both is Malformed; a portal-only grant admits no Schwab tool.
. "$(dirname "$0")/_root.sh"
cd infra/aws/ec2/opal-gateway || { echo "gateway dir absent"; echo "RESULT: FAIL"; exit 1; }
F="tests/test_portal_grant.py"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
grep -q "moto" "$F" && { echo "$F imports moto (must run on site Z)"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 100 python -m pytest "$F" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_portal_grant_zero_masters_parses test_portal_only_grant_admits_no_schwab_tool; do
  printf "%s\n" "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf "%s\n" "$out" | grep -cE " FAILED| ERROR")
echo "pytest rc=$rc; named tests passed $p of 2; failed/error lines $failed"
if [ "$rc" = 0 ] && [ "$p" = 2 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
