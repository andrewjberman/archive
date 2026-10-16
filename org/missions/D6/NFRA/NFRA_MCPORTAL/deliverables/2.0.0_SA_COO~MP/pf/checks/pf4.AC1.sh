#!/usr/bin/env bash
# MP-pf-4 AC1 (the segment compute reads the tool_index block ONLY; CTO round-2 ruling 3, CVO row Z-C-S41): tests/test_admin_gateway_breakdown.py passes with 0 failed and each named test PASSES:
#   test_channel_row_firm_key_never_makes_a_segment   a catalog with a tool_index row that declares a bucket but no `serves`, PLUS a channel-artifact row (read_tool = that tool) and a silver row that each carry
#                                                     `firm: cottonwood` (the owning-firm key), yields ONE segment of the single pair (unresolved, unresolved) and no segment named cottonwood
#   test_tool_index_serves_pair_makes_a_segment       the same catalog with `serves: [{vendor: schwab, firm: cottonwood}]` on the tool_index row yields the segment (schwab, cottonwood)
# The first is a negative arm, the second the positive arm that shows the first is not vacuous (the planted owning-firm rows are present in both).
. "$(dirname "$0")/../../pd/checks/_root.sh"
named_pytest "planted owning-firm arms" tests/test_admin_gateway_breakdown.py \
  test_channel_row_firm_key_never_makes_a_segment test_tool_index_serves_pair_makes_a_segment
