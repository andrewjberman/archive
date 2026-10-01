#!/usr/bin/env bash
# OA-f-9 AC3 (control; CTO ruling CTO_RULING_20261001_NFRA_OPALAI_ANALYST_REFS_READ.md, NEGATIVE write): widening the
# Analyst's READ set to agent/refs leaves its WRITE set unchanged. The fence at ${OA_F9_REF:-HEAD}, with a runtime config
# whose state_dir is C:/opal_runtime/state (payload strings only, nothing on disk is touched):
#   arm1 Write to <checkout>/opal/agent/refs/TEAMS_DUTY.md   -> DENIED by G1
#   arm2 Edit  to <checkout>/opal/agent/refs/THREAD_MEMORY.md -> DENIED by G1
#   arm3 (positive control) Write under state_dir/threads/    -> not denied
. "$(dirname "$0")/_root.sh"
REF="${OA_F9_REF:-HEAD}"; G="opal/agent/hooks/concierge-gate.sh"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
JQD="$(pwd)/.tools"; [ -f "$JQD/jq.exe" ] || { echo "vendored jq absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f9ac3_$$")"; mkdir -p "$T/bin"
cp "$JQD/jq.exe" "$T/bin/jq.exe"
git -C opal_ai show "$REF:$G" > "$T/g.sh" 2>/dev/null || { echo "fence absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
printf '{"checkout_dir":"C:/opal_runtime/opal_ai","state_dir":"C:/opal_runtime/state","workspace_probe_file":"X","prod_ref":"PROD"}\n' > "$T/c.json"
CFG="$(cygpath -w "$T/c.json" 2>/dev/null || echo "$T/c.json")"
run() { printf '%s' "$1" | env PATH="$T/bin:/usr/bin:/bin" OPAL_RUNTIME_CONFIG="$CFG" TMPDIR=/nonexistent-tmp TEMP=/nonexistent-tmp TMP=/nonexistent-tmp bash "$T/g.sh" 2>&1; }
o1=$(run '{"tool_name":"Write","tool_input":{"file_path":"C:/opal_runtime/opal_ai/opal/agent/refs/TEAMS_DUTY.md","content":"x"}}')
o2=$(run '{"tool_name":"Edit","tool_input":{"file_path":"C:\\opal_runtime\\opal_ai\\opal\\agent\\refs\\THREAD_MEMORY.md","old_string":"a","new_string":"b"}}')
o3=$(run '{"tool_name":"Write","tool_input":{"file_path":"C:/opal_runtime/state/threads/t1.md","content":"x"}}')
rm -rf "$T"
d1=$(printf '%s' "$o1" | grep -c 'concierge-gate G1'); d2=$(printf '%s' "$o2" | grep -c 'concierge-gate G1'); d3=$(printf '%s' "$o3" | grep -c '"deny"')
echo "opal_ai $REF: arm1 refs Write G1-deny=$d1; arm2 refs Edit G1-deny=$d2; arm3 state_dir Write deny=$d3"
if [ "$d1" = 1 ] && [ "$d2" = 1 ] && [ "$d3" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
