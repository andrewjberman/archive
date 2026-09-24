#!/usr/bin/env bash
# MP-w-1 AC2 (built): the nested mcportal repo builds -- `bun run build` exits 0 and emits dist/index.html with at least
# one JS asset.
. "$(dirname "$0")/_root.sh"
[ -f mcportal/package.json ] || { echo "mcportal/package.json absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd mcportal && timeout 110 bun run build 2>&1 | tr -d '\r'); rc=$?
idx=no; [ -f mcportal/dist/index.html ] && idx=yes
js=$(ls mcportal/dist/assets/*.js 2>/dev/null | wc -l | tr -d ' ')
printf '%s\n' "$out" | tail -3
echo "build rc=$rc; dist/index.html=$idx; js assets=$js"
if [ "$rc" = 0 ] && [ "$idx" = yes ] && [ "$js" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
