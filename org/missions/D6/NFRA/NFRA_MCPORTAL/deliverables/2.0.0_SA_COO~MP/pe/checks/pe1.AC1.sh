#!/usr/bin/env bash
# MP-pe-1 AC1 (the breakdown groups by source; decomposition PE.2): tests/test_admin_gateway_breakdown.py passes with 0 failed and each named test PASSES:
#   test_no_tool_lands_in_microsoft_365_without_a_graph_scope        a tool with no spec, no declaration and no graph scope is not in m365
#   test_declared_source_group_names_the_bucket_group                a tool_index source_group {id,name,kind bucket} makes a group with that id and name, kind bucket
#   test_tool_declaring_two_buckets_appears_in_each                  a list of two elements lists the tool in both groups
#   test_undeclared_tool_lands_in_no_source_declared                 no declaration, no graph scope -> id undeclared, name "No source declared", kind undeclared
#   test_integration_spec_still_wins_over_a_declaration              a tool with an integration spec stays in its integration channel even when declared
#   test_malformed_declaration_reads_undeclared                      a source_group missing id, or kind not bucket, is treated as not declared
#   test_grouping_basis_states_the_undeclared_count                  the body's grouping_basis ends "N tool(s) declare no source." with the true N
#   test_groups_are_ordered_bucket_integration_native_undeclared     channel order is bucket, integration, native, undeclared (ids sorted within a kind)
#   test_declared_graph_kind_places_the_tool_in_m365                 (A1) a tool declared kind graph is in m365
#   test_people_view_places_tools_in_the_breakdowns_groups           (A1) the People view gives each tool the same group id and name as the breakdown
. "$(dirname "$0")/../../pd/checks/_root.sh"
named_pytest "breakdown grouping tests" tests/test_admin_gateway_breakdown.py \
  test_no_tool_lands_in_microsoft_365_without_a_graph_scope test_declared_source_group_names_the_bucket_group \
  test_tool_declaring_two_buckets_appears_in_each test_undeclared_tool_lands_in_no_source_declared \
  test_integration_spec_still_wins_over_a_declaration test_malformed_declaration_reads_undeclared \
  test_grouping_basis_states_the_undeclared_count test_groups_are_ordered_bucket_integration_native_undeclared \
  test_declared_graph_kind_places_the_tool_in_m365 test_people_view_places_tools_in_the_breakdowns_groups
