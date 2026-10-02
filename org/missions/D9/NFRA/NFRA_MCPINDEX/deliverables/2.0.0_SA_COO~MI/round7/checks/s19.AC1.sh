#!/usr/bin/env bash
# MX-s-19 AC1: the LIVE writer census reads 1 writer on ALL 4 BD silver tables (MX-s-16's census, unscoped).
. "$(dirname "$0")/_root.sh"
out=$(timeout 110 bash "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round6/checks/s16.AC1.sh" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
