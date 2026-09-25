#!/usr/bin/env bash
# AMGT_RESAPP round 40, AMGT-ro-1 AC1 -- FWD-30 on the LANDED plane with extras GRADED: the rich export built from the
# landed fixture through the adapter's own dispatch (rm-4's handler_rich_to_file.py, copied to a temp dir so it writes
# nowhere in the repo) carries NOTHING the page does not show. usage: bash <this>   (from the repo root; no server)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/checks/ro-1.rich_handler.py "$T/handler_rich_to_file.py"  # ~143's handler + the read_description stub (row Z-S271)
PYTHONPATH="$ROOT" python "$T/handler_rich_to_file.py" > "$T/build.log" 2>&1 || { cat "$T/build.log"; echo "rich build failed"; exit 1; }
RICH="$T/served/BA_US_Equity.md"; [ -s "$RICH" ] || { echo "no rich body at $RICH"; exit 1; }
cd portal && node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --rich "$RICH" > "$T/cmp.txt" 2>&1; rc=$?
grep -E '^(FIGURES|CITES|ABSENCES|PAGE ABSENCE|EXPORT)' "$T/cmp.txt"
fx=$(grep -o '^FIGURES .* extra=[0-9]*' "$T/cmp.txt" | grep -o 'extra=[0-9]*$'); ax=$(grep -o '^ABSENCES .* extra=[0-9]*' "$T/cmp.txt" | grep -o 'extra=[0-9]*$')
echo "harness rc=$rc; figures $fx; absences $ax"
[ "$rc" -eq 0 ] && [ "$fx" = "extra=0" ] && grep -q '^EXPORT-COMPARE OK' "$T/cmp.txt"
