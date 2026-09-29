#!/usr/bin/env bash
# t9 AC1: every portal_* catalog row sits in portal_datasets naming read_tool + accessor equal to portal_index ROWS, with >= 4 rows (this cell adds one).
. "$(dirname "$0")/_root.sh"
out=$(python "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round4/checks/portal_rows.py" "$GW/app/refs/DATA_CATALOG.yaml" "$GW/app/integrations/portal_index/integration.py" 4 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
