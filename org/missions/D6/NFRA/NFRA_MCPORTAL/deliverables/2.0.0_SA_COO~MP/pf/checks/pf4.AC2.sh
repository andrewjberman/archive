#!/usr/bin/env bash
# MP-pf-4 AC2 (the seam to the REAL neighbour, the repo's DATA_CATALOG.yaml; a bound, so it passes at the base): the handler's segment reader over the real catalog returns no pair the tool_index `serves` lists do
# not hold, while the catalog carries owning-firm `firm:` keys outside tool_index (the trap, so the probe is not vacuous). Reads from _pf4_realcat.py; today it prints
#   real catalog: tool_index_rows=99 firm_keys_outside_tool_index=273 pairs_from_tool_index=0 pairs_returned=0 extra_pairs=0
. "$(dirname "$0")/../../pd/checks/_root.sh"
line=$(timeout 100 python org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks/_pf4_realcat.py 2>&1 | tr -d '\r' | tail -1)
echo "$line"
ok=$(python -c "
import re, sys
m = re.search(r'tool_index_rows=(\d+) firm_keys_outside_tool_index=(\d+) pairs_from_tool_index=(\d+) pairs_returned=(\d+) extra_pairs=(\d+)', sys.argv[1])
print('yes' if m and int(m.group(1)) >= 1 and int(m.group(2)) >= 1 and int(m.group(4)) == int(m.group(3)) and int(m.group(5)) == 0 else 'no')" "$line")
if [ "$ok" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
