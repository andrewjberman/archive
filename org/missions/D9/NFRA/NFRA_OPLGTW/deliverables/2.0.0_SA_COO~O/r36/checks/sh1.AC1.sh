#!/usr/bin/env bash
# OPLGTW OG-sh-1 AC1 (round-36 E4): the gateway tool list_shared_folder(url) resolves a sharing URL by Graph
# /shares/u!<base64url>/driveItem, then /children. It is READ class and classified in app/data_entitlement.py. Named tests in
# tests/test_og_sh1.py; the family and guard suites add no failing id beyond the baseline.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_sh1.py test_ogsh1_ac01 test_ogsh1_ac02 test_ogsh1_ac03; r0=$?
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_data_entitlement_family.py tests/test_data_entitlement_guard.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
new=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED ([^ ]+).*/\1/' | tr '\\' '/' | while read -r id; do grep -qxF "$id" "$GW/tests/baseline/failing_ids_full.txt" || echo "$id"; done | grep -c .)
echo "family+guard suites: failing ids not in the baseline: $new (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
