#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-7 AC2 -- FWD-30 ON THE SERVED PLANE with extras GRADED: the deployed function's own
# responses, the page rendered from them (--fixture) against the served rich body (--rich), read EXPORT-COMPARE OK.
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T=$(bash org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/checks/ro-7.served.sh | tail -1); [ -d "$T" ] || { echo "no capture"; exit 1; }
cd portal && node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --fixture "$T/served/served_fixture.BA_US_Equity.json" --rich "$T/served/BA_US_Equity.rich.md" > "$T/cmp.txt" 2>&1; rc=$?
grep -E '^(FIGURES|CITES|ABSENCES|PAGE ABSENCE|EXPORT)' "$T/cmp.txt"; rm -rf "$T"
echo "served-plane export compare rc=$rc"; [ "$rc" -eq 0 ]
