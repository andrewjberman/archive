#!/usr/bin/env bash
# OPLGTW OG-ng-1 AC1 (round-37 NAMING-S3PREFIX, CTO msgs 34368 and 34376): the naming gate grades an IAM s3:prefix condition value CONFORMANT only when it equals a legacy_addresses row key part COMMITTED AT HEAD for the committing project, with exactly one trailing "*".
#   ac01 a registered prefix + exactly one trailing "*" on the registered bucket grades CONFORMANT;
#   ac02 the same value WITHOUT the trailing "*" is not admitted BY THIS CLAUSE (no IAM-PREFIX-ADMITTED line); the gate grades it as before (MX-c-9 may admit a bare registered key part for its own reader);
#   ac03 each of these is not admitted by this clause: a mid-path "*", a bare "*", "**", a "?", a prefix one segment longer, one segment shorter, an unregistered prefix, an empty key part -- a tier-first shaped value (gold/ silver/ platinum/ ...) is REFUSED as before, a value the gate never grades (a bare "*", a non-tier-first prefix) stays ungraded and is NOT admitted either (A2);
#   ac04 a row whose reader is ANOTHER project REFUSES; ac05 a row staged in the same commit or present only in the working tree REFUSES (HEAD only);
#   ac06 the same string as a resource ARN or as a code literal is REFUSED (the clause fires for an s3:prefix condition value only);
#   ac07 a registered prefix granted on a DIFFERENT bucket (the statement's Resource ARN) REFUSES;
#   ac08 every commit that uses the clause prints IAM-PREFIX-ADMITTED n=<k> bucket=<b> prefixes=<list> registry_head=<sha>.
# (The laptop CTO's seven conditions: RULING_20261015_064xZ_NAMING_GATE_IAM_PREFIX_CLAUSE_CONDITIONS.md @bf9198273e.)
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
T=.tools/tests/test_naming_gate_s3prefix.py
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 115 python -m pytest "$T" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ng1_ac01 test_ng1_ac02 test_ng1_ac03 test_ng1_ac04 test_ng1_ac05 test_ng1_ac06 test_ng1_ac07 test_ng1_ac08; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 8; failed/error lines $failed"
[ "$rc" = 0 ] && [ "$p" = 8 ] && [ "$failed" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
