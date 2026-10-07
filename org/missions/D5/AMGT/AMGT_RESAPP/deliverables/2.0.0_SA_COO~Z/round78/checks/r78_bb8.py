"""AMGT_RESAPP round 78 -- AMGT-bb-8: each peer price served with the currency of the listing it is quoted on
(round-77 enrichment item 7; DSGN_AMGTV1 round-46 countersign ruling 2, FWD-8).

  --crit AC1|AC2|AC3 --where local

AC1 (build): `lib.research.peers.price_listing.record_for_price(member, resolve)` on planted peer rows:
    C1 a row whose ticker is its own record's ticker (HD -> HD_US_Equity) keeps that record, basis "own_ticker";
    C2 a row matched by company name to a US listing while the row is not a United States row (688910, Taiwan, matched
       to TSM_US_Equity) is REFUSED: no record, and a plain reason;
    C3 a row matched by company name to a listing in its own country (710891, Switzerland, ROG_SW_Equity) keeps it,
       basis "name_match";
    C4 a United States row with a plain ticker and no record of its own (MSFT) takes the record `resolve("MSFT US")`
       names, basis "us_ticker"; when `resolve` knows nothing, no record and no reason;
    C5 a non-US row with no record (677172, South Korea) gets no record and no reason; `resolve` is not asked.
AC2 (seam, the real neighbour): over the stored peer sets of 2317_TT_Equity, BA_US_Equity and VLO_US_Equity, read by
    `scoped_amgt.read_peer_set`, with the pool list's own resolver: every row gets an answer, the Taiwan row matched to
    TSM_US_Equity is refused, and NO answer pairs a US-listing record with a row from another country.
AC3 (bound): the existing price-currency tests still pass (lib/research/api/tests/test_peer_price_currency.py).
Verdict: R78 BB8 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import Counter

BOUND_TEST = "lib/research/api/tests/test_peer_price_currency.py"
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze")
SETS = ("2317_TT_Equity", "BA_US_Equity", "VLO_US_Equity")


def _row(ticker, name, price, country, key=None, how=None):
    return {"ticker": ticker, "name": name, "price": price, "country": country, "cap_currency": "USD",
            "identity": {"matched_as": how, "raw_identifier": ticker, "resolution": "MEASURED" if key else "UNRESOLVED",
                         "security_key": key},
            "security_key": key}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        if not os.path.isfile(BOUND_TEST):
            clause("C1 the bound test file exists", False, BOUND_TEST)
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", BOUND_TEST],
                           capture_output=True, timeout=600)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 the existing price-currency tests pass", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    try:
        from lib.research.peers import price_listing
    except ImportError as err:
        clause("C0 lib.research.peers.price_listing imports", False, str(err))
        return verdict(a, ok)
    fn = getattr(price_listing, "record_for_price", None)
    if not callable(fn):
        clause("C0 price_listing.record_for_price exists", False, "absent")
        return verdict(a, ok)

    if a.crit == "AC1":
        asked = []

        def knows(form):
            asked.append(form)
            return {"MSFT US": "MSFT_US_Equity"}.get(form)

        def knows_nothing(form):
            asked.append(form)
            return None

        own = fn(_row("HD", "Home Depot, Inc.", 349.52, "United States", "HD_US_Equity", "association_key"), knows)
        clause("C1 a row on its own record's ticker keeps the record",
               own.get("record_key") == "HD_US_Equity" and own.get("basis") == "own_ticker" and not own.get("reason"), repr(own))
        tsm = fn(_row("688910", "Taiwan Semiconductor Manufacturing Co., Ltd.", 2365.0, "Taiwan", "TSM_US_Equity",
                      "company_name"), knows)
        text = str(tsm.get("reason") or "")
        clause("C2 a home-exchange price matched to the US listing is refused with a plain reason",
               tsm.get("record_key") is None and tsm.get("basis") is None and text.strip()
               and not [w for w in BANNED if w in text.lower()], repr(tsm))
        rog = fn(_row("710891", "Roche Holding Ltd", 368.4, "Switzerland", "ROG_SW_Equity", "company_name"), knows)
        clause("C3 a name match to a listing in the row's own country keeps the record",
               rog.get("record_key") == "ROG_SW_Equity" and rog.get("basis") == "name_match" and not rog.get("reason"), repr(rog))
        del asked[:]
        us = fn(_row("MSFT", "Microsoft Corporation", 499.86, "United States"), knows)
        first = list(asked)
        none = fn(_row("MSFT", "Microsoft Corporation", 499.86, "United States"), knows_nothing)
        clause("C4 a United States row with a plain ticker takes the record the list names for '<ticker> US'",
               us.get("record_key") == "MSFT_US_Equity" and us.get("basis") == "us_ticker" and first == ["MSFT US"]
               and none.get("record_key") is None and not none.get("reason"), f"{us!r} asked {first}")
        del asked[:]
        kr = fn(_row("677172", "Samsung Electronics Co., Ltd.", 230500.0, "South Korea"), knows)
        clause("C5 a non-US row with no record gets none, and the list is not asked",
               kr.get("record_key") is None and kr.get("basis") is None and not kr.get("reason") and asked == [], f"{kr!r} asked {asked}")
        return verdict(a, ok)

    from lib.research.api import scoped_amgt
    from lib.research.identity import crosswalk

    def resolver(form):
        hit = crosswalk.resolve(form)
        return hit.get("security_key") if hit.get("resolution") == crosswalk.RESOLUTION_MEASURED else None

    rows = []
    for key in SETS:
        members = (scoped_amgt.read_peer_set(key) or {}).get("members") or []
        print(f"   {key}: stored peer rows {len(members)}")
        rows.extend(m for m in members if isinstance(m, dict))
    bases = Counter()
    refused = []
    crossed = []
    unanswered = 0
    for m in rows:
        out = fn(m, resolver)
        if not isinstance(out, dict) or "record_key" not in out:
            unanswered += 1
            continue
        bases[out.get("basis")] += 1
        if out.get("reason"):
            refused.append((m.get("ticker"), (m.get("identity") or {}).get("security_key")))
        rk = out.get("record_key")
        if rk and str(rk).endswith("_US_Equity") and m.get("country") != "United States":
            crossed.append((m.get("ticker"), m.get("country"), rk))
    print(f"   rows {len(rows)}; by basis {dict(bases)}; refused {refused}; crossed {crossed}")
    clause("C1 every stored row gets an answer", rows and unanswered == 0, f"{len(rows) - unanswered} of {len(rows)}")
    clause("C2 the Taiwan row matched to TSM_US_Equity is refused", ("688910", "TSM_US_Equity") in refused)
    clause("C3 no answer pairs a US-listing record with a row from another country", rows and not crossed, f"{len(crossed)} crossed")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB8 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
