#!/usr/bin/env bash
# MP-pd-3 AC1 (F2, the gateway handler; decomposition PD.3): tests/test_admin_people_access.py passes with 0 failed and each
# named test PASSES:
#   test_access_post_invokes_writer_with_set_person_access_and_relays_verdict   the POST calls invoke_grant_writer with action set_person_access and relays the verdict
#   test_access_post_payload_matches_pd2_event_shape                            the event carries tid, oid, change, expect_revision, owner_header with the PD.2 names
#   test_access_post_bad_shape_is_400_before_invoke                             a bad change shape is 400 and the invoke fake records zero calls
#   test_access_post_non_owner_is_refused_and_no_invoke                         a non-owner is 403 and zero invoke calls
#   test_access_get_reads_record_when_live                                      the GET answers record_kind live with the record
#   test_access_get_not_live_when_type_unknown                                  access_state refuses the key -> record_kind "not live", record null, 200
#   test_access_bad_guid_is_400                                                 a tid or oid that is not a GUID is 400
. "$(dirname "$0")/_root.sh"
named_pytest "access handler tests" tests/test_admin_people_access.py \
  test_access_post_invokes_writer_with_set_person_access_and_relays_verdict test_access_post_payload_matches_pd2_event_shape \
  test_access_post_bad_shape_is_400_before_invoke test_access_post_non_owner_is_refused_and_no_invoke \
  test_access_get_reads_record_when_live test_access_get_not_live_when_type_unknown test_access_bad_guid_is_400
