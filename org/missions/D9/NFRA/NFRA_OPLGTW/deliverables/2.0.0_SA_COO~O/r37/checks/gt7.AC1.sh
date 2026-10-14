#!/usr/bin/env bash
# OPLGTW OG-gt-7 AC1 (round-37 FWD22-W4, FWD-22): the ten tools are registered and the registry count test reads the new pin.
#  - app/tools.py declares all ten functions as @mcp.tool() registrations;
#  - tests/test_entitlement_admin.py passes whole (9 of 9), which includes the registry count pin at 75.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
names="harvest_resolve_security harvest_security_coverage harvest_get_chatter harvest_search_articles harvest_get_article harvest_get_fundamentals harvest_query_columns harvest_get_research harvest_get_filing_analysis harvest_get_peers_and_scores"
reg=0; for n in $names; do grep -qE "^def $n\(" "$GW/app/tools.py" && reg=$((reg+1)); done
echo "tools registered in app/tools.py: $reg of 10"
out=$(cd "$GW" && timeout 110 python -m pytest tests/test_entitlement_admin.py -q -p no:cacheprovider --color=no 2>&1 | tr -d ''); r0=$?
passed=$(printf '%s
' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); failed=$(printf '%s
' "$out" | grep -cE ' failed|^FAILED|^ERROR')
echo "entitlement-admin suite (the registry count pin is 75): passed ${passed:-0} of 9, failed lines $failed, rc $r0"
[ "${passed:-0}" = 9 ] && [ "$failed" = 0 ] || r0=1
restore_audit
[ "$reg" = 10 ] && [ "$r0" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
