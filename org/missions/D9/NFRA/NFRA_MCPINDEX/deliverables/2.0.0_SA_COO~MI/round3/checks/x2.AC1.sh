#!/usr/bin/env bash
# MX-x-2 AC1 (row Z-W3-S4; amended A1 on the CTO ruling of Z-W13-S3 @8ed938b2d7): the portal_* catalog rows have their
# own section and each names its reader -- read_tool + accessor equal to portal_index's ROWS -- with no raw key literal.
. "$(dirname "$0")/_root.sh"
C="$GW/app/refs/DATA_CATALOG.yaml"
I="$GW/app/integrations/portal_index/integration.py"
out=$(python "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round3/checks/x2_catalog.py" "$C" "$I" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
