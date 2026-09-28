#!/usr/bin/env bash
# MX-x-2 AC1 (row Z-W3-S4): the portal_* catalog rows have their own section and each carries the exact key it describes.
. "$(dirname "$0")/_root.sh"
C="$GW/app/refs/DATA_CATALOG.yaml"
out=$(python "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round3/checks/x2_catalog.py" "$C" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
