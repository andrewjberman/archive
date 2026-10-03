#!/usr/bin/env bash
# OPLGTW OG-sr-1 AC1 (the CVO's post-hoc half on OG-rl-3, finding "the shared-value refusal is ONE-SIDED"): the two
# named tests pass on this tree -- the mail route and the transcript route each REFUSE a presented bearer whose value is
# also another route's credential (the teams_route OTHER_ROUTE_BEARERS pattern), and the existing suites stay green.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r14_sr_audit_$$.jsonl"
pytest_named tests/test_mail_route.py test_ogsr1_mail_refuses_shared_value; r1=$?
pytest_named tests/test_transcript_route.py test_ogsr1_transcript_refuses_shared_value; r2=$?
restore_audit; rm -f "$AUDIT_PATH"
echo "mail rc=$r1; transcript rc=$r2"
[ "$r1" = 0 ] && [ "$r2" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
