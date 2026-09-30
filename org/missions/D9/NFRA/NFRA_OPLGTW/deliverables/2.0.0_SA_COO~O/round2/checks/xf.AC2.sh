#!/usr/bin/env bash
# OPLGTW OG-x-4 AC2 (CTO ruling msg 26488 (2)): on the HOST, the maximal query's peak child RSS is under 80% of the
# 268,435,456-byte job cap, i.e. <= 214,748,364 bytes. Reads CAPACITY_X4.json (see xf.AC1.sh); XF_CAPACITY is TEST-ONLY.
. "$(dirname "$0")/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~11"
F="${XF_CAPACITY:-$D/CAPACITY_X4.json}"
[ -f "$F" ] || { echo "measurement $F absent; maximal query graded 0 of 1"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, sys
CAP = 268435456
LIMIT = int(CAP * 0.80)
d = json.load(open(sys.argv[1], encoding="utf-8"))
jobs = [j for j in d.get("ac2", {}).get("jobs", []) if str(j.get("job")) == "maximal"]
if len(jobs) != 1:
    print("maximal job rows found: %d (need exactly 1)" % len(jobs)); print("RESULT: FAIL"); sys.exit(1)
pk = int(jobs[0]["peak_child_rss_bytes"])
print("maximal query peak=%d limit(80%% of %d)=%d ok=%s code=%s" % (pk, CAP, LIMIT, jobs[0].get("ok"), jobs[0].get("code")))
good = pk <= LIMIT
print("RESULT: PASS" if good else "RESULT: FAIL")
sys.exit(0 if good else 1)
EOF
