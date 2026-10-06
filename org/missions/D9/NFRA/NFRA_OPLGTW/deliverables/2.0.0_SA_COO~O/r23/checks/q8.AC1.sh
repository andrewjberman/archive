#!/usr/bin/env bash
# OPLGTW OG-q-8 AC1 (CTO R29/R30.1): a blank or null cusip never qualifies a dim_asset row. Four named tests in
# tests/test_schwab_q8_blank_cusip.py, through the shipped build_default_service() construction: (01) the dim_asset QUERY
# returns 0 blank-cusip rows when a held position has a blank cusip; (02) the dim_asset DOWNLOAD returns 0 blank-cusip
# rows in the same case; (03) None and whitespace-only position cusips are dropped while every non-blank held CUSIP is
# still returned; (04) a grant whose held positions carry ONLY blank cusips refuses asset_read_denied_unqualified.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r23_q8_audit_$$.jsonl"
pytest_named tests/test_schwab_q8_blank_cusip.py test_ogq8_ac01 test_ogq8_ac02 test_ogq8_ac03 test_ogq8_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
