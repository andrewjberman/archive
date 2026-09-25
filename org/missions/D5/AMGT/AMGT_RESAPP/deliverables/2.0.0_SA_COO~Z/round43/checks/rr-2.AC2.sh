#!/usr/bin/env bash
# AMGT_RESAPP round 43, AMGT-rr-2 AC2 -- THE CASES AXIS CAN FAIL (R-8's control): the harness, run on RKT_LN_Equity's SERVED page
# (whose base case is SERVED at 7386.63) against the export body the deployed function served at round 43's cut -- which reads
# "Upside / Base / Downside cases: SERVED -- the payload carries no case block" -- answers NOT OK on the CASES line.
# usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
F="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round43/checks/fixtures"
cd portal && node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --fixture "$F/served_fixture.RKT_LN_Equity.json" \
  --rich "$F/RKT_LN_Equity.rich.at-cut.md" > /tmp/rr2ac2.$$ 2>&1; rc=$?
grep -E '^(CASES|EXPORT)' /tmp/rr2ac2.$$; rm -f /tmp/rr2ac2.$$
echo "harness on the cut's served body: rc=$rc (the control needs 1)"
[ "$rc" -eq 1 ]
