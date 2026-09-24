#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-1 AC2 (DIFFERENCE CONTROL) -- the harness GRADES extras: pointed at round 38's committed
# rich body (rm-4's, which carries the 17 figures the page does not show), it must answer NOT OK with exit 1.
# usage: bash <this>   (from the repo root; no server)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
STALE="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~143/served/BA_US_Equity.md"
node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --rich "$STALE" > .scratch.ro1ac2.txt 2>&1; rc=$?
grep -E '^(FIGURES|EXPORT)' .scratch.ro1ac2.txt; rm -f .scratch.ro1ac2.txt
echo "harness on the stale body: rc=$rc (the control needs 1)"
[ "$rc" -eq 1 ]
