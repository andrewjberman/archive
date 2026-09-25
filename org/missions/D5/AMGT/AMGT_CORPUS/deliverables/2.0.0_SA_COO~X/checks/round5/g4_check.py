"""AMGT_CORPUS round 5 -- the issuer's checker for CRPS-g-4's evidence file (read-only).

  python g4_check.py structure <evidence.json>   -> 'outcomes N of 19 rows_valid V' then VALID/INVALID
  python g4_check.py quotes    <evidence.json>   -> 'fence_quotes_verbatim N of 19'
"""
import json
import os
import re
import sys

PRD = "org/missions/D5/AMGT/AMGT_CORPUS/prd/AMGT_CORPUS_PRD.md"
STATES = {"met", "unmet", "unmeasurable"}


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip()


def load(path):
    if not os.path.exists(path):
        print("MISSING %s" % path)
        sys.exit(1)
    return json.load(open(path, encoding="utf-8"))


def structure(doc):
    rows = doc.get("outcomes") or []
    ids = [r.get("id") for r in rows]
    want = ["FWD-%d" % i for i in range(1, 20)]
    valid = 0
    for r in rows:
        ok = (r.get("id") in want and norm(r.get("fence_quote")) and norm(r.get("instrument"))
              and norm(r.get("output_excerpt")) and r.get("state") in STATES
              and (r.get("state") != "unmeasurable" or norm(r.get("reason"))))
        valid += 1 if ok else 0
    covered = len(set(ids) & set(want))
    print("outcomes %d of 19 rows_valid %d duplicates %d" % (covered, valid, len(ids) - len(set(ids))))
    print("VALID" if covered == 19 and valid == 19 and len(ids) == 19 else "INVALID")


def quotes(doc):
    prd = norm(open(PRD, encoding="utf-8").read())
    rows = doc.get("outcomes") or []
    hit = sum(1 for r in rows if norm(r.get("fence_quote")) and norm(r.get("fence_quote")) in prd)
    print("fence_quotes_verbatim %d of 19" % hit)


if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    doc = load(path)
    structure(doc) if mode == "structure" else quotes(doc)
