#!/usr/bin/env bash
# MP-pf-8 AC1 (an index list holding an unbroken real-length name scrolls inside its own box; CTO msg 34947, row Z-S64): the named test exists in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources),
# `bun test src` exits 0 with >=72 pass (71 after MP-pf-5, plus this one) and 0 fail:
#   "an index list holding an unbroken real-length name scrolls inside its own box"   gateway.css holds `overflow-x: auto` for the `.gateway-indexes` rule, and the checked-in fixture (gateway.cgroup.fixture.ts) holds an index name of 60 or more characters with no space in it
. "$(dirname "$0")/../../pc/checks/_root.sh"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
t="an index list holding an unbroken real-length name scrolls inside its own box"
n=0; grep -rqF -- "$t" mcportal/src && n=1
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named test present in sources $n of 1; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 1 ] && [ "${pass:-0}" -ge 72 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
