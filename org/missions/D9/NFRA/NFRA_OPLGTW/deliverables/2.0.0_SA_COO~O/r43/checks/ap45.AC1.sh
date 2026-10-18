#!/usr/bin/env bash
# OPLGTW OG-ap-45 AC1 (round 43, landing site Z's tenth release eff517546e (and a0c83303ee under it) on the sitez trunk): the merge shape and content. Grading: _ap37_check.py mode 1 (the same grading as OG-ap-37; the record names the commit to land in `dell_sha`).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP45_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap45_landing.json}"
[ -f "$REC" ] || { echo "ap45_landing.json absent"; echo "RESULT: FAIL"; exit 1; }
python "$(dirname "$0")/_ap43_check.py" "$(native "$REC")" 1
rc=$?; restore_audit; exit $rc
