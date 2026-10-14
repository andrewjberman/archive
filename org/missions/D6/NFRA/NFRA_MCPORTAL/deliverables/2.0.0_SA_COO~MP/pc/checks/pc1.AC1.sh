#!/usr/bin/env bash
# MP-pc-1 AC1 (G1, row Z-C-S31; decomposition PC.2): tests/test_admin_fabric_gitstate.py passes with 0 failed, and each
# named test PASSES:
#   test_refused_rc_zero_reads_no_with_at                 pointer rc 0 -> {"refused": false, "at": <at>}
#   test_refused_rc_nonzero_reads_refused_with_at_and_note pointer rc != 0 -> {"refused": true, "at", "note"}
#   test_refused_no_pointer_reads_not_recorded             no pointer (404) -> "not recorded"
#   test_refused_basis_names_the_state_that_applies        per-box integration_refused_basis starts "refused:", "no:" or
#                                                          "not recorded:" to match that box's state
#   test_refused_fetch_count_equals_box_count_at_1x_and_10x  the C17 bound, unchanged: one get per box
. "$(dirname "$0")/_root.sh"
named_pytest "gitstate three states" tests/test_admin_fabric_gitstate.py test_refused_rc_zero_reads_no_with_at test_refused_rc_nonzero_reads_refused_with_at_and_note test_refused_no_pointer_reads_not_recorded test_refused_basis_names_the_state_that_applies test_refused_fetch_count_equals_box_count_at_1x_and_10x
