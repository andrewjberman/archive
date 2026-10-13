#!/usr/bin/env bash
# OPLGTW OG-rd-1 AC1 (round-36 E3, row Z-S95): W/RD1_502.json reads the gateway's own record of every 502 on
# /hx/teams/channels/.../messages over the stated window. count_502 equals the items listed, and each item carries a
# cause_class from the closed set. The verdict is gateway, upstream or mixed. A positive control (a 200 on the same route in
# the window) was found, so the instrument sees the route.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~62/RD1_502.json"
[ -f "$F" ] || { echo "RD1_502.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
C = {"gateway_timeout", "gateway_error", "graph_throttled", "graph_5xx", "graph_4xx", "unreadable"}
items = d.get("items", [])
n = d.get("count_502")
good = sum(1 for i in items if i.get("cause_class") in C)
pc = d.get("positive_control_200", 0)
print("window %s; count_502 %s; items %d; items with a closed-set cause %d; verdict %s; positive control 200s %s"
      % (d.get("window"), n, len(items), good, d.get("verdict"), pc))
ok = (isinstance(n, int) and n == len(items) and good == len(items)
      and d.get("verdict") in ("gateway", "upstream", "mixed") and isinstance(pc, int) and pc >= 1)
raise SystemExit(0 if ok else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
