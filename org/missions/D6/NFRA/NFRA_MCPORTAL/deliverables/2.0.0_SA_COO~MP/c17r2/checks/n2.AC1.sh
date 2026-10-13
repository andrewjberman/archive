#!/usr/bin/env bash
# MP-n-2 AC1 (C17 round 2 E1, gateway side; decomposition C17R2.2): tests/test_admin_fabric_gitstate.py passes with 0 failed
# and each named test PASSES:
#   test_refused_fetch_count_equals_box_count_at_1x_and_10x   E1 (1): a planted stub store, 1x and 10x window history:
#                                                             _refused's get_object count == the roster box count (4) at both
#   test_pointer_rc_nonzero_reads_at_and_note                 E1 (2): a planted pointer with rc != 0 -> {at, note}
#   test_pointer_rc_zero_or_absent_reads_not_recorded         E1 (2): rc == 0, and an absent pointer -> "not recorded"
#   test_refused_reads_no_window_body                         the window scan is gone: _refused fetches no history key
. "$(dirname "$0")/../../cp2/checks/_root.sh"
named_pytest "gitstate tests" tests/test_admin_fabric_gitstate.py test_refused_fetch_count_equals_box_count_at_1x_and_10x test_pointer_rc_nonzero_reads_at_and_note test_pointer_rc_zero_or_absent_reads_not_recorded test_refused_reads_no_window_body
