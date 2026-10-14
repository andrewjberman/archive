#!/usr/bin/env bash
# MX-c-9 AC2 (FWD-21 on list v4): the catalog's harvest rows cover v4's 24 top-level prefixes and row 12b's seven
# research tables, read at the v4 pin @7e0da2dfee (never the moving file). Instrument c11_harvest.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
L=org/tier1_exec/1.0.0_SA_CTO/deliverables/SERVABLE_PREFIXES_OPAL_DATA_HARVEST_20261013.md
T="${TMPDIR:-/tmp}/mx_r11_c9ac2_$$"; mkdir -p "$T"
MSYS_NO_PATHCONV=1 git show "7e0da2dfee:$L" > "$T/list.md"
[ -s "$T/list.md" ] || { rm -rf "$T"; echo "list at 7e0da2dfee unreadable"; echo "RESULT: FAIL"; exit 1; }
HD="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~34/blocked_harvest_rows"   # A2: held on call -a63a
out=$(timeout 60 python "$(native "$H/c11_harvest.py")" "$(native "$T/list.md")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" "$(native "$(pwd)/$HD")" 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
printf '%s\n' "$out" | tail -30
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
