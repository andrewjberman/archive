#!/usr/bin/env bash
# OPLGTW OG-mp-1 AC2: the worker's new tests (tests/test_og_mp1.py, at least 3) pass, and so do the five admin neighbours
# (tests/test_admin_people.py, tests/test_admin_people_access.py, tests/test_admin_refusals.py, tests/test_admin_tenants.py, tests/test_owner_gate.py; 31 passed at the base).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_mp1.py tests/test_admin_people.py tests/test_admin_people_access.py tests/test_admin_refusals.py tests/test_admin_tenants.py tests/test_owner_gate.py
rc=$?
restore_audit
exit $rc
