#!/usr/bin/env bash
# MS-ig-1 AC1 (the built behaviour): tests/test_mcpmsp_internal_role.py passes with nothing failed and each named test
# PASSES: an unset INTERNAL_READER_ROLE_ARN keeps today's client (nothing moves before the role exists); a set ARN makes
# query_v0._fetch_capped read through a client assumed from that ARN; the byte cap still holds on that path; and an
# AssumeRole failure with the ARN set refuses (no silent fall back to the gateway identity).
. "$(dirname "$0")/_root.sh"
if pytest_named "$G/tests/test_mcpmsp_internal_role.py" 1 \
  test_unset_arn_keeps_existing_client test_set_arn_reads_via_internal_role \
  test_byte_cap_holds_on_internal_role test_assume_failure_refuses_without_fallback; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
