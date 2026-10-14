#!/usr/bin/env bash
# MP-pd-2 AC1 (F2, the writer; decomposition PD.2): the Lambda's tests/test_person_access.py passes with 0 failed and each
# named test PASSES:
#   test_person_access_first_write_creates_revision_1            a first write (expect_revision null) lands revision 1 with the audit in the same transaction
#   test_person_access_update_requires_current_revision          a stale expect_revision -> STALE-REVISION and zero writes
#   test_person_access_header_refusals_make_zero_store_calls     no header, a non-owner and a stale header each refuse before any store call
#   test_person_access_bad_shape_refused_before_store            a bad change shape or a non-GUID tid -> BAD-PERSON-ACCESS / BAD-TID, zero store calls
#   test_person_access_stop_and_restore_round_trip               stopped true then false: two revisions, each outcome's before and after in the change record
#   test_person_access_refused_when_record_kind_not_live         the staged access_state without person_access -> RECORD-KIND-NOT-LIVE, zero store calls
#   test_person_access_revoke_is_a_tombstone_never_a_delete      status revoked writes revision + 1 and no delete op is ever issued
. "$(dirname "$0")/_root.sh"
named_pytest_in "writer person_access tests" "$LAM" tests/test_person_access.py \
  test_person_access_first_write_creates_revision_1 test_person_access_update_requires_current_revision \
  test_person_access_header_refusals_make_zero_store_calls test_person_access_bad_shape_refused_before_store \
  test_person_access_stop_and_restore_round_trip test_person_access_refused_when_record_kind_not_live \
  test_person_access_revoke_is_a_tombstone_never_a_delete
