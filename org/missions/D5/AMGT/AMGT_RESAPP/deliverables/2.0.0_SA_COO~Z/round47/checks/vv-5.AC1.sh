#!/usr/bin/env bash
# AMGT_RESAPP round 47, AMGT-vv-5 AC1 -- FWD-30's harness reads DSGN_AMGTV1's page: it loads (HeroGraphic) and it sees the header
# CARDS' figures, so the one served fixture (1299_HK_Equity) reads EXACT parity on all four sets.
# At the cut on portal DEV 5fac7a37: MODULE_NOT_FOUND '@/ui/components/graphic/HeroGraphic' (ThesisCards.tsx:29); with that
# stubbed, FIGURES page=176 rich=182 extra=6 -- the six header|<mnemonic> figures HeaderCards.tsx shows under
# data-card-figure-mnemonic / data-card-figure-state="SERVED", which pageFigures() never reads (it reads data-stat-tile only).
# usage: bash <this>   (from the repo root of the worktree under test)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
FX="$ROOT/org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/checks/fixtures"
T="$(mktemp)"; trap 'rm -f "$T"' EXIT
( cd portal && timeout 110 node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs \
    --fixture "$FX/served_fixture.1299_HK_Equity.json" --rich "$FX/1299_HK_Equity.rich.md" ) > "$T" 2>&1; rc=$?
grep -E "^(FIGURES|CITES|ABSENCES|CASES) " "$T"
grep -m1 -E "Cannot find module|^Error" "$T"
n=$(grep -cE "^(FIGURES|CITES|ABSENCES|CASES) .* missing=0 extra=0$" "$T")
fig=$(grep -E "^FIGURES " "$T")
echo "harness rc=$rc; sets exact (missing=0 extra=0): $n of 4"
case "$fig" in *"page=182 "*) ;; *) echo "FIGURES page count is not the export's 182: $fig";; esac
[ "$rc" = "0" ] && [ "$n" = "4" ] && case "$fig" in *"page=182 "*) true;; *) false;; esac && { echo "FWD-30 HARNESS READS THE REDESIGNED PAGE: YES"; exit 0; }
echo "FWD-30 HARNESS READS THE REDESIGNED PAGE: NO"; exit 1
