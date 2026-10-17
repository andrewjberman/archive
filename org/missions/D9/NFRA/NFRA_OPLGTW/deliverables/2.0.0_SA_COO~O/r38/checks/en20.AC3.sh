#!/usr/bin/env bash
# OPLGTW OG-en-20 AC3 (round 40): the window test files pass together, in both orders, with the same count.
#  - pytest over tests/test_og_en4.py, en12, cl2, en13, en15, en17, en18 in one run (forward) passes with no failure;
#  - the same nine files in the reverse order pass with the same passed count (a test must not depend on what ran before it);
#  - base: tests/test_og_en18.py is absent, so both runs error and no passed count is printed (FAIL as expected).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
GW=infra/aws/ec2/opal-gateway
run() {
  ( cd "$GW" && timeout 280 python -m pytest -q -p no:cacheprovider "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | tail -1 )
}
fwd=$(run tests/test_og_en4.py tests/test_og_en12.py tests/test_og_cl2.py tests/test_og_en13.py tests/test_og_en15.py tests/test_og_en17.py tests/test_og_en18.py tests/test_og_en19.py tests/test_og_en20.py)
rev=$(run tests/test_og_en20.py tests/test_og_en19.py tests/test_og_en18.py tests/test_og_en17.py tests/test_og_en15.py tests/test_og_en13.py tests/test_og_cl2.py tests/test_og_en12.py tests/test_og_en4.py)
pf=$(printf '%s' "$fwd" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); ff=$(printf '%s' "$fwd" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
pr=$(printf '%s' "$rev" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); fr=$(printf '%s' "$rev" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1)
echo "en4, en12, cl2, en13, en15, en17, en18, en19, en20 forward: passed ${pf:-0}; failed ${ff:-0}"
echo "en20, en19, en18, en17, en15, en13, cl2, en12, en4 reverse: passed ${pr:-0}; failed ${fr:-0}"
restore_audit
[ "${ff:-0}" = 0 ] && [ "${fr:-0}" = 0 ] && [ "${pf:-0}" -ge 1 ] && [ "${pr:-0}" -ge 1 ] && [ "${pf:-0}" = "${pr:-0}" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
