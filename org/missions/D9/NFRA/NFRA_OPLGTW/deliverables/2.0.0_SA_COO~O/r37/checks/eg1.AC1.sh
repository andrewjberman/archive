#!/usr/bin/env bash
# OPLGTW OG-eg-1 AC1 (round-37 EGRESS, PRD v3.10 E1+E2): the harvest runner stops re-reading whole silver prefixes, and its cycle record counts its S3 GETs.
#   ac01 the cached silver_latest returns EXACTLY what the uncached one returns, across a sequence that writes new parts between calls (tie-break rules intact);
#   ac02 at one fixed pair count (50 watermark calls + 10 appends over a 30-part table) the GET count inside the cache context is 30 plus the NEW parts, against 60 x 30 without it;
#   ac03 outside the cache context behaviour is unchanged (every call is a full scan);
#   ac04 the cache holds at most two (source, table, fields) entries (an evicted one is rebuilt on its next use with the same result);
#   ac05 the cycle record carries integer s3_get_count and s3_get_bytes equal to the counting client's totals for the cycle, and nothing is sent (a record, never an alert).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(timeout 115 python -m pytest lib/opal_data_harvest/test_eg1_silver_cache.py -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_eg1_ac01 test_eg1_ac02 test_eg1_ac03 test_eg1_ac04 test_eg1_ac05; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 5; failed/error lines $failed"
[ "$rc" = 0 ] && [ "$p" = 5 ] && [ "$failed" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
