#!/usr/bin/env bash
# MP-k-1 AC1 (FWD-17 ACCEPT, C11, A17; decomposition CP2.3-K): tests/test_admin_fabric_calls.py passes with 0 failed and
# each named test PASSES:
#   test_calls_absent_box_reads_absent            NoSuchKey open_calls.json -> status absent, open null, no calls from it
#   test_calls_open_filter_and_order              state=open keeps OPEN rows, oldest first; state=all keeps all; other -> 400
#   test_close_writes_one_request_under_requests  202; exactly ONE put_object, key box=<B>/requests/<rid>.json, body per CP2.3-K
#   test_close_refuses_call_not_open              a CLOSED or unknown call_id -> 409 and zero put_object
#   test_close_bad_input_400                      off-roster box, empty ruling, 4001-char ruling -> 400 and zero put_object
#   test_calls_non_owner_is_refused               GET and POST by a non-owner -> 403 and zero store calls
. "$(dirname "$0")/_root.sh"
named_pytest "calls tests" tests/test_admin_fabric_calls.py test_calls_absent_box_reads_absent test_calls_open_filter_and_order test_close_writes_one_request_under_requests test_close_refuses_call_not_open test_close_bad_input_400 test_calls_non_owner_is_refused
