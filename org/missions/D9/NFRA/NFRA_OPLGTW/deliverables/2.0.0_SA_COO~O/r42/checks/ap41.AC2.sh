#!/usr/bin/env bash
# OPLGTW OG-ap-41 AC2 (round 42): the landing leaves the EC2 manifest block as trunk has it (opal-gateway deployed_commit 4257a2aa42, previous d077cef043: dell1's cg-3 release) and moves nothing else in it.
# Grading: _ap37_check.py mode 2; the record names expected_deployed_commit and expected_previous_commit.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP41_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap41_landing.json}"
[ -f "$REC" ] || { echo "ap41_landing.json absent"; echo "RESULT: FAIL"; exit 1; }
python "$(dirname "$0")/../../r38/checks/_ap37_check.py" "$(native "$REC")" 2
rc=$?; restore_audit; exit $rc
