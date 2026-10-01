#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-ml-1 AC1 (C7 interactive, mail tools; adoption of gw-mail-tools-int per the triage @6d41bd25ec):
# the three f-branch test files plus the existing attachment suite pass whole. Counted from pytest's own summary.
. "$(dirname "$0")/_root.sh"
F="tests/test_read_email_fields.py tests/test_list_email_filtered.py tests/test_inspect_email_attachment.py tests/test_attachment_tools.py"
miss=0; for f in $F; do [ -f "$GW/$f" ] || { echo "absent: $GW/$f"; miss=$((miss+1)); }; done
AUDIT_PATH="$(mktemp)"; export AUDIT_PATH
out=$(cd "$GW" && timeout 110 python -m pytest $F -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
restore_audit; rm -f "$AUDIT_PATH"
sum=$(printf '%s\n' "$out" | grep -E '^[0-9]+ (passed|failed)|passed|failed' | tail -1)
p=$(printf '%s\n' "$sum" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+'); p=${p:-0}
f=$(printf '%s\n' "$sum" | grep -oE '[0-9]+ (failed|errors?)' | awk '{s+=$1} END {print s+0}')
echo "files absent $miss of 4; pytest rc=$rc; passed $p (expected 24 or more); failed/error $f"
if [ "$miss" = 0 ] && [ "$rc" = 0 ] && [ "$p" -ge 24 ] && [ "$f" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
