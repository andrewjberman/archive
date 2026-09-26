#!/usr/bin/env bash
# AMGT_RESAPP round 45, AMGT-tt-1 AC1 -- the export carries every absence the page shows, as the page states it, on every name.
# Over round 45's pinned population (95 folders, the capture C:/tmp/amgt-r44-close read at 2026-09-26T13:29:01Z), the export is
# REBUILT in process from this tree and compared with the harness; the line counts names whose ABSENCES read missing=0, and names
# reading EXPORT-COMPARE OK, with the CASES axis graded. usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
CK=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
PYTHONPATH="$ROOT" python $CK/sweep.py --require-cases --folders-file $CK/population_at_cut.txt --cache C:/tmp/amgt-r44-close \
  --out "$T/local.tsv" > "$T/sweep.log" 2>&1; rc=$?
head -1 "$T/sweep.log"; tail -2 "$T/sweep.log"
python - "$T/local.tsv" "$rc" <<'PY'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8"), delimiter="\t"))
n = len(rows)
same = sum(1 for r in rows if r.get("abs_missing") == "0")
ok = sum(1 for r in rows if r.get("verdict") == "OK")
print("absences missing=0 on %d of %d names; EXPORT-COMPARE OK on %d of %d; sweep rc=%s" % (same, n, ok, n, sys.argv[2]))
for r in [r for r in rows if r.get("abs_missing") != "0"][:6]:
    print("  abs_missing=%s %s" % (r.get("abs_missing"), r.get("security_key")))
sys.exit(0 if n == 95 and same == n and ok == n and sys.argv[2] == "0" else 1)
PY
