#!/usr/bin/env bash
# MP-pc-3 AC1 (FWD-21 read on the page + G1 panel half; decomposition PC.2, PC.3): the seven named tests exist in
# mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources -- the MP-p-2 method), the
# People page folder exists, public/routes.json lists /people, and `bun test src` exits 0 with >=7 pass and 0 fail.
#   "people page lists every person with channels and tools"
#   "a person holding nothing reads holds nothing"
#   "depth freshness and cadence show their claims and absent is said"
#   "routes json equals the app routes"                        (existing test; it must still pass with /people added)
#   "git state reads no with the pass time for a clean integrate"
#   "git state reads refused with time and note"
#   "git state reads not recorded without a pointer"
. "$(dirname "$0")/_root.sh"
P=mcportal/src/pages/people
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
rj=$(python -c "import json;print('yes' if '/people' in json.load(open('mcportal/public/routes.json'))['paths'] else 'no')" 2>&1 | tr -d '\r')
n=0; for t in "people page lists every person with channels and tools" "a person holding nothing reads holds nothing" "depth freshness and cadence show their claims and absent is said" "routes json equals the app routes" "git state reads no with the pass time for a clean integrate" "git state reads refused with time and note" "git state reads not recorded without a pointer"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 7; routes.json lists /people: $rj; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 7 ] && [ "$rj" = yes ] && [ "${pass:-0}" -ge 7 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
