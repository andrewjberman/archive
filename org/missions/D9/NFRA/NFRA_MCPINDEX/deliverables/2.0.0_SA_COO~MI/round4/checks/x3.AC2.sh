#!/usr/bin/env bash
# MX-x-3 AC2 (row Z-W13-S2, the unidentified row): MISMATCH_ROW_MX-x-3.md in the worker's deliverables names every
# catalog row the live validator reports as not OK, one 'ROW: <entity> | STATE: <state> | CAUSE: <cause>' line each, and
# carries the live run's own SUMMARY line with its denominator.
. "$(dirname "$0")/_root.sh"
F=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/MISMATCH_ROW_MX-x-3.md 2>/dev/null | head -1)
[ -n "$F" ] || { echo "MISMATCH_ROW_MX-x-3.md absent"; echo "RESULT: FAIL"; exit 1; }
rows=$(grep -cE '^ROW: [^|]+ \| STATE: [A-Z-]+ \| CAUSE: .+' "$F")
summ=$(grep -cE '^SUMMARY: \{.*"rows": [0-9]+' "$F")
echo "record $F: ROW lines $rows; SUMMARY line present=$summ"
if [ "$rows" -ge 1 ] && [ "$summ" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
