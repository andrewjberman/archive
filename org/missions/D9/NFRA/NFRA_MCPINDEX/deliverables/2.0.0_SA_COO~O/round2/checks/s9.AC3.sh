#!/usr/bin/env bash
# MX-s-9 AC3 (egress ledgered): the seat's egress ledger records >=2 Black Diamond calls (the ONE discovery read of the
# persisted template + qt4 dimension catalog, and the qt4 pull), each line naming a UTC time, the endpoint class and the
# purpose; and it records the asset_super_class discovery outcome as either a dim id or 'absent'.
. "$(dirname "$0")/_root.sh"
L=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.4.0_DS_ClientPlatform~D/EGRESS_LEDGER_MX-s-9.md
[ -f "$L" ] || { echo "ledger absent: $L -- RESULT: FAIL"; exit 1; }
calls=$(grep -cE '^\| *20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9:]+Z *\|' "$L")
sc=$(grep -ciE 'super.?class.*(dim id|dim_id|absent)' "$L")
echo "ledgered calls=$calls; super-class outcome lines=$sc"
if [ "$calls" -ge 2 ] && [ "$sc" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
