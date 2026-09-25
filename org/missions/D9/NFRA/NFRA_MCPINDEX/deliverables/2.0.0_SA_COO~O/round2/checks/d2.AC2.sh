#!/usr/bin/env bash
# MX-d-2 AC2 (C2 on the composed path, dormant by default): the two named tests pass, nothing failed.
#   test_discover_registers_dormant         with ENABLED_INTEGRATIONS empty the family adds zero tools; with its id set it adds
#                                           exactly its pinned list, and validate_integration_spec returns []
#   test_discover_tools_carry_class         every discover tool resolves by name through destructive_ops.classify and
#                                           data_entitlement to a declared class (MX-c-4's composed path)
. "$(dirname "$0")/_root.sh"
if pytest_named tests/test_opal_discover.py test_discover_registers_dormant test_discover_tools_carry_class; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
