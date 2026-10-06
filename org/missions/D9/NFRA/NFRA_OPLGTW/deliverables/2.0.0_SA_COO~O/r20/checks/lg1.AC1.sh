#!/usr/bin/env bash
# OPLGTW OG-lg-1 AC1 (CTO R24, round-19 analysis s.3): /login's tier-based admit set and its own audit record, proven by
# six named tests in tests/test_login_admit_r24.py: (01) a non-restricted principal completes NeedsLogin -> /login ->
# consent and its principal-keyed cache is written; (02) a restricted principal is refused 403 and the refusal is
# audited; (03) the server-held identity (OTP_MAILBOX / MS_INGEST_IDENTITY) is admitted as before; (04) empty settings
# with an unresolvable tier admit nobody (fail closed); (05, A1/R25.1) opalbloomberg@ is ADMITTED and its allowlist
# still denies an out-of-scope tool;
# (06) every /login request writes exactly one audit record carrying outcome, principal key/email digest and reason.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r20_lg1_audit_$$.jsonl"
pytest_named tests/test_login_admit_r24.py test_oglg1_ac01 test_oglg1_ac02 test_oglg1_ac03 test_oglg1_ac04 test_oglg1_ac05 test_oglg1_ac06; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
