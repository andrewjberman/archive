#!/usr/bin/env bash
# MS-t-1 AC1 (the built behaviour): tests/test_mcpmsp_asker_firm.py passes with nothing failed, and each of the five named
# tests PASSES: a registered tenant resolves to ("firm", <firm>); an unregistered tenant is refused asker_tenant_denied
# with ONE refusal entry carrying no message text; a firm asker's fetch goes through the firm role (FIRM_ROLE_ARNS[firm]);
# a firm with no configured role ARN is refused; and a firm asker's fetch NEVER uses the gateway identity's own S3 client.
. "$(dirname "$0")/_root.sh"
if pytest_named "$G/tests/test_mcpmsp_asker_firm.py" 1 \
  test_registered_tenant_is_firm_principal test_unregistered_tenant_refused_and_logged \
  test_firm_fetch_assumes_firm_role test_missing_role_arn_refuses test_firm_fetch_never_uses_gateway_identity \
  test_tenant_firm_admitted_by_adapter; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
