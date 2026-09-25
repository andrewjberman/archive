#!/usr/bin/env bash
# MP-t-5 AC1 (built): the page tests pass -- the three named tests exist in the page test sources, and `bun test src/pages`
# exits 0 with at least 3 passing and 0 failing. (bun 1.3.x prints a test's name only on FAILURE, measured by
# 0.9.0_WK_NFRA_MCPORTAL~1 on MP-w-1, so names are read from the sources and the runner's own counts decide the rest.)
#   "entitlements shows the person's data grant"
#   "narrow posts the scope change to the narrow route"
#   "recent changes lists newest first with before and after"
. "$(dirname "$0")/_root.sh"
[ -d mcportal/src/pages/mcp-server/entitlements ] || { echo "entitlements page dir absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "entitlements shows the person's data grant" "narrow posts the scope change to the narrow route" "recent changes lists newest first with before and after"; do
  grep -rqF -- "$t" mcportal/src/pages && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src/pages 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 3; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 3 ] && [ "${pass:-0}" -ge 3 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
