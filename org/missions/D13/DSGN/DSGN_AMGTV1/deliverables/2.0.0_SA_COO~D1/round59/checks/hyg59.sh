#!/usr/bin/env bash
# hyg59.sh -- DSGN_AMGTV1 round 59 bound (2.0.0_SA_COO~D1): the SecurityAnalysis page still typechecks and lints.
# Usage: bash hyg59.sh <outer-worktree-root>. Prints one line per tool, then "HYG59: PASS" or "HYG59: FAIL". Writes nothing.
# Why this and not battery29: round 59 moves and removes markup that battery29's harnesses anchor on; their re-anchor is the round's
# batched repair cell, cut after A-F merge (ledger/ROUND_ANALYSIS.round58.md R1). Each build cell keeps tsc and eslint green.
root="${1:?outer worktree root}"
cd "$root/portal" || { echo "HYG59: FAIL (no portal/ under $root)"; exit 1; }
timeout 900 node node_modules/typescript/bin/tsc -b --noEmit >/tmp/hyg59_tsc.$$ 2>&1; t=$?
echo "tsc -b --noEmit rc=$t"; [ $t -ne 0 ] && head -20 /tmp/hyg59_tsc.$$
timeout 600 node node_modules/eslint/bin/eslint.js --quiet src/pages/SecurityAnalysis >/tmp/hyg59_es.$$ 2>&1; e=$?
echo "eslint --quiet src/pages/SecurityAnalysis rc=$e"; [ $e -ne 0 ] && grep -v baseline-browser /tmp/hyg59_es.$$ | head -20
rm -f /tmp/hyg59_tsc.$$ /tmp/hyg59_es.$$
if [ $t -eq 0 ] && [ $e -eq 0 ]; then echo "HYG59: PASS"; exit 0; else echo "HYG59: FAIL"; exit 1; fi
