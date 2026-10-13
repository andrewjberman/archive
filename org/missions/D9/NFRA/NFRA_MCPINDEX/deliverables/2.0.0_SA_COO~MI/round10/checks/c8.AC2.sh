#!/usr/bin/env bash
# MX-c-8 AC2 (FWD-21 rows): one harvest_datasets row per SERVE-NOW prefix of SERVABLE_PREFIXES v3, read at its pin
# @0b2778751a (never the moving file); 16 of 16 prefixes (row 8 = six gold tables); no WITHHOLD row; each row names a
# reader or its gap owner. Instrument c10_harvest.py.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
L=org/tier1_exec/1.0.0_SA_CTO/deliverables/SERVABLE_PREFIXES_OPAL_DATA_HARVEST_20261013.md
T="${TMPDIR:-/tmp}/mx_r10_c8ac2_$$"; mkdir -p "$T"
MSYS_NO_PATHCONV=1 git show "0b2778751a:$L" > "$T/list.md"
[ -s "$T/list.md" ] || { rm -rf "$T"; echo "list at 0b2778751a unreadable"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 60 python "$(native "$H/c10_harvest.py")" "$(native "$T/list.md")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" 2>&1 | tr -d '\r'); rc=$?
rm -rf "$T"
printf '%s\n' "$out" | tail -20
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
