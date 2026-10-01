#!/usr/bin/env bash
# MX-g-3 AC1 (G-RDR, train R7; ruling 27413): the NFRA_MCPMSP reader census, run on THIS tree, reads unrouted=0 --
# portal_index and opal_discover read portal-v2 through app/internal_role.py (or firm_role.py).
. "$(dirname "$0")/_root.sh"
out=$(timeout 110 bash "org/missions/D6/NFRA/NFRA_MCPMSP/deliverables/2.0.0_SA_COO~MS/round2/checks/e1z.AC1.sh" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
