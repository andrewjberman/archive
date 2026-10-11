"""ADVI_FIRMBKTS round 3 close: the issuer's real run of FWD-1's contents and independence clauses (2.0.0_SA_COO~B1).

Compares ANSWERS_A.json and ANSWERS_B.json (in the readers' folder) per arm, using READING_KEY.json, which neither
reader saw. A field AGREES when both answers are equal after lowercasing and dropping non-alphanumerics and the
answer is not 'unknown'. Fields: system, firm, tier, table (the contents clause at the table grain). The free-text
`contents` pairs are written to --pairs for the issuer (and the CVO) to read; they are not graded here.
Prints every count with its denominator.
"""
import argparse
import json
import os
import re
import subprocess

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
FIELDS = ("system", "firm", "tier", "table")


def _root(arg):
    if arg:
        return arg
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip()


def _norm(v):
    return re.sub(r"[^a-z0-9]", "", str(v).lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--dir-a", required=True)
    ap.add_argument("--dir-b", required=True)
    ap.add_argument("--pairs")
    a = ap.parse_args()
    root = _root(a.root)

    def load(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    key = load(os.path.join(root, DELIV, "2.0.0_SA_COO~B1", "round3", "READING_KEY.json"))
    locs = {e["id"]: e["location"] for e in load(os.path.join(a.dir_a, "LOCATIONS.json"))["locations"]}
    da, db = load(os.path.join(a.dir_a, "ANSWERS_A.json")), load(os.path.join(a.dir_b, "ANSWERS_B.json"))
    ra = {x["id"]: x for x in da["answers"]}
    rb = {x["id"]: x for x in db["answers"]}
    pairs = []
    print("readers: A=%s B=%s; locations=%d; arm map=%d" % (da.get("reader"), db.get("reader"), len(locs), len(key)))
    print("listing A: %s | listing B: %s" % (sorted(os.listdir(a.dir_a)), sorted(os.listdir(a.dir_b))))
    for name in ("canonical", "legacy"):
        ids = sorted(i for i, v in key.items() if v["arm"] == name)
        n = len(ids)
        line = ["ARM %-9s n=%d" % (name, n)]
        for f in FIELDS:
            agree = sum(1 for i in ids if _norm(ra[i][f]) == _norm(rb[i][f]) and _norm(ra[i][f]) != "unknown")
            unk = sum(1 for i in ids if "unknown" in (_norm(ra[i][f]), _norm(rb[i][f])))
            line.append("%s agree %d of %d (an unknown in %d)" % (f, agree, n, unk))
        allf = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(rb[i][f]) != "unknown" for f in FIELDS))
        line.append("all four agree %d of %d" % (allf, n))
        print(" | ".join(line))
        if name == "canonical":
            right = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(rb[i][f]) == _norm(key[i]["truth"][f])
                                              for f in FIELDS))
            print("  canonical arm: both readers equal the table's own dest on all four fields at %d of %d" % (right, n))
        for i in ids:
            pairs.append({"arm": name, "location": locs[i], "A": ra[i], "B": rb[i]})
    if a.pairs:
        with open(a.pairs, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(pairs, fh, indent=1, ensure_ascii=True)
        print("pairs written: %d to %s" % (len(pairs), a.pairs))


if __name__ == "__main__":
    main()
