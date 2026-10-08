#!/usr/bin/env bash
# OPLGTW OG-cc-1 AC1: see cc1.AC1.py. Every count is recomputed from live S3 and the gateway's own qualification code.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/closure_census_record.json"
timeout 115 python "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/cc1.AC1.py")" "$(native "$REC")" "$(native "$PWD")" | tr -d '\r'
