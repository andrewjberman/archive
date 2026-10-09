#!/usr/bin/env bash
# MX-c-7 AC1 (FWD-19, contract 4): the emitted catalog holds the operations lead's six entries E-30..E-35. E-30/E-31
# mirror their reader's census verdict (SERVED + tool, or GAP + owner); E-32..E-35 are GAP, unowned, no tool. E-1..E-29
# are kept. Instrument c7_needs.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
D=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables
out=$(timeout 60 python "$(native "$H/c7_needs.py")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" \
  "$(native "$(pwd)/$D/0.9.0_WK_NFRA_MCPINDEX~30/census_trade_rec.json")" \
  "$(native "$(pwd)/$D/0.9.0_WK_NFRA_MCPINDEX~31/census_billing.json")" "$(native "$(pwd)/$GW")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -8
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
