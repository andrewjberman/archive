"""ADVI_FIRMBKTS round 3 check for cells FB-f-3 and FB-f-4 (the two blind readers), issuer 2.0.0_SA_COO~B1.

--reader A|B --dir <the reader's own directory> grades ANSWERS_<reader>.json against LOCATIONS.json in that directory
(3 arms). Agreement between the readers is NOT graded here: it is the issuer's real run (r3_agree.py).
Arm R3 is the independence-by-construction arm: the directory's listing is printed and must hold ONLY LOCATIONS.json
and the reader's one answers file, and LOCATIONS.json must be byte-identical to the list the issuer cut (sha256).
Never edit this file.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
SHA = DELIV + "/2.0.0_SA_COO~B1/round3/LOCATIONS.sha256"
FIELDS = ("system", "firm", "tier", "table", "contents")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", choices=("A", "B"), required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = a.root or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    res = []
    try:
        with open(os.path.join(a.dir, "LOCATIONS.json"), "rb") as fh:
            raw = fh.read()
        ids = [e["id"] for e in json.loads(raw.decode("ascii"))["locations"]]
        with open(os.path.join(a.dir, "ANSWERS_%s.json" % a.reader), encoding="utf-8") as fh:
            doc = json.load(fh)
        answers = doc.get("answers") or []
        got = [x.get("id") for x in answers]
        dup = len(got) - len(set(got))
        missing = set(ids) - set(got)
        extra = set(got) - set(ids)
        print("  locations=%d answers=%d duplicates=%d unanswered=%d unknown ids=%d"
              % (len(ids), len(answers), dup, len(missing), len(extra)))
        res.append(("R1 every location id is answered exactly once, by a named worker serial",
                    bool(ids) and not dup and not missing and not extra
                    and str(doc.get("reader", "")).startswith("0.9.0_WK_")))
        blank = [x.get("id") for x in answers
                 if not all(isinstance(x.get(f), str) and x.get(f).strip() for f in FIELDS)]
        print("  answers with a blank field: %d" % len(blank))
        res.append(("R2 every answer names system, firm, tier, table and contents (a field may read 'unknown')",
                    not blank and bool(answers)))
        listing = sorted(os.listdir(a.dir))
        print("  DIRECTORY LISTING (%s): %s" % (a.dir, listing))
        with open(os.path.join(root, SHA), encoding="ascii") as fh:
            want = fh.read().strip()
        same = hashlib.sha256(raw).hexdigest() == want
        print("  LOCATIONS.json sha256 equals the issuer's cut: %s" % same)
        res.append(("R3 the directory holds only LOCATIONS.json and ANSWERS_%s.json, and the list is the issuer's "
                    "cut byte for byte" % a.reader,
                    listing == sorted(["LOCATIONS.json", "ANSWERS_%s.json" % a.reader]) and same))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s)" % (a.dir, type(e).__name__))
        res = [("ANSWERS_%s.json and LOCATIONS.json present" % a.reader, False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 READER %s: %d of 3 arms" % (a.reader, n))
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
