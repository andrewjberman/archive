#!/usr/bin/env bash
# OPLGTW OG-q-7 AC1 (CTO round-16 analysis s.4 item 1): the C3 holdings restriction on the dim_asset DOWNLOAD paths,
# proven through the shipped build_default_service() construction with NO asset_policy seam. The four named tests in
# tests/test_schwab_q7_asset_download.py pass: (01) a dim_asset prepare_download holds only CUSIPs held by the grant's
# accounts; (02) a planted UNHELD CUSIP is absent from it; (03) a grant whose accounts hold nothing refuses
# asset_read_denied_unqualified; (04) the dim_asset QUERY returns the same held set as before (unchanged).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r17_q7_audit_$$.jsonl"
pytest_named tests/test_schwab_q7_asset_download.py test_ogq7_ac01 test_ogq7_ac02 test_ogq7_ac03 test_ogq7_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
