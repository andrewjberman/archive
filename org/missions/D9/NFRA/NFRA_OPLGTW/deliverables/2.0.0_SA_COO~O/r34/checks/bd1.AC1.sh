#!/usr/bin/env bash
# OPLGTW OG-bd-1 AC1 (round-34 E8, CTO ruling @135719d313): the caller census of blackdiamond_list_fees in
# W/BD1_CENSUS.json, read from the gateway audit lake (records scanned > 0, window stated), finds 0 unprofiled callers.
# A nonzero count is the ruling's STOP: the deny is not built, and an Andrew admission call is owed.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~57/BD1_CENSUS.json"
[ -f "$F" ] || { echo "BD1_CENSUS.json absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
callers = d.get("callers", []); scanned = d.get("records_scanned", 0)
unprof = [c for c in callers if c.get("profiled") is not True]
print("window %s; audit records scanned %s; distinct callers of blackdiamond_list_fees %d; unprofiled %d"
      % (d.get("window"), scanned, len(callers), len(unprof)))
raise SystemExit(0 if isinstance(scanned, int) and scanned > 0 and d.get("window") and not unprof else 1)
PY
[ "$?" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
