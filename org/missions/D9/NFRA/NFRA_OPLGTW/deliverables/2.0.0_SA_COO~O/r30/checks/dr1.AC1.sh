#!/usr/bin/env bash
# OPLGTW OG-dr-1 AC1 (round-29 analysis, row Z-S67): the gateway deploy DRAINS before it restarts, so a token refresh in
# flight finishes and no session family is revoked. Three named tests in tests/test_deploy_drain_before_restart.py,
# offline (a fake state store; no AWS, no host): (01) a graceful stop arriving WHILE a refresh is in flight lets the
# refresh finish: the client receives the rotated token, the family's generation advanced exactly once, the family is
# active, and the server then stops; (02) NEGATIVE CONTROL: the same harness with an abrupt stop loses the answer
# after the rotation is written, the client's retry presents the just-rotated token, and the family reads revoked
# with reason refresh_token_reuse (the mechanism of row Z-S67, reproduced); (03) the deploy's host step and the unit
# file, read as text: the service is stopped gracefully with a stop wait at least as long as the cell's stated
# drain bound, and no line kills it outright.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r30_dr1_audit_$$.jsonl"
pytest_named tests/test_deploy_drain_before_restart.py test_ogdr1_ac01 test_ogdr1_ac02 test_ogdr1_ac03; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
