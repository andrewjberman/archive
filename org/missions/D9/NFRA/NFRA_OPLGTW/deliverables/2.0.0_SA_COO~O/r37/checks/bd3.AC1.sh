#!/usr/bin/env bash
# OPLGTW OG-bd-3 AC1 (CTO ruling msg 33941, route (a)): master_admin tier admission for TIER_ADMITTED_TOOLS holds on the
# PROFILED branch too. Named tests in tests/test_og_bd3.py: (ac01) a profiled master_admin is ALLOWED
# blackdiamond_list_fees; (ac02) a profiled NON-admin whose grant lacks the tool stays DENIED; (ac03) the unprofiled cases
# are exactly bd-2's. And OG-bd-2's own three tests still pass, and the family + guard suites add no failing id beyond
# the baseline.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_bd3.py test_ogbd3_ac01 test_ogbd3_ac02 test_ogbd3_ac03; r0=$?
pytest_named tests/test_og_bd2.py test_ogbd2_ac01 test_ogbd2_ac02 test_ogbd2_ac03; r1=$?
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_data_entitlement_family.py tests/test_data_entitlement_guard.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
new=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED ([^ ]+).*/\1/' | tr '\\' '/' | while read -r id; do grep -qxF "$id" "$GW/tests/baseline/failing_ids_full.txt" || echo "$id"; done | grep -c .)
echo "family+guard suites: failing ids not in the baseline: $new (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$r1" = 0 ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
