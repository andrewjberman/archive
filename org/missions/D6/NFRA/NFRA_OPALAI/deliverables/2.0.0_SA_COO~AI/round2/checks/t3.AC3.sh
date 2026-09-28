#!/usr/bin/env bash
# ROUND-2 RE-CUT COPY of round 1 t3.AC3.sh (2.0.0_SA_COO~AI). ONE amendment: the fence and the checkout it guards are a detached opal_ai worktree at $OA_NESTED_PIN
# (_pin.sh), never the nested HEAD, where round 2's E2 adds a G4 line by design.
# OA-t-3 AC3 (the fence binds in the runtime, both directions, one harness): with OPAL_RUNTIME_CONFIG naming a state
# dir, a write INSIDE the state dir passes, a write to the agent's own prompt is denied, a call to Andrew's proxy
# gateway is denied and a whoami on opal-gateway-bbg passes; with OPAL_RUNTIME_CONFIG unset, the same state-dir write is
# DENIED (fail closed). No session serial is involved: the runtime fence keys on nothing but its config.
. "$(dirname "$0")/_root.sh"
. "$(dirname "$0")/_pin.sh"
H="$PT/opal/agent/hooks/concierge-gate.sh"
[ -f "$H" ] || { echo "$H absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/oa_t3_ac3_$$"; mkdir -p "$T/state"
SW=$(cygpath -m "$T/state"); CK=$(cygpath -m "$PT")
python - "$T/cfg.json" "$CK" "$SW" <<'EOF'
import json, sys
json.dump({"checkout_dir": sys.argv[2], "state_dir": sys.argv[3], "workspace_probe_file": "C:/nonexistent/probe", "prod_ref": "PROD"},
          open(sys.argv[1], "w", encoding="utf-8"))
EOF
CFG=$(cygpath -w "$T/cfg.json")
j() { printf '{"session_id":"oa-t3-ac3","tool_name":"%s","tool_input":%s}' "$1" "$2"; }
verdict() { # verdict <with-config:yes|no> <json>
  if [ "$1" = yes ]; then o=$(printf '%s' "$2" | env -u OPAL_AGENT_SERIAL OPAL_RUNTIME_CONFIG="$CFG" bash "$H" 2>&1); rc=$?
  else o=$(printf '%s' "$2" | env -u OPAL_AGENT_SERIAL -u OPAL_RUNTIME_CONFIG bash "$H" 2>&1); rc=$?; fi
  if printf '%s' "$o" | grep -q '"permissionDecision":"deny"'; then echo DENY; elif [ "$rc" = 0 ]; then echo PASS; else echo "ERROR$rc"; fi
}
n=0; ok=0
chk() { n=$((n+1)); got=$(verdict "$2" "$3"); if [ "$got" = "$1" ]; then ok=$((ok+1)); echo "ok   [$1] $4"; else echo "FAIL [$4] expected $1 got $got"; fi; }
chk PASS yes "$(j Write "{\"file_path\":\"$SW/threads/t/2026-09-24.md\"}")" "state-dir write, config set"
chk DENY yes "$(j Edit "{\"file_path\":\"$CK/opal/agent/prompt.md\"}")" "edit own prompt, config set"
chk DENY yes "$(j mcp__opal-gateway__send_chat_message '{"chat_id":"x","message":"y"}')" "Andrew proxy gateway, config set"
chk PASS yes "$(j mcp__opal-gateway-bbg__whoami '{}')" "whoami on opal-gateway-bbg, config set"
chk DENY no  "$(j Write "{\"file_path\":\"$SW/threads/t/2026-09-24.md\"}")" "state-dir write, config UNSET (fail closed)"
rm -rf "$T"
echo "fence arms as expected: $ok of $n"
if [ "$ok" = "$n" ] && [ "$n" = 5 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
