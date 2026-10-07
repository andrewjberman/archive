#!/usr/bin/env bash
# OPLGTW OG-al-2 AC3 (AMENDMENT 1, row Z-S65): two named tests in tests/test_opal_portal_status_id_shape.py -- (05) an
# execution id that is not a plain token (a slash, dot-dot, a query or fragment mark, a percent escape, a space, a
# newline) is refused before ANY HTTP request; (06) a UUID-shaped id and every shape the portal mints reach the status
# GET. And tests/test_opal_portal_send_split.py still passes whole (the send path shares the check).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r26_al2c_audit_$$.jsonl"
pytest_named tests/test_opal_portal_status_id_shape.py test_ogal2_ac05 test_ogal2_ac06; r=$?
ss=no; (cd "$GW" && timeout 300 python -m pytest tests/test_opal_portal_send_split.py -q -p no:cacheprovider --color=no >/dev/null 2>&1) && ss=yes
restore_audit; rm -f "$AUDIT_PATH"
echo "send-split tests still green: $ss"
[ "$r" = 0 ] && [ "$ss" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
