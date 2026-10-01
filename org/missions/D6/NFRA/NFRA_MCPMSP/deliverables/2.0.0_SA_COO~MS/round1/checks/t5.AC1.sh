#!/usr/bin/env bash
# MS-t-5 AC1 (the built behaviour): the gateway's tests/test_admin_tenants.py passes with nothing failed and each named
# test PASSES: a non-owner POST /api/admin/tenants/{tid} is refused before any invoke; an owner POST invokes the writer
# with action=register_tenant, the tid, the firm and the forwarded owner header, and relays its verdict; and the
# gateway itself writes nothing to the store.
. "$(dirname "$0")/_root.sh"
if pytest_named "$G/tests/test_admin_tenants.py" 1 \
  test_non_owner_refused test_owner_forwards_register_tenant test_gateway_writes_nothing; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
