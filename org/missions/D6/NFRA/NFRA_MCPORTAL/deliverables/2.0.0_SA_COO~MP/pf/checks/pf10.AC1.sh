#!/usr/bin/env bash
# MP-pf-10 AC1 (the six stale gateway tests, row Z-S67): each of the six named tests PASSES and its two files read 0 failed.
#   tests/test_admin_gateway_breakdown.py: test_every_live_tool_in_exactly_one_channel, test_real_server_tool_inventory
#   tests/test_admin_people.py: test_people_lists_every_candidate_even_holding_nothing, test_cadence_reads_absent_with_reason,
#                               test_real_server_people_inventory, test_people_principal_never_leaks_into_other_fields
# Each file is run on its own (named_pytest runs one file and exits), so the two runs are subshells and the verdict joins them.
. "$(dirname "$0")/../../pc/checks/_root.sh"
( named_pytest "breakdown" tests/test_admin_gateway_breakdown.py test_every_live_tool_in_exactly_one_channel test_real_server_tool_inventory ); a=$?
( named_pytest "people" tests/test_admin_people.py test_people_lists_every_candidate_even_holding_nothing test_cadence_reads_absent_with_reason \
    test_real_server_people_inventory test_people_principal_never_leaks_into_other_fields ); b=$?
echo "breakdown rc=$a people rc=$b"
if [ "$a" = 0 ] && [ "$b" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
