#!/usr/bin/env bash
# MP-t-5 AC1 (built): the page tests pass -- three named tests, no failure:
#   "entitlements shows the person's data grant"
#   "narrow posts the scope change to the narrow route"
#   "recent changes lists newest first with before and after"
. "$(dirname "$0")/_root.sh"
[ -d mcportal/src/pages/mcp-server/entitlements ] || { echo "entitlements page dir absent"; echo "RESULT: FAIL"; exit 1; }
out=$(cd mcportal && timeout 110 bun test src/pages 2>&1 | tr -d '\r'); rc=$?
n=0; for t in "entitlements shows the person's data grant" "narrow posts the scope change to the narrow route" "recent changes lists newest first with before and after"; do
  printf '%s\n' "$out" | grep -F "$t" | grep -qv -i 'fail' && n=$((n+1)); done
fails=$(printf '%s\n' "$out" | grep -oE '[0-9]+ fail' | head -1 | awk '{print $1}')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests passing $n of 3; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 3 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
