#!/usr/bin/env bash
# OPLGTW OG-tm-1 checks: tm1.sh AC1|AC2|AC3 runs tm1.<AC>.py (see each file's docstring).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
D="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks"
case "$1" in
  AC1) timeout 100 python "$(native "$D/tm1.AC1.py")" | tr -d '\r' ;;
  AC2) timeout 110 python "$(native "$D/tm1.AC2.py")" "$(native "$PWD")" | tr -d '\r' ;;
  AC3) timeout 100 python "$(native "$D/tm1.AC3.py")" | tr -d '\r' ;;
  *) echo "usage: tm1.sh AC1|AC2|AC3"; exit 2 ;;
esac
