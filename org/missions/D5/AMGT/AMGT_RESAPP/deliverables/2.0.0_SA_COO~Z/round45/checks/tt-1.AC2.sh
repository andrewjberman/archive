#!/usr/bin/env bash
# AMGT_RESAPP round 45, AMGT-tt-1 AC2 -- THE VERDICT COUNTS A DROPPED ABSENCE: the harness, run on the two PRE-FIX served exports
# pinned in round45/checks/controls (RKT_LN_Equity, AMD_US_Equity, captured 2026-09-26T13:29Z), must read EXPORT-COMPARE NOT OK
# (rc=1) on both, because each drops one page absence. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
CT="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/controls"
bad=0
for k in RKT_LN_Equity AMD_US_Equity; do
  out="$(node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --fixture "$CT/served_fixture.$k.json" --rich "$CT/$k.served.rich.md" 2>&1)"; rc=$?
  echo "$k: harness rc=$rc; $(printf '%s\n' "$out" | grep -E '^ABSENCES ') ; $(printf '%s\n' "$out" | grep -E '^EXPORT-COMPARE')"
  [ "$rc" = "1" ] || bad=1
done
echo "THE VERDICT COUNTS A DROPPED ABSENCE: $([ $bad = 0 ] && echo YES on 2 of 2 || echo NO)"
exit $bad
