#!/usr/bin/env bash
# OPLGTW OG-gd-2 AC1 (round-46 OG-gd-2): W/GD2_GRADE_READ.json covers FWD-10..FWD-19 and FWD-22, one entry each, every PROOF arm of the
# PRD's text recorded, every arm carrying a claim in {measured, inferred, absent}, and every arm NOT run naming the owed
# act (who + what). It carries NO grade word: the CTO grades at the round-46 analysis.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~162/GD2_GRADE_READ.json"
[ -f "$REC" ] || { echo "GD2_GRADE_READ.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
want = ["FWD-%d" % i for i in list(range(10, 20)) + [22]]
out = d.get("outcomes", [])
got = [o.get("fwd") for o in out]
cov = sum(1 for w in want if got.count(w) == 1)
arms = [a for o in out for a in o.get("arms", [])]
CL = {"measured", "inferred", "absent"}
noclaim = sum(1 for a in arms if a.get("claim") not in CL)
unrun_noact = sum(1 for a in arms if not a.get("ran") and not ((a.get("owed_act") or {}).get("who") and (a.get("owed_act") or {}).get("what")))
noarm = sum(1 for o in out if not o.get("arms"))
graded = sum(1 for o in out if str(o.get("grade", "")).upper() in {"REALIZED", "NOT_REALIZED", "HELD", "PASS", "FAIL"})
print("fwd covered %d of 11; extra entries %d; outcomes with no arm %d" % (cov, len(got) - cov, noarm))
print("arms %d; claim-less %d; un-run without an owed act %d; grade words %d (want 0)" % (len(arms), noclaim, unrun_noact, graded))
print("VERDICT " + ("PASS" if cov == 11 and len(got) == 11 and noarm == 0 and arms and noclaim == 0 and unrun_noact == 0 and graded == 0 else "FAIL"))
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | grep -v '^VERDICT'
printf '%s\n' "$res" | grep -q '^VERDICT PASS' && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
