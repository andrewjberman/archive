"""AMGT_CORPUS round 13 -- the issuer's checker for CRPS-o-1's evidence file (read-only).

  python o1_check.py structure <evidence.json> -> 'outcomes N of 19 rows_valid V duplicates D not_met M acted A owned O'
                                                  then VALID/INVALID
  python o1_check.py quotes    <evidence.json> -> 'fence_quotes_verbatim N of 19'

A row is valid when it carries id, fence_quote, instrument, output_excerpt, denominator, and a state in met / unmet /
unmeasurable (unmeasurable also carries a reason). A row NOT met also carries exercising_act (never a wait: the word
"wait" refuses it) and an owner from the three the round-12 analysis names.
"""
import json
import os
import re
import sys

PRD = "org/missions/D5/AMGT/AMGT_CORPUS/prd/AMGT_CORPUS_PRD.md"
STATES = {"met", "unmet", "unmeasurable"}
OWNERS = {"AMGT_CORPUS", "AMGT_RESAPP", "DSGN_AMGTV1"}


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip()


def load(path):
    if not os.path.exists(path):
        print("MISSING %s" % path)
        sys.exit(1)
    return json.load(open(path, encoding="utf-8"))


def row_ok(r, want):
    base = (r.get("id") in want and norm(r.get("fence_quote")) and norm(r.get("instrument"))
            and norm(r.get("output_excerpt")) and norm(r.get("denominator")) and r.get("state") in STATES
            and (r.get("state") != "unmeasurable" or norm(r.get("reason"))))
    if not base:
        return False
    if r.get("state") == "met":
        return True
    act = norm(r.get("exercising_act"))
    return bool(act) and not re.search(r"\bwait", act, re.I) and r.get("owner") in OWNERS


def structure(doc):
    rows = doc.get("outcomes") or []
    ids = [r.get("id") for r in rows]
    want = ["FWD-%d" % i for i in range(1, 20)]
    valid = sum(1 for r in rows if row_ok(r, want))
    not_met = [r for r in rows if r.get("state") != "met"]
    acted = sum(1 for r in not_met if norm(r.get("exercising_act")) and not re.search(r"\bwait", r.get("exercising_act") or "", re.I))
    owned = sum(1 for r in not_met if r.get("owner") in OWNERS)
    covered = len(set(ids) & set(want))
    print("outcomes %d of 19 rows_valid %d duplicates %d not_met %d acted %d owned %d"
          % (covered, valid, len(ids) - len(set(ids)), len(not_met), acted, owned))
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
