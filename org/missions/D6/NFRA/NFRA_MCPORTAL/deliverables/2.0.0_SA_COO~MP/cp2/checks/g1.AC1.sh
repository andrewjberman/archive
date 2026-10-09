#!/usr/bin/env bash
# MP-s-1 AC1 (FWD-16 ACCEPT, C14, A16; decomposition CP2.3-G): tests/test_admin_fabric_gitstate.py passes with 0 failed and
# each named test PASSES:
#   test_gitstate_state_rule                    four planted boxes read committed-not-pushed / pushed-not-on-trunk / on trunk / not recorded
#   test_gitstate_absent_box_reads_not_recorded NoSuchKey latest.json -> status and state 'not recorded', fields null
#   test_gitstate_integration_refused           an integrate pass with rc!=0 is shown; none -> the literal 'not recorded'
#   test_gitstate_store_unreadable_returns_503  AccessDenied -> 503 store unreadable
#   test_gitstate_non_owner_is_refused          a non-owner -> 403 and zero store calls
. "$(dirname "$0")/_root.sh"
named_pytest "gitstate tests" tests/test_admin_fabric_gitstate.py test_gitstate_state_rule test_gitstate_absent_box_reads_not_recorded test_gitstate_integration_refused test_gitstate_store_unreadable_returns_503 test_gitstate_non_owner_is_refused
