#!/usr/bin/env bash
# AMGT_RESAPP round 43, AMGT-rr-3 AC2 -- FWD-30 on the SERVED plane over the LIVE research library (the population Andrew named,
# read fresh with its read time printed), CASES axis graded (R-8): every name reads EXPORT-COMPARE OK and every case value the page
# shows reaches the export. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round43/checks/sweep.py \
  --served --live --require-cases --cache "$T/cache" --out "$T/served.tsv" > "$T/sweep.log" 2>&1; rc=$?
head -1 "$T/sweep.log"
grep -v ' OK $' "$T/sweep.log" | grep -E '^[0-9]+/[0-9]+ ' | head -20
tail -2 "$T/sweep.log"
exit $rc
