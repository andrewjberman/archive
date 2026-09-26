#!/usr/bin/env bash
# MX-s-4 AC1: the newest asset-dim download log written after issue reads download rc 0 and no FAILED line (s4_read.py).
. "$(dirname "$0")/_root.sh"
out=$(timeout 200 python org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~O/round2/checks/s4_read.py AC1 . 2>&1 | tr -d '\r')
printf '%s\n' "$out" | grep -v '^OK$\|^NOT-OK$'
if printf '%s\n' "$out" | tail -1 | grep -qx OK; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
