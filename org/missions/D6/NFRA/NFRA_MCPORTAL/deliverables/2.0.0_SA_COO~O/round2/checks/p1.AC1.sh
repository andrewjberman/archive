#!/usr/bin/env bash
# MP-p-1 AC1 (E5 + E6's client): the two named tests exist in the mcportal sources, and `bun test src` exits 0 with at
# least 6 passing (round 1's 4 plus these 2) and 0 failing. (bun 1.3.x prints a test's name only on FAILURE, so names are
# read from the sources and the runner's own counts decide the rest.)
#   "a non-JSON 200 is refused with a plain reason"
#   "recent changes asks for every principal"
. "$(dirname "$0")/_root.sh"
[ -f mcportal/src/api/admin.ts ] || { echo "mcportal/src/api/admin.ts absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "a non-JSON 200 is refused with a plain reason" "recent changes asks for every principal"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 2; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 2 ] && [ "${pass:-0}" -ge 6 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
