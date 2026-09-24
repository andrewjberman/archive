#!/usr/bin/env bash
# OA-t-4 AC2 (seam, REAL neighbour = the live gateway's OAuth server): the watch's own discovery mode reads the live
# metadata and reports refresh_token support and the registration endpoint -- and what it reports equals a direct read of
# the same document (the control: the watch is not printing a constant).
. "$(dirname "$0")/_root.sh"
W="opal_ai/opal/agent/teams_watch/teams-watch.py"
[ -f "$W" ] || { echo "$W absent"; echo "RESULT: FAIL"; exit 1; }
BASE="https://mcp.opalinvest.dev"
direct=$(timeout 30 curl -s -m 25 "$BASE/.well-known/oauth-authorization-server" | python -c "
import json,sys
d=json.load(sys.stdin); print('refresh_token=%s registration=%s' % ('yes' if 'refresh_token' in d.get('grant_types_supported',[]) else 'no', d.get('registration_endpoint','NONE')))" 2>/dev/null || echo "DIRECT-READ-FAIL")
watch=$(timeout 60 python "$W" --discover-auth "$BASE" 2>&1 | tr -d '\r' | grep -m1 '^AUTH: ' | sed 's/^AUTH: //')
echo "direct: $direct"; echo "watch:  ${watch:-(no AUTH line)}"
if [ "$direct" != "DIRECT-READ-FAIL" ] && [ "$watch" = "$direct" ] && printf '%s' "$watch" | grep -q 'refresh_token=yes'; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
