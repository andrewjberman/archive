"""AMGT_RESAPP round 77 -- AMGT-ba-16 (the comparable's restricted selection and the Peers V mapping). Issuer checks.

  python r77_ba16.py --crit AC1|AC2|AC3 [--where local]

AC1 (build)   peers_v reads peer rows in the SCANNER-FACTOR vocabulary through ONE declared table
              (peers_v.SCANNER_FACTOR_MAP): a 12-peer set carrying fcfy / ey_ntm / shldr_yield / peg_ntm yields
              measured z-scores; every ABSENT, measure or V, carries an absent_reason.
AC2 (build)   comparable(): the set is built only from members that carry a key AND factor values, and the record
              prints its restriction (eligible N of M); a set with none eligible reads no comparable, with the reason;
              a member that is the subject's own company (comparable.company_identifier) is never a candidate.
AC3 (control) Andrew's floors are unchanged: |K| >= 8 and |M| >= 3; the subject is dropped from its own peer set.
              PASSES at the base.

Pure fixtures: no S3 read, no vendor call, no engine re-run (allow_rerun=False).
"""
import argparse
import sys
from unittest import mock

OK = []


def clause(label, ok, detail=""):
    OK.append(bool(ok))
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))


def scanner_row(i, with_factors=True):
    row = {"ticker": "P%02d" % i, "name": "Peer %d" % i, "market_cap_musd": 1000.0 + 50 * i, "cap_currency": "USD"}
    row["factors"] = ({"fcfy": 2.0 + 0.35 * i, "ey_ntm": 3.0 + 0.4 * i, "shldr_yield": 1.0 + 0.2 * i,
                       "peg_ntm": 1.0 + 0.1 * i, "eps_fwd_gr_1yr": 5.0 + i} if with_factors else {})
    return row


def ac1():
    from lib.research.scores import peers_v

    table = getattr(peers_v, "SCANNER_FACTOR_MAP", None)
    clause("C1 ONE declared mapping table exists (peers_v.SCANNER_FACTOR_MAP)", isinstance(table, dict) and bool(table),
           "found %s" % type(table).__name__)
    subject = scanner_row(6)
    peers = {"K%02d" % i: scanner_row(i) for i in range(12)}
    out = peers_v.score_peers_v(subject, peers, subject_key="SUBJ_US_Equity")
    measured = [m for m, rec in (out.get("measures") or {}).items() if isinstance(rec, dict) and rec.get("z") is not None]
    clause("C2 a 12-peer set in the scanner vocabulary yields three or more measured z-scores and a V",
           len(measured) >= 3 and isinstance(out.get("V"), (int, float)), "measured %s V %s" % (sorted(measured), out.get("V")))
    absent = [rec for rec in (out.get("measures") or {}).values() if isinstance(rec, dict) and rec.get("z") is None]
    clause("C3 every measure the scanner serves no factor for is ABSENT with an absent_reason",
           all(rec.get("absent_reason") for rec in absent), "%d absent measure(s)" % len(absent))
    empty = peers_v.score_peers_v(scanner_row(6, False), {"K%02d" % i: scanner_row(i, False) for i in range(12)},
                                  subject_key="SUBJ_US_Equity")
    recs = list((empty.get("measures") or {}).values())
    clause("C4 with no factor values, V and all six measures are ABSENT, each with an absent_reason",
           empty.get("V") is None and bool(empty.get("absent_reason")) and len(recs) == 6
           and all(isinstance(r, dict) and r.get("absent_reason") for r in recs),
           "V reason %r" % (empty.get("absent_reason"),))


def universe_fixture():
    return {
        "as_of": "2026-09-15", "snapshot_date": "2026-09-14",
        "holdings_source": {"DIVZ": "gold/holding/date=2026-09-11/holding.parquet"},
        "names": [
            {"security_key": "HELD_US_Equity", "ticker": "HELD US", "name": "Held Co", "source": "both",
             "books": ["DIVZ"], "weight_by_book": {"DIVZ": 3.3}, "resolution": "MEASURED"},
            {"security_key": "HELB_US_Equity", "ticker": "HELB US", "name": "Held B Co", "source": "both",
             "books": ["DIVZ"], "weight_by_book": {"DIVZ": 1.1}, "resolution": "MEASURED"},
            {"security_key": "FREE_US_Equity", "ticker": "FREE US", "name": "Free Co", "source": "coverage",
             "books": [], "weight_by_book": {}, "resolution": "MEASURED"},
            {"security_key": "TWIN_US_Equity", "ticker": "TWIN US", "name": "Held Twin Listing", "source": "both",
             "books": ["DIVZ"], "weight_by_book": {"DIVZ": 0.5}, "resolution": "MEASURED"},
        ],
        "denominators": {"union": 4},
    }


def _no_x1(form, path=None):
    return {"query": form, "security_key": None, "resolution": "UNRESOLVED", "matched_as": None,
            "reason": "fixture: X-1 knows nothing"}


