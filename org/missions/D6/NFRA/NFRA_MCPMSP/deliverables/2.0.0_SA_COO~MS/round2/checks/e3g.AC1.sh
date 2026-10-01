#!/usr/bin/env bash
# MS-rq-1 AC1 (the built behaviour): tests/test_admin_refusals.py passes with nothing failed and each named test
# PASSES: a non-owner is refused before any read or invoke; GET lists asker_sender_refusal entries newest first with the
# C4 fields (and no text); POST approve for a tid with no tenant row invokes register_tenant THEN widen; POST approve for a
# registered tid invokes widen only; the gateway itself writes nothing to the store; and (AMENDMENT 1) the listing's
# sender_email/sender_domain come from the entry's args, never from its user (the caller).
. "$(dirname "$0")/_root.sh"
if pytest_named "$G/tests/test_admin_refusals.py" 1 \
  test_non_owner_refused test_lists_refusals_newest_first_c4_fields \
  test_approve_unregistered_tenant_registers_then_widens test_approve_registered_tenant_only_widens \
  test_gateway_writes_nothing test_sender_fields_read_from_entry_args; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
