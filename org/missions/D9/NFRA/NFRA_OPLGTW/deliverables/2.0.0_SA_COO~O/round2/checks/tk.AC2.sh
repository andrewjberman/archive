#!/usr/bin/env bash
# OPLGTW OG-t-1 AC2 (R-3 (b) and (d), ruling Q1): the principal-keyed tier, its floor, its negative arms, and the
# machine/bearer paths never reaching resolve_tier as a person -- 8 named tests.
. "$(dirname "$0")/_root.sh"
export AUDIT_PATH="$(mktemp)"
pytest_named tests/test_tier_principal.py test_admin_principal_resolves_master_admin test_same_email_other_oid_is_not_admin \
  test_changed_display_email_stays_admin test_no_principal_resolves_read_only test_write_capable_principal_resolves_standard \
  test_broker_mints_no_admin_scope_for_same_email_other_oid test_unverified_provider_floors_every_principal \
  test_machine_paths_never_reach_resolve_tier; ok=$?
rm -f "$AUDIT_PATH"; restore_audit
[ $ok = 0 ] && { echo "RESULT: PASS"; exit 0; }; echo "RESULT: FAIL"; exit 1
