#!/usr/bin/env bash
# MX-t-13 AC1: a black_diamond integration is registered and a catalog row's read_tool names one of its bd_* functions.
. "$(dirname "$0")/_root.sh"
out=$(timeout 120 python "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round5/checks/r5_probe.py" t13 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
