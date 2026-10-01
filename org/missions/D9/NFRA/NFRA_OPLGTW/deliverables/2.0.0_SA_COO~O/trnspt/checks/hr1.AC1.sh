#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-hr-1 AC1 (C7 headless, the transcripts route): own bearer, constant-time, own prefix only; the
# /ms/* bearer and the mail bearer refused here; off-allowlist and empty-allowlist refused (fail closed); GET-only
# Graph path allowlist, fail closed; allow-by-key output; audit without content; NeedsLogin returned, never alerted.
# 9 named tests, Graph and the token broker stubbed.
. "$(dirname "$0")/_root.sh"
AUDIT_PATH="$(mktemp)"; export AUDIT_PATH
pytest_named tests/test_transcript_route.py \
  test_bearer_constant_time_own_prefix_only \
  test_ms_bearer_refused_on_transcript_prefix \
  test_transcript_bearer_refused_on_ms_prefix \
  test_off_allowlist_meeting_refused \
  test_empty_allowlist_fails_closed \
  test_graph_path_allowlist_get_only_fails_closed \
  test_output_allow_by_key \
  test_audit_records_ids_bytes_label_never_text \
  test_needs_login_returned_not_alerted
ok=$?; restore_audit; rm -f "$AUDIT_PATH"
if [ "$ok" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
