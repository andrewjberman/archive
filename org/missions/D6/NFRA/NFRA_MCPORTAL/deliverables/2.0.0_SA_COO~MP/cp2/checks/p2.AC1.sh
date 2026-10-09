#!/usr/bin/env bash
# MP-p-2 AC1 (FWD-15..17 on the page; decomposition CP2.4): the five named tests exist in mcportal/src/pages/control-plane or
# mcportal/src/pages/open-calls, and `bun test src` exits 0 with >=5 pass and 0 fail. (bun 1.3.x prints a name only on
# FAILURE, so names are read from the sources and the runner's counts decide the rest -- the MP-t-5 / MP-x-2 method.)
#   "overlap panel lists the deploy-open Terraform surface first"
#   "git state panel reads not recorded for an unrecorded box"
#   "open calls page reads absent for a box with no list"
#   "open calls shows box project seat and age"
#   "close posts the ruling and shows the request pending"
. "$(dirname "$0")/_root.sh"
P1=mcportal/src/pages/control-plane; P2=mcportal/src/pages/open-calls
[ -d "$P2" ] || { echo "$P2 absent"; echo "RESULT: FAIL"; exit 1; }
n=0; for t in "overlap panel lists the deploy-open Terraform surface first" "git state panel reads not recorded for an unrecorded box" "open calls page reads absent for a box with no list" "open calls shows box project seat and age" "close posts the ruling and shows the request pending"; do
  grep -rqF -- "$t" "$P1" "$P2" && n=$((n+1)); done
out=$(cd mcportal && NO_COLOR=1 timeout 110 bun test src 2>&1 | tr -d '\r' | sed -E 's/\x1b\[[0-9;]*m//g'); rc=$?
pass=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ pass' | tail -1 | tr -dc '0-9')
fails=$(printf '%s\n' "$out" | grep -oE '^ *[0-9]+ fail' | tail -1 | tr -dc '0-9')
printf '%s\n' "$out" | tail -4
echo "bun test rc=$rc; named tests present in sources $n of 5; pass=${pass:-?}; fail=${fails:-?}"
if [ "$rc" = 0 ] && [ "$n" = 5 ] && [ "${pass:-0}" -ge 5 ] && [ "${fails:-1}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
