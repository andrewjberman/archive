#!/usr/bin/env bash
# MP-z-2 AC1 (FWD-20 on the page, S16; decomposition GW.3, GW.4): the five named tests exist in mcportal/src (bun 1.3.x
# prints a name only on FAILURE, so names are read from the sources -- the MP-p-2 method), and `bun test src` exits 0
# with >=5 pass and 0 fail.
#   "gateway page lists every channel with its tools and indexes"
#   "a channel with no holder reads no one"
#   "an unrated channel reads unrated"
#   "an unreadable grant store is shown and never reads as no grants"
#   "routes json equals the app routes"
#   AMENDMENT 1 (Andrew-direct readability): "boxes table shows a seat count with the full list behind a disclosure",
#   "short columns do not wrap mid-token"
. "$(dirname "$0")/_root.sh"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "gateway page lists every channel with its tools and indexes" "a channel with no holder reads no one" "an unrated channel reads unrated" "an unreadable grant store is shown and never reads as no grants" "routes json equals the app routes" "boxes table shows a seat count with the full list behind a disclosure" "short columns do not wrap mid-token"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 7; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 7 ] && [ "${pass:-0}" -ge 7 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
