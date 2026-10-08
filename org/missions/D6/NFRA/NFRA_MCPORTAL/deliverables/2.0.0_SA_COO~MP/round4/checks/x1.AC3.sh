#!/usr/bin/env bash
# MP-x-1 AC3 (C3: the handler lives on the production admin router): app.admin_api.routes holds exactly one GET route
# whose path is /fabric/boxes.
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && MOCK_GRAPH=1 timeout 60 python -c "
import app.admin_api as a
hits=[r for r in a.routes if getattr(r,'path','')=='/fabric/boxes' and 'GET' in (getattr(r,'methods',None) or set())]
print('fabric/boxes GET routes=%d' % len(hits))
" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -3
if [ "$rc" = 0 ] && printf '%s\n' "$out" | grep -qx 'fabric/boxes GET routes=1'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
