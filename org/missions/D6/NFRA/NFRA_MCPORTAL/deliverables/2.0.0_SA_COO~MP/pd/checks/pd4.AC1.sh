#!/usr/bin/env bash
# MP-pd-4 AC1 (F2, the page; decomposition PD.3): the eight named tests exist in mcportal/src (bun 1.3.x prints a name only on
# FAILURE, so names are read from the sources -- the MP-p-2 method), and `bun test src` exits 0 with >=8 pass and 0 fail.
#   "person row with a principal shows channel and tool switches"
#   "a row without a principal shows no control and says why"
#   "record kind not live reads per-person control is not live yet"
#   "stop and restore post the change with the expected revision"
#   "a refused write shows the reason and changes nothing on the page"
#   "history lists only set_person_access entries for the person"
#   "access client posts change and expect_revision"
#   "routes json equals the app routes"                          (existing test; it must still pass)
. "$(dirname "$0")/_root.sh"
P=mcportal/src/pages/people
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "person row with a principal shows channel and tool switches" "a row without a principal shows no control and says why" "record kind not live reads per-person control is not live yet" "stop and restore post the change with the expected revision" "a refused write shows the reason and changes nothing on the page" "history lists only set_person_access entries for the person" "access client posts change and expect_revision" "routes json equals the app routes"; do
  grep -rqF -- "$t" mcportal/src && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 8; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 8 ] && [ "${pass:-0}" -ge 8 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
