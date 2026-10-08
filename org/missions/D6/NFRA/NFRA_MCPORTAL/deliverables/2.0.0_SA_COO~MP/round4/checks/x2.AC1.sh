#!/usr/bin/env bash
# MP-x-2 AC1 (FWD-14 ACCEPT i-ii on the page): the five named tests exist in mcportal/src/pages/control-plane and
# `bun test src/pages/control-plane` exits 0 with >=5 pass and 0 fail. (bun 1.3.x prints a name only on FAILURE, so names
# are read from the sources and the runner's counts decide the rest -- the MP-t-5 method.)
#   "control plane lists every roster box"
#   "a not reporting box reads not reporting"
#   "every figure shows its age"
#   "an unreadable store shows the reason and no numbers"
#   "the view refreshes while open"   (AMENDMENT 1, CTO~O ruling msg 32041 on C12)
. "$(dirname "$0")/_root.sh"
P=mcportal/src/pages/control-plane
[ -d "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "control plane lists every roster box" "a not reporting box reads not reporting" "every figure shows its age" "an unreadable store shows the reason and no numbers" "the view refreshes while open"; do
  grep -rqF -- "$t" "$P" && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src/pages/control-plane 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 5; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 5 ] && [ "${pass:-0}" -ge 5 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
