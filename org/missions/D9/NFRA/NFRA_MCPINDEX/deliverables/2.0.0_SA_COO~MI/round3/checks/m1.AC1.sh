#!/usr/bin/env bash
# MX-m-1 AC1 (the measure batch is on the record, each measure with its denominator): the record
# MEASURE_BATCH_ROUND3.md in the worker's deliverables dir carries the four sections `## (a)` .. `## (d)`, and EACH
# section carries a `DENOMINATOR:` line and a `FINDING:` line. The findings themselves are graded at L9 (J1).
. "$(dirname "$0")/_root.sh"
R=$(ls org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~*/MEASURE_BATCH_ROUND3.md 2>/dev/null | head -1)
[ -n "$R" ] || { echo "MEASURE_BATCH_ROUND3.md absent under deliverables/0.9.0_WK_NFRA_MCPINDEX~*/"; echo "RESULT: FAIL"; exit 1; }
ok=0
for s in a b c d; do
  sec=$(awk -v h="## ($s)" 'index($0,h)==1{f=1;next} /^## /{if(f)exit} f' "$R")
  if printf '%s\n' "$sec" | grep -q '^DENOMINATOR:' && printf '%s\n' "$sec" | grep -q '^FINDING:'; then ok=$((ok+1)); else echo "  section ($s): missing, or without DENOMINATOR:/FINDING:"; fi
done
echo "record $R: sections complete $ok of 4"
if [ "$ok" = 4 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
