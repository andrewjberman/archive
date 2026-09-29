#!/usr/bin/env bash
# AMGT_RESAPP round 46, AMGT-uu-2 AC2 -- THE VERDICT STILL COUNTS A DROPPED ABSENCE, WITH THE MOUNT (row Z-S294's tightened control).
# The harness, run on the two PRE-FIX served exports pinned in round45/checks/controls (RKT_LN_Equity, AMD_US_Equity, captured
# 2026-09-26T13:29Z), must print "ABSENCES ... missing=1" AND "EXPORT-COMPARE NOT OK" on BOTH. A crash (no such lines) FAILS
# this check -- it never reads as the control firing. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
CT="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/controls"
fired=0
for k in RKT_LN_Equity AMD_US_Equity; do
  out="$(timeout 55 node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --fixture "$CT/served_fixture.$k.json" --rich "$CT/$k.served.rich.md" 2>&1)"; rc=$?
  abs="$(printf '%s\n' "$out" | grep -E '^ABSENCES ')"; ver="$(printf '%s\n' "$out" | grep -E '^EXPORT-COMPARE')"
  echo "$k: harness rc=$rc; ${abs:-<no ABSENCES line>}; ${ver:-<no EXPORT-COMPARE line>}"
  if printf '%s' "$abs" | grep -q ' missing=1 ' && printf '%s' "$ver" | grep -q 'NOT OK'; then fired=$((fired+1)); fi
done
echo "THE VERDICT COUNTS A DROPPED ABSENCE (tokens, not rc): $fired of 2"
[ "$fired" = "2" ]
