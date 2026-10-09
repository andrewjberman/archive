#!/usr/bin/env bash
# OPLGTW OG-ap-2 checks: ap2.sh AC1|AC2 (see ap2_check.py).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap2_arm1.json"
case "$1" in
  AC1) timeout 110 python "$(native "$D/ap2_check.py")" AC1 "$(native "$PWD")" | tr -d '\r' ;;
  AC2) timeout 110 python "$(native "$D/ap2_check.py")" AC2 "$(native "$REC")" "$(native "$PWD")" | tr -d '\r' ;;
  *) echo "usage: ap2.sh AC1|AC2"; exit 2 ;;
esac
