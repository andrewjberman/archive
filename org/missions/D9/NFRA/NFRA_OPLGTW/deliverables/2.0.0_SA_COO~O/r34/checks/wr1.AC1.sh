#!/usr/bin/env bash
# OPLGTW OG-wr-1 AC1 (round-34 E5, row W43-S7; CTO ruling (d), ROUND_ANALYSIS.round32.md ADDENDUM 1): W/WR1_READ.json, read on
# the gateway host through the INSTALLED code by one SSM command, shows both masters primed. For every master/dataset pair
# measured, primed_dates equals window_dates (>= 250), and warm_seconds is a number.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~56/WR1_READ.json"
[ -f "$F" ] || { echo "WR1_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body", {}); pairs = b.get("pairs", [])
masters = sorted({p.get("master") for p in pairs})
bad = [p for p in pairs if not (isinstance(p.get("window_dates"), int) and p["window_dates"] >= 250
       and p.get("primed_dates") == p["window_dates"] and isinstance(p.get("warm_seconds"), (int, float)))]
print("ssm %s; masters %d %s; pairs %d; pairs not primed or unmeasured %d"
      % (d.get("ssm_command_id", "NONE")[:8], len(masters), masters, len(pairs), len(bad)))
raise SystemExit(0 if d.get("ssm_command_id") and len(masters) >= 2 and pairs and not bad else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
