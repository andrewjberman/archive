#!/usr/bin/env bash
# OPLGTW TRNSPT-DEPS OG-ml-1 AC2: list_email_filtered and inspect_email_attachment are read class (BOTH lists), no
# Graph scope added, read_email's $select carries the four C7 fields, pypdf is pinned, the LD-0613 hunk was dropped
# (LD-0613.md unchanged since the cut base), and the hard tool count (test_ogz2_ac08) matches the registry.
. "$(dirname "$0")/_root.sh"
H="$(pwd)/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks"
reg=$(cd "$GW" && timeout 60 python "$(native "$H/_reg.py")" list_email_filtered inspect_email_attachment 2>&1 | tr -d '\r')
printf '%s\n' "$reg"
sel=0; for fld in ccRecipients internetMessageId conversationId sentDateTime; do
  grep -E '\$select' "$GW/app/tools.py" | grep -q "$fld" && sel=$((sel+1)); done
pin=$(grep -ciE '^pypdf[=<>~]=' "$GW/requirements.txt")
base=$(git merge-base HEAD CLOUD 2>/dev/null)
ld=$( [ -n "$base" ] && git diff --name-only "$base" HEAD -- org/tier0/ledger/LD-0613.md | grep -c . )
AUDIT_PATH="$(mktemp)"; export AUDIT_PATH
pytest_named tests/test_entitlement_admin.py test_ogz2_ac08; c=$?; restore_audit; rm -f "$AUDIT_PATH"
echo "read_email \$select fields present $sel of 4; pypdf pins $pin; LD-0613 changed since base ${base:0:10}: ${ld:-UNREAD}"
if printf '%s\n' "$reg" | grep -q "^REG 2 of 2; SCOPES same$" && [ "$sel" = 4 ] && [ "$pin" = 1 ] && [ "$ld" = 0 ] && [ "$c" = 0 ]; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
