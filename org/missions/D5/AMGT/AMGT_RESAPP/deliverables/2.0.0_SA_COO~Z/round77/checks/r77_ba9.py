"""AMGT_RESAPP round 77 -- AMGT-ba-9: the name-search resolver (row Z-S228; CTO adjudication @4a89bef967, section E).

  --crit AC1|AC2 --where local

AC1 (build): `lib.research.api.name_search.resolve_query(q)` over the crosswalk:
    C1 an exact key or stored form passes through: status "exact" and the security key ("992 HK" and "992_HK_Equity"
       both read 992_HK_Equity);
    C2 a company name returns candidates: "Lenovo" and "lenovo" read status "candidates" and list 992_HK_Equity, each
       candidate carrying a non-empty security_key, name and ticker;
    C3 no match reads status "none", candidates [] and a plain reason; an empty query reads the same;
    C4 the denominator: every keyed crosswalk record's own security key passes through as "exact" (N of N printed).
AC2 (build): the plant tests in lib/research/api/tests/test_name_search.py pass.
Verdict: R77 BA9 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

TEST = "lib/research/api/tests/test_name_search.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC2":
        if not os.path.isfile(TEST):
            clause("C1 the plant test file exists", False, TEST)
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST], capture_output=True,
                           timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 every plant case passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    try:
        from lib.research.api import name_search
    except ImportError as err:
        clause("C0 lib.research.api.name_search imports", False, str(err))
        return verdict(a, ok)
    fn = getattr(name_search, "resolve_query", None)
    if not callable(fn):
        clause("C0 name_search.resolve_query exists", False, "absent")
        return verdict(a, ok)
    e1, e2 = fn("992 HK"), fn("992_HK_Equity")
    clause("C1 an exact form passes through",
           all(r.get("status") == "exact" and r.get("security_key") == "992_HK_Equity" for r in (e1, e2)),
           f"{e1.get('status')} {e1.get('security_key')}")
    good = []
    for q in ("Lenovo", "lenovo"):
        r = fn(q)
        cands = r.get("candidates") or []
        good.append(r.get("status") == "candidates" and any(c.get("security_key") == "992_HK_Equity" for c in cands)
                    and all(c.get("security_key") and c.get("name") and c.get("ticker") for c in cands))
        print(f"   {q!r}: status {r.get('status')} candidates {[c.get('security_key') for c in cands][:5]}")
    clause("C2 a company name returns its candidates", all(good))
    n1, n2 = fn("zzqx no such company 7781"), fn("")
    clause("C3 no match reads a plain reason",
           all(r.get("status") == "none" and (r.get("candidates") or []) == [] and isinstance(r.get("reason"), str)
               and r.get("reason").strip() for r in (n1, n2)), f"{n1.get('status')} {n1.get('reason')!r}")
    from lib.research.identity import crosswalk

    document = crosswalk.load_crosswalk()[0]
    keys = sorted({r["security_key"] for r in document["records"] if r.get("security_key")})
    miss = []
    for k in keys:
        r = fn(k)
        if not (r.get("status") == "exact" and r.get("security_key") == k):
            miss.append(k)
    print(f"   keyed crosswalk records {len(keys)}; passing through exact {len(keys) - len(miss)}; e.g. missing {miss[:4]}")
    clause("C4 every key passes through as exact", keys and not miss, f"{len(keys) - len(miss)} of {len(keys)}")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R77 BA9 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
