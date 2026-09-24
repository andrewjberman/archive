#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-3 AC2 (BOUND) -- the Thesis tab still renders under its own harnesses and compiles.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
ok=0
for h in drafting tabs; do node "src/pages/SecurityAnalysis/__harness__/$h.harness.cjs" > ".scratch.$h.txt" 2>&1; r=$?; echo "$h exit=$r :: $(tail -1 ".scratch.$h.txt")"; rm -f ".scratch.$h.txt"; [ "$r" -eq 0 ] || ok=1; done
timeout 300 npx tsc -b --noEmit > .scratch.tsc.txt 2>&1; r=$?; echo "tsc exit=$r"; rm -f .scratch.tsc.txt; [ "$r" -eq 0 ] || ok=1
exit "$ok"
