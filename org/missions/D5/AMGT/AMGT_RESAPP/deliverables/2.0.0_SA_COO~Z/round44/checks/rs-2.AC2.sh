#!/usr/bin/env bash
# AMGT_RESAPP round 44, AMGT-rs-2 AC2 -- FWD-30 on the SERVED plane over the LIVE research library, read fresh with its read time printed
# (C-BACKFILL-DENOMINATOR-IS-THE-RESEARCH-FOLDER), CASES axis graded: every name reads EXPORT-COMPARE OK. usage: bash <this>
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round44/checks/sweep.py \
  --served --live --require-cases --cache "$T/cache" --out "$T/served.tsv" > "$T/sweep.log" 2>&1; rc=$?
head -1 "$T/sweep.log"; grep -v ' OK $' "$T/sweep.log" | grep -E '^[0-9]+/[0-9]+ ' | head -20
tail -2 "$T/sweep.log"
exit $rc
