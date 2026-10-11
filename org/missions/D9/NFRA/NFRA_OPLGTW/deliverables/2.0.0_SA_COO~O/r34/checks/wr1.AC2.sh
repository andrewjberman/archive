#!/usr/bin/env bash
# OPLGTW OG-wr-1 AC2 (round-34 E5, CTO ruling (d) step 2): the warm 13-month read is under the 60 s ALB default on every
# master/dataset pair in W/WR1_READ.json. A FAIL here is the ruling's own trigger for step 3 (the bounded fan-out); it is a
# measured finding, filed as a BLOCKING row, and never retried into a pass.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~56/WR1_READ.json"
[ -f "$F" ] || { echo "WR1_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
pairs = json.load(open(sys.argv[1], encoding="utf-8")).get("body", {}).get("pairs", [])
w = [p.get("warm_seconds") for p in pairs if isinstance(p.get("warm_seconds"), (int, float))]
print("warm 13-month read seconds over %d pair(s): max %s (want < 60)" % (len(w), max(w) if w else "NONE"))
raise SystemExit(0 if w and len(w) == len(pairs) and max(w) < 60 else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
