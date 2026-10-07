"""AMGT_RESAPP round 78 -- AMGT-bb-10: ONE served marker for a name outside coverage (round-77 enrichment item 7; row
AMGT_RESAPP-Z-S364; DSGN_AMGTV1 round-47 close, "No coverage marker is served").

  --crit AC1|AC2 --where local

AC1 (build): `lib.research.api.coverage_marker.marker(security_key, covered_keys)` on planted lists:
    C1 a key in the covered list reads status "covered", covered True, no sentence;
    C2 a key outside it reads status "outside_coverage", covered False and ONE plain sentence; an empty key reads the same;
    C3 `covered_keys` None (the list could not be read) reads status "not_known", covered None and a plain sentence,
       never "outside_coverage";
    C4 every answer carries exactly the keys status, covered, sentence, covered_names; no sentence carries a system word.
AC2 (seam, the real neighbour): against the real covered list (`covered_security_keys()`) and the real pool list
    (`crosswalk.load_crosswalk()`): every covered name reads "covered" (N of N), MSFT_US_Equity and ABNB_US_Equity read
    "outside_coverage" with the sentence, AMD_US_Equity reads "covered", and the pool's names split into the two
    statuses with nothing left over (covered + outside = pool names, all three counts printed).
Verdict: R78 BB10 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter

BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze")
FIELDS = {"status", "covered", "sentence", "covered_names"}
OUTSIDE = ("MSFT_US_Equity", "ABNB_US_Equity")
CONTROL = "AMD_US_Equity"


def _plain(text):
    return isinstance(text, str) and bool(text.strip()) and not [w for w in BANNED if w in text.lower()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    try:
        from lib.research.api import coverage_marker
    except ImportError as err:
        clause("C0 lib.research.api.coverage_marker imports", False, str(err))
        return verdict(a, ok)
    fn = getattr(coverage_marker, "marker", None)
    if not callable(fn):
        clause("C0 coverage_marker.marker exists", False, "absent")
        return verdict(a, ok)

    if a.crit == "AC1":
        held = ["AMD_US_Equity", "BA_US_Equity", "BP/_LN_Equity"]
        inside = fn("BA_US_Equity", held)
        clause("C1 a covered name reads covered, with no sentence",
               inside.get("status") == "covered" and inside.get("covered") is True and inside.get("sentence") is None
               and inside.get("covered_names") == 3, repr(inside))
        out, empty = fn("MSFT_US_Equity", held), fn(None, held)
        print(f"   sentence: {out.get('sentence')!r}")
        clause("C2 a name outside the list says so in one plain sentence",
               all(r.get("status") == "outside_coverage" and r.get("covered") is False and _plain(r.get("sentence"))
                   for r in (out, empty)) and out.get("sentence") == empty.get("sentence"), repr(out.get("status")))
        unread = fn("MSFT_US_Equity", None)
        clause("C3 an unread list reads not known, never outside coverage",
               unread.get("status") == "not_known" and unread.get("covered") is None and _plain(unread.get("sentence"))
               and unread.get("covered_names") is None and unread.get("sentence") != out.get("sentence"), repr(unread))
        clause("C4 every answer carries the four fields and no system word",
               all(set(r) == FIELDS for r in (inside, out, empty, unread)))
        return verdict(a, ok)

    from lib.research.coverage.covered_universe import covered_security_keys
    from lib.research.identity import crosswalk

    covered = sorted(covered_security_keys())
    pool = sorted({r["security_key"] for r in crosswalk.load_crosswalk()[0]["records"] if r.get("security_key")})
    wrong = [k for k in covered if fn(k, covered).get("status") != "covered"]
    clause("C1 every covered name reads covered", covered and not wrong, f"{len(covered) - len(wrong)} of {len(covered)}")
    reads = {k: fn(k, covered) for k in OUTSIDE}
    for k, r in reads.items():
        print(f"   {k}: {r.get('status')!r} {r.get('sentence')!r}")
    clause("C2 MSFT US and ABNB US read outside coverage with the sentence; AMD US reads covered",
           all(r.get("status") == "outside_coverage" and _plain(r.get("sentence")) for r in reads.values())
           and fn(CONTROL, covered).get("status") == "covered")
    split = Counter(fn(k, covered).get("status") for k in pool)
    print(f"   pool names {len(pool)}; by status {dict(split)}; covered list {len(covered)}")
    clause("C3 the pool's names split into the two statuses with nothing left over",
           pool and set(split) <= {"covered", "outside_coverage"} and split["covered"] + split["outside_coverage"] == len(pool)
           and split["outside_coverage"] >= 2, f"{split['covered']} + {split['outside_coverage']} = {len(pool)}")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB10 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
