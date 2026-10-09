"""ADVI_FIRMBKTS round 1 close: the issuer's real run of FWD-1 (2.0.0_SA_COO~F1).

Compares READING_A.json and READING_B.json per arm (canonical = the address() locations, legacy = the same objects'
legacy keys), using the arm map in mapping.json that neither reader saw. For each field (system, firm, tier) a location
AGREES when both readers give the same answer after lowercasing and dropping non-alphanumerics, and that answer is not
'unknown'. Prints every count with its denominator, and writes the contents pairs to --pairs for the issuer to read.
"""
import argparse
import json
import os
import re
import subprocess

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
FIELDS = ("system", "firm", "tier")


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
    ap.add_argument("--pairs")
    a = ap.parse_args()
    root = _root(a.root)

    def load(name):
        with open(os.path.join(root, DELIV, name), encoding="utf-8") as fh:
            return json.load(fh)

    mapping = load("mapping.json")
    locs = {e["id"]: e["location"] for e in load("reading_list.json")["locations"]}
    ra = {x["id"]: x for x in load("READING_A.json")["answers"]}
    rb = {x["id"]: x for x in load("READING_B.json")["answers"]}
    arm = {}
    for r in mapping["rows"]:
        ids = r.get("reading_ids") or {}
        if ids:
            arm[ids["canonical"]] = "canonical"
            arm[ids["legacy"]] = "legacy"
    pairs = []
    print("readers: A=%s B=%s; reading list=%d; arm map=%d" % (
        load("READING_A.json").get("reader"), load("READING_B.json").get("reader"), len(locs), len(arm)))
    for name in ("canonical", "legacy"):
        ids = sorted(i for i, v in arm.items() if v == name)
        n = len(ids)
        line = ["ARM %-9s n=%d" % (name, n)]
        for f in FIELDS:
            agree = sum(1 for i in ids if _norm(ra[i][f]) == _norm(rb[i][f]) and _norm(ra[i][f]) != "unknown")
            unk = sum(1 for i in ids if "unknown" in (_norm(ra[i][f]), _norm(rb[i][f])))
            line.append("%s agree %d of %d (an unknown in %d)" % (f, agree, n, unk))
        allf = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(rb[i][f]) != "unknown" for f in FIELDS))
        line.append("all three agree %d of %d" % (allf, n))
        print(" | ".join(line))
        for i in ids:
            pairs.append({"arm": name, "location": locs[i], "A": ra[i], "B": rb[i]})
    if a.pairs:
        with open(a.pairs, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(pairs, fh, indent=1, ensure_ascii=True)
        print("pairs written: %d to %s" % (len(pairs), a.pairs))


if __name__ == "__main__":
    main()
