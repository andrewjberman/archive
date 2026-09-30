#!/usr/bin/env bash
# AMGT_RESAPP round 48, AMGT-ww-4 AC2 -- the bound: FWD-30 does not regress. The rich export is REBUILT from THIS tree's
# render_pack over the deployed function's captured inputs and compared by DSGN_AMGTV1's exportCompare harness (round 45 sweep over the LIVE library,
# local mode, CASES graded) on three names. Must read OK on 3 of 3 before and after ww-4.
# usage: bash <this>   (from the repo root of the worktree under test; reads the deployed function read-only)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
CK=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" timeout 115 python $CK/sweep.py --live --require-cases --only AMD_US_Equity,GOOGL_US_Equity,1299_HK_Equity \
  --cache "$T/cache" --out "$T/local.tsv" > "$T/sweep.log" 2>&1; rc=$?
tail -2 "$T/sweep.log"
python - "$T/local.tsv" "$rc" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t"))
ok = sum(1 for r in rows if r.get("verdict") == "OK")
print("rebuilt export vs page: EXPORT-COMPARE OK on %d of %d; sweep rc=%s" % (ok, len(rows), sys.argv[2]))
sys.exit(0 if len(rows) == 3 and ok == 3 and sys.argv[2] == "0" else 1)
PY
