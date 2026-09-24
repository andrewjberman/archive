#!/usr/bin/env bash
# OA-t-2 AC1 (built): provision-account.ps1 -Plan prints the eight planned acts as PLAN: lines, exits 0, and creates
# nothing (Opal_Agent still absent afterwards).
. "$(dirname "$0")/_root.sh"
P="opal_ai/opal/runtime/provision"
[ -f "$P/provision-account.ps1" ] || { echo "$P/provision-account.ps1 absent"; echo "RESULT: FAIL"; exit 1; }
W=$(cygpath -w "$P/provision-account.ps1"); C=$(cygpath -w "$P/runtime.config.example.json")
out=$(timeout 100 powershell -NoProfile -ExecutionPolicy Bypass -File "$W" -Plan -Config "$C" 2>&1 | tr -d '\r'); rc=$?
want="CREATE-USER Opal_Agent|ASSERT-NOT-MEMBER Administrators|ASSERT-NOT-MEMBER CodexSandboxUsers|MKDIR checkout_dir|MKDIR state_dir|ACL checkout_dir Opal_Agent:RX|ACL state_dir Opal_Agent:M|SECRET DPAPI operator"
hit=0; IFS='|'; for w in $want; do printf '%s\n' "$out" | grep -E '^PLAN:' | grep -qF "$w" && hit=$((hit+1)); done; unset IFS
absent=$(powershell -NoProfile -Command "if (Get-LocalUser -Name Opal_Agent -ErrorAction SilentlyContinue) {'present'} else {'absent'}" | tr -d '\r')
echo "rc=$rc; PLAN acts matched $hit of 8; Opal_Agent after plan: $absent"
if [ "$rc" = 0 ] && [ "$hit" = 8 ] && [ "$absent" = absent ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
