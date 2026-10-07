#!/usr/bin/env bash
# OPLGTW OG-al-2 AC1 (Andrew-direct 2026-10-07 ~04:1xZ, "rec approved"): four named tests in
# tests/test_identity_scope_status_row.py, against the TRACKED identity_tool_allowlist.txt:
# (01) the scoped concierge identity is admitted for opal_data_refresh_status, on any client;
# (02) a scoped identity is still DENIED a tool that neither the seed nor the overlay names;
# (03) the concierge's consent_scopes are the same set with and without the new row (the tool maps to no Graph scope);
# (04) the overlay's opal_data_refresh_upload row is still client-qualified and still refuses another client.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r26_al2_audit_$$.jsonl"
pytest_named tests/test_identity_scope_status_row.py test_ogal2_ac01 test_ogal2_ac02 test_ogal2_ac03 test_ogal2_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
