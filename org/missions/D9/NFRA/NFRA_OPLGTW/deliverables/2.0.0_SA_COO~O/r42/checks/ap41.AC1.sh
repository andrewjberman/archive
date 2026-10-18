#!/usr/bin/env bash
# OPLGTW OG-ap-41 AC1 (round 42, landing site Z's two live gateway release commits efcc8ae19f and d077cef043 on the sitez trunk): the merge shape and content. Grading: _ap37_check.py mode 1 (the same grading as OG-ap-37; the record names the commit to land in `dell_sha`).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP41_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap41_landing.json}"
[ -f "$REC" ] || { echo "ap41_landing.json absent"; echo "RESULT: FAIL"; exit 1; }
python "$(dirname "$0")/../../r38/checks/_ap37_check.py" "$(native "$REC")" 1
rc=$?; restore_audit; exit $rc
