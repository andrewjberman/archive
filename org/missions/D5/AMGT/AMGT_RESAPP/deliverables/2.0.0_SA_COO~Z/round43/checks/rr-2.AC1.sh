#!/usr/bin/env bash
# AMGT_RESAPP round 43, AMGT-rr-2 AC1 -- FWD-30 with the CASES axis graded (R-8): over the 89-name snapshot (universe.json,
# 2026-09-10T23:18Z) at round 43's capture (C:/tmp/amgt-r43-cache, outside the repo), the export REBUILT from this tree reads
# EXPORT-COMPARE OK for every name AND the harness grades the Model Cases line on every name, with every case value the page shows
# reaching the export and none extra. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round43/checks/sweep.py \
  --require-cases --cache C:/tmp/amgt-r43-cache --out "$T/local.tsv" > "$T/sweep.log" 2>&1; rc=$?
grep -v ' OK $' "$T/sweep.log" | grep -E '^[0-9]+/89 ' | head -20
tail -2 "$T/sweep.log"
exit $rc
