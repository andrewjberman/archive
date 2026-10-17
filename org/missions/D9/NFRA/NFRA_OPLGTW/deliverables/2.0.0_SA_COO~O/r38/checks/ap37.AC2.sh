#!/usr/bin/env bash
# OPLGTW OG-ap-37 AC2 (round 41, landing dell1's gateway release 1753c741d9 on the sitez trunk): the manifest block names the live release. Grading: _ap37_check.py mode 2.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP37_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap37_landing.json}"
[ -f "$REC" ] || { echo "ap37_landing.json absent"; echo "RESULT: FAIL"; exit 1; }
python "$(dirname "$0")/_ap37_check.py" "$(native "$REC")" 2
rc=$?; restore_audit; exit $rc
