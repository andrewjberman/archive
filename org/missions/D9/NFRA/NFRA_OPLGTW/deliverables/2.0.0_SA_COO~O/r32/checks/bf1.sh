#!/usr/bin/env bash
# OPLGTW OG-bf-1 checks: bf1.sh AC1|AC2 runs bf1.<AC>.py against the worker's record (see each file's docstring).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/backfill_record.json"
case "$1" in
  AC1) timeout 115 python "$(native "$D/bf1.AC1.py")" "$(native "$REC")" "$(native "$PWD")" | tr -d '\r' ;;
  AC2) timeout 115 python "$(native "$D/bf1.AC2.py")" "$(native "$REC")" "$(native "$PWD")" | tr -d '\r' ;;
  *) echo "usage: bf1.sh AC1|AC2"; exit 2 ;;
esac
