#!/usr/bin/env bash
# MX-o-2 AC3 (FWD-19 seam probe, the REAL neighbour). SERVED -> the reader, called once in-process against live served
# S3 under the Opal-internal principal on the census probe_scope, returns >= 1 row, every row's keys equal to the
# fixture's, scope stated, as_of with claim measured, completeness stated, no fixture row served. GAP -> PASS by
# branch. Instrument ops_probe.py (read-only; prints counts, keys and dates only).
H="$(cd "$(dirname "$0")" && pwd)"
. "$H/_root.sh"
C="org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~31/census_billing.json"
vs=$(python -c "import json,sys; c=json.load(open(sys.argv[1],encoding='utf-8')); print(c.get('verdict'), c.get('probe_scope') or '-')" "$(native "$(pwd)/$C")" 2>&1 | tr -d '\r')
v=${vs%% *}; sc=${vs#* }
echo "census verdict: $v; probe_scope: $sc"
if [ "$v" = GAP ]; then echo "GAP branch: no reader to probe"; echo "RESULT: PASS"; exit 0; fi
[ "$v" = SERVED ] || { echo "RESULT: FAIL"; exit 1; }
out=$(timeout 120 python "$(native "$H/ops_probe.py")" "$(native "$(pwd)/$GW")" ops_billing billing "$sc" 2>&1 | tr -d '\r'); rc=$?
printf '%s\n' "$out" | tail -6
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
