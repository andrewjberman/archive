#!/usr/bin/env bash
# MX-q-3 AC1: in-process on this tree, opal_discover('macro data') names an MCP TOOL (kind mcp_tool, defined as a
# function under app/integrations) as next_tool for mac.01 -- never the query_v0 HTTP route.
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && timeout 300 python "$OLDPWD/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round5/checks/r5_probe.py" q3route 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
