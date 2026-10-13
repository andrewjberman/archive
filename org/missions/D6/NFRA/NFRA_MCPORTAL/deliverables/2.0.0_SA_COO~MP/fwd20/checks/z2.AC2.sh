#!/usr/bin/env bash
# MP-z-2 AC2 (the build is real; GW.4): `bun run build` in mcportal exits 0, and dist/routes.json exists, parses, has
# version 1, and lists "/", "/control-plane", "/open-calls" and "/gateway".
. "$(dirname "$0")/_root.sh"
[ -d mcportal/src ] || { echo "mcportal/src absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun run build 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -3
r=$(python -c "
import json,sys
try:
    d=json.load(open('mcportal/dist/routes.json',encoding='utf-8'))
except Exception as e:
    print('UNREAD:'+type(e).__name__); sys.exit()
need={'/','/control-plane','/open-calls','/gateway'}
print('version=%s paths=%d missing=%d' % (d.get('version'), len(d.get('paths',[])), len(need-set(d.get('paths',[])))))
" | tr -d '\r')
echo "build rc=$rc; dist/routes.json: $r"
if [ "$rc" = 0 ] && printf '%s' "$r" | grep -qE '^version=1 paths=[0-9]+ missing=0$'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
