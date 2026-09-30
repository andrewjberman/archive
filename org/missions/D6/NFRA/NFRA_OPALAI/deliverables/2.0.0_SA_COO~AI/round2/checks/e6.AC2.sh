#!/usr/bin/env bash
# OA-e-6 AC2 (the control that makes AC1 mean anything): both OPERATOR arms read OPEN -- so a closed Opal_Agent arm is
# the account's reach, not a dead listener -- the local account Opal_Agent exists NOW (Get-LocalUser, a live read), and a
# view server the cell started for the probe is recorded as stopped.
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~14/E6_LOOPBACK_REACH.json"
[ -f "$F" ] || { echo "measurement file absent: $F"; echo "RESULT: FAIL"; exit 1; }
ctl=$(timeout 30 python - "$F" <<'EOF'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    op = {int(a["port"]): a["result"] for a in d["arms"] if not str(a["account_whoami"]).strip().lower().endswith("\\opal_agent")}
    vs = d.get("view_server") or {}
    stopped = (not vs.get("started_by_cell")) or bool(vs.get("stopped"))
    print(f"operator 8194={op.get(8194,'?')} 8790={op.get(8790,'?')} view_server_stopped={'yes' if stopped else 'no'}")
except Exception as e:
    print(f"file unparseable: {type(e).__name__}")
EOF
)
acct=$(timeout 40 powershell -NoProfile -Command "if (Get-LocalUser -Name Opal_Agent -ErrorAction SilentlyContinue) { 'present' } else { 'absent' }" 2>&1 | tr -d '\r' | tail -1)
echo "$ctl; Opal_Agent account=$acct"
if printf '%s' "$ctl" | grep -q 'operator 8194=OPEN 8790=OPEN view_server_stopped=yes' && [ "$acct" = present ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
