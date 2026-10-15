#!/usr/bin/env bash
# OPLGTW OG-eg-1 AC2 (round-37 EGRESS): the existing harvest suites that read or write silver still pass, so the silver output is unchanged.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(timeout 118 python -m pytest lib/research/harvest/tests/test_store.py lib/research/harvest/tests/test_o3_silver_tie_break.py lib/research/harvest/test_at4_mixed_prefix_reads.py lib/opal_data_harvest/test_ai5_batched_silver_append.py lib/opal_data_harvest/test_n1_received_bytes_and_run_record.py lib/opal_data_harvest/test_ar1_silver_fields.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
echo "existing silver suites: rc=$rc; $(printf '%s\n' "$out" | tail -1 | cut -c1-90)"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
