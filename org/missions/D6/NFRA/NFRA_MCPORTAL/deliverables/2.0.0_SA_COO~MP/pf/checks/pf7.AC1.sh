#!/usr/bin/env bash
# MP-pf-7 AC1 (the comparator, with the planted principal checked BOTH ways): the worker's test file deliverables/0.9.0_WK_NFRA_MCPORTAL~37/test_r3_principal_sets.py passes with 0 failed and each named test PASSES:
#   test_equal_sets_report_equal                          two equal non-empty sets: equal true, only_page_n 0, only_raw_n 0, vacuous false
#   test_principal_only_in_raw_means_the_page_misses_it   a planted principal in the raw set only: equal false, only_raw_n 1 (the page MISSES a holder: the failure Z-C-S40 asks about)
#   test_principal_only_in_page_is_reported               a planted principal in the page set only: equal false, only_page_n 1
#   test_two_empty_sets_are_not_evidence                  both sets empty: equal false and vacuous true
#   test_scan_denied_stops_without_a_run                  a read file whose SIM line reads Scan=implicitDeny and ends `RESULT: STOP` makes the command exit 3 and write NO run file
# Anchored: the root comes from the _root.sh this script sources, itself reached through THIS script's path, never from the shell's cwd.
. "$(dirname "$0")/../../pc/checks/_root.sh"
D=org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~37
[ -f "$D/test_r3_principal_sets.py" ] || { echo "$D/test_r3_principal_sets.py absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd "$D" && timeout 110 python -m pytest test_r3_principal_sets.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
n=0; for t in test_equal_sets_report_equal test_principal_only_in_raw_means_the_page_misses_it test_principal_only_in_page_is_reported test_two_empty_sets_are_not_evidence test_scan_denied_stops_without_a_run; do
  printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
echo "comparator tests: $tail; named tests PASSED $n of 5"
if [ "$n" = 5 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
