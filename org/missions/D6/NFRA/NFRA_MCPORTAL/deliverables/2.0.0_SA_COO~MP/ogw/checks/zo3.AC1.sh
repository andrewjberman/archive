#!/usr/bin/env bash
# MP-zo-3 AC1 (PRD v0.10 FWD-26 writer side, CVO note on W1'; decomposition v20 OGW1.3): the grant writer's WIDENING rule and the repaired stale test.
# FIVE named tests exist in the writer's tests (names read from the sources), and pytest on the whole tests directory exits 0 with >=PASS_MIN passed and 0 failed
# (base: 35 passed, 1 FAILED -- the stale test; after: that test repaired plus four new = 40 passed):
#   test_person_access_refused_when_record_kind_not_live                                           (repaired in place)
#   test_widening_without_confirm_is_refused_before_any_store_call
#   test_widening_with_the_verified_owners_confirm_is_written_and_recorded
#   test_subtract_restore_and_stop_need_no_widening_confirm
#   test_widening_confirm_from_a_non_owner_master_admin_is_refused_before_any_store_call
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_OGW_W_PASS_MIN:-40}"
L=infra/aws/lambda/mcportal/mcportal-grant-writer-lambda
[ -d "$L/tests" ] || { echo "$L/tests absent"; echo "RESULT: FAIL"; exit 1; }
n=0
for t in test_person_access_refused_when_record_kind_not_live \
         test_widening_without_confirm_is_refused_before_any_store_call \
         test_widening_with_the_verified_owners_confirm_is_written_and_recorded \
         test_subtract_restore_and_stop_need_no_widening_confirm \
         test_widening_confirm_from_a_non_owner_master_admin_is_refused_before_any_store_call; do
  grep -rqE -- "^def $t\(" "$L/tests" && n=$((n+1))
done
out=$(timeout 115 python -m pytest "$L/tests" -q -p no:cacheprovider 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | tail -1 | tr -dc '0-9')
failed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -3
echo "pytest rc=$rc; named tests present in sources $n of 5; passed=${passed:-?} (min $PASS_MIN); failed=${failed:-0}"
if [ "$rc" = 0 ] && [ "$n" = 5 ] && [ "${passed:-0}" -ge "$PASS_MIN" ] && [ "${failed:-0}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
