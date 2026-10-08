#!/usr/bin/env bash
# OPLGTW OG-rf-1 AC1 (R50, PRD v2.0 item 6, acceptance A25): the budget bounds the START of the consuming transaction,
# never its answer. Four named tests in tests/test_oauth_send_budget.py, offline (the durable store faked, the budget
# shortened in the test only):
#   (01) refresh: the transaction is SENT inside the budget and its result arrives AFTER the budget -> HTTP 200 with
#        the new access/refresh pair; the family is still `active`; presenting the NEW refresh token next succeeds.
#   (02) refresh: the budget elapses BEFORE the transaction is sent -> 503 `temporarily_unavailable`; the transaction
#        is never sent (the fake records zero sends, even after the abandoned worker finishes); the stored generation
#        and token hash are unchanged; presenting the SAME refresh token again then succeeds.
#   (03) code redemption: the same as (01) for authorization_code -> 200, the code consumed once, the family active.
#   (04) code redemption: the same as (02) -> 503, the code NOT consumed; redeeming it again then succeeds.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r32_rf1_audit_$$.jsonl"
pytest_named tests/test_oauth_send_budget.py test_ogrf1_ac01 test_ogrf1_ac02 test_ogrf1_ac03 test_ogrf1_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
