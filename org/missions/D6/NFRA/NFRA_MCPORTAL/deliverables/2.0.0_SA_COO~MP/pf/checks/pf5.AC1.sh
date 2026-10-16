#!/usr/bin/env bash
# MP-pf-5 AC1 (S2, the 390 px scroll cue; CTO round-2 table): a table that scrolls inside its box shows a visible cue that more columns lie off the edge. The named test exists in mcportal/src (bun 1.3.x prints a name
# only on FAILURE, so names are read from the sources), `bun test src` exits 0 with >=71 pass (the 70 of PF round 2, plus this one) and 0 fail:
#   "a scroll box shows a cue that more columns lie off the edge"
. "$(dirname "$0")/../../pd/checks/_root.sh"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
t="a scroll box shows a cue that more columns lie off the edge"
n=0; grep -rqF -- "$t" mcportal/src && n=1
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named test present in sources $n of 1; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 1 ] && [ "${pass:-0}" -ge 71 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
