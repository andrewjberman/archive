#!/usr/bin/env bash
# OPLGTW OG-up-1 AC1 (CTO R33): the send split. Five named tests in tests/test_opal_portal_send_split.py:
# (01) a real send returns right after /trigger with the execution id and ONE status read, and never waits past 60 s;
# (02) the new read-only tool opal_data_refresh_status returns the status by execution id and the served manifest's
#      displayed date, and makes no POST or PUT;
# (03) a confirm=True re-send whose two files (name and size) equal those of a trigger this process made in the last
#      30 minutes returns that execution id with already_triggered true and does NOT call /trigger again;
# (04) the same re-send after 30 minutes, or with a different size, DOES trigger;
# (05) the limit is named: a fresh process (the in-process record cleared) triggers again.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r25_up1_audit_$$.jsonl"
pytest_named tests/test_opal_portal_send_split.py test_ogup1_ac01 test_ogup1_ac02 test_ogup1_ac03 test_ogup1_ac04 test_ogup1_ac05; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
