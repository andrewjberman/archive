#!/usr/bin/env bash
# OA-f-10 AC1 (the falsifier, CTO ruling CTO_RULING_20261001_OPAL_AGENT_DAPI_8194_WALL.md R2.1): does a per-user Windows
# Firewall rule block LOOPBACK on this box? Measured by a TCP connect to 127.0.0.1:8194 from INSIDE the Codex OFFLINE
# sandbox (whose identity the live codex_sandbox_offline_block_loopback_* rules name) and from OUTSIDE (the operator,
# the live control). Validates the worker's record F10_FALSIFIER.json:
#   inside and outside each {whoami, result in OPEN|REFUSED|TIMEOUT}; inside.whoami != outside.whoami (a different
#   identity actually ran inside); outside OPEN (the control is live); mechanism equals the one the results imply:
#   inside OPEN -> LOOPBACK-EXEMPT; inside REFUSED or TIMEOUT -> FIREWALL-RULE.
. "$(dirname "$0")/_root.sh"
J="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~25/F10_FALSIFIER.json"
[ -f "$J" ] || { echo "F10_FALSIFIER.json absent at $J"; echo "RESULT: FAIL"; exit 1; }
python - "$J" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print(f"unreadable: {e}"); print("RESULT: FAIL"); sys.exit(1)
V = {"OPEN", "REFUSED", "TIMEOUT"}
i, o = d.get("inside") or {}, d.get("outside") or {}
ir, orr = i.get("result"), o.get("result")
iw, ow = str(i.get("whoami", "")).strip().lower(), str(o.get("whoami", "")).strip().lower()
implied = None if ir not in V else ("LOOPBACK-EXEMPT" if ir == "OPEN" else "FIREWALL-RULE")
mech = d.get("mechanism")
print(f"inside whoami={iw or 'none'} result={ir}; outside whoami={ow or 'none'} result={orr}; "
      f"distinct identity={'yes' if iw and ow and iw != ow else 'no'}; mechanism={mech} implied={implied}")
ok = (ir in V and orr == "OPEN" and iw and ow and iw != ow and mech == implied and bool(d.get("measured_at")))
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
