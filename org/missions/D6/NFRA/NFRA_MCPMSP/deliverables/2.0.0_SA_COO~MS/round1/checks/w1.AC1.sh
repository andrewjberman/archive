#!/usr/bin/env bash
# MS-w-1 AC1 (the built behaviour): the writer's tests/test_register_tenant.py passes with nothing failed and each named
# test PASSES: an owner-verified register_tenant for a live firm writes one tenant_firm record at POLICY#TENANT#<tid>;
# a firm absent from LIVE_FIRMS is refused before any store call; a tid already registered to another firm is refused;
# and one record item is written per outcome.
. "$(dirname "$0")/_root.sh"
if pytest_named "$MPW_DIR/tests/test_register_tenant.py" 1 \
  test_register_tenant_writes_tenant_firm test_register_tenant_refused_firm_not_live \
  test_register_tenant_refused_other_firm_row test_register_tenant_records_each_outcome; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
