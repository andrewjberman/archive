#!/usr/bin/env bash
# OPLGTW OG-nw-2 AC1 (round-37 G6-INTERNAL, PRD v3.9): the news DynamoDB reads go through the internal reader role.
#   ac01 with INTERNAL_READER_ROLE_ARN set, _ddb() is a DynamoDB client built from the ASSUMED credentials (no default-credential client is created);
#   ac02 with it unset, _ddb() is today's lazily created default client (behaviour unchanged);
#   ac03 with it set and AssumeRole failing, a tool answers an unavailable refusal with ZERO DynamoDB calls and no fallback to the default identity;
#   ac04 the S3 side of internal_role (s3_client) is unchanged: its two existing suites pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
pytest_named tests/test_og_nw2.py test_ognw2_ac01 test_ognw2_ac02 test_ognw2_ac03 test_ognw2_ac04; r0=$?
out=$(cd "$GW" && timeout 100 python -m pytest tests/test_mcpmsp_internal_role.py tests/test_internal_role_routing.py tests/test_og_nw1.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); r1=$?
echo "existing internal-role and news suites: rc=$r1; $(printf '%s\n' "$out" | tail -1 | cut -c1-80)"
restore_audit
[ "$r0" = 0 ] && [ "$r1" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
