#!/usr/bin/env bash
# OPLGTW OG-ad-1 AC2 (round-37, PRD v3.14, CVO half refusal Z-S162): the named offline tests of the admission change pass, and the entitlement suites that pin the sets still pass (the family pin moves by exactly five).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_ad1.py test_ogad1_ac01 test_ogad1_ac02 test_ogad1_ac03 test_ogad1_ac04 test_ogad1_ac05; r0=$?
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_data_entitlement_family.py tests/test_entitlement_admin.py tests/test_og_bd2.py tests/test_og_bd3.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); failed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | head -1 | grep -oE '[0-9]+')
echo "entitlement suites: pytest rc=$rc; passed ${passed:-0}; failed ${failed:-0} (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$rc" = 0 ] && [ "${failed:-0}" = 0 ] && [ "${passed:-0}" -ge 19 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
