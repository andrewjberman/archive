#!/usr/bin/env bash
# MP-p-2 AC2 (the deploy's own build step, deploy-to-ec2.sh: `bun run build` = tsc -b && vite build): exits 0, writes
# mcportal/dist/index.html, and the Open Calls route is in the built bundle (the string '/open-calls' in dist/assets/*.js).
. "$(dirname "$0")/_root.sh"
[ -d mcportal/src/pages/open-calls ] || { echo "mcportal/src/pages/open-calls absent"; echo "RESULT: FAIL"; exit 1; }
rm -rf mcportal/dist
out=$(cd mcportal && NO_COLOR=1 timeout 200 bun run build 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
printf '%s\n' "$out" | tail -4
idx=no; [ -f mcportal/dist/index.html ] && idx=yes
rt=$(cat mcportal/dist/assets/*.js 2>/dev/null | grep -c '/open-calls')
echo "build rc=$rc; dist/index.html=$idx; bundle files naming /open-calls=$rt"
if [ "$rc" = 0 ] && [ "$idx" = yes ] && [ "${rt:-0}" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
