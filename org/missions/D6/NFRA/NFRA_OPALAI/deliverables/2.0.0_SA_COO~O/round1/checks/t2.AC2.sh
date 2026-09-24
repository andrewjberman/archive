#!/usr/bin/env bash
# OA-t-2 AC2 (refusal, difference control against AC1's -Plan arm): the SAME script without -Plan, in this NON-elevated
# session, exits 3 with "ELEVATION REQUIRED" and changes nothing -- no Opal_Agent, no checkout_dir, no state_dir.
. "$(dirname "$0")/_root.sh"
P="opal_ai/opal/runtime/provision"
[ -f "$P/provision-account.ps1" ] || { echo "$P/provision-account.ps1 absent"; echo "RESULT: FAIL"; exit 1; }
W=$(cygpath -w "$P/provision-account.ps1"); C=$(cygpath -w "$P/runtime.config.example.json")
elev=$(powershell -NoProfile -Command "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)" | tr -d '\r')
cdir=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['checkout_dir'])" "$P/runtime.config.example.json" 2>/dev/null)
sdir=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['state_dir'])" "$P/runtime.config.example.json" 2>/dev/null)
b1=no; [ -n "$cdir" ] && [ -e "$(cygpath -u "$cdir")" ] && b1=yes
b2=no; [ -n "$sdir" ] && [ -e "$(cygpath -u "$sdir")" ] && b2=yes
out=$(timeout 100 powershell -NoProfile -ExecutionPolicy Bypass -File "$W" -Config "$C" 2>&1 | tr -d '\r'); rc=$?
a1=no; [ -n "$cdir" ] && [ -e "$(cygpath -u "$cdir")" ] && a1=yes
a2=no; [ -n "$sdir" ] && [ -e "$(cygpath -u "$sdir")" ] && a2=yes
absent=$(powershell -NoProfile -Command "if (Get-LocalUser -Name Opal_Agent -ErrorAction SilentlyContinue) {'present'} else {'absent'}" | tr -d '\r')
msg=$(printf '%s\n' "$out" | grep -c 'ELEVATION REQUIRED')
echo "session elevated=$elev; rc=$rc; ELEVATION REQUIRED lines=$msg; Opal_Agent=$absent; checkout_dir before/after=$b1/$a1; state_dir before/after=$b2/$a2"
if [ "$elev" = False ] && [ "$rc" = 3 ] && [ "$msg" -ge 1 ] && [ "$absent" = absent ] && [ "$b1$a1" = nono ] && [ "$b2$a2" = nono ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
