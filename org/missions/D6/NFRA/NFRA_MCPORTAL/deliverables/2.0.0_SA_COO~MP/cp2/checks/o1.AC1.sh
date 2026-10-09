#!/usr/bin/env bash
# MP-o-1 AC1 (FWD-15 ACCEPT, C13, A15; decomposition CP2.3-O): tests/test_admin_fabric_overlap.py passes with 0 failed and
# each named test PASSES:
#   test_terraform_with_open_deploy_rated_above_shared_log   A15: a planted tf: overlap with an OPEN deploy naming it > a planted append: overlap
#   test_overlap_needs_two_roster_boxes                      one box, or one roster box + one unrostered box, is no overlap
#   test_deploys_absent_box_reads_absent                     NoSuchKey on a box's open_deploys.json -> status absent, open null
#   test_overlap_store_unreadable_returns_503                AccessDenied on the listing -> 503 store unreadable, no overlaps key
#   test_overlap_non_owner_is_refused                        a non-owner -> 403 and zero store calls
. "$(dirname "$0")/_root.sh"
named_pytest "overlap tests" tests/test_admin_fabric_overlap.py test_terraform_with_open_deploy_rated_above_shared_log test_overlap_needs_two_roster_boxes test_deploys_absent_box_reads_absent test_overlap_store_unreadable_returns_503 test_overlap_non_owner_is_refused
