#!/usr/bin/env bash
# OPLGTW OG-rv-3 AC1 (round-37 RIVAL-HOOKUP, FWD-22): the ten rival-funds tools are registered and the registry count test reads the new pin.
#  - app/tools.py declares the ten tool functions as @mcp.tool() registrations;
#  - tests/test_entitlement_admin.py passes whole (9 of 9), which includes the registry count pin at 105.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
names="etfs_get_peer_group etfs_get_rival_fund_holdings etfs_who_holds etfs_get_security_reference etfs_get_coverage etfs_get_fund_trades etfs_get_fund_flows etfs_compare_peers etfs_get_research_notes etfs_get_rival_page_status"
reg=0; for n in $names; do grep -qE "^def $n\(" "$GW/app/tools.py" && reg=$((reg+1)); done
echo "tools registered in app/tools.py: $reg of 10"
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_entitlement_admin.py -q -p no:cacheprovider --color=no 2>&1 | tr -d ''); r0=$?
passed=$(printf '%s
' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); failed=$(printf '%s
' "$out" | grep -cE ' failed|^FAILED|^ERROR')
echo "entitlement-admin suite (the registry count pin is 105): passed ${passed:-0} of 9, failed lines $failed, rc $r0"
[ "${passed:-0}" = 9 ] && [ "$failed" = 0 ] || r0=1
restore_audit
[ "$reg" = 10 ] && [ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
