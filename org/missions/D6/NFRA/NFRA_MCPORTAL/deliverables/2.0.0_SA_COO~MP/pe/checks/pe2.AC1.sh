#!/usr/bin/env bash
# MP-pe-2 AC1 (the Gateway view groups and reads plainly; decomposition PE.2): the seven named tests exist in mcportal/src (bun 1.3.x prints a name only on FAILURE,
# so names are read from the sources -- the MP-p-2 method), and `bun test src` exits 0 with >=57 pass and 0 fail (base: 51 pass; the six new tests add six).
#   "summary table lists every group with its kind and tool count"
#   "a summary row links to its group section"
#   "a bucket group reads AWS bucket"
#   "a group with no declared source reads as a gap"
#   "the grouping basis line is shown"
#   "the tool total counts a tool once when two groups list it"
#   "routes json equals the app routes"                         (existing test; it must still pass)
. "$(dirname "$0")/../../pd/checks/_root.sh"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "summary table lists every group with its kind and tool count" "a summary row links to its group section" "a bucket group reads AWS bucket" "a group with no declared source reads as a gap" "the grouping basis line is shown" "the tool total counts a tool once when two groups list it" "routes json equals the app routes"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 7; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 7 ] && [ "${pass:-0}" -ge 57 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
