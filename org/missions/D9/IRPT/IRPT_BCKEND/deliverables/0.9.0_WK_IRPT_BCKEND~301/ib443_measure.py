#!/usr/bin/env python3
"""IB-pr-443 step 3.  Read only; public-security dated values only (no account, quantity or amount is in the gather file).

    python -I ib443_measure.py --control
    python -I ib443_measure.py <gather.json> <calls.json> <out_dir>

For each of the five one-day-off security-days of IB-pr-441: both witnesses over the prior trading day, the day and the next; the custodian's mark;
the priced trades of that security within three trading days; the series five trading days either side; the distribution rows in the estate; and
ONE verdict made by decide() below.  The same decide() runs on the planted control.  Verdict rule (stated before the data is read):

  with a struck trade (Buy or Sale, Price > 0) on a day u within three trading days where the witnesses' values for u differ:
      the trade price equals the first witness's value for u only      -> SECOND_WITNESS_OFF  (measured)   [mutual fund only: its trade is struck at that day's NAV]
      the trade price equals the second witness's value for u only     -> FIRST_WITNESS_OFF   (measured)
      it equals both or neither                                        -> CANNOT_BE_TOLD      (absent)
      an exchange-traded security's trade price is intraday and cannot decide a close -> CANNOT_BE_TOLD (absent)
  with no struck trade, from the two series alone:
      the second witness's value for t is the half-up cent rounding of the first witness's sub-cent value, and the same holds on EVERY other
      sub-cent day of the series                                       -> CANNOT_BE_TOLD      (inferred)  [neither is shown to be on the wrong day]
      the second witness repeats its value of the prior day at t while the first moves, and the first's value for t equals no value of the
      second witness on any day of the series                          -> SECOND_WITNESS_OFF  (inferred)
      the same with the witnesses exchanged                            -> FIRST_WITNESS_OFF   (inferred)
      otherwise                                                        -> CANNOT_BE_TOLD      (absent)
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE.parents[6]
sys.path[:0] = [str(root / "lib"), str(root), str(HERE)]
import ib441_measure as m  # noqa: E402
import trading_calendar as tc  # noqa: E402

CUSIP = {"MEIIX": "552983694", "MISIX": "92647K309", "PZA": "46138E537", "SHM": "78468R739"}
KIND = {"MEIIX": "mutual_fund", "MISIX": "mutual_fund", "SHM": "exchange_traded", "PZA": "exchange_traded"}
KIND_HOW = {"MEIIX": "inferred from the five-letter fund-share ticker form and an institutional share class given by the estate; not stated by the estate",
            "MISIX": "inferred from the five-letter fund-share ticker form and an institutional share class given by the estate; not stated by the estate",
            "SHM": "inferred: a three-letter exchange ticker, share class 'Not Available' in the estate, sub-cent closes; not stated by the estate",
            "PZA": "inferred: a three-letter exchange ticker, share class 'Not Available' in the estate, sub-cent closes; not stated by the estate"}


def r4(x):
    return None if x is None else round(float(x), 4)


def half_up(x):
    return float(Decimal(repr(round(float(x), 6))).quantize(Decimal("0.01"), ROUND_HALF_UP))


def is_subcent(x):
    return Decimal(repr(round(float(x), 6))).as_tuple().exponent < -2


def decide(kind, i, tdays, A, R, trades):
    """-> (verdict, claim, reason, deciding_evidence).  A: first witness {day: v}; R: second {day: v}; trades: [(trade_day, price)] (Buy/Sale, price > 0), within three
    trading days of tdays[i]."""
    t = tdays[i]
    usable = []
    for d, p in trades:
        a, r = A.get(d), R.get(d)
        if a is None or r is None or m.same(a, r):
            continue
        usable.append((d, p, m.same(p, a), m.same(p, r)))
    if trades:
        if kind != "mutual_fund":
            return ("CANNOT_BE_TOLD", "absent", "the security is exchange-traded: a trade price is an intraday price and cannot decide a close", None)
        for d, p, ma, mr in usable:
            if ma and not mr:
                return ("SECOND_WITNESS_OFF", "measured", "a priced fund trade on %s is struck at the first witness's value for that day and not the second's" % d,
                        "trade %s price %s equals the first witness's %s and not the second's %s" % (d, p, r4(A[d]), r4(R[d])))
            if mr and not ma:
                return ("FIRST_WITNESS_OFF", "measured", "a priced fund trade on %s is struck at the second witness's value for that day and not the first's" % d,
                        "trade %s price %s equals the second witness's %s and not the first's %s" % (d, p, r4(R[d]), r4(A[d])))
        return ("CANNOT_BE_TOLD", "absent", "the priced trades within three trading days match both witnesses or neither", None)
    f, s = A.get(t), R.get(t)
    if f is None or s is None:
        return ("CANNOT_BE_TOLD", "absent", "one witness has no value for the day", None)
    sub = [d for d in tdays if A.get(d) is not None and R.get(d) is not None and is_subcent(A[d])]
    if is_subcent(f) and sub and all(abs(half_up(A[d]) - R[d]) < 5e-5 for d in sub):
        return ("CANNOT_BE_TOLD", "inferred",
                "neither witness is shown to be on the wrong day: the second witness's close is the first witness's sub-cent close rounded half-up to the cent, "
                "which here coincides with the prior day's close; the same rounding holds on all %d sub-cent days of this series" % len(sub), None)
    prior = tdays[i - 1] if i > 0 else None
    if prior and R.get(prior) is not None and m.same(s, R[prior]) and A.get(prior) is not None and not m.same(f, A[prior]) \
            and not any(R.get(d) is not None and m.same(f, R[d]) for d in tdays):
        return ("SECOND_WITNESS_OFF", "inferred",
                "the second witness repeats its prior day's value at the day while the first witness moves to a value the second witness shows on no day",
                "second witness %s: %s then %s (repeated); first witness %s: %s then %s; the first's %s appears in no day of the second's series"
                % (prior, r4(R[prior]), r4(s), prior, r4(A[prior]), r4(f), r4(f)))
    if prior and A.get(prior) is not None and m.same(f, A[prior]) and R.get(prior) is not None and not m.same(s, R[prior]) \
            and not any(A.get(d) is not None and m.same(s, A[d]) for d in tdays):
        return ("FIRST_WITNESS_OFF", "inferred",
                "the first witness repeats its prior day's value at the day while the second witness moves to a value the first witness shows on no day",
                "first witness %s: %s then %s (repeated); second witness %s: %s then %s; the second's %s appears in no day of the first's series"
                % (prior, r4(A[prior]), r4(f), prior, r4(R[prior]), r4(s), r4(s)))
    return ("CANNOT_BE_TOLD", "absent", "the series do not decide which witness holds another day's value", None)


def control_run():
    td = ["d%d" % k for k in range(8)]
    truth = [10.0, 11.0, 12.5, 13.0, 14.0, 15.5, 16.0, 17.0]
    i = 3
    T = {td[k]: truth[k] for k in range(8)}
    late = {td[k]: truth[k - 1] if k == i else truth[k] for k in range(8)}      # a witness one day LATE at d3
    out = []
    # three planted security-days WITH a struck trade (a mutual fund: struck at the NAV of its trade date)
    out.append(decide("mutual_fund", i, td, late, T, [("d3", 13.0)])[0])                        # first witness late; trade at truth -> FIRST_WITNESS_OFF
    out.append(decide("mutual_fund", i, td, T, late, [("d3", 13.0)])[0])                        # second witness late                -> SECOND_WITNESS_OFF
    out.append(decide("mutual_fund", i, td, late, T, [("d3", 99.0)])[0])                        # trade matches neither              -> CANNOT_BE_TOLD
    # three planted security-days with NO trade (the series branch)
    stale = {td[k]: (truth[k - 1] if k == i else truth[k]) for k in range(8)}
    out.append(decide("mutual_fund", i, td, T, stale, [])[0])                                   # second repeats the prior value         -> SECOND_WITNESS_OFF
    out.append(decide("mutual_fund", i, td, stale, T, [])[0])                                   # first repeats                          -> FIRST_WITNESS_OFF
    sc = {td[k]: (truth[k] + 0.005 if k in (i, 5) else truth[k]) for k in range(8)}              # sub-cent first witness, second = half-up cent
    rd = {td[k]: (half_up(sc[td[k]])) for k in range(8)}
    rd["d3"] = 13.01
    sc["d3"] = 13.005
    sc["d5"] = 15.505
    rd["d5"] = 15.51
    out.append(decide("exchange_traded", i, td, sc, rd, [])[0])                                 # rounding on every sub-cent day         -> CANNOT_BE_TOLD
    return out


PLANTED = ["FIRST_WITNESS_OFF", "SECOND_WITNESS_OFF", "CANNOT_BE_TOLD", "SECOND_WITNESS_OFF", "FIRST_WITNESS_OFF", "CANNOT_BE_TOLD"]


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(r, "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    G = json.load(open(sys.argv[1]))
    calls = json.load(open(sys.argv[2]))
    out_dir = Path(sys.argv[3])
    ctl = control_run()
    ax = G["axis"]
    wide = [d.isoformat() for d in tc.trading_days_between(dt.date(2026, 5, 1), dt.date(2026, 10, 9))]
    secdays = []
    for tk, date, typ in G["five"]:
        c = CUSIP[tk]
        A, R = G["anchor"][c], G["reader"][tk]
        M = {d: v["most_common_mark"] for d, v in G["mark"][c].items()}
        i = ax.index(date)
        prior, nxt = ax[i - 1], (ax[i + 1] if i + 1 < len(ax) else None)

        def three(S, name):
            return {"prior_day": r4(S.get(prior)), "day": r4(S.get(date)), "next_day": r4(S.get(nxt)) if nxt else None,
                    "dates": {"prior_day": prior, "day": date, "next_day": nxt},
                    "null_reasons": {k: (name + " has no value for " + dd if dd and S.get(dd) is None else None)
                                     for k, dd in (("prior_day", prior), ("day", date), ("next_day", nxt)) if (dd is None or S.get(dd) is None)} or None}
        fw, sw, cm = three(A, "first witness"), three(R, "second witness"), three(M, "custodian mark")
        if nxt is None:
            for w, nm in ((fw, "first witness"), (sw, "second witness"), (cm, "custodian mark")):
                w["null_reasons"] = dict(w["null_reasons"] or {}, next_day="no trading day after %s has closed (2026-10-12 is after the read; the first witness's partition for it is absent, the second witness's latest bar is %s)"
                                         % (date, max(R)))
        cm["label"] = "the CUSTODIAN's mark (Market Value / Units, the most common value over the position rows of the holdings partition): the custodian's own mark, NOT an independent witness"
        # ---- third value: priced Buy / Sale of this security within three trading days
        wi = wide.index(date)
        span = set(wide[max(0, wi - 3):wi + 4])
        rows = G["tx"][c]
        trades = [(r["trade"], r["price"], r) for r in rows if r["kind"] in ("Buy", "Sale") and r["price"] and r["price"] > 0 and r["trade"] in span]
        values = [{"trade_date": r["trade"], "settle_date": r["settle"], "kind": r["kind"], "price": r["price"]} for _, _, r in sorted(trades, key=lambda x: x[0])]
        others = [{"trade_date": r["trade"], "kind": r["kind"], "price": r["price"]} for r in rows
                  if r["trade"] in span and r["kind"] not in ("Buy", "Sale") and r["price"] and r["price"] > 0]
        all_priced = [r for r in rows if r["kind"] in ("Buy", "Sale") and r["price"] and r["price"] > 0]
        near = sorted(all_priced, key=lambda r: abs(wide.index(r["trade"]) - wi) if r["trade"] in wide else 999)[:1]
        third = {"found": bool(values), "values": values,
                 "where_looked": "the silver transactions table beside the holdings table (every date partition, rows de-duplicated on TransactionID), rows of CUSIP %s; "
                                 "Buy and Sale rows with a Price above 0 and a trade date from %s to %s (three trading days either side of %s): %d. The table holds %d row(s) of this "
                                 "security in all, %d of them priced Buy or Sale rows%s"
                                 % (c, wide[max(0, wi - 3)], wide[min(len(wide) - 1, wi + 3)], date, len(values), len(rows), len(all_priced),
                                    ("; nearest priced Buy or Sale row: %s %s on %s (%d trading day(s) away)" % (near[0]["kind"], near[0]["price"], near[0]["trade"], abs(wide.index(near[0]["trade"]) - wi))
                                     if near and near[0]["trade"] in wide else "")),
                 "priced_rows_in_the_span_that_are_not_a_Buy_or_Sale": others,
                 "kind_of_security": KIND[tk], "kind_how_known": KIND_HOW[tk],
                 "what_a_trade_price_can_tell": ("a mutual fund's purchase or redemption is struck at the NAV of its trade date, so a Buy or Sale would equal the true close of that day and could say which witness holds it"
                                                 if KIND[tk] == "mutual_fund" else
                                                 "an exchange-traded security's trade price is an intraday price and need not equal a close; at most it brackets the day's range, it cannot date a close"),
                 "has_no_trade_so_nothing_here_to_apply": not values}
        # ---- series five trading days either side
        lo, hi = max(0, i - 5), min(len(ax) - 1, i + 5)
        days5 = ax[lo:hi + 1]
        # a repeated value at t in either witness
        def rep(S):
            return {"equals_prior_day": (S.get(date) is not None and S.get(prior) is not None and m.same(S[date], S[prior])),
                    "equals_next_day": (nxt is not None and S.get(date) is not None and S.get(nxt) is not None and m.same(S[date], S[nxt]))}
        sub = [d for d in ax if A.get(d) is not None and R.get(d) is not None and is_subcent(A[d])]
        series = {"dates": days5, "first_witness": [r4(A.get(d)) for d in days5], "second_witness": [r4(R.get(d)) for d in days5],
                  "custodian_mark_not_independent": [r4(M.get(d)) for d in days5],
                  "first_witness_value_repeated_at_t": rep(A), "second_witness_value_repeated_at_t": rep(R),
                  "witnesses_equal_on_the_day_at_1e-4": bool(A.get(date) is not None and R.get(date) is not None and m.same(A[date], R[date])),
                  "witnesses_equal_on_the_day_to_the_cent": bool(A.get(date) is not None and R.get(date) is not None and m.cent(A[date], R[date])),
                  "ib441_direction": next((x["direction"] for x in json.load(open(HERE.parent / "0.9.0_WK_IRPT_BCKEND~299" / "IB138-2_type_overlap_and_fund_check.json"))["one_day_off_detail"]
                                          if x["ticker"] == tk and x["date"] == date), None),
                  "sub_cent_first_witness_days_in_the_fetched_windows": len(sub),
                  "of_them_second_witness_equals_the_half_up_cent_rounding": sum(1 for d in sub if abs(half_up(A[d]) - R[d]) < 5e-5),
                  "sub_cent_days_listed": [{"date": d, "first_witness": r4(A[d]), "second_witness": r4(R[d])} for d in sub],
                  "custodian_mark_equals_first_witness_on_the_days_shown": all(M.get(d) is None or A.get(d) is None or m.same(M[d], A[d]) for d in days5)}
        # other value differences between the witnesses inside the five-day span, from the series (a fact, not a verdict)
        series["days_in_the_span_where_the_witnesses_differ_beyond_1e-4"] = [
            {"date": d, "first_witness": r4(A[d]), "second_witness": r4(R[d])} for d in days5 if A.get(d) is not None and R.get(d) is not None and not m.same(A[d], R[d])]
        # ---- distribution rows in the estate (Dividend, Dividend Reinvestment)
        dist = [{"trade_date": r["trade"], "kind": r["kind"], "trading_days_from_the_day": (wide.index(r["trade"]) - wi) if r["trade"] in wide else None}
                for r in rows if r["kind"] in ("Dividend", "Dividend Reinvestment") and r["trade"]]
        within = [x for x in dist if x["trading_days_from_the_day"] is not None and abs(x["trading_days_from_the_day"]) <= 3]
        nearest = sorted((x for x in dist if x["trading_days_from_the_day"] is not None), key=lambda x: abs(x["trading_days_from_the_day"]))[:1]
        distribution = {"within_three_trading_days": within, "nearest_in_the_estate": nearest[0] if nearest else None,
                        "how_read": "Dividend and Dividend Reinvestment rows of this CUSIP in the transactions table (kind and trade date only); no source was asked for distributions"}
        tr = [(d, p) for d, p, _ in trades]
        v, cl, why, ev = decide(KIND[tk], i, ax, A, R, tr)
        secdays.append({"ticker": tk, "cusip": c, "type_pair": typ.replace("Securities Issued by Registered Investment Companies or Business Development Companies", "RIC/BDC"),
                        "date": date, "first_witness": fw, "second_witness": sw, "custodian_mark": cm, "third_value": third, "series_either_side": series,
                        "distribution_on_or_beside_the_day": distribution, "verdict": v, "claim": cl, "reason": why, "deciding_evidence": ev})
    counts = {k: sum(1 for d in secdays if d["verdict"] == k) for k in ("FIRST_WITNESS_OFF", "SECOND_WITNESS_OFF", "CANNOT_BE_TOLD")}
    nc = [len(c["ticker_list"]) for c in calls]
    anc_meta = G["anchor_meta"].get("2026-10-09")
    # ---- the last day
    four = []
    for tk, c in CUSIP.items():
        a9, a8 = G["anchor"][c].get("2026-10-09"), G["anchor"][c].get("2026-10-08")
        four.append(a9 is not None and a8 is not None and m.same(a9, a8))
    out = {"the_five_are_those_of_ib_pr_441": [(d["ticker"], d["date"]) for d in secdays] == [(t, dd) for t, dd, _ in G["five"]] and len(secdays) == 5,
           "source_of_the_five": "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~299/IB138-2_type_overlap_and_fund_check.json, one_day_off_detail: 5 entries, read unchanged (SHM 2026-06-30, SHM 2026-07-20, MEIIX 2026-07-02, MISIX 2026-10-09, PZA 2026-07-31)",
           "first_witness_is": "the Schwab anchor's closing_price by CUSIP in its daily partition (the last row of the day where a CUSIP repeats; the repeats read identical)",
           "second_witness_is": "the reader's unadjusted Close (fetch_yahoo, read_yahoo_close), Yahoo Finance",
           "tolerance": "relative 1e-4 (and 'equal to the cent' stated beside it)",
           "security_days": secdays, "verdict_counts": counts,
           "last_day_first_witness_partition": {
               "is_the_prior_days": None, "claim": "absent", "securities_compared": 0, "equal_to_second_witness_same_day": 0, "equal_to_second_witness_prior_day": 0,
               "last_modified_utc": anc_meta["last_modified_utc"], "partition_objects": anc_meta["objects"], "partition_rows": anc_meta["rows_in_partition"],
               "how_read": "NOT COUNTED. The per-security, per-day classification for 2026-10-09 over the 894 securities needs the second witness's bars for the 890 tickers this cell may "
                           "not ask the reader for again; IB-pr-441's output (IB138-2_type_overlap_and_fund_check.json) holds counts by type and the five detail lines, not the per-security, per-day values, "
                           "and no scratch cache of that cell is on this box (its scratch folder under C:/dev is absent). So the three counts are 0 because nothing was compared, not because nothing matched. "
                           "What is read without a fetch: the first witness's partition object for 2026-10-09 was last modified at the time given (UTC); IB-pr-441 found, over all the securities that had a value on that "
                           "day, ONE security one-day-off on 2026-10-09 (MISIX; its type table shows 2026-10-09 with count 1 in the Inst column and in no other) - that cell's own finding, held here, not re-measured.",
               "ib441_finding_held": {"claim": "held", "finding": "one security read one-day-off on 2026-10-09 out of all that had a value that day (894 securities both witnesses carry, in all)", "from": "IB138-2_type_overlap_and_fund_check.json one_day_off_summary dates_by_count_top and one_day_off_detail"},
               "partition_object_is": "the first witness's (anchor) partition for 2026-10-09, listed and read for the four named CUSIPs only",
               "sample_of_four_not_a_count": "of the four named securities, %d had a first-witness value for 2026-10-09 equal to its 2026-10-08 value; four securities are not the population and no answer is drawn from them" % sum(four),
               "reading_for_the_reader": "IB-pr-441's one-day-off count does not bear on this question: a first-witness partition that were wholly the prior day's would read 'neither' against a correct second-witness bar for 2026-10-09 (the bar would match no first-witness value), not one-day-off; the per-day 'neither' count for that date is not in the trunk's outputs. For the one named security (MISIX) the first witness's 2026-10-09 value differs from its 2026-10-08 value, so that security's value is not the prior day's"},
           "fetch": {"calls": [{"call": k + 1, "tickers": n} for k, n in enumerate(nc)], "distinct_tickers_asked": sum(nc),
                     "tickers_asked": sorted(t for c in calls for t in c["ticker_list"]), "tickers_asked_more_than_once": sum(nc) - len({t for c in calls for t in c["ticker_list"]}),
                     "tickers_with_bars": sum(c["with_bars"] for c in calls), "tickers_with_no_bars": sum(c["no_bars"] for c in calls),
                     "window_asked": "2026-06-05 to 2026-10-13 inclusive (the reader script's constant, copied from IB-pr-441, which contains the face's window 2026-06-20 to 2026-10-13); the reader's latest bar is " + max(max(r) for r in G["reader"].values()),
                     "source": "Yahoo Finance through fetch_yahoo only; the 890 overlap tickers were not asked"},
           "control": {"planted": PLANTED, "read": ctl, "how": "decide() run on six planted security-days: three with a struck trade (first witness a day late, second a day late, trade matches neither) and three with none (second repeats, first repeats, half-cent rounding)"},
           "classes_admitted_by_this_cell": 0, "other_sources_asked": 0, "claims_regraded_in_product": False}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "IB140-1_five_days_third_value.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    # ---- the one-page read
    L = ["# IB-pr-443 -- the five one-day-off security-days against a third dated value (read only)", "",
         "Worker 0.9.0_WK_IRPT_BCKEND~301, round 140. First witness = the Schwab anchor's closing_price by CUSIP; second = the reader's unadjusted Close (Yahoo Finance, one call, 4 tickers). "
         "The custodian mark is the holdings partition's own mark (not independent). Nothing is built, served or admitted by this cell; no class is admitted.", ""]
    for d in secdays:
        f, s, k, tv, se = d["first_witness"], d["second_witness"], d["custodian_mark"], d["third_value"], d["series_either_side"]
        L += ["## %s on %s (%s; %s)" % (d["ticker"], d["date"], d["type_pair"], tv["kind_of_security"]),
              "- days: prior %s, day %s, next %s" % (f["dates"]["prior_day"], f["dates"]["day"], f["dates"]["next_day"]),
              "- first witness : %s | %s | %s" % (f["prior_day"], f["day"], f["next_day"]),
              "- second witness: %s | %s | %s" % (s["prior_day"], s["day"], s["next_day"]),
              "- custodian mark (not independent): %s | %s | %s" % (k["prior_day"], k["day"], k["next_day"]),
              "- third value: %s" % ("found: %s" % tv["values"] if tv["found"] else "NONE. " + tv["where_looked"]),
              "- distribution on or beside the day: %s; nearest in the estate: %s" % (d["distribution_on_or_beside_the_day"]["within_three_trading_days"] or "none within three trading days",
                                                                                   d["distribution_on_or_beside_the_day"]["nearest_in_the_estate"]),
              "- series, %s .. %s: first %s; second %s" % (se["dates"][0], se["dates"][-1], se["first_witness"], se["second_witness"]),
              "- VERDICT: %s (claim %s). %s" % (d["verdict"], d["claim"], d["reason"]),
              "- deciding evidence: %s" % (d["deciding_evidence"] or "none (no witness is named)"), ""]
    q = out["last_day_first_witness_partition"]
    L += ["## The last day (2026-10-09)", "- is_the_prior_days: %s (claim %s); compared %d; equal same day %d; equal prior day %d; first witness's partition last modified %s UTC"
          % (q["is_the_prior_days"], q["claim"], q["securities_compared"], q["equal_to_second_witness_same_day"], q["equal_to_second_witness_prior_day"], q["last_modified_utc"]),
          "- " + q["how_read"], "",
          "Verdict counts: %s. Fetch: %d call(s), %d tickers, %d asked more than once. Control: planted %s, read %s." % (counts, len(nc), sum(nc), out["fetch"]["tickers_asked_more_than_once"], PLANTED == ctl, ctl), ""]
    (out_dir / "IB140-1_FIVE_DAYS_THIRD_VALUE_READ.md").write_text("\n".join(L), encoding="utf-8")
    print(json.dumps({"verdicts": [(d["ticker"], d["date"], d["verdict"], d["claim"]) for d in secdays], "counts": counts, "control": ctl == PLANTED, "calls": nc}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
