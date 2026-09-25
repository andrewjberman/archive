#!/usr/bin/env bash
# AMGT_RESAPP round 42, AMGT-rq-2 AC2 -- FWD-30 on the SERVED plane across the 89-name snapshot (universe.json, read
# 2026-09-10T23:18Z; ABSENCE axis on 89, FIGURE axis on the 31 with figures): a FRESH capture of every name's page routes and
# its DEPLOYED rich body reads EXPORT-COMPARE OK for every name. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round42/checks/rq-1.local_sweep.py \
  --served --cache "$T/cache" --out "$T/served.tsv" > "$T/sweep.log" 2>&1; rc=$?
grep -v ' OK $' "$T/sweep.log" | grep -E '^[0-9]+/89 ' | head -20
tail -1 "$T/sweep.log"
exit $rc
