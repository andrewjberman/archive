#!/usr/bin/env bash
# MX-d-4 AC2 (R-14): every SERVABLE row opal_discover returns for three asks carries freshness.served_written_at with claim 'measured' (and a value) or 'absent' (with an error_class).
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && timeout 300 python "$OLDPWD/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round4/checks/discover_probe.py" written "model portfolio AUM" "model portfolio benchmark returns" "market overview returns" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
