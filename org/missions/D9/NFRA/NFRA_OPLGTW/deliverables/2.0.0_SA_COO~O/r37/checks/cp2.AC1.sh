#!/usr/bin/env bash
# OPLGTW OG-cp-2 AC1 (round-37 R37-PERSON): the two tests OG-cp-1 turned red are green and nothing else regresses.
#   test_schwab_host_inputs.py::test_grant_writer_stages_the_contract_only_from_the_standard (the staged contract equals the standard byte for byte)
#   test_admin_people_access.py::test_access_get_not_live_when_type_unknown (its premise: a deployment that does not know the type)
# plus the whole of test_schwab_host_inputs.py, test_admin_people_access.py, test_access_state.py and test_og_cp1.py with no failing id outside the baseline.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 115 python -m pytest tests/test_schwab_host_inputs.py tests/test_admin_people_access.py tests/test_access_state.py tests/test_og_cp1.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r0=$?
ids=$(printf '%s\n' "$out" | grep -E '^(FAILED|ERROR) ' | sed -E 's/^(FAILED|ERROR) ([^ ]+).*/\2/' | sed 's#\\#/#g')
new=0; for i in $ids; do grep -qF "${i#tests/}" "$GW/tests/baseline/failing_ids_full.txt" || new=$((new+1)); done
two=$(printf '%s\n' "$out" | grep -cE 'PASSED .*(test_grant_writer_stages_the_contract_only_from_the_standard|test_access_get_not_live_when_type_unknown)')
echo "$(printf '%s\n' "$out" | tail -1 | cut -c1-90); failing ids not in the baseline: $new (want 0); the two named tests passed: $two of 2"
restore_audit
[ "$new" = 0 ] && [ "$two" = 2 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
