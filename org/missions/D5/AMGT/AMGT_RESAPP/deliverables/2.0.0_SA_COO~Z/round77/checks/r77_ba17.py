"""AMGT_RESAPP round 77 -- AMGT-ba-17 (the CSC column contract). Issuer checks.

  python r77_ba17.py --crit AC1|AC2 [--where local]

AC1 (build)   every PRESENT column of lib.research.peers.csc.build_csc_map() carries the contract's fields beside its
              value: period_or_horizon, currency (with currency_reason or currency_source where it is not an ISO code)
              and source_field.
AC2 (control) the ABSENT partition is unchanged: it is the seventeen minus the present, each ABSENT column carries
              derivable_from and reason and NO value. PASSES at the base.

Pure: the map is built from the module's own tables, no read.
"""
import argparse
import sys

OK = []


def clause(label, ok, detail=""):
    OK.append(bool(ok))
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))


def ac1():
    from lib.research.peers import csc

    m = csc.build_csc_map()
    present = m.get("present") or []
    clause("C0 five columns are PRESENT", len(present) == 5, "got %d" % len(present))
    by = {e.get("column"): e for e in present}
    miss = [c for c, e in by.items() if not (e.get("period_or_horizon") and e.get("source_field")
                                             and isinstance(e.get("currency"), str) and e.get("currency"))]
    clause("C1 every PRESENT column carries period_or_horizon, currency and source_field",
           bool(present) and not miss, "missing on %s" % miss)
    usd = [c for c in ("Mkt Cap", "EV") if (by.get(c) or {}).get("currency") != "USD"]
    clause("C2 Mkt Cap and EV state USD (they are served in USD millions)", not usd, "not USD: %s" % usd)
    ratio = [c for c in ("P/E 2025", "P/E 2026")
             if not ((by.get(c) or {}).get("currency") == "none" and (by.get(c) or {}).get("currency_reason"))]
    clause("C3 the two P/E columns state currency none, with the reason (a ratio carries no currency)", not ratio,
           "wrong on %s" % ratio)
    price = by.get("Price") or {}
    clause("C4 Price states that its currency is per member, and names where it is read",
           price.get("currency") == "per member" and bool(price.get("currency_source")), str(price.get("currency")))
    src = [c for c, e in by.items() if e.get("code") and str(e.get("code")) not in str(e.get("source_field"))]
    clause("C5 source_field names the column's own scanner code or row field", bool(present) and not src,
           "not naming its code: %s" % src)


def ac2():
    from lib.research.peers import csc

    m = csc.build_csc_map()
    present, absent = m.get("present") or [], m.get("absent") or []
    clause("C1 the subtraction holds: 5 present + 12 absent = the seventeen",
           len(present) == 5 and len(absent) == 12 and len(csc.CSC_COLUMNS) == 17
           and {e["column"] for e in present} | {e["column"] for e in absent} == set(csc.CSC_COLUMNS))
    bad = [e.get("column") for e in absent
           if "value" in e or "derivable_from" not in e or not e.get("reason")]
    clause("C2 every ABSENT column carries derivable_from and a reason, and NO value", not bad, "bad: %s" % bad)
    clause("C3 no PRESENT column carries a fiscal-year label over a trailing or NTM figure",
           all("20" not in str(e.get("display_label")) for e in present))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    {"AC1": ac1, "AC2": ac2}[a.crit]()
    ok = bool(OK) and all(OK)
    print("R77 BA17 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
