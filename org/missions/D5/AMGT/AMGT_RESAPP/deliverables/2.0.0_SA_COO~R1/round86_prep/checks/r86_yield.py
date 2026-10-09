"""AMGT_RESAPP round-86 PREP -- the fresh-draw yield (row AMGT_RESAPP-D1-W338-S1).

  python r86_yield.py --crit AC1 --draft <drafting JSON> [--floor N]

Grades a drafting document (the stored draft, or an offline one written with no store write) for NU_US_Equity:
    Y1 served sentences >= the floor (default 38: the stored NU draft repaired in place in round 85, jj-2);
    Y2 every served sentence's text is verbatim in at least one passage it cites (the pipeline's own gate,
       lib/research/drafting/verbatim.check_against_sources, run on the sentence TEXT as the span -- a sentence
       that is the filing's own sentence passes, a paraphrase does not);
    Y3 0 served sentences restated or glued (r85_sentences' own rules).
Verdict: R86 YIELD AC1: YES|NO (exit 0|1). At the base on round 85's offline NU draft (jj-1, a fresh draw):
NO -- Y1 22 of 38; Y2 0 of 22 (today's gate passes a sentence on one 8-token verbatim RUN, so a served sentence is a
paraphrase carrying a run, never wholly the filing's text); Y3 PASS.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R85 = os.path.normpath(os.path.join(HERE, "..", "..", "round85_prep", "checks"))


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--draft", required=True)
    ap.add_argument("--floor", type=int, default=38)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    for p in (root, R85):
        if p and p not in sys.path:
            sys.path.insert(0, p)
    import r85_sentences as rs
    from lib.research.drafting import verbatim

    doc = json.load(open(a.draft, encoding="utf-8"))
    passages = {r.get("id"): r.get("passage") or "" for r in doc.get("evidence_records") or []}
    served = [s for sec in doc.get("sections") or [] for s in sec.get("sentences") or []]
    held = doc.get("held_no_span") or []
    print("   served %d, held %d, denominators %s" % (len(served), len(held), doc.get("denominators")))
    y1 = say(len(served) >= a.floor, "Y1 served sentences %d, floor %d" % (len(served), a.floor))
    bad = [i for i, s in enumerate(served)
           if verbatim.check_against_sources([s.get("text") or ""], [passages.get(e, "") for e in s.get("evidence") or []]) != "PASS"]
    y2 = say(bool(served) and not bad, "Y2 served sentences verbatim in a cited passage: %d of %d" % (len(served) - len(bad), len(served)))
    texts = [s.get("text") or "" for s in served]
    rest = sum(1 for t in texts if rs.restated(t))
    glued = sum(1 for t in texts if rs.GLUE_RE.search(t))
    y3 = say(rest == 0 and glued == 0, "Y3 restated %d of %d, glued %d of %d" % (rest, len(texts), glued, len(texts)))
    ok = y1 and y2 and y3
    print("R86 YIELD AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
