#!/usr/bin/env bash
# OPLGTW OG-hg-1 AC1 (CTO R35 cell 1): .tools/halt-gate-worker-order-test.sh passes. Its fixture is a release tree cut on
# a sha that PREDATES the worker slot's first order:
# case 1 -- the gate finds the worker's order in the SHARED root and proceeds;
# case 2 -- an order whose LAST <status> tag is terminal does not admit, though an earlier tag in the file reads staged;
# case 3 -- an order whose FIRST tag is terminal and whose LAST tag is pending DOES admit;
# case 4 -- a [STOP] addressed to the issuer still halts the worker's deploy.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
T=".tools/halt-gate-worker-order-test.sh"
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 200 bash "$T" 2>&1 | tr -d '\r'); rc=$?
p=$(printf '%s\n' "$out" | grep -cE '^PASS: case [1-4]( |$)'); f=$(printf '%s\n' "$out" | grep -cE '^FAIL')
echo "rc=$rc; cases passed $p of 4; FAIL lines $f"
[ "$rc" = 0 ] && [ "$p" = 4 ] && [ "$f" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
