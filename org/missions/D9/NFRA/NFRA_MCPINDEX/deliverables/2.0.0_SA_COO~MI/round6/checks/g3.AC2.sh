#!/usr/bin/env bash
# MX-g-3 AC2: the routing is unit-proven both ways -- with INTERNAL_READER_ROLE_ARN set, portal_index and opal_discover take
# their S3 client from internal_role.s3_client(); unset, they keep the default client (the query_v0 pattern, query_v0.py:98-104).
. "$(dirname "$0")/_root.sh"
pytest_named tests/test_internal_role_routing.py test_portal_index_reads_through_internal_role test_opal_discover_heads_through_internal_role test_unset_arn_keeps_default_client; rc=$?
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
