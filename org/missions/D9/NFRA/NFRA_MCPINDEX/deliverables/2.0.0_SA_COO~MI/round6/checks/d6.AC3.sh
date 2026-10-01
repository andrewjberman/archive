#!/usr/bin/env bash
# MX-d-6 AC3: the reachability grade (item 1(c), Z-W15-S3): EVERY DATA_CATALOG.yaml row that names a read_tool is routed to
# that tool by discover on one of its own example_questions. Graded by discover calls, never by presence.
. "$(dirname "$0")/_root.sh"
P="$(pwd)/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round6/checks/r6_probe.py"
out=$(cd "$GW" && timeout 110 python "$(native "$P")" reach 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
