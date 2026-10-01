#!/usr/bin/env bash
# MX-d-6 AC2 (control): "ETF positioning" still names etfs_get_positioning, AND the MX-v-6 routing harness does not fall
# below its round-6 base count (24 of 27, measured by the issuer 2026-10-01 on CLOUD 81887e8ae8). Item 1(b).
. "$(dirname "$0")/_root.sh"
P="$(pwd)/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round6/checks/r6_probe.py"
out=$(cd "$GW" && timeout 60 python "$(native "$P")" control 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
rt=$(cd "$GW" && timeout 100 python tests/routing/run_routing.py 2>&1 | tr -d '\r' | grep -E '^ROUTING:' | tail -1)
echo "${rt:-ROUTING: no line} (floor 24)"
n=$(printf '%s' "$rt" | sed -n -E 's/^ROUTING: ([0-9]+) of.*/\1/p')
if [ -z "$n" ] || [ "$n" -lt 24 ]; then rc=1; fi
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
