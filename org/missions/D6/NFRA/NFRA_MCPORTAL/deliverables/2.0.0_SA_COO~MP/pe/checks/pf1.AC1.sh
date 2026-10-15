#!/usr/bin/env bash
# MP-pf-1 AC1 (the breakdown segments an assets/bd bucket by vendor and firm; decomposition PF.1): tests/test_admin_gateway_breakdown.py passes with 0 failed and each named test PASSES:
#   test_assets_bucket_splits_into_vendor_firm_segments           opal-data-assets tools with vendor/firm fields give one segment per pair
#   test_multi_none_and_unresolved_firms_are_own_segments         firm multi, none and unresolved are their own segments, never folded into a named firm
#   test_missing_vendor_or_firm_reads_unresolved                  a missing, non-string or empty vendor/firm reads the literal unresolved
#   test_bucket_without_vendor_firm_fields_has_no_segments        a bucket other than assets/bd (e.g. opal-data-harvest) carries no segments key
#   test_segments_order_named_firms_before_multi_none_unresolved  vendor ascending; named firms, then multi, none, unresolved
#   test_tool_in_two_buckets_is_segmented_only_where_it_is_assets_or_bd
. "$(dirname "$0")/../../pd/checks/_root.sh"
named_pytest "segment tests" tests/test_admin_gateway_breakdown.py \
  test_assets_bucket_splits_into_vendor_firm_segments test_multi_none_and_unresolved_firms_are_own_segments \
  test_missing_vendor_or_firm_reads_unresolved test_bucket_without_vendor_firm_fields_has_no_segments \
  test_segments_order_named_firms_before_multi_none_unresolved test_tool_in_two_buckets_is_segmented_only_where_it_is_assets_or_bd
