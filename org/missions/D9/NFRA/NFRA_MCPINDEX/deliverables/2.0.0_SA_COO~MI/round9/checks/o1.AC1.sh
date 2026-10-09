#!/usr/bin/env bash
# MX-o-1 AC1 (PRD v0.8 FWD-19, contract 2): the trade_rec census -- every candidate producer with its denominator, a
# SERVED|GAP verdict, the surviving source read once (SERVED) or the owner named (GAP). Instrument ops_census.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
C="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~30/census_trade_rec.json"
[ -f "$C" ] || { echo "census absent at $C"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 60 python "$(native "$H/ops_census.py")" "$(native "$(pwd)/$C")" trade_rec 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -8
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
