#!/usr/bin/env bash
# OPLGTW OG-ap-12 AC2 (A2, row Z-S100): the live grade read from the QUEUE, since a scheduled sweep's drain report is a
# discarded return value. W/AP12_GRADE.json shows, around the SCHEDULED 12:15Z schwab sweep:
# - the sweep was the scheduled one;
# - the planted foreign (eclipse) record survived it (returned by a post-sweep non-destructive receive);
# - the queue held exactly the two planted records at plant and one after, so the schwab record was drained.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/AP12_GRADE.json"
[ -f "$F" ] || { echo "AP12_GRADE.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
ev = d.get("evidence", {}) or {}
sched = d.get("sweep_was_scheduled") is True
foreign = d.get("foreign_survived_schwab_sweep") is True
plant, after = ev.get("depth_at_plant"), ev.get("depth_after_sweep")
drained = plant == 2 and after == 1 and foreign
print("sweep run %s; sweep_was_scheduled=%s; foreign_survived_schwab_sweep=%s; depth %s -> %s; schwab_drained_by_queue=%s"
      % (d.get("sweep_run_id", "NONE"), sched, foreign, plant, after, drained))
raise SystemExit(0 if sched and foreign and drained and d.get("sweep_run_id") else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
