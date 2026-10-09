#!/usr/bin/env bash
# OPLGTW OG-bh-1 checks: bh1.sh AC1|AC2 runs bh1.<AC>.py against the worker's records (see each file's docstring).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~46"
case "$1" in
  AC1) timeout 100 python "$(native "$D/bh1.AC1.py")" "$(native "$W/bh1_census_record.json")" | tr -d '\r' ;;
  AC2) timeout 115 python "$(native "$D/bh1.AC2.py")" "$(native "$W/bh1_census_record.json")" "$(native "$W/bh1_backfill_record.json")" "$(native "$PWD")" | tr -d '\r' ;;
  *) echo "usage: bh1.sh AC1|AC2"; exit 2 ;;
esac
