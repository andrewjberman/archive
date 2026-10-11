#!/usr/bin/env bash
# OPLGTW OG-bd-1 AC2 (round-34 E8, row W45-S2): decide() denies blackdiamond_list_fees to an unprofiled principal. A profiled
# principal keeps today's answer, and the five Schwab tools stay denied. The tests are named in tests/test_og_bd1.py, and
# the data-entitlement guard and family suites still pass (each measured against the failing-ID baseline:
# no NEW failing id).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_bd1.py test_ogbd1_ac01 test_ogbd1_ac02 test_ogbd1_ac03; r0=$?
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_data_entitlement_family.py tests/test_data_entitlement_guard.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
new=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED ([^ ]+).*/\1/' | while read -r id; do grep -qxF "$id" "$GW/tests/baseline/failing_ids_full.txt" || echo "$id"; done | grep -c .)
echo "family+guard suites: failing ids not in the baseline: $new (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
