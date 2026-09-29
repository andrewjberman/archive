#!/usr/bin/env bash
# MX-d-4 AC1 (R-13): in-process on this tree, opal_discover('model portfolio AUM') names mdpf_get_aum_metrics with args {scope: global} as next_tool for its mp.01 match.
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && timeout 300 python "$OLDPWD/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round4/checks/discover_probe.py" route "model portfolio AUM" mp.01 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
nt=$(printf '%s\n' "$out" | grep -c 'next_tool=mdpf_get_aum_metrics args={"scope": "global"}')
rc=1; [ "$nt" = 1 ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
