#!/usr/bin/env bash
# OA-e-8 AC2 (the baseline is the RECORD's, not a recollection): the file's baseline cites
# docs/architecture/OPAL_ANALYST_PRD.md with total_seconds 345 and data_layer_seconds 0.92, and that file at HEAD still
# carries both figures ("5m45s" and "0.92s") inside its s.11.1 section.
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~12/E8_SPEED_STAGES.json"
P="docs/architecture/OPAL_ANALYST_PRD.md"
[ -f "$F" ] || { echo "measurement file absent: $F"; echo "RESULT: FAIL"; exit 1; }
b=$(python -c "
import json,sys
b=json.load(open(sys.argv[1],encoding='utf-8')).get('baseline') or {}
print(b.get('source',''), b.get('total_seconds',''), b.get('data_layer_seconds',''))" "$F" 2>/dev/null | tr -d '\r')
sec=$(git show "HEAD:$P" | awk '/^### .*11.1/{f=1;next} f&&/^### /{exit} f')
h1=$(printf '%s\n' "$sec" | grep -c '5m45s'); h2=$(printf '%s\n' "$sec" | grep -c '0\.92s')
echo "file baseline=[$b]; source s.11.1 lines with 5m45s=$h1, with 0.92s=$h2"
set -- $b
if [ "$1" = "$P" ] && [ "$2" = 345 ] && [ "$3" = 0.92 ] && [ "$h1" -ge 1 ] && [ "$h2" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
