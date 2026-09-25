#!/usr/bin/env bash
# MX-t-8 AC2 (R-6 W4-S1, the fence by exact key prefix, and C4's no-zero rule): the three named tests pass, nothing failed.
#   test_portal_tool_reads_its_exact_prefix_only   each tool reads only its own exact key prefix in opal-data-portal-v2
#   test_sibling_prefix_is_refused                 (negative control) a read aimed at a sibling property's prefix is refused
#   test_empty_partition_is_not_zero               a planted empty/absent object answers "no data for that date", never 0
. "$(dirname "$0")/_root.sh"
if pytest_named tests/test_portal_index.py test_portal_tool_reads_its_exact_prefix_only test_sibling_prefix_is_refused test_empty_partition_is_not_zero; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
