#!/usr/bin/env bash
# OPLGTW OG-gt-13 AC1 (round-37 G1-INTERNAL): the published-analysis Lambda invoke goes through the internal reader role.
#   ac01 with INTERNAL_READER_ROLE_ARN set, _invoke() uses a Lambda client built from the ASSUMED credentials (no default-credential client is created);
#   ac02 with it unset, _invoke() uses today's lazily created default client (behaviour unchanged);
#   ac03 with it set and AssumeRole failing, the tool answers harvest_published_unavailable with ZERO invokes and no fallback to the default identity;
#   ac04 s3_client and dynamodb_client are unchanged: their existing suites pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_gt13.py test_oggt13_ac01 test_oggt13_ac02 test_oggt13_ac03 test_oggt13_ac04; r0=$?
out=$(cd "$GW" && timeout 100 python -m pytest tests/test_mcpmsp_internal_role.py tests/test_internal_role_routing.py tests/test_og_gt5.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r1=$?
echo "existing internal-role and published-analysis suites: rc=$r1; $(printf '%s\n' "$out" | tail -1 | cut -c1-80)"
restore_audit
[ "$r0" = 0 ] && [ "$r1" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
