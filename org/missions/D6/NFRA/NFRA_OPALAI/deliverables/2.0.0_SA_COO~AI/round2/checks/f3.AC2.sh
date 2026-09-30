#!/usr/bin/env bash
# OA-f-3 AC2 (bound): the fixed script at opal_ai ${OA_NESTED_REF:-HEAD} still PARSES (PowerShell's own parser, 0 errors)
# and its -Plan dry run still prints exactly the eight PLAN acts of the G-ACCT handoff and exits 0. -Plan changes nothing
# (it needs no elevation). The config is a scratch copy of the keys, so nothing under C:\opal_runtime is touched.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
F="opal/runtime/provision/provision-account.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f3ac2_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$F" > "$T/p.ps1" 2>/dev/null
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
python -c "import json,sys;json.dump({'checkout_dir':sys.argv[2]+'\\\\co','state_dir':sys.argv[2]+'\\\\st','workspace_probe_file':sys.argv[2]+'\\\\probe.txt','prod_ref':'PROD'},open(sys.argv[1],'w'))" "$T/cfg.json" "$WT"
perr=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\p.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
plan=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\p.ps1" -Config "$WT\\cfg.json" -Plan 2>&1 | tr -d '\r'); prc=$?
n=$(printf '%s\n' "$plan" | grep -c '^PLAN: ')
rm -rf "$T"
echo "opal_ai $REF: parse errors=${perr:-none}; -Plan rc=$prc PLAN lines=$n"
if [ "$perr" = 0 ] && [ "$prc" = 0 ] && [ "$n" = 8 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
