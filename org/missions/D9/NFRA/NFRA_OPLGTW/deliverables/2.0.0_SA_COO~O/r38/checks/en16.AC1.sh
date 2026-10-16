#!/usr/bin/env bash
# OPLGTW OG-en-16 AC1 (round 39): the OG-en-14 tests no longer depend on test order.
#  - pytest over tests/test_og_en4.py, tests/test_og_en12.py then tests/test_og_en14.py, IN THAT ORDER, in one run, passes (the pair en4 then en14 and en12 then en14 each failed at the base with "Missing required env var: TENANT_ID");
#  - the same three files in the reverse order pass too.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
run() {
  ( cd "$GW" && timeout 200 python -m pytest -q -p no:cacheprovider "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | tail -1 )
}
fwd=$(run tests/test_og_en4.py tests/test_og_en12.py tests/test_og_en14.py)
rev=$(run tests/test_og_en14.py tests/test_og_en12.py tests/test_og_en4.py)
pf=$(printf '%s' "$fwd" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); ff=$(printf '%s' "$fwd" | grep -oE '[0-9]+ failed' | grep -oE '[0-9]+')
pr=$(printf '%s' "$rev" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); fr=$(printf '%s' "$rev" | grep -oE '[0-9]+ failed' | grep -oE '[0-9]+')
echo "forward order en4, en12, en14: passed ${pf:-0}; failed ${ff:-0}"
echo "reverse order en14, en12, en4: passed ${pr:-0}; failed ${fr:-0}"
restore_audit
[ "${ff:-0}" = 0 ] && [ "${fr:-0}" = 0 ] && [ "${pf:-0}" -ge 1 ] && [ "${pr:-0}" -ge 1 ] && [ "${pf:-0}" = "${pr:-0}" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
