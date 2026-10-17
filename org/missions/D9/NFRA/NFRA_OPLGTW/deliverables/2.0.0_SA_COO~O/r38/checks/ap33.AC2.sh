#!/usr/bin/env bash
# OPLGTW OG-ap-33 AC2 (round 40, landing the AMGT_HARVST release 319c9413a2 on trunk): gateway conflicted paths equal the live release blobs, gateway tests equal trunk's, the manifest opal-gateway block equals trunk's.
# Record: W/ap33_landing.json {trunk_base_sha, hvst_sha, release_sha, merge_sha[, stop_row]}; override AP33_REC_OVERRIDE. The grading is _ap33_check.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${AP33_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/ap33_landing.json}"
[ -f "$REC" ] || { echo "ap33_landing.json absent"; echo "RESULT: FAIL"; exit 1; }
python "$(dirname "$0")/_ap33_check.py" "$(native "$REC")" 2
rc=$?; restore_audit; exit $rc
