#!/usr/bin/env bash
# OPLGTW OG-up-2 AC1 (CTO R36): the re-send dedupe keys on CONTENT. Four named tests in
# tests/test_opal_portal_dedupe_content.py: (01) two sends of the same two names and sizes whose content hash DIFFERS
# both trigger (2 POSTs of /trigger); (02) the same names, sizes AND hashes within 30 minutes trigger once and the second
# returns already_triggered true; (03) when either file has an unreadable hash (no file.hashes and no cTag) the send is
# NOT deduped: it triggers; (04) the hash comes from the drive item the tool already resolves: no extra request.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r26_up2_audit_$$.jsonl"
pytest_named tests/test_opal_portal_dedupe_content.py test_ogup2_ac01 test_ogup2_ac02 test_ogup2_ac03 test_ogup2_ac04; r=$?
restore_audit; rm -f "$AUDIT_PATH"
[ "$r" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
