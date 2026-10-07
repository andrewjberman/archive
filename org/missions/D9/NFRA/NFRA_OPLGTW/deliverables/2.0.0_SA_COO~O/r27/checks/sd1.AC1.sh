#!/usr/bin/env bash
# OPLGTW OG-sd-1 AC1 (round-24 analysis, row Z-W28-S13): the status tool's displayed_date reads the served manifest's
# own date key. Three named tests in tests/test_opal_portal_status_displayed_date.py: (01) a manifest carrying exactly
# the live manifest's top-level key set (as row Z-W28-S13 records it) yields a non-null displayed_date equal to that
# manifest's date value; (02) a manifest with no date-like key yields null and the text still rides back;
# (03) the eight keys the function read before this cell still resolve, in their old order.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r27_sd1_audit_$$.jsonl"
pytest_named tests/test_opal_portal_status_displayed_date.py test_ogsd1_ac01 test_ogsd1_ac02 test_ogsd1_ac03; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
