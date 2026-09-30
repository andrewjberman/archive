#!/usr/bin/env bash
# MX-s-15 AC1: dim_transaction is declared beside the three dim_* tables on all 6 surfaces (datasets.json, query.py
# schemas + grains, data_entitlement DATASETS, schwab_audit _DATASETS, the reader role's prefix list for both masters).
. "$(dirname "$0")/_root.sh"
out=$(timeout 120 python "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round5/checks/r5_probe.py" s15 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
