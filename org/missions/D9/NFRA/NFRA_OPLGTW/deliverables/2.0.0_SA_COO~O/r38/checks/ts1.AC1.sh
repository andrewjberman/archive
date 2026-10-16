#!/usr/bin/env bash
# OPLGTW OG-ts-1 AC1 (round 38 remediation): the OG-gp-1 and OG-gf-1 suites pass at HEAD, the two ac01 classification pins pass, and the difference controls
# (test_ogts1_control_gp1, test_ogts1_control_gf1: a planted unaccounted classification key makes the pin fail) exist and pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 115 python -m pytest tests/test_og_gp1.py tests/test_og_gf1.py tests/test_og_ts1.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); failed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | head -1 | grep -oE '[0-9]+')
ac01=$(cd "$GW" && timeout 100 python -m pytest tests/test_og_gp1.py::test_oggp1_ac01 tests/test_og_gf1.py::test_oggf1_ac01 -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r' | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+')
ctl=$(cd "$GW" && grep -hcE '^def test_ogts1_control_(gp1|gf1)' tests/test_og_gp1.py tests/test_og_gf1.py tests/test_og_ts1.py 2>/dev/null | awk '{s+=$1} END{print s+0}')
echo "gp1 and gf1 suites: pytest rc=$rc; passed ${passed:-0}; failed ${failed:-0} (want 0); named: ac01 pins ${ac01:-0} of 2, controls ${ctl:-0} (want 1 or more)"
restore_audit
[ "$rc" = 0 ] && [ "${failed:-0}" = 0 ] && [ "${passed:-0}" -ge 1 ] && [ "${ac01:-0}" = 2 ] && [ "${ctl:-0}" -ge 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
