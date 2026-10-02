#!/usr/bin/env bash
# OPLGTW OG-o-4 AC2 (row W5-S6): tests/test_schwab_query.py::test_ogo4_ac02 passes -- a 500-row page of narrow rows
# returns 500 rows (rows counted once across representations, OG-x-2's measure()).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r13_o4_audit_$$.jsonl"
pytest_named tests/test_schwab_query.py test_ogo4_ac02; rc=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
