#!/usr/bin/env bash
# OPLGTW OG-u-2 AC1 (W3-S5, PRD v1.1 C1 R-5 clause): a client record carries an explicit logical idle expiry; an exchange
# extends it; an idle client is refused invalid_client while its record is still present (logical, not TTL); a
# pre-existing record without expires_at counts from its created_at (never rewritten or deleted by this cell); a live
# refresh family keeps its client. 5 named tests.
. "$(dirname "$0")/_root.sh"
export AUDIT_PATH="$(mktemp)"
pytest_named tests/test_dcr_idle_lifetime.py test_new_client_carries_idle_expiry test_token_exchange_extends_client_expiry \
  test_idle_client_refused_invalid_client test_legacy_client_expiry_counts_from_created_at test_live_refresh_family_keeps_client; ok=$?
rm -f "$AUDIT_PATH"; restore_audit
[ $ok = 0 ] && { echo "RESULT: PASS"; exit 0; }; echo "RESULT: FAIL"; exit 1
