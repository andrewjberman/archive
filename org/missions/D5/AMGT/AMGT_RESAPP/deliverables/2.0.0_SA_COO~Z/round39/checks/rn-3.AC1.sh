#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-3 AC1 -- Z-S251's class is retired: no file under portal/src or portal/scripts asserts
# the retired band identity (the literal 0A1733 or the triplet 10,23,51) EXCEPT the allow-list (token definitions,
# IRPT's own render bundle, the fixture that pins --bg-header, and ui-measure.mjs's re-keyed comments, all named in
# Z-S251 as correctly kept). usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
ALLOW='^(src/pages/InvestorReporting/render/brand\.ts|src/pages/InvestorReporting/render/brand\.tokens\.json|src/pages/InvestorReporting/render/print\.css|src/pages/SecurityAnalysis/__harness__/tests/uiMeasureFixture\.html|scripts/ui-measure\.mjs)$'
grep -rlE '0A1733|10, ?23, ?51' src scripts | sort > .scratch.rn3.hits.txt
total=$(wc -l < .scratch.rn3.hits.txt | tr -d ' ')
grep -vE "$ALLOW" .scratch.rn3.hits.txt > .scratch.rn3.left.txt; left=$(wc -l < .scratch.rn3.left.txt | tr -d ' ')
echo "files carrying the retired identity: $total (allow-listed: $((total-left)))"; echo "outside the allow-list ($left):"; cat .scratch.rn3.left.txt
rm -f .scratch.rn3.hits.txt .scratch.rn3.left.txt
[ "$left" -eq 0 ]
