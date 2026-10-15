#!/usr/bin/env bash
# OPLGTW OG-ng-1 AC1 (round-37 NAMING-S3PREFIX, CTO msgs 34368 and 34376): the naming gate grades an IAM s3:prefix condition value CONFORMANT only when it equals a legacy_addresses row key part COMMITTED AT HEAD for the committing project, with at most one trailing "*".
#   ac01 a registered prefix with a trailing * grades CONFORMANT; ac02 the same without the * grades CONFORMANT;
#   ac03 near misses REFUSE (a doubled **, a prefix missing its trailing slash, a longer or shorter prefix, an unregistered prefix);
#   ac04 a row whose reader is ANOTHER project REFUSES; ac05 a registry row present only in the working tree or index (not HEAD) REFUSES;
#   ac06 the same registered string as a resource ARN or any other attribute is graded exactly as before (the clause fires for an s3:prefix condition value only);
#   ac07 every commit that touches a .tf with an s3:prefix value prints a counted line (admitted, refused, registry_head), like the CATALOG-EXEMPT line.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
T=.tools/tests/test_naming_gate_s3prefix.py
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 115 python -m pytest "$T" -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
p=0; for t in test_ng1_ac01 test_ng1_ac02 test_ng1_ac03 test_ng1_ac04 test_ng1_ac05 test_ng1_ac06 test_ng1_ac07; do printf '%s\n' "$out" | grep -E "::$t(\[.*\])? PASSED" >/dev/null && p=$((p+1)); done
failed=$(printf '%s\n' "$out" | grep -cE ' FAILED| ERROR')
echo "pytest rc=$rc; named tests passed $p of 7; failed/error lines $failed"
[ "$rc" = 0 ] && [ "$p" = 7 ] && [ "$failed" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
