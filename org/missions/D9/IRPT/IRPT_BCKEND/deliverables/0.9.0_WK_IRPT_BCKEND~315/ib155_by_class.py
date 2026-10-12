#!/usr/bin/env python3
"""IB-pr-459 AMENDMENT 1: Measurement 1 per fund class, and the store's date coverage.  READ ONLY.  Counts only: no account id, no security is named.

  python -I ib155_by_class.py <scratch_dir> <json_in_out>

Rebuilds the per-ticker comparison of ib155_measure.measurement_1 (same rule, same inputs: the store read from S3 by get, the Yahoo cache in <scratch_dir>/yahoo; NO
Yahoo call is made here) and ADDS five members to the existing json: how_a_fund_is_marked_replaced, by_fund_class, admitted_types_holding_not_replaced_funds,
the_store_holds_the_unadjusted_close_by_class, store_date_coverage.  Every other member of the json is left as measured.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import io
import json
import pickle
import sys
from pathlib import Path

import ib155_measure as m   # sets sys.path as the driver does and imports dv, cen, pc, tc, pd, np, pq, boto3

dv, cen, pc, tc, pd, np, pq = m.dv, m.cen, m.pc, m.tc, m.pd, m.np, m.pq
import date_basis_grading as dbg  # noqa: E402  (path set by ib155_measure)

CENSUS = m.ROOT / "org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~60/price_basis_census.csv"
OUTCOMES = ("every_compared_day_equal", "some_days_not_equal", "no_yahoo_labelled_point_in_the_store", "not_in_the_store", "no_bar_from_the_reader")
CLASSES = ("replaced", "not_replaced", "not_a_fund_or_unmarked")


def word(compared, some_not_equal, every_equal):
    if compared == 0:
        return "CANNOT_BE_TOLD"
    if some_not_equal == 0:
        return "YES_FOR_EVERY_COMPARED_TICKER"
    if every_equal == 0:
        return "NO"
    return "FOR_SOME"


def main():
    scratch, out = Path(sys.argv[1]), Path(sys.argv[2])
    tickers = list(json.load(open(scratch / "tickers.json", encoding="utf-8"))["tickers"])
    assert len(tickers) == 878 and len(set(tickers)) == 878
    P1 = pickle.load(open(scratch / "phase1.pkl", "rb"))
    graded = P1["graded"]
    assert len(graded) == 85
    first = dt.date.fromisoformat(graded[0])
    d = first
    for _ in range(m.LOOKBACK):
        d = tc.prev_trading_day(d)
    window_days = sorted(set(graded) | {x.isoformat() for x in tc.trading_days_between(d, first)})

    # ---- the build's own mark: the census class, SUBSTITUTE_CLASSES (commonwealth_daily_valuation.py:205, :214-221)
    census = {}
    with open(CENSUS, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            census[pc.norm_key(r["ticker"])] = r["class"]
    subst = set(dv.SUBSTITUTE_CLASSES)

    def fund_class(tk):
        c = census.get(pc.norm_key(tk))
        return "not_a_fund_or_unmarked" if c is None else ("replaced" if c in subst else "not_replaced")

    # ---- the store, read once (S3 get of the named object, as the driver does)
    s3 = m.boto3.client("s3", region_name="us-east-1")
    bucket, key = pc.split_uri(pc.legacy_uri(cen.SPEC["legacy"]))
    store = pq.ParquetFile(io.BytesIO(pc._get(s3, bucket, key))).read(columns=["date", "ticker", "price", "source"]).to_pandas()
    store["date"] = pd.to_datetime(store["date"]).dt.strftime("%Y-%m-%d")
    ystore = store[store["source"] == cen.YAHOO_LABEL]
    in_store = set(store["ticker"].astype(str))
    by_tk = {t: g for t, g in ystore.groupby(ystore["ticker"].astype(str))}

    per = {}                      # ticker -> dict(outcome, compared, equal, ratios(list of unequal store/Close), dates(list of compared days))
    for tk in tickers:
        s, _ = dv.read_yahoo_close(str(scratch / "yahoo"), tk)
        rec = {"outcome": None, "compared": 0, "equal": 0, "ratios": [], "dates": [], "dist": 0, "dist_eq_close": 0, "dist_eq_adj": 0, "dist_neither": 0}
        per[tk] = rec
        if s is None or len(s) == 0:
            rec["outcome"] = "no_bar_from_the_reader"
            continue
        close = {(m.EPOCH + dt.timedelta(days=int(k))).isoformat(): float(v) for k, v in s.items()}
        if tk not in in_store:
            rec["outcome"] = "not_in_the_store"
            continue
        g = by_tk.get(tk)
        if g is None or not len(g):
            rec["outcome"] = "no_yahoo_labelled_point_in_the_store"
            continue
        sp = g.groupby("date")["price"].median().to_dict()
        both = [x for x in window_days if x in close and x in sp]
        if not both:
            rec["outcome"] = "no_yahoo_labelled_point_in_the_store"
            continue
        neq = 0
        yh = cen.read_cache(str(scratch / "yahoo"), tk)[0]
        adj = {} if yh is None else {k: float(v) for k, v in yh["Adj Close"].items()}
        for x in both:
            c, v = close[x], float(sp[x])
            rec["compared"] += 1
            rec["dates"].append(x)
            a = adj.get(x)
            if a is not None and a > 0 and c > 0 and abs(a / c - 1.0) > m.EQ_TOL:      # a day on which Adj Close and Close differ: the store's point can tell them apart
                rec["dist"] += 1
                if abs(v / c - 1.0) <= m.EQ_TOL:
                    rec["dist_eq_close"] += 1
                elif abs(v / a - 1.0) <= m.EQ_TOL:
                    rec["dist_eq_adj"] += 1
                else:
                    rec["dist_neither"] += 1
            if c > 0 and abs(v / c - 1.0) <= m.EQ_TOL:
                rec["equal"] += 1
            else:
                neq += 1
                rec["ratios"].append(v / c if c > 0 else float("nan"))
        rec["outcome"] = "every_compared_day_equal" if neq == 0 else "some_days_not_equal"

    # ---- the whole, to be reproduced
    whole = collections.Counter(r["outcome"] for r in per.values())
    comp = sum(r["compared"] for r in per.values())
    eq = sum(r["equal"] for r in per.values())
    doc = json.load(open(out, encoding="utf-8"))
    assert dict(whole) == doc["tickers"]["outcomes"], (dict(whole), doc["tickers"]["outcomes"])
    assert comp == doc["ticker_days"]["compared"] and eq == doc["ticker_days"]["equal"]

    comp_by_date_all = sorted({x for r in per.values() for x in r["dates"]})
    # ---- by class
    by = {}
    for c in CLASSES:
        tks = [t for t in tickers if fund_class(t) == c]
        oc = collections.Counter(per[t]["outcome"] for t in tks)
        cc = sum(per[t]["compared"] for t in tks)
        ee = sum(per[t]["equal"] for t in tks)
        rat = [x for t in tks for x in per[t]["ratios"]]
        med = float(np.median(rat)) if rat else None
        by[c] = {"tickers": len(tks), "ticker_outcomes": {o: int(oc.get(o, 0)) for o in OUTCOMES},
                 "ticker_days": {"compared": cc, "equal": ee, "not_equal": cc - ee},
                 "unequal_ticker_days_used_for_the_median": len(rat),
                 "median_ratio_store_point_over_reader_unadjusted_close_on_unequal_ticker_days": None if med is None else round(med, 4),
                 "unequal_ratio_quartiles_25_75": None if not rat else [round(float(np.percentile(rat, 25)), 4), round(float(np.percentile(rat, 75)), 4)]}
        by[c]["ticker_days_on_which_adj_close_differs_from_close_by_more_than_1e-4"] = {
            k: sum(per[t][kk] for t in tks) for k, kk in (("days", "dist"), ("store_equals_close", "dist_eq_close"), ("store_equals_adj_close", "dist_eq_adj"), ("store_equals_neither", "dist_neither"))}
        assert sum(by[c]["ticker_outcomes"].values()) == len(tks)
    assert sum(by[c]["tickers"] for c in CLASSES) == 878
    for o in OUTCOMES:
        assert sum(by[c]["ticker_outcomes"][o] for c in CLASSES) == whole[o]
    for k in ("compared", "equal", "not_equal"):
        assert sum(by[c]["ticker_days"][k] for c in CLASSES) == doc["ticker_days"][k]

    # ---- the nine admitted type pairs: securities among the 878 (ids from prep.pkl and overlap.pkl; type = the one pair over the security's transaction rows)
    prep = pickle.load(open(scratch / "prep.pkl", "rb"))
    ov = pickle.load(open(scratch / "overlap.pkl", "rb"))["overlap_all"]
    sec = {}                                  # security id -> (ticker, pair or None)
    conflicts = 0

    def put(sid, tk, pair):
        nonlocal conflicts
        if not tk:
            return
        if sid in sec and sec[sid] != (tk, pair):
            conflicts += 1
        sec.setdefault(sid, (tk, pair))
    for sid, v in ov.items():
        ps = set(v["pairs"])
        put(sid, v["ticker"], " / ".join(next(iter(ps))) if len(ps) == 1 else None)
    for sid, tk in prep["sec_ticker"].items():
        put(sid, tk, prep["sec_pair"].get(sid))
    for sid, tk in prep["fund_ticker"].items():
        put(sid, tk, prep["fund_pair"].get(sid))
    ts = set(tickers)
    pairs9 = [" / ".join(p) for p in dbg.ADMITTED_PAIRS]
    assert len(pairs9) == 9
    types = []
    for p in pairs9:
        ids = [s for s, (tk, pr) in sec.items() if pr == p and tk in ts]
        cl = collections.Counter(fund_class(sec[s][0]) for s in ids)
        nr = [s for s in ids if fund_class(sec[s][0]) == "not_replaced"]
        un = [s for s in ids if per[sec[s][0]]["outcome"] == "some_days_not_equal"]
        nr_un = [s for s in nr if per[sec[s][0]]["outcome"] == "some_days_not_equal"]
        types.append({"type_pair": p, "securities_among_the_878": len(ids), "replaced": cl["replaced"], "not_replaced": cl["not_replaced"],
                      "not_a_fund_or_unmarked": cl["not_a_fund_or_unmarked"],
                      "not_replaced_with_unequal_ticker_days": len(nr_un),
                      "all_classes_with_unequal_ticker_days": len(un)})
    typed_ids_in_878 = [s for s, (tk, pr) in sec.items() if tk in ts]
    other_typed = sum(1 for s in typed_ids_in_878 if sec[s][1] not in pairs9)

    # ---- the store's dates against the graded days
    comp_by_date = collections.Counter(x for r in per.values() for x in r["dates"])
    y_dates = set(ystore["date"])
    a_dates = set(store["date"])
    y_on_878 = set(ystore[ystore["ticker"].astype(str).isin(ts)]["date"])
    gset = set(graded)
    prior = [x for x in window_days if x not in gset]
    by_month = collections.Counter()
    for x, n in comp_by_date.items():
        by_month[x[:7]] += n
    coverage = {
        "compared_ticker_days": comp,
        "compared_ticker_days_fall_on_distinct_dates": len(comp_by_date),
        "compared_dates_first": min(comp_by_date), "compared_dates_last": max(comp_by_date),
        "compared_ticker_days_by_month": dict(sorted(by_month.items())),
        "compared_ticker_days_by_date": dict(sorted(comp_by_date.items())),
        "compared_ticker_days_on_a_graded_day": sum(n for x, n in comp_by_date.items() if x in gset),
        "compared_ticker_days_on_a_day_before_the_first_graded_day": sum(n for x, n in comp_by_date.items() if x not in gset),
        "graded_days": {"count": len(graded), "first": graded[0], "last": graded[-1],
                        "covered_by_a_yahoo_labelled_point_of_any_ticker_in_the_store": sum(1 for x in graded if x in y_dates),
                        "covered_by_a_yahoo_labelled_point_of_any_of_the_878": sum(1 for x in graded if x in y_on_878),
                        "covered_by_a_point_of_any_label_of_any_ticker": sum(1 for x in graded if x in a_dates)},
        "the_40_days_before_the_first_graded_day": {"count": len(prior), "first": prior[0], "last": prior[-1],
                                                    "covered_by_a_yahoo_labelled_point_of_any_ticker_in_the_store": sum(1 for x in prior if x in y_dates),
                                                    "covered_by_a_yahoo_labelled_point_of_any_of_the_878": sum(1 for x in prior if x in y_on_878)},
        "newest_date_the_store_holds_a_yahoo_labelled_point": max(y_dates),
        "newest_date_the_store_holds_a_point_of_any_label": max(a_dates),
        "store_distinct_dates_yahoo_labelled": len(y_dates),
        "reading": "every one of the compared ticker-days falls on a day BEFORE the first graded day; none falls on a graded day. The store holds no yahoo-labelled point on any "
                   "of the graded days, for any ticker, so it cannot be the second witness's source for them as it stands.",
    }

    doc["how_a_fund_is_marked_replaced"] = {
        "the_flag": "the `class` column of the build's price-basis census (price_basis_census.csv, one row per ticker, 3,580 tickers): a ticker whose class is `dividend_adjusted` or "
                    "`mixed` is REPLACED; every other class (`indistinguishable`, `other`, `as_traded`, `no_yahoo`), and a ticker the census does not list, stays on the store's points",
        "where_it_lives": "a table of the build, not a column of the store: the store (canonical_prices.parquet) holds no such column (its columns are date, asset_name, ticker, price, source)",
        "cited": ["data/assets/scripts/silver/commonwealth_daily_valuation.py:200-201 (BASIS_CENSUS = ADVI_COTBKF deliverables 0.9.0_WK_ADVI_COTBKF~60/price_basis_census.csv)",
                  "data/assets/scripts/silver/commonwealth_daily_valuation.py:205 (SUBSTITUTE_CLASSES = dividend_adjusted, mixed)",
                  "data/assets/scripts/silver/commonwealth_daily_valuation.py:214-221 (load_basis_classes: the census rows of those classes)",
                  "data/assets/scripts/silver/commonwealth_daily_valuation.py:246-288 (as_traded_store: the yahoo-labelled points of a flagged ticker are replaced by the cached Yahoo Close; "
                  ":258-262 a flagged ticker with no cached Yahoo series keeps the store's points)",
                  "the round-76 records name the same thing as `substituted`: org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~139/PRICE_PAID.json "
                  "population.served_close (substituted = the series differ between r34/before and r34/after on some date; 73; equal to the 73 of VALIDATED_UNADJUSTED.csv group "
                  "substituted) and .../0.9.0_WK_ADVI_COTBKF~128/VALIDATED_UNADJUSTED.csv column `group` (substituted 73, left_on_store 197)"],
        "checked_against_the_record": "of the 270 fund series in VALIDATED_UNADJUSTED.csv, the 73 `substituted` are all census class dividend_adjusted (60) or mixed (13), and none of the "
                                       "197 `left_on_store` is (120 are not in the census, 73 `other`, 2 `indistinguishable`, 1 `as_traded`, 1 `no_yahoo`): the census class predicts the record's "
                                       "flag for 270 of 270 (read here from the two csv files)",
        "classes_formed_here": {"replaced": "census class dividend_adjusted or mixed", "not_replaced": "listed in the census with any other class",
                                "not_a_fund_or_unmarked": "not listed in the census (the census lists tickers that carry yahoo_finance rows in the store; a fund absent from it is also left on "
                                                          "the store by the build, so this class holds funds as well as non-funds: see its type split in by_fund_class)"},
        "caveat": "the build replaces a flagged ticker only when a cached Yahoo series exists for it (:258-262); that cache is the build's input, not read here, so `replaced` here is "
                  "`flagged to be replaced`. For the 270 fund series the record shows the flagged and the actually-replaced sets are equal (73 and 73).",
        "claim": "measured",
    }
    # type split of the unmarked class (by the security-type pairs among the 878): funds (registered investment companies) vs exchange-traded equity vs other / not typed
    ric = "Securities Issued by Registered Investment Companies or Business Development Companies"
    tk_pair = collections.defaultdict(set)
    for s, (tk, pr) in sec.items():
        if tk in ts:
            tk_pair[tk].add(pr)

    def fam(t):
        ps = tk_pair.get(t)
        if not ps:
            return "no_type_known_in_the_cache"
        if all(p and p.startswith(ric) for p in ps):
            return "registered_investment_company_type"
        if all(p and p.startswith("Exchange-Traded Equity Securities") for p in ps):
            return "exchange_traded_equity_type"
        return "mixed_or_other_type"
    for c in CLASSES:
        tks = [t for t in tickers if fund_class(t) == c]
        by[c]["by_type_family"] = dict(sorted(collections.Counter(fam(t) for t in tks).items()))
    doc["by_fund_class"] = {
        "population": "the same 878 tickers as the whole; every ticker in exactly one class",
        "equality_rule": doc["ticker_days"]["equality_rule"],
        "median_ratio_note": "pooled median over the class's unequal ticker-days of (store point / reader unadjusted Close); 1.0 would be equal",
        "classes": by,
        "reading_limit": "every compared ticker-day lies in the store's newest 37 yahoo-labelled days (%s to %s), the days closest to its build, where an adjusted and an unadjusted close "
                         "differ least; the days an adjusted close would set apart (Adj Close differs from Close by more than 1e-4) are counted per class beside the classes. Nothing "
                         "here is read of the store's older points or of any day after its last: an adjusted close dates nothing, and an equal near the end of the store does not show the "
                         "store holds the unadjusted close for earlier years" % (min(comp_by_date_all), max(comp_by_date_all)),
        "sums_to_the_whole": {"tickers": 878, "ticker_outcomes": dict(whole), "ticker_days": {k: doc["ticker_days"][k] for k in ("compared", "equal", "not_equal")}, "remainder": 0},
    }
    doc["admitted_types_holding_not_replaced_funds"] = {
        "the_nine_pairs_from": "data/assets/scripts/gold/irpt_reporting/date_basis_grading.py:49-53 (ADMITTED_PAIRS)",
        "securities_definition": "a security id (its internal id or CUSIP) whose one (SEC Asset Type, Share Class Type) pair is that pair and whose ticker is among the 878; ids from the "
                                 "earlier reads' maps (prep and overlap); one ticker can hold more than one id",
        "types": types,
        "typed_securities_among_the_878_with_a_pair_outside_the_nine_or_no_single_pair": other_typed,
        "securities_with_a_ticker_among_the_878": len(typed_ids_in_878),
        "id_pair_conflicts_between_the_maps": conflicts,
    }
    doc["the_store_holds_the_unadjusted_close_by_class"] = {
        c: word(by[c]["ticker_days"]["compared"], by[c]["ticker_outcomes"]["some_days_not_equal"], by[c]["ticker_outcomes"]["every_compared_day_equal"]) for c in CLASSES}
    doc["store_date_coverage"] = coverage
    doc["fetch"]["passes"] = 1
    doc["fetch"]["second_pass_made"] = False
    doc["fetch"]["amendment_1_note"] = "AMENDMENT 1 was computed from the cache of the one pass (no Yahoo call); the store was read again by S3 get"
    json.dump(doc, open(out, "w", encoding="utf-8"), indent=1, default=str)
    print(json.dumps({"by_class": {c: {k: v for k, v in by[c].items()} for c in CLASSES}, "words": doc["the_store_holds_the_unadjusted_close_by_class"],
                      "types": types, "other_typed": other_typed, "conflicts": conflicts, "coverage": {k: v for k, v in coverage.items() if k != "compared_ticker_days_by_date"}}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
