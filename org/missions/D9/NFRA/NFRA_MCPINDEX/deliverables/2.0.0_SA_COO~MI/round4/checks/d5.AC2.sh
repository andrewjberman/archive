#!/usr/bin/env bash
# MX-d-5 AC2 (Z-W2-S8, scoped by the issuer): the ETF ask is NOT mis-routed -- its first match is a platinum/etfs row, or, while the catalog holds no platinum/etfs row (a widening held at Andrew), the answer is NOT_CATALOGUED.
. "$(dirname "$0")/_root.sh"
out=$(cd "$GW" && timeout 300 python "$OLDPWD/org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round4/checks/discover_probe.py" first "ETF holdings and fund flows" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out"
rows=$(grep -c "platinum/etfs" "$GW/app/refs/DATA_CATALOG.yaml")
fst=$(printf '%s\n' "$out" | sed -n 's/.*first=\(.*\)$/\1/p'); cat_=$(printf '%s\n' "$out" | sed -n 's/^catalogued=\([A-Za-z]*\) .*/\1/p')
echo "catalog platinum/etfs mentions=$rows; catalogued=$cat_; first=$fst"
rc=1
if [ "$rows" -gt 0 ]; then case "$fst" in platinum/etfs*) rc=0;; esac; else [ "$cat_" = False ] && rc=0; fi
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
