#!/usr/bin/env bash
# OPLGTW OG-gr-2 AC1 (analysis round 14 s.4 item 4; READ-ONLY per Andrew-direct 2026-10-03 ~17:3xZ): GRAIN_R15.json
# explains the dim_position 2026-09-21 collision at both masters and lands on exactly one verdict:
#   GRAIN_FOUND     -- a grain unique on 52 of 52 snapshots with its added column never blank (one row per snapshot), or
#   UPSTREAM_DEFECT -- the colliding rows counted per master (both > 0), the defect named, and its owner named;
# and it records writes 0 (no data, no pipeline touched).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~22/GRAIN_R15.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); v = d.get("verdict"); w = d.get("writes")
if v == "GRAIN_FOUND":
    rows = d.get("snapshots", [])
    uniq = sum(1 for r in rows if r.get("unique") is True)
    blanks = sum(int(r.get("added_blank", 1)) for r in rows)
    print("verdict GRAIN_FOUND; snapshots %d; unique %d; added-column blanks %d; writes %s" % (len(rows), uniq, blanks, w))
    ok = len(rows) == 52 and uniq == 52 and blanks == 0 and w == 0
elif v == "UPSTREAM_DEFECT":
    c = d.get("colliding_rows_by_master", {})
    print("verdict UPSTREAM_DEFECT; colliding rows by master %s; defect named %s; owner named %s; writes %s"
          % (c, bool(d.get("defect")), bool(d.get("owner")), w))
    ok = len(c) == 2 and all(int(x) > 0 for x in c.values()) and bool(d.get("defect")) and bool(d.get("owner")) and w == 0
else:
    print("verdict %r is neither GRAIN_FOUND nor UPSTREAM_DEFECT" % (v,))
    ok = False
print("RESULT: PASS" if ok else "RESULT: FAIL")
sys.exit(0 if ok else 1)
PY
