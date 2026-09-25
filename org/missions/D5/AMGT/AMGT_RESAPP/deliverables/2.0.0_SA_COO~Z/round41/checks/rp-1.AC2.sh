#!/usr/bin/env bash
# AMGT_RESAPP round 41, AMGT-rp-1 AC2 -- THE INSTRUMENT CONTROL: the table's BA_US_Equity row EQUALS a fresh served read by
# round 40's own check (ro-7.AC2.sh: capture the deployed function, compare with exportCompare.harness.cjs --fixture --rich).
# 15 counts compared (three sets x page/rich/same/missing/extra). usage: bash <this>   (from the repo root)
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
TSV=org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/fwd30_population.tsv
[ -f "$TSV" ] || { echo "FAIL: no table"; exit 1; }
FRESH=$(bash org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round40/checks/ro-7.AC2.sh 2>&1)
python - "$TSV" <<PYEOF
import re, sys
fresh = """$FRESH"""
row = None
lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
head = lines[0].split("\t")
for ln in lines[1:]:
    d = dict(zip(head, ln.split("\t")))
    if d.get("security_key") == "BA_US_Equity":
        row = d
if row is None:
    print("FAIL: no BA_US_Equity row"); sys.exit(1)
same = total = 0
for label, s in (("FIGURES", "fig"), ("CITES", "cit"), ("ABSENCES", "abs")):
    m = re.search(r"^%s page=(\d+) rich=(\d+) same=(\d+) missing=(\d+) extra=(\d+)" % label, fresh, re.M)
    if not m:
        print("FAIL: the fresh read printed no %s line" % label); sys.exit(1)
    for c, v in zip(("page", "rich", "same", "missing", "extra"), m.groups()):
        total += 1
        same += row[s + "_" + c] == v
        if row[s + "_" + c] != v:
            print("  differs %s_%s: table %s, fresh %s" % (s, c, row[s + "_" + c], v))
print("BA_US_Equity row EQUALS a fresh served read: %d of %d counts" % (same, total))
sys.exit(0 if same == total == 15 else 1)
PYEOF
