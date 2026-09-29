#!/usr/bin/env bash
# OA-e-6 AC1 (the measurement): the loopback-reach file holds exactly four arms -- {operator, Opal_Agent} x {8194, 8790},
# each once -- every result in {OPEN, REFUSED, TIMEOUT}; the Opal_Agent arms' recorded whoami ends in \opal_agent and
# the operator arms' does not; and the verdict is the one the two Opal_Agent arms imply (REACHABLE iff both OPEN,
# NOT-REACHABLE iff neither, PARTIAL otherwise).
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~14/E6_LOOPBACK_REACH.json"
[ -f "$F" ] || { echo "measurement file absent: $F"; echo "RESULT: FAIL"; exit 1; }
timeout 30 python - "$F" <<'EOF'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8")); arms = d["arms"]; verdict = d.get("verdict", "")
    cells = {}
    for a in arms:
        who = str(a["account_whoami"]).strip().lower()
        cls = "agent" if who.endswith("\\opal_agent") else "operator"
        cells.setdefault((cls, int(a["port"])), []).append(str(a["result"]))
except Exception as e:
    print(f"file unparseable: {type(e).__name__}: {e}"); print("RESULT: FAIL"); sys.exit(1)
need = [(c, p) for c in ("operator", "agent") for p in (8194, 8790)]
once = sum(1 for k in need if len(cells.get(k, [])) == 1)
valid = sum(1 for v in cells.values() for r in v if r in ("OPEN", "REFUSED", "TIMEOUT"))
ag = [cells.get(("agent", p), ["?"])[0] for p in (8194, 8790)]
want = "REACHABLE" if ag == ["OPEN", "OPEN"] else ("NOT-REACHABLE" if "OPEN" not in ag else "PARTIAL")
print(f"arms={len(arms)}; cells filled once {once} of 4; valid results {valid}; agent arms 8194={ag[0]} 8790={ag[1]}; "
      f"verdict={verdict} implied={want}")
good = len(arms) == 4 and once == 4 and valid == 4 and verdict == want
print("RESULT: PASS" if good else "RESULT: FAIL"); sys.exit(0 if good else 1)
EOF
