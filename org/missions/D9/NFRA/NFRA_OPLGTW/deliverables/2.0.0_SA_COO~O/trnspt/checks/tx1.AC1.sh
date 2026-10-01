#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-tx-1 AC1 (PRD v1.2 C7 interactive, transcript tools; spec sections 4-5): the three transcript
# tools, the list_calendar change, innerError codes distinct, no unattributed fallback, audit ids only, scoped and
# restricted principals denied. 8 named tests in one new file, Graph stubbed.
. "$(dirname "$0")/_root.sh"
AUDIT_PATH="$(mktemp)"; export AUDIT_PATH
pytest_named tests/test_transcript_tools.py \
  test_find_online_meeting_filters_by_join_url \
  test_list_transcripts_follows_next_link \
  test_read_transcript_vtt_full_body_sha256 \
  test_inner_error_codes_distinct \
  test_no_unattributed_fallback \
  test_audit_carries_ids_never_text \
  test_scoped_and_restricted_principals_denied \
  test_list_calendar_selects_online_meeting_and_series
ok=$?; restore_audit; rm -f "$AUDIT_PATH"
if [ "$ok" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
