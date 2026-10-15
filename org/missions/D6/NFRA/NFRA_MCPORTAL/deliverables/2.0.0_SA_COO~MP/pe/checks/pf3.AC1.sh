#!/usr/bin/env bash
# MP-pf-3 AC1 (a declared `store` source group is a group, not a gap, and a tool is listed under every pair it serves; decomposition PF.7): tests/test_admin_gateway_breakdown.py passes with 0 failed and each named test PASSES:
#   test_declared_store_kind_makes_a_store_group                a tool_index source_group {id: ycharts, name: Ycharts, kind: store} puts the tool in a channel id ycharts, name Ycharts, kind store
#   test_store_declaration_is_not_malformed                     the same tool is NOT in undeclared, and a store element with an empty id is still malformed
#   test_groups_are_ordered_bucket_store_integration_native_undeclared   the channels order of PF.7
#   test_tool_serving_two_pairs_is_listed_in_each_segment       a tool whose serves holds two pairs is in both segments
#   test_missing_serves_reads_unresolved_pair                   no serves, an empty serves and a non-list serves all read the unresolved pair
. "$(dirname "$0")/../../pd/checks/_root.sh"
named_pytest "store and serves tests" tests/test_admin_gateway_breakdown.py \
  test_declared_store_kind_makes_a_store_group test_store_declaration_is_not_malformed \
  test_groups_are_ordered_bucket_store_integration_native_undeclared test_tool_serving_two_pairs_is_listed_in_each_segment \
  test_missing_serves_reads_unresolved_pair
