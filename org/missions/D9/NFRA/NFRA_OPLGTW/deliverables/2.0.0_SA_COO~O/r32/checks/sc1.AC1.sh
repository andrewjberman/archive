#!/usr/bin/env bash
# OPLGTW OG-sc-1 AC1: see sc1.AC1.py. Every column list is re-read from the live parquet footer.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~40/silver_schema_record.json"
timeout 115 python "$(native "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r32/checks/sc1.AC1.py")" "$(native "$REC")" | tr -d '\r'
