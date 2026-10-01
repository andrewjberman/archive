#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-hr-2 AC1 (C7 headless, the mail route, PRD @c9fd271499): sender-table only, with NO thread reach;
# $value bytes ONLY for a non-inline application/pdf under the cap, with sha256; everything else metadata only;
# allow-by-key output = O4's $select plus the body; own bearer on its own prefix; GET only; audit without content.
# 10 named tests, Graph and the token broker stubbed.
. "$(dirname "$0")/_root.sh"
AUDIT_PATH="$(mktemp)"; export AUDIT_PATH
pytest_named tests/test_mail_route.py \
  test_off_table_sender_refused \
  test_off_table_sender_in_table_thread_refused \
  test_empty_sender_table_fails_closed \
  test_pdf_value_bytes_with_sha256_under_cap \
  test_pdf_over_cap_metadata_only \
  test_non_pdf_and_inline_metadata_only \
  test_output_allow_by_key_select_plus_body \
  test_transcript_and_ms_bearers_refused_on_mail_prefix \
  test_graph_get_only_fails_closed \
  test_audit_records_ids_bytes_label_never_content
ok=$?; restore_audit; rm -f "$AUDIT_PATH"
if [ "$ok" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
