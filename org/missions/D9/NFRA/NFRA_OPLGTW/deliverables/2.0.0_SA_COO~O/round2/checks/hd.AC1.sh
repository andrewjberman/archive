#!/usr/bin/env bash
# OPLGTW OG-u-1 AC1 (W3-S11, W3-S18): /ms/site_children authenticates before it validates; the two browser OIDC paths
# are in AUTH_PATHS and take the FAIL-CLOSED auth bucket. 5 named tests.
. "$(dirname "$0")/_root.sh"
export AUDIT_PATH="$(mktemp)"
pytest_named tests/test_auth_hardening.py test_site_children_no_credential_no_params_is_401 \
  test_site_children_valid_credential_no_params_is_400 test_browser_login_path_in_auth_paths \
  test_browser_callback_path_in_auth_paths test_browser_callback_uses_auth_bucket; ok=$?
rm -f "$AUDIT_PATH"; restore_audit
[ $ok = 0 ] && { echo "RESULT: PASS"; exit 0; }; echo "RESULT: FAIL"; exit 1
