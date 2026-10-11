"""ADVI_FIRMBKTS round 2 check for cells FB-e-2 and FB-e-3 (the two blind readers), issuer 2.0.0_SA_COO~B1.

--reader A grades ANSWERS_A.json, --reader B grades ANSWERS_B.json, each against LOCATIONS.json (2 arms).
Both files live in the readers' own folder. Agreement between the readers is NOT graded here: it is the issuer's
real run at the round close (r2_agree.py). --root points at another tree (the issuer's positive control).
Never edit this file.
"""
import argparse
import json
import os
import subprocess
import sys

BLIND = "org/tier1_exec/2.0.0_SA_COO~B1/round2/blind"
FIELDS = ("system", "firm", "tier", "table", "contents")


def _root(arg):
    if arg:
        return arg
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip()


def arms(root, reader):
    with open(os.path.join(root, BLIND, "LOCATIONS.json"), encoding="utf-8") as fh:
        ids = [e["id"] for e in json.load(fh)["locations"]]
    with open(os.path.join(root, BLIND, "ANSWERS_%s.json" % reader), encoding="utf-8") as fh:
        doc = json.load(fh)
    answers = doc.get("answers") or []
    got = [a.get("id") for a in answers]
    dup = len(got) - len(set(got))
    missing = set(ids) - set(got)
    extra = set(got) - set(ids)
    print("  locations=%d answers=%d duplicates=%d unanswered=%d unknown ids=%d"
          % (len(ids), len(answers), dup, len(missing), len(extra)))
    r1 = bool(ids) and not dup and not missing and not extra and str(doc.get("reader", "")).startswith("0.9.0_WK_")
    blank = [a.get("id") for a in answers
             if not all(isinstance(a.get(f), str) and a.get(f).strip() for f in FIELDS)]
    print("  answers with a blank field: %d" % len(blank))
    return [("R1 every location id is answered exactly once, by a named worker serial", r1),
            ("R2 every answer names system, firm, tier, table and contents (firm and system may read 'unknown')",
             not blank and bool(answers))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", choices=("A", "B"), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    try:
        res = arms(_root(a.root), a.reader)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: ANSWERS_%s.json or LOCATIONS.json (%s)" % (a.reader, type(e).__name__))
        res = [("ANSWERS_%s.json and LOCATIONS.json present" % a.reader, False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 2 READER %s: %d of 2 arms" % (a.reader, n))
    sys.exit(0 if n == 2 else 1)


if __name__ == "__main__":
    main()
