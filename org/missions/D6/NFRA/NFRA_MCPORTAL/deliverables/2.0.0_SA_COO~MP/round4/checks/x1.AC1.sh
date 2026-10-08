#!/usr/bin/env bash
# MP-x-1 AC1 (FWD-14 ACCEPT i-iii, decomposition R4.3): tests/test_admin_fabric.py passes with 0 failed, and each of the
# five named tests PASSES at least once:
#   test_not_reporting_box_reads_not_reporting      a roster box with no record in the window -> status "not reporting"
#   test_counts_match_records_dedup_measured        commits/projects equal a planted record set, one sha twice -> measured kept
#   test_store_unreadable_returns_503               AccessDenied on the listing -> 503 {"error":"store unreadable"}, no boxes
#   test_roster_equals_devices_register             app/refs/fabric_boxes.json names == org/devices/DEVICES.json devices[].name
#   test_non_owner_is_refused                       a non-owner identity -> 403, and the store is never called
. "$(dirname "$0")/_root.sh"
T="$GW/tests/test_admin_fabric.py"
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_admin_fabric.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
n=0; for t in test_not_reporting_box_reads_not_reporting test_counts_match_records_dedup_measured test_store_unreadable_returns_503 test_roster_equals_devices_register test_non_owner_is_refused; do
  printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
echo "fabric tests: $tail; named tests PASSED $n of 5"
if [ "$n" = 5 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
