#!/usr/bin/env bash
# OA-f-6 AC1 (built, CTO ruling msg 26306): at opal_ai ${OA_F6_REF:-HEAD}, provision-account.ps1 BREAKS INHERITANCE and
# sets explicit ACEs on FOUR targets -- the runtime root (C:\opal_runtime, the checkout's parent), runtime.config.json,
# checkout_dir and state_dir -- with NO Authenticated Users grant. Read from its own -Plan output against a scratch
# config (no elevation, nothing changed): rc 0, >= 8 PLAN lines, >= 4 PLAN lines naming INHERITANCE-OFF, 0 PLAN lines
# naming Authenticated Users. The script PARSES, and against the round-2 DEV base e63eb06 the only files changed are the
# cell's four (provision-account.ps1, verify-boundary.ps1, boundary-arm-checkout.ps1, boundary-arm-config.ps1).
. "$(dirname "$0")/_root.sh"
REF="${OA_F6_REF:-HEAD}"; BASE="e63eb06"
F="opal/runtime/provision/provision-account.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f6ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$F" > "$T/p.ps1" 2>/dev/null
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
python -c "import json,sys;json.dump({'checkout_dir':sys.argv[2]+'\\\\root\\\\opal_ai','state_dir':sys.argv[2]+'\\\\root\\\\state','workspace_probe_file':sys.argv[2]+'\\\\probe.txt','prod_ref':'PROD'},open(sys.argv[1],'w'))" "$T/cfg.json" "$WT"
perr=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\p.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
plan=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\p.ps1" -Config "$WT\\cfg.json" -Plan 2>&1 | tr -d '\r'); prc=$?
n=$(printf '%s\n' "$plan" | grep -c '^PLAN: ')
inh=$(printf '%s\n' "$plan" | grep '^PLAN: ' | grep -ci 'INHERITANCE-OFF')
au=$(printf '%s\n' "$plan" | grep '^PLAN: ' | grep -ci 'Authenticated Users')
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F -e "$F" -e "opal/runtime/provision/verify-boundary.ps1" -e "opal/runtime/provision/boundary-arm-checkout.ps1" -e "opal/runtime/provision/boundary-arm-config.ps1" | grep -c .)
rm -rf "$T"
echo "opal_ai $REF: parse errors=${perr:-none}; -Plan rc=$prc PLAN lines=$n INHERITANCE-OFF=$inh AuthenticatedUsers=$au; other files changed vs $BASE=$others"
if [ "$perr" = 0 ] && [ "$prc" = 0 ] && [ "$n" -ge 8 ] && [ "$inh" -ge 4 ] && [ "$au" = 0 ] && [ "$others" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
