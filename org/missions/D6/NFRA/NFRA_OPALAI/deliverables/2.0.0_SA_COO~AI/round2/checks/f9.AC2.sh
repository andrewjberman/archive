#!/usr/bin/env bash
# OA-f-9 AC2 (built): jq for the runtime fence is provisioned and found without a workspace file (row Z-S50 defect 5).
#   arm1 fence at ${OA_F9_REF:-HEAD}, PATH without jq, HOME holding .local/bin/jq.exe -> a Read call is NOT denied
#   arm2 (difference control) the same, HOME holding no jq                           -> denied, reason 'jq not found'
#   arm3 provision-account.ps1 -Plan, config WITH jq_exe    -> exactly one 'PLAN: JQ' line naming that jq_exe
#   arm4 provision-account.ps1 -Plan, config WITHOUT jq_exe -> no 'PLAN: JQ' line, the 10 base PLAN lines unchanged
. "$(dirname "$0")/_root.sh"
REF="${OA_F9_REF:-HEAD}"
G="opal/agent/hooks/concierge-gate.sh"; P="opal/runtime/provision/provision-account.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
JQSRC="$(pwd)/.tools/jq.exe"; [ -f "$JQSRC" ] || { echo "vendored jq absent at $JQSRC"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f9ac2_$$")"; mkdir -p "$T/h1/.local/bin" "$T/h2"
git -C opal_ai show "$REF:$G" > "$T/g.sh" 2>/dev/null || { echo "fence absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
git -C opal_ai show "$REF:$P" > "$T/p.ps1" 2>/dev/null || { echo "provision-account.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
cp "$JQSRC" "$T/h1/.local/bin/jq.exe"
IN='{"tool_name":"Read","tool_input":{"file_path":"README.md"}}'
o1=$(printf '%s' "$IN" | env -u OPAL_RUNTIME_CONFIG PATH=/usr/bin:/bin HOME="$T/h1" bash "$T/g.sh" 2>&1)
o2=$(printf '%s' "$IN" | env -u OPAL_RUNTIME_CONFIG PATH=/usr/bin:/bin HOME="$T/h2" bash "$T/g.sh" 2>&1)
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
python - "$T" "$WT" <<'PY'
import json, sys, os
t, wt = sys.argv[1], sys.argv[2]
base = {"checkout_dir": wt + "\\co", "state_dir": wt + "\\st", "workspace_probe_file": wt + "\\probe", "prod_ref": "PROD"}
json.dump(dict(base, jq_exe=wt + "\\src\\jq.exe"), open(os.path.join(t, "cj.json"), "w"))
json.dump(base, open(os.path.join(t, "cn.json"), "w"))
PY
p3=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\p.ps1" -Config "$WT\\cj.json" -Plan 2>&1 | tr -d '\r')
p4=$(timeout 60 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\p.ps1" -Config "$WT\\cn.json" -Plan 2>&1 | tr -d '\r')
rm -rf "$T"
d1=$(printf '%s' "$o1" | grep -c '"deny"'); d2=$(printf '%s' "$o2" | grep -c 'jq not found')
j3=$(printf '%s\n' "$p3" | grep -c '^PLAN: JQ '); n3=$(printf '%s\n' "$p3" | grep '^PLAN: JQ ' | grep -c -F 'src\jq.exe')
j4=$(printf '%s\n' "$p4" | grep -c '^PLAN: JQ'); n4=$(printf '%s\n' "$p4" | grep -c '^PLAN: ')
echo "opal_ai $REF: arm1 HOME jq -> deny lines=$d1; arm2 no jq -> 'jq not found' lines=$d2; arm3 PLAN: JQ lines=$j3 naming jq_exe=$n3; arm4 PLAN: JQ lines=$j4, PLAN lines=$n4"
if [ "$d1" = 0 ] && [ "$d2" -ge 1 ] && [ "$j3" = 1 ] && [ "$n3" = 1 ] && [ "$j4" = 0 ] && [ "$n4" = 10 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
