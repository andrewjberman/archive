#!/usr/bin/env bash
# MX-c-6 AC1 (FWD-12, FWD-15, FWD-17, FWD-18): the emitted catalog's `needs:` list holds E-1..E-29 exactly, each with
# need/source/status/tool/owner/retires/op_class; status in the enum; every GAP/DENIED/UNMEASURED names an owner; the
# 8 unowned gaps are exactly E-9..E-12, E-20, E-26..E-28; every entry names the C#/W# it retires (or a retires_none reason); the YCharts PARTIAL
# entry carries its live error.
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
out=$(timeout 60 python "$(native "$H/c6_needs.py")" "$(native "$(pwd)/$GW/app/refs/DATA_CATALOG.yaml")" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
