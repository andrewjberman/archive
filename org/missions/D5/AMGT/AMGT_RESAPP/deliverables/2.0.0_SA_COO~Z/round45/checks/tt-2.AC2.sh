#!/usr/bin/env bash
# AMGT_RESAPP round 45, AMGT-tt-2 AC2 -- FWD-30 on the SERVED plane over the LIVE research library, read fresh with its read time
# printed (C-BACKFILL-DENOMINATOR-IS-THE-RESEARCH-FOLDER), CASES graded: every name reads EXPORT-COMPARE OK AND its ABSENCES read
# missing=0. usage: bash <this>
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
CK=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python $CK/sweep.py --served --live --require-cases --cache "$T/cache" --out "$T/served.tsv" > "$T/sweep.log" 2>&1; rc=$?
head -1 "$T/sweep.log"; tail -2 "$T/sweep.log"
python - "$T/served.tsv" "$rc" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t"))
n = len(rows)
same = sum(1 for r in rows if r.get("abs_missing") == "0")
ok = sum(1 for r in rows if r.get("verdict") == "OK")
print("served: absences missing=0 on %d of %d names; EXPORT-COMPARE OK on %d of %d; sweep rc=%s" % (same, n, ok, n, sys.argv[2]))
sys.exit(0 if n and same == n and ok == n and sys.argv[2] == "0" else 1)
PY
