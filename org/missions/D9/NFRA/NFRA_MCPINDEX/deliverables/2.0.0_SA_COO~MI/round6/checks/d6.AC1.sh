#!/usr/bin/env bash
# MX-d-6 AC1: in-process on this tree, opal_discover names blackdiamond_list_fees for "what fees did Black Diamond charge"
# and a schwab_* tool for "Schwab positions" (round-5 analysis item 1(a); row Z-W21-S22).
. "$(dirname "$0")/_root.sh"
P="$(pwd)/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round6/checks/r6_probe.py"
out=$(cd "$GW" && timeout 110 python "$(native "$P")" route 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
