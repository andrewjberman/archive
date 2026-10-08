#!/usr/bin/env bash
# MP-x-2 AC3 (the deploy's own build step, deploy-to-ec2.sh: `bun run build` = tsc -b && vite build): exits 0 and writes
# mcportal/dist/index.html.
. "$(dirname "$0")/_root.sh"
rm -rf mcportal/dist
out=$(cd mcportal && NO_COLOR=1 timeout 200 bun run build 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
printf '%s\n' "$out" | tail -4
idx=no; [ -f mcportal/dist/index.html ] && idx=yes
echo "build rc=$rc; dist/index.html=$idx"
if [ "$rc" = 0 ] && [ "$idx" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
