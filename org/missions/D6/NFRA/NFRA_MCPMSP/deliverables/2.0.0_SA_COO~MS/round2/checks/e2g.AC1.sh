#!/usr/bin/env bash
# MS-sg-1 AC1 (the built behaviour): tests/test_mcpmsp_sender_gate.py passes with nothing failed and each named test
# PASSES: an allowed domain whose tenant is registered to that domain's firm is served; a domain outside Andrew's four is
# refused and logged; an allowed domain in a tenant registered to ANOTHER firm (or unregistered) is refused; a guest-form
# (#EXT#) address is refused; an opalinvest.com / 49financial.com sender is refused asker_pilot_scope ONLY when the
# calling identity is in MSP_CALLING_IDENTITIES (and served as before when it is not); the refusal entry carries
# sender_email and sender_domain and no text/message field.
. "$(dirname "$0")/_root.sh"
if pytest_named "$G/tests/test_mcpmsp_sender_gate.py" 1 \
  test_allowed_domain_matching_tenant_served test_domain_not_allowed_refused_and_logged \
  test_domain_tenant_mismatch_refused test_guest_form_refused \
  test_opal_sender_refused_only_for_msp_calling_identity test_refusal_entry_has_sender_email_domain_no_text; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
