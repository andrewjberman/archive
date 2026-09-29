#!/usr/bin/env bash
# OA-e-2 AC1 (built, rows Z-S18/Z-S19): the runtime fence at opal_ai ${OA_NESTED_REF:-HEAD} DENIES
# mcp__opal-gateway-bbg__opal_data_refresh_upload, and still PASSES an ordinary serve call
# (mcp__opal-gateway-bbg__read_chat_messages, the positive control -- a fence that denies everything fails here) and
# still DENIES an existing G4 call (mcp__opal-gateway-bbg__send_email, the unchanged-arm control). Then the fence's OWN
# test, test_concierge_gate.sh at the same ref, names the upload tool and reports 0 failed.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/e2ac1_$$")"; mkdir -p "$T/state"
git -C opal_ai archive "$REF" opal/agent/hooks 2>/dev/null | tar -x -C "$T" 2>/dev/null
G="$T/opal/agent/hooks/concierge-gate.sh"
if [ ! -f "$G" ]; then echo "concierge-gate.sh absent at opal_ai $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; fi
python -c "import json,sys;json.dump({'checkout_dir':'X','state_dir':sys.argv[2],'workspace_probe_file':'X','prod_ref':'X'},open(sys.argv[1],'w'))" "$T/cfg.json" "$T/state"
arm() { # arm <tool> -> DENY | PASS | ERROR
    local out rc
    out=$(printf '{"session_id":"e2","tool_name":"%s","tool_input":{}}' "$1" | OPAL_RUNTIME_CONFIG="$T/cfg.json" timeout 20 bash "$G" 2>&1); rc=$?
    [ $rc -ne 0 ] && { echo "ERROR"; return; }
    printf '%s' "$out" | grep -q '"permissionDecision":"deny"' && echo DENY || echo PASS
}
up=$(arm mcp__opal-gateway-bbg__opal_data_refresh_upload)
rd=$(arm mcp__opal-gateway-bbg__read_chat_messages)
em=$(arm mcp__opal-gateway-bbg__send_email)
TT="$T/opal/agent/hooks/test_concierge_gate.sh"
names=$(grep -c 'opal_data_refresh_upload' "$TT" 2>/dev/null); names=${names:-0}
# AMENDED (row NFRA_OPALAI-Z-W11-S2): the fence test takes ~89 s on this device; 60 s cut it off. 105 s stays inside
# the worker harness's 120 s bound (the three arms above take a few seconds).
summ=$(timeout 105 bash "$TT" 2>&1 | tr -d '\r' | grep -m1 '^RESULT:')
failed=$(printf '%s' "$summ" | sed -n 's/.* \([0-9][0-9]*\) failed.*/\1/p')
rm -rf "$T"
echo "opal_ai $REF: upload=$up read_chat_messages=$rd send_email=$em; fence test names upload=$names; fence test '${summ:-no summary}'"
if [ "$up" = DENY ] && [ "$rd" = PASS ] && [ "$em" = DENY ] && [ "$names" -ge 1 ] && [ "${failed:-x}" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
