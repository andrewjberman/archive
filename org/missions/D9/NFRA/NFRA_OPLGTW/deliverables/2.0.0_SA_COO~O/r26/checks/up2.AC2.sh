#!/usr/bin/env bash
# OPLGTW OG-up-2 AC2 (nothing else moved): these gateway test files pass WHOLE, each in its own process:
# test_opal_portal_send_split, test_opal_portal_status_id_shape, test_identity_scope_status_row, test_scoped_consent_r253,
# test_data_entitlement_guard. And identity_tool_allowlist.txt and app/graph_scope_map.py are unchanged by this cell.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
export AUDIT_PATH="${TMP:-/tmp}/og_r26_up2b_audit_$$.jsonl"
ok=0; n=0
for f in tests/test_opal_portal_send_split.py tests/test_opal_portal_status_id_shape.py tests/test_identity_scope_status_row.py tests/test_scoped_consent_r253.py tests/test_data_entitlement_guard.py; do
  n=$((n+1)); (cd "$GW" && timeout 300 python -m pytest "$f" -q -p no:cacheprovider --color=no >/dev/null 2>&1) && ok=$((ok+1))
done
restore_audit; rm -f "$AUDIT_PATH"
ch=$(git diff --name-only 4bec5a9b16 HEAD -- "$GW/identity_tool_allowlist.txt" "$GW/app/graph_scope_map.py" | grep -c .)
echo "test files green $ok of $n; allowlist and scope map changed since the cut: $ch (want 0)"
[ "$ok" = "$n" ] && [ "$ch" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
