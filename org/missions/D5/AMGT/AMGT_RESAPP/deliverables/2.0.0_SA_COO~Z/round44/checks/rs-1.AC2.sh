#!/usr/bin/env bash
# AMGT_RESAPP round 44, AMGT-rs-1 AC2 (BOUND) -- the page and the export still say the same thing everywhere: over round 44's fixed
# capture of the LIVE research library (95 folders, read_at 2026-09-26T03:55:02Z), the REBUILT export reads EXPORT-COMPARE OK for every
# name with the CASES axis graded. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round44/checks/sweep.py \
  --require-cases --live --cache C:/tmp/amgt-r43-live95 --out "$T/local.tsv" > "$T/sweep.log" 2>&1; rc=$?
head -1 "$T/sweep.log"; grep -v ' OK $' "$T/sweep.log" | grep -E '^[0-9]+/[0-9]+ ' | head -20
tail -2 "$T/sweep.log"
exit $rc
