#!/usr/bin/env bash
# OPLGTW OG-cp-1 AC1 (PRD v2.9 C-PERSON; CTO msgs 33954, 33958): the gateway reads a per-person `person_access` record
# from the grant store. Six named tests in tests/test_og_cp1.py:
#   ac01 no record (and a non-active record) = today's answers exactly;
#   ac02 a narrowing record denies a tool the floor admits (person_record_denied), the master_admin included;
#   ac03 a widening record admits, for an Opal principal, a served tool the identity-scope floor denied it;
#   ac04 a widening to a tool the gateway does not serve admits nothing;
#   ac05 a record never admits a non-Opal principal (widening ignored; narrowing still honoured);
#   ac06 an unreadable store or malformed record fails CLOSED (person_record_unavailable), never "no record".
# Plus the contract-parity test test_ogd1_ac03 (the closed record-type set, now with person_access), and the bd-2, bd-3,
# family, guard and entitlement-admin suites adding no failing id beyond the baseline (one bounded pytest run).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_cp1.py test_ogcp1_ac01 test_ogcp1_ac02 test_ogcp1_ac03 test_ogcp1_ac04 test_ogcp1_ac05 test_ogcp1_ac06; r0=$?
# test_ogd1_ac03 prints through its own output, which moves pytest -v's PASSED off the id line, so it is read by node id
# and pytest's summary instead of pytest_named.
pa=$(cd "$GW" && timeout 60 python -m pytest "tests/test_access_state.py::test_ogd1_ac03" -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r1=$?
pa_ok=$(printf '%s\n' "$pa" | grep -cE '^1 passed')
echo "contract parity test_ogd1_ac03: rc=$r1; 1 passed: $([ "$pa_ok" -ge 1 ] && echo yes || echo no)"
[ "$pa_ok" -ge 1 ] || r1=1
out=$(cd "$GW" && timeout 100 python -m pytest tests/test_og_bd2.py tests/test_og_bd3.py tests/test_data_entitlement_family.py tests/test_data_entitlement_guard.py tests/test_entitlement_admin.py -rA -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
new=$(printf '%s\n' "$out" | grep -E '^FAILED ' | sed -E 's/^FAILED ([^ ]+).*/\1/' | tr '\\' '/' | while read -r id; do grep -qxF "$id" "$GW/tests/baseline/failing_ids_full.txt" || echo "$id"; done | grep -c .)
echo "bd2+bd3+family+guard+admin suites: failing ids not in the baseline: $new (want 0)"
restore_audit
[ "$r0" = 0 ] && [ "$r1" = 0 ] && [ "$new" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
