#!/usr/bin/env bash
# MP-z-7 AC1 (CTO round analysis z-round1 @11c572fef9, item 2): the Gateway page states ONCE that Schwab master 08335338 is the one Black Diamond reports.
# The named test exists in mcportal/src (bun 1.3.x prints a name only on FAILURE, so names are read from the sources), and `bun test src` exits 0 with >=PASS_MIN pass and 0 fail:
#   "the page states once that Schwab master 08335338 is the one Black Diamond reports"
. "$(dirname "$0")/../../pc/checks/_root.sh"
PASS_MIN="${MP_GWZ_PASS_MIN:-74}"
P=mcportal/src/pages/gateway
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
t="the page states once that Schwab master 08335338 is the one Black Diamond reports"
n=0; grep -rqF -- "$t" mcportal/src && n=1
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named test present in sources $n of 1; pass=${pass:-?} (min $PASS_MIN); fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 1 ] && [ "${pass:-0}" -ge "$PASS_MIN" ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
