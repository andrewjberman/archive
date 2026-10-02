#!/usr/bin/env bash
# OPLGTW OG-rl-3 AC3 (CTO ruling AC3): with the bearer from Secrets Manager gateway/teams/bearer (read in memory, sent
# on stdin to curl, never printed or put on argv), GET /hx/teams/me and GET /hx/teams/chats return 200.
# A 502 whose body carries graph_status 403 is a MISSING GRAPH SCOPE on MS_INGEST_IDENTITY: it prints
# GRAPH-SCOPE-MISSING and is a BLOCKING row to Andrew, not a code fix. Only status codes and top-level JSON key names
# are printed; no chat content.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
n=0
B=$(aws secretsmanager get-secret-value --region us-east-1 --secret-id gateway/teams/bearer --query SecretString --output text | tr -d '\r\n')
[ -n "$B" ] || { echo "bearer read EMPTY"; echo "RESULT: FAIL"; exit 1; }
for p in me chats; do
  out=$(printf 'Authorization: Bearer %s\n' "$B" | curl -s -H @- -o - -w '\n%{http_code}' "https://mcp.opalinvest.dev/hx/teams/$p" | tr -d '\r')
  code=$(printf '%s\n' "$out" | tail -1)
  shape=$(printf '%s\n' "$out" | sed '$d' | python -c "
import json,sys
try:
    d=json.loads(sys.stdin.read())
    ks=sorted(d.keys()) if isinstance(d,dict) else type(d).__name__
    gs=d.get('graph_status') if isinstance(d,dict) else None
    print('keys %s graph_status %s' % (ks, gs))
except Exception as e:
    print('not-json')
")
  echo "GET /hx/teams/$p -> $code ($shape)"
  if [ "$code" = 502 ] && printf '%s' "$shape" | grep -q "graph_status 403"; then echo "GRAPH-SCOPE-MISSING on /hx/teams/$p (BLOCKING row to Andrew)"; fi
  [ "$code" = 200 ] && n=$((n+1))
done
unset B
echo "BEARER ARMS $n of 2"
[ "$n" = 2 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
