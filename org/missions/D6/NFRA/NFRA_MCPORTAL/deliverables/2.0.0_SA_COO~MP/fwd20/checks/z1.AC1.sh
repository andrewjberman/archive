#!/usr/bin/env bash
# MP-z-1 AC1 (FWD-20 ACCEPT, C15, C16; decomposition GW.3): tests/test_admin_gateway_breakdown.py passes with 0 failed and
# each named test PASSES:
#   test_every_live_tool_in_exactly_one_channel      planted registry: each tool once; an integration's tools under its id
#   test_unclassified_tool_reads_unclassified         a tool data_entitlement.classify does not know -> "unclassified"
#   test_unrated_without_ratings_file                 no channel_ratings.json -> every channel "unrated", reason null
#   test_channel_with_no_holder_is_empty_list         a channel no candidate holds -> holders []
#   test_kill_switch_empties_every_channel            kill switch on -> every holders [], basis says so
#   test_grant_store_unreadable_is_labelled           Scan refused -> grant_store unreadable + reason, never "no grants"
#   test_breakdown_non_owner_is_refused               a non-owner -> 403 and zero store calls
. "$(dirname "$0")/_root.sh"
named_pytest "breakdown tests" tests/test_admin_gateway_breakdown.py test_every_live_tool_in_exactly_one_channel test_unclassified_tool_reads_unclassified test_unrated_without_ratings_file test_channel_with_no_holder_is_empty_list test_kill_switch_empties_every_channel test_grant_store_unreadable_is_labelled test_breakdown_non_owner_is_refused
