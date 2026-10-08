#!/usr/bin/env bash
# OPLGTW OG-g5-1 AC1: see g5.AC1.py. The record is the worker's; every count is re-read from the SSM invocations.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~39/g5_enumerate_record.json"
timeout 100 python "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/g5.AC1.py")" "$(native "$REC")" | tr -d '\r'
