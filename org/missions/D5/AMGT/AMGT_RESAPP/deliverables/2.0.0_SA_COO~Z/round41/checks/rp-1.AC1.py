"""AMGT_RESAPP round 41, AMGT-rp-1 AC1 -- the FWD-30 population table has ONE row per coverage-list folder.
Reads the worker's TSV and the coverage list; prints the denominators; exit 0 only on the table's shape.
usage: python <this>   (from the repo root)"""
import json
import sys
from pathlib import Path

TSV = Path("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/fwd30_population.tsv")
UNIVERSE = Path("org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~4/universe.json")
SETS = ("fig", "cit", "abs")
COUNTS = [s + "_" + c for s in SETS for c in ("page", "rich", "same", "missing", "extra")] + ["abs_covered"]
HEADER = ["folder", "security_key"] + COUNTS + ["verdict", "reason"]
VERDICTS = ("OK", "NOT_OK", "CAPTURE_FAILED")

if not TSV.exists():
    print("FAIL: no table at %s" % TSV)
    sys.exit(1)
folders = [n["folder"] for n in json.load(open(UNIVERSE, encoding="utf-8"))["names"]]
lines = TSV.read_text(encoding="utf-8").splitlines()
head, rows = lines[0].split("\t"), [ln.split("\t") for ln in lines[1:] if ln.strip()]
bad = []
if head != HEADER:
    bad.append("header differs: %r" % head)
by_folder = {}
for r in rows:
    if len(r) != len(HEADER):
        bad.append("row with %d fields: %r" % (len(r), r[:2]))
        continue
    d = dict(zip(HEADER, r))
    by_folder.setdefault(d["folder"], []).append(d)
    if d["verdict"] not in VERDICTS:
        bad.append("%s: verdict %r" % (d["folder"], d["verdict"]))
    elif d["verdict"] == "CAPTURE_FAILED":
        if not d["reason"].strip():
            bad.append("%s: CAPTURE_FAILED with no reason" % d["folder"])
    elif not all(d[c].isdigit() for c in COUNTS):
        bad.append("%s: a count is not a whole number" % d["folder"])
missing = [f for f in folders if f not in by_folder]
extra = [f for f in by_folder if f not in folders]
dup = [f for f, v in by_folder.items() if len(v) > 1]
keys = [v[0]["security_key"] for v in by_folder.values()]
n = {v: sum(1 for x in by_folder.values() if x[0]["verdict"] == v) for v in VERDICTS}
print("rows %d of %d folders; missing %d; extra %d; duplicated %d; distinct keys %d" % (
    len(rows), len(folders), len(missing), len(extra), len(dup), len(set(keys))))
print("verdicts: OK %d, NOT_OK %d, CAPTURE_FAILED %d" % (n["OK"], n["NOT_OK"], n["CAPTURE_FAILED"]))
for b in bad[:20]:
    print("  " + b)
ok = not bad and not missing and not extra and not dup and len(rows) == len(folders)
print("TABLE SHAPE %s" % ("OK" if ok else "NOT OK"))
sys.exit(0 if ok else 1)
