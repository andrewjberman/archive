#!/usr/bin/env bash
# OPLGTW OG-ed-1 AC2: the worker's new tests (tests/test_og_ed1.py, at least 4) pass, and so do the neighbours that touch the email deny and the consent flow
# (tests/test_email_deny.py, tests/test_og_en14.py, tests/test_scoped_consent_r253.py, tests/test_data_entitlement_guard.py, tests/test_login_admit_r24.py).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_ed1.py tests/test_email_deny.py tests/test_og_en14.py tests/test_scoped_consent_r253.py tests/test_data_entitlement_guard.py tests/test_login_admit_r24.py
rc=$?
restore_audit
exit $rc
