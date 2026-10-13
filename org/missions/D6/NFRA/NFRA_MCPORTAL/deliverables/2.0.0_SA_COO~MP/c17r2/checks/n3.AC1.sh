#!/usr/bin/env bash
# MP-n-3 AC1 (C17 round 2 E1, producer side; 4.0.0_SA_CRO~Z consent conditions 1-4): .tools/tests/test_fabric_gitstate_pointer.py
# passes with 0 failed and each named test PASSES:
#   test_pointer_written_on_integrate_only                  (1) --mode integrate writes last_integrate.json; box/manual/dry do not
#   test_pointer_key_uses_prefix_and_box                    (2) the key is <PREFIX>/box=<B>/last_integrate.json, same client
#   test_pointer_rc_and_at_join_the_pass_record             (3) rc == --rc; at == the stamped record's at; note <= 200 chars;
#                                                               body keys exactly {at, rc, note}, ASCII
#   test_failed_pointer_put_reported_and_others_attempted   (4) a raising pointer put: LAST line carries pointer=no:<Exc>,
#                                                               both existing keys still attempted, exit code unchanged
. "$(dirname "$0")/../../cp2/checks/_root.sh"
TF=.tools/tests/test_fabric_gitstate_pointer.py
[ -f "$TF" ] || { echo "$TF absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 110 python -m pytest "$TF" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
n=0; for t in test_pointer_written_on_integrate_only test_pointer_key_uses_prefix_and_box test_pointer_rc_and_at_join_the_pass_record test_failed_pointer_put_reported_and_others_attempted; do
  printf '%s\n' "$out" | grep -qE "::${t}(\[[^]]*\])? PASSED" && n=$((n+1)); done
tail=$(printf '%s\n' "$out" | tail -1)
failed=$(printf '%s' "$tail" | grep -oE '[0-9]+ (failed|error)' | grep -oE '[0-9]+' | head -1); failed=${failed:-0}
echo "pointer tests: $tail; named tests PASSED $n of 4"
if [ "$n" = 4 ] && [ "$failed" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
