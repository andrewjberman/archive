#!/usr/bin/env bash
# OPLGTW OG-tp-1 AC3 (round 47): the worker's new test file tests/test_og_tp1.py passes and the existing tests that import tools.py's search, poll and gate paths still pass
# (test_principal_cutover and test_browser_oidc each carry one red already at the live ref and are not in the set).
. "$(dirname "$0")/_gwtests.sh"
gwtests tests/test_og_tp1.py tests/test_opal_users_gate.py tests/test_identity_scope.py tests/test_login_admit_r24.py tests/test_scoped_consent_r253.py tests/test_transcript_tools.py
rc=$?; restore_audit
exit $rc
