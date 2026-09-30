#!/usr/bin/env bash
# MX-q-3 AC2: tests/test_query_v0_tool.py exits 0 and its 4 named tests pass.
. "$(dirname "$0")/_root.sh"
pytest_named tests/test_query_v0_tool.py test_mx_q3_tool_registered_safe test_mx_q3_uncatalogued_key_refused test_mx_q3_entitled test_mx_q3_same_answer_as_route
rc=$?
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
