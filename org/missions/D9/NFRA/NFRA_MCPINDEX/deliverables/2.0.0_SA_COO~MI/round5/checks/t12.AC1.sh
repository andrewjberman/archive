#!/usr/bin/env bash
# t12 AC1: every portal_* catalog row sits in portal_datasets naming read_tool + accessor equal to portal_index ROWS, with >= 6 rows (this cell adds one; MX-t-10 makes 5).
. "$(dirname "$0")/_root.sh"
out=$(python "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round5/checks/portal_rows.py" "$GW/app/refs/DATA_CATALOG.yaml" "$GW/app/integrations/portal_index/integration.py" 6 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
