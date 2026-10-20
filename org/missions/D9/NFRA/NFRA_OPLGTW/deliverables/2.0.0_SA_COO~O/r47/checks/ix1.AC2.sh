#!/usr/bin/env bash
# OPLGTW OG-ix-1 AC2 (round 47): the worker's new test file tests/test_og_ix1.py passes and the existing breakdown, people-view and route tests still pass.
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_ix1.py tests/test_admin_gateway_breakdown.py tests/test_admin_people.py tests/test_og_cd2.py tests/test_og_cd1.py
rc=$?; restore_audit
exit $rc
