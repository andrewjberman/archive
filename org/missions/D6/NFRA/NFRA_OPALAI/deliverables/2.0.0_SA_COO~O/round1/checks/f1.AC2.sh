#!/usr/bin/env bash
# OA-f-1 AC2 (the tracked overlay row is client-qualified, and the client is real): at HEAD,
# infra/aws/ec2/opal-gateway/identity_tool_allowlist.txt has NO unqualified 'opalbloomberg@opalinvest.com
# opal_data_refresh_upload' row and exactly one qualified with client=<id>; that <id> is a client_id carried by at least
# one live refresh family for opalbloomberg@opalinvest.com in gateway-access-state-table (read-only scan).
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
rows=$(git show HEAD:infra/aws/ec2/opal-gateway/identity_tool_allowlist.txt 2>/dev/null | tr -d '\r' | sed 's/#.*//' | grep -iE '^[[:space:]]*opalbloomberg@opalinvest\.com[[:space:]]+opal_data_refresh_upload')
unq=$(printf '%s\n' "$rows" | grep . | grep -vc 'client=')
q=$(printf '%s\n' "$rows" | grep -c 'client=')
cid=$(printf '%s\n' "$rows" | grep -o 'client=[^[:space:]]*' | head -1 | cut -d= -f2)
T="${TMPDIR:-/tmp}/oa_f1_ac2_$$"; mkdir -p "$T"
timeout 90 "$AWS" dynamodb scan --table-name gateway-access-state-table --output json > "$T/s.json" 2>/dev/null
live=$(python - "$T/s.json" "$cid" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
try:
    items = json.load(open(sys.argv[1], encoding='utf-8'))['Items']
except Exception as e:
    print('SCAN-FAILED'); raise SystemExit(0)
v = lambda it, k: list(it.get(k, {}).values())[0] if it.get(k) else ''
ids = {v(i, 'client_id') for i in items if str(v(i, 'email')).lower() == 'opalbloomberg@opalinvest.com' and v(i, 'sk') == 'oauth_refresh_family'}
print('families_clients=%d match=%s' % (len(ids), 'yes' if sys.argv[2] and sys.argv[2] in ids else 'no'))
EOF
)
rm -rf "$T"
echo "unqualified upload rows=$unq; client-qualified=$q (client=${cid:-NONE}); live: $live"
if [ "$unq" = 0 ] && [ "$q" = 1 ] && printf '%s' "$live" | grep -q 'match=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