def member(ticker, rung, distance, key, factors):
    return {"ticker": ticker, "name": ticker, "rung_reached": rung, "log_cap_distance": distance,
            "identity": {"security_key": key, "resolution": "MEASURED"}, "universe_weights": {"sp500": 0.1},
            "factors": factors}


def ac2():
    from lib.research.identity import crosswalk as crosswalk_module
    from lib.research.posture import comparable as cm

    has_seam = hasattr(cm, "company_identifier")
    clause("C0 comparable.company_identifier(security_key, member=None) exists", has_seam)
    company = {"FREE_US_Equity": "CO-FREE", "TWIN_US_Equity": "CO-FREE", "HELD_US_Equity": "CO-HELD",
               "HELB_US_Equity": "CO-HELB"}

    def fake_company(security_key, member=None):
        return company.get(security_key)

    patches = [mock.patch.object(crosswalk_module, "resolve", side_effect=_no_x1)]
    if has_seam:
        patches.append(mock.patch.object(cm, "company_identifier", side_effect=fake_company))
    for p in patches:
        p.start()
    try:
        peer_set = {"members": [
            member("HELB", 3, 0.01, "HELB_US_Equity", {}),                 # deeper rung, but carries NO factor values
            member("HELD", 2, 0.30, "HELD_US_Equity", {"fcfy": 2.5}),      # eligible
        ]}
        out = cm.comparable("FREE_US_Equity", universe_fixture(), "2026-09-15", peer_set=peer_set, allow_rerun=False)
        restriction = out.get("restriction") or {}
        clause("C1 the comparable is chosen only among members carrying a key and factor values",
               out.get("comparable") == "HELD_US_Equity", "got %s" % out.get("comparable"))
        clause("C2 the record prints its restriction: eligible 1 of 2",
               restriction.get("eligible") == 1 and restriction.get("of") == 2, str(restriction)[:160])
        none = {"members": [member("HELB", 3, 0.01, "HELB_US_Equity", {}), member("HELD", 2, 0.3, "HELD_US_Equity", {})]}
        out2 = cm.comparable("FREE_US_Equity", universe_fixture(), "2026-09-15", peer_set=none, allow_rerun=False)
        clause("C3 a set with none eligible reads no comparable, with the reason stating 0 of 2",
               out2.get("comparable") is None and (out2.get("restriction") or {}).get("eligible") == 0
               and bool(out2.get("reason")), str(out2.get("reason"))[:160])
        twin = {"members": [
            member("TWIN", 3, 0.0, "TWIN_US_Equity", {"fcfy": 9.9}),       # the subject's own company, second listing
            member("HELD", 2, 0.30, "HELD_US_Equity", {"fcfy": 2.5}),
        ]}
        out3 = cm.comparable("FREE_US_Equity", universe_fixture(), "2026-09-15", peer_set=twin, allow_rerun=False)
        clause("C4 the subject's own company under another identifier is never its comparable, and is counted",
               out3.get("comparable") == "HELD_US_Equity"
               and (out3.get("denominators") or {}).get("same_company_as_subject") == 1,
               "comparable %s denominators %s" % (out3.get("comparable"), str(out3.get("denominators"))[:200]))
    finally:
        for p in patches:
            p.stop()


def bloomberg_row(i):
    return {"FREE_CASH_FLOW_YIELD": 2.0 + 0.3 * i, "BEST_EPS": 5.0 + i, "BEST_PE_RATIO": 15.0 + i,
            "TRAIL_12M_EPS": 4.0 + 0.5 * i, "EV_TO_T12M_SALES": 2.0 + 0.1 * i}


def ac3():
    from lib.research.scores import peers_v

    clause("C1 the ruled floors: |K| >= 8 and |M| >= 3",
           peers_v.MIN_PEERS_FOR_V >= 8 and peers_v.MIN_MEASURES_FOR_V >= 3 and peers_v.MIN_PEERS_PER_MEASURE == 6)
    seven = peers_v.score_peers_v(bloomberg_row(3), {"K%d" % i: bloomberg_row(i) for i in range(7)})
    clause("C2 V is suppressed at seven peers", seven.get("V") is None and seven.get("K") == 7)
    peers = {"K%d" % i: bloomberg_row(i) for i in range(9)}
    peers["SUBJ"] = bloomberg_row(3)
    out = peers_v.score_peers_v(bloomberg_row(3), peers, subject_key="SUBJ")
    clause("C3 the subject is dropped from its own peer set (K 9 of 10 rows)", out.get("K") == 9)
    clause("C4 a peer row in Bloomberg mnemonics still scores (the mapping adds a vocabulary, it removes none)",
           isinstance(out.get("V"), (int, float)), "V %s M %s" % (out.get("V"), out.get("M")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    {"AC1": ac1, "AC2": ac2, "AC3": ac3}[a.crit]()
    ok = bool(OK) and all(OK)
    print("R77 BA16 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
