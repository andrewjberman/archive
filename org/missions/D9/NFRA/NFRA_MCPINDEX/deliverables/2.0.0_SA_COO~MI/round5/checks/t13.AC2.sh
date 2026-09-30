#!/usr/bin/env bash
# MX-t-13 AC2: tests/test_blackdiamond.py exits 0 and its 4 named tests pass.
. "$(dirname "$0")/_root.sh"
pytest_named tests/test_blackdiamond.py test_mx_t13_tool_registered_safe test_mx_t13_catalog_gated test_mx_t13_scope_fenced test_mx_t13_answer_carries_as_of
rc=$?
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
