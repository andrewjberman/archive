#!/usr/bin/env bash
# OPLGTW OG-bd-2 AC1 (round-36 E1, Andrew YES sitez-1b36, CTO round-35 analysis): decide() denies blackdiamond_list_fees to
# an unprofiled principal that is NOT master_admin tier. A master_admin principal with no profile is ADMITTED by tier (no
# profile written), a profiled principal keeps today's answer, and the Schwab tools stay denied to unprofiled. Named tests
# in tests/test_og_bd2.py; the family and guard suites add no failing id beyond the baseline.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_bd2.py test_ogbd2_ac01 test_ogbd2_ac02 test_ogbd2_ac03; r0=$?
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_data_entitlement_family.py tests/test_data_entitlement_guard.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
new=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED ([^ ]+).*/\1/' | tr '\\' '/' | while read -r id; do grep -qxF "$id" "$GW/tests/baseline/failing_ids_full.txt" || echo "$id"; done | grep -c .)
echo "family+guard suites: failing ids not in the baseline: $new (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
