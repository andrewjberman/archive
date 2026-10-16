#!/usr/bin/env bash
# MP-pf-6 AC1 (the comparator's planted arms): the worker's test file deliverables/0.9.0_WK_NFRA_MCPORTAL~36/test_r2_principal_sets.py passes with 0 failed and each named test PASSES:
#   test_equal_sets_report_equal                      two equal non-empty sets: equal true, only_scan_n 0, only_history_n 0
#   test_principal_only_in_scan_fails                  a planted principal in the scan set only: equal false, only_scan_n 1
#   test_principal_only_in_history_fails               a planted principal in the history set only: equal false, only_history_n 1
#   test_two_empty_sets_are_not_evidence               both sets empty: equal false and `vacuous` true (an empty equals an empty proves nothing)
. "$(dirname "$0")/../../pc/checks/_root.sh"
D=org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~36
[ -f "$D/test_r2_principal_sets.py" ] || { echo "$D/test_r2_principal_sets.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$D" && timeout 110 python -m pytest test_r2_principal_sets.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
n=0; for t in test_equal_sets_report_equal test_principal_only_in_scan_fails test_principal_only_in_history_fails test_two_empty_sets_are_not_evidence; do
  printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
echo "comparator tests: $tail; named tests PASSED $n of 4"
if [ "$n" = 4 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
