#!/usr/bin/env bash
# OPLGTW OG-rt-1 AC3 (round 47): the worker's new test file tests/test_og_rt1.py passes and the existing entitlement, account-reference, Schwab query, grant-admin and contract tests still pass
# (test_og_ms1 is in the set; test_ogz1_ac08 carries one red at the live ref).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_rt1.py tests/test_data_entitlement_guard.py tests/test_entitlement_admin.py tests/test_account_ref.py tests/test_schwab_query.py tests/test_grant_calendar_months.py tests/test_og_ms1.py tests/test_admin_people.py
rc=$?; restore_audit
exit $rc
