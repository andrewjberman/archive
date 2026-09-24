#!/usr/bin/env bash
# AMGT_RESAPP round 39, AMGT-rn-5 AC2 -- FWD-30's field-by-field comparison on the SERVED plane: the export-compare
# harness, pointed at the SERVED fixture (--fixture) and the SERVED rich body (--rich), reads the same figures, the
# same cites and the same absences, and exits 0. usage: bash <this> <served fixture> <served rich .md>  (repo root)
set -u
FIX=${1:?served fixture}; RICH=${2:?served rich body}
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
[ -s "$ROOT/$FIX" ] && [ -s "$ROOT/$RICH" ] || { echo "inputs absent: $FIX / $RICH"; exit 1; }
node src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs --fixture "$ROOT/$FIX" --rich "$ROOT/$RICH" > .scratch.rn5.cmp.txt 2>&1; rc=$?
cat .scratch.rn5.cmp.txt; rm -f .scratch.rn5.cmp.txt
echo "exportCompare --rich on the served plane: rc=$rc"
[ "$rc" -eq 0 ]
