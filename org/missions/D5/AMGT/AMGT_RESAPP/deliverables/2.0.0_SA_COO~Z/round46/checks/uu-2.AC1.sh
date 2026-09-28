#!/usr/bin/env bash
# AMGT_RESAPP round 46, AMGT-uu-2 AC1 -- the export-compare harness loads the page WITH HeaderBrief's TimelinePanel mount
# (row Z-S292) and still compares: one served fixture (1299_HK_Equity, captured 2026-09-28T20:26Z against CodeSha256
# vBSCqd71...Mrew=) reads FIGURES/CITES/ABSENCES/CASES lines with missing=0, harness rc=0.
# EXERCISED only when the portal tree under test MOUNTS TimelinePanel in HeaderBrief.tsx; otherwise NOT_EXERCISED (exit 1).
# usage: bash <this>   (from the repo root of the worktree under test)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
FX="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/fixtures"
HB=portal/src/pages/SecurityAnalysis/components/HeaderBrief.tsx
TP=portal/src/pages/SecurityAnalysis/components/TimelinePanel.tsx
if [ ! -f "$TP" ] || ! grep -q "TimelinePanel" "$HB"; then
  echo "NOT_EXERCISED: $TP absent or not mounted in $HB -- this check needs the mount"; exit 1
fi
echo "mount: $(grep -c "TimelinePanel" "$HB") TimelinePanel reference(s) in $HB"
T="$(mktemp)"; trap 'rm -f "$T"' EXIT
( cd portal && timeout 110 node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs \
    --fixture "$FX/served_fixture.1299_HK_Equity.json" --rich "$FX/1299_HK_Equity.rich.md" ) > "$T" 2>&1; rc=$?
grep -E "^(FIGURES|CITES|ABSENCES|CASES) " "$T"
grep -m1 -E "Error|Cannot find" "$T"
n=$(grep -cE "^(FIGURES|CITES|ABSENCES|CASES) .* missing=0 " "$T")
echo "harness rc=$rc; sets with missing=0: $n of 4"
[ "$rc" = "0" ] && [ "$n" = "4" ] && { echo "LOADS AND COMPARES WITH THE MOUNT: YES"; exit 0; }
echo "LOADS AND COMPARES WITH THE MOUNT: NO"; exit 1
