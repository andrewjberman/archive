#!/usr/bin/env bash
# OPLGTW OG-ap-12 AC2 (the live grade after the grant, row Z-S97; same bar as OG-ap-11 AC2): around the SCHEDULED 12:15Z schwab sweep after the deploy,
# W/AP12_GRADE.json shows:
# - the planted synthetic NON-schwab record survived the schwab sweep and is absent from its report;
# - the planted synthetic schwab record was drained and reported by it;
# - the sweep run named is the scheduled one (an EventBridge-invoked run, not an ad-hoc invoke).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/AP12_GRADE.json"
[ -f "$F" ] || { echo "AP12_GRADE.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
k = ["foreign_survived_schwab_sweep", "foreign_absent_from_schwab_report", "schwab_drained_and_reported", "sweep_was_scheduled"]
vals = {x: d.get(x) for x in k}
print("sweep run %s; %s" % (d.get("sweep_run_id", "NONE"), "; ".join("%s=%s" % (x, vals[x]) for x in k)))
raise SystemExit(0 if all(v is True for v in vals.values()) and d.get("sweep_run_id") else 1)
EOF
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
