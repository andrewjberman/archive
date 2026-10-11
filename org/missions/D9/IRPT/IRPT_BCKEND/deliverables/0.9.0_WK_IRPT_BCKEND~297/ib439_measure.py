#!/usr/bin/env python3
"""IB-pr-439 measure.  Read only.  Counts only: no account key, balance or single account's holding is written.

    python -I ib439_measure.py <partition_cache> <phase1.pkl> <fundtx.json> <out.json>
    python -I ib439_measure.py --control      the planted overlap-classifier control

ITEM 1 reads the column list and the candidate-column value counts the fetch cached for every source partition, restricted to the 85 graded days.
ITEM 2's CLASSIFIER (classify_day) is defined and controlled here; it is DRAWN into a table only if a type field exists (it does not: no fetch is made).
ITEM 3 with no admitted class is the rule in force: the totals and the serving rule are taken from phase 1 (the unchanged v0.35 / cash-rule modules).
"""
from __future__ import annotations

import collections
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / "0.9.0_WK_IRPT_BCKEND~293"))
import ib429_claims_v035 as v35  # noqa: E402

TOL = 1e-4
FPNIX_CUSIP = "30254T643"
COLS4 = ("equal", "one_day_off", "neither", "no_bar")


def same(a, b):
    """relative 1e-4, the tolerance of ib429_claims.same."""
    return abs(a - b) <= TOL * max(abs(a), abs(b))


def classify_day(reader, anchor, tdays, i):
    """The reader's bar for trading day tdays[i] against the anchor's close for it.  reader / anchor: {day: value} (a missing key = no value).
    equal; one_day_off (not equal for t, and the bar equals the anchor close of the prior OR the next trading day); neither; no_bar."""
    t = tdays[i]
    r, a = reader.get(t), anchor.get(t)
    if r is None:
        return "no_bar"
    if a is not None and same(r, a):
        return "equal"
    for j in (i - 1, i + 1):
        if 0 <= j < len(tdays):
            n = anchor.get(tdays[j])
            if n is not None and same(r, n):
                return "one_day_off"
    return "neither"


def control_run():
    """Known by construction.  Trading days d0..d6, graded d1..d5.  A: reader labels one day LATE (bar(t) = close(t-1)); B: reader = anchor;
    C: a missing bar and a wrong price; D: reader labels one day EARLY (bar(t) = close(t+1))."""
    td = ["d0", "d1", "d2", "d3", "d4", "d5", "d6"]
    anc = {"A": [10, 11, 12, 12, 13, 14, 15], "B": [20, 21, 22, 23, 24, 25, 26], "C": [30, 31, 32, 33, 34, 35, 36], "D": [40, 41, 42, 42, 43, 44, 45]}
    rdr = {"A": {td[i]: anc["A"][i - 1] for i in range(1, 6)}, "B": {td[i]: anc["B"][i] for i in range(1, 6)},
           "C": {"d1": 31, "d3": 99, "d4": 34, "d5": 35}, "D": {td[i]: anc["D"][i + 1] for i in range(1, 6)}}
    out = {}
    for s in anc:
        a = {td[i]: v for i, v in enumerate(anc[s])}
        res = [classify_day(rdr[s], a, td, i) for i in range(1, 6)]
        c = collections.Counter(res)
        moved = sum(1 for k, i in enumerate(range(1, 6)) if res[k] == "equal" and a[td[i]] != a[td[i - 1]])
        out[s] = {**{k: c.get(k, 0) for k in COLS4}, "equal_on_days_the_close_moved": moved}
    return out


# A: bars d1..d5 = 10,11,12,12,13 against anchor 11,12,12,13,14 -> off, off, equal (12=12, close unchanged), off, off.
# D: bars d1..d5 = 42,42,43,44,45 against anchor 41,42,42,43,44 -> off (next close 42), equal (42=42; close moved 41->42 so it counts), off, off, off.
PLANTED = {"A": {"equal": 1, "one_day_off": 4, "neither": 0, "no_bar": 0, "equal_on_days_the_close_moved": 0},
           "B": {"equal": 5, "one_day_off": 0, "neither": 0, "no_bar": 0, "equal_on_days_the_close_moved": 5},
           "C": {"equal": 3, "one_day_off": 0, "neither": 1, "no_bar": 1, "equal_on_days_the_close_moved": 3},
           "D": {"equal": 1, "one_day_off": 4, "neither": 0, "no_bar": 0, "equal_on_days_the_close_moved": 1}}


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    cache, p1, ftx, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    P = pickle.load(open(p1, "rb"))
    graded = P["graded"]
    fx = json.load(open(ftx))

    def load(kind, day):
        return pickle.load(open(cache / ("%s_%s.pkl" % (kind, day)), "rb"))

    # ---- item 1
    cols, per_part_schema, cand, rows_read = set(), collections.Counter(), collections.defaultdict(collections.Counter), 0
    held, tick_of, anchor_any, fpn = set(), collections.defaultdict(set), set(), set()
    fpn_by_type = collections.defaultdict(set)

    def load_anchor(day):
        t = load("anc", day)
        if t is None:
            return None
        return {(c or "").strip(): float(p) for c, p in zip(t["cusip"], t["closing_price"]) if (c or "").strip() and p is not None and float(p) > 0}
    for d in graded:
        s = load("src", d)
        cols |= set(s["_schema"])
        per_part_schema[tuple(s["_schema"])] += 1
        rows_read += len(s["CUSIP"])
        assert s["_rows"] == len(s["CUSIP"])
        for c, v in s["_cand"].items():
            for k, n in v.items():
                cand[c][k] += n
        a = load("anc", d)
        anc_today = set()
        if a is not None:
            for c, p in zip(a["cusip"], a["closing_price"]):
                c = (c or "").strip()
                if c and p is not None and float(p) > 0:
                    anc_today.add(c)
        anchor_any |= anc_today
        for k, c in enumerate(s["CUSIP"]):
            c = (c or "").strip()
            if not c:
                continue
            held.add(c)
            for x in (s["Ticker"][k], s["Symbol"][k]):
                x = None if x is None else str(x).strip()
                if x and x.lower() != "none" and x.upper() != c.upper():
                    tick_of[c].add(x)
            if c == FPNIX_CUSIP:
                fpn.add((s["AccountID"][k], d))
        if any((c or "").strip() == FPNIX_CUSIP for c in s["CUSIP"]):
            A, B = load_anchor(d), load_anchor(P["prev_of"][d])
            if A is None or B is None:
                A = B = None
            types = v35.typed_rows(s["CUSIP"], s["Market Value"], s["Units"], s["Cash Equivalent"], A, B)
            for k, c in enumerate(s["CUSIP"]):
                if (c or "").strip() == FPNIX_CUSIP:
                    fpn_by_type[types[k]].add((s["AccountID"][k], d))
    both = {c for c in held if c in anchor_any}
    both_t = {c for c in both if tick_of.get(c)}
    tickers = {t for c in both_t for t in tick_of[c]}
    first_tickers = len({sorted(tick_of[c])[0] for c in both_t})
    schema_variants = [{"partitions": n, "columns": len(k), "missing_vs_union": sorted(cols - set(k))} for k, n in per_part_schema.most_common()]
    columns_read = sorted(cols)

    def with_col(name):
        return sum(n for k, n in per_part_schema.items() if name in k)
    cands = [
        {"column": "Cash Equivalent", "values": dict(cand["Cash Equivalent"]), "verdict": "NOT a type: a two-valued flag (true/false) saying whether a row is a cash equivalent; the order rules a cash-equivalent flag alone is not an instrument type; it does not separate stocks, funds and bonds"},
        {"column": "Holding Supervised", "values": dict(cand["Holding Supervised"]), "verdict": "NOT a type: states whether the holding is supervised by the advisor (Supervised/Unsupervised); present in %d of %d partitions only" % (with_col("Holding Supervised"), len(graded))},
        {"column": "Account Supervised", "values": dict(cand["Account Supervised"]), "verdict": "NOT a type: the same flag at account grain; present in %d of %d partitions only" % (with_col("Account Supervised"), len(graded))},
        {"column": "Asset Display Name", "values": dict(cand["Asset Display Name"]), "verdict": "NOT a type: a name column, null on every row read"},
        {"column": "_source / _feed / _schema_version", "values": {"_source": dict(cand["_source"]), "_feed": dict(cand["_feed"]), "_schema_version": dict(cand["_schema_version"])}, "verdict": "NOT a type: lineage columns, one value each (the feed, not the instrument)"},
        {"column": "Expense Ratio", "values": dict(cand["Expense Ratio"]), "verdict": "NOT a type: a number, non-null on %d rows; a non-null ratio tends to sit on funds, but it names no kind and using it would be inventing a type" % cand["Expense Ratio"]["nonnull"]},
        {"column": "Last Dividend", "values": dict(cand["Last Dividend"]), "verdict": "NOT a type: a number (the last dividend), not a kind"},
        {"column": "Alternative Identifier", "values": dict(cand["Alternative Identifier"]), "verdict": "NOT a type: a secondary identifier, non-null on few rows"},
        {"column": "Asset Name / Original Asset Name / Ticker / Symbol / CUSIP / AssetID", "values": "free text or identifiers (high cardinality)", "verdict": "NOT a type: names and identifiers; the order forbids inventing a type from names or tickers"},
    ]
    # ---- item 3: the rule in force (no class admitted)
    claims = {a: dict(v) for a, v in P["claims_cash"].items()}
    sv = v35.serve_v035(claims, graded)
    pa = [v for v in sv["per_account"].values() if v[0]]
    assert (sv["eligible"], sv["served"], sv["blank"]) == (P["serve_cash"]["eligible"], P["serve_cash"]["served"], P["serve_cash"]["blank"])
    tc = P["tally_cash"]
    fp_days = len(fpn)
    fp_ad = P["secs"].get(FPNIX_CUSIP, {}).get("account_days")
    ft = dict(fx)
    ft["source_found"] = True
    ft["table"] = "blackdiamond/<scope>/silver/fact_transactions/ (date=YYYY-MM-DD partitions; the sibling of the holdings table fact_holdings/ under the same silver parent)"
    ft["silver_tables_beside_the_holdings_table"] = ["fact_allocations", "fact_allocations_s2", "fact_holdings", "fact_holdings_s2", "fact_model_assignment", "fact_model_blend",
                                                      "fact_model_definition", "fact_model_roster", "fact_realized", "fact_realized_s2", "fact_transactions", "fact_transactions_s2",
                                                      "fact_unrealized", "fact_unrealized_s2"]
    ft["first_date"] = ft["first_trade_date"]
    ft["last_date"] = ft["last_trade_date"]
    ft["first_date_is"] = "the earliest and latest Trade Date of the de-duplicated rows; the partitions run %s to %s" % (ft["first_partition_date"], ft["last_partition_date"])
    ft["other_transaction_table_examined"] = {
        "table": "commonwealth/<scope>/silver/transactions/ (the table the ADVI_COTBKF scripts read via commonwealth_crosswalk._silver_prefix)",
        "used": False,
        "why": "its schema carries Quantity and Amount but no Price column (25 columns read from the 2026-06-23 partition: Advisor_ID .. source_record), so a purchase or redemption 'with a price' is not stated there; 14 as-of partitions listed, none read beyond one schema and value-count sample; the table beside the holdings table carries Price, Trade Date, Transaction Type and Sub Type",
    }
    ctl = control_run()
    doc = {
        "same_account_days_read": bool(P["same_cash"] and P["same_pre"]),
        "same_account_days_read_basis": "phase 1 (the unchanged IB-pr-438 phase-1 script over the same partitions) totals under the cash rule equal UNGRADEABLE 43,310; ACCT_PRIOR_DATE 55; ACCT_OWN_DATE 19,832; NOTHING_TO_GRADE 13,599; present 76,796, and its v0.35 totals before the cash rule equal IB-pr-435's",
        "graded_days": len(graded), "first_graded_day": graded[0], "last_graded_day": graded[-1],
        "instrument_type_field": {
            "present": False, "name": None, "values": {}, "rows_read": rows_read,
            "partitions_read": len(graded), "columns_read": columns_read, "schema_variants_across_partitions": schema_variants,
            "candidates_examined": cands,
            "which_is_the_type_field_and_why": "none: no column of the source states what KIND of instrument a row is. The nearest, Cash Equivalent, is a two-valued cash flag (the order: a flag alone is not a type). Nothing was derived from names, tickers or Expense Ratio.",
        },
        "stopped_no_type_field": True,
        "stopped_note": "Per the order: no overlap table is drawn; the sizing is taken with no class admitted (it equals the rule in force); no Yahoo Finance call was made.",
        "securities_both_witnesses_carry": {
            "count": len(both_t), "basis": "securities (CUSIP) held by an account of the source on one or more of the 85 days (%d), carried by the Schwab anchor with a positive closing_price on one or more of the 85 days (%d of those), and with a ticker in the source that is not the CUSIP itself (%d of those)" % (len(held), len(both), len(both_t)),
            "held_by_an_account": len(held), "carried_by_the_anchor_too": len(both), "with_a_ticker": len(both_t),
            "distinct_tickers_they_would_need": len(tickers), "distinct_tickers_by_first_ticker_per_security": first_tickers,
            "over_the_1500_ticker_stop": len(tickers) > 1500,
            "note": "counted from the cached source and anchor partitions only (S3 reads); no ticker was asked of any reader because the order stops at the missing type field before the fetch",
        },
        "fetch": {"calls": [], "call_count": 0, "distinct_tickers_asked": 0, "tickers_asked_more_than_once": 0,
                  "why_no_calls": "no instrument-type field exists, so the order draws no overlap table and goes straight to the sizing; nothing is asked of Yahoo Finance",
                  "edge_bars_had": "not applicable: no reader series was fetched"},
        "overlap_by_type": {},
        "one_day_off_rule": "For a security and a trading day t of the 85: the reader's bar for t is compared with the Schwab anchor's closing_price for t at relative 1e-4. equal = within that tolerance. Not equal, and the reader's bar for t is within that tolerance of the anchor's close for the PRIOR or the NEXT trading day = one_day_off. Otherwise neither. No reader bar for t = no_bar. (The classifier is defined and controlled in ib439_measure.py; no table is drawn for want of a type field.)",
        "unchanged_price_rule": "When the anchor's close for t equals its close for the prior (or next) trading day, the reader's bar equals the anchor's for t and the day is `equal`, never `one_day_off` (equal is tested first); it is counted in `equal` but NOT in `equal_on_days_the_close_moved`, because on an unchanged day a correct date label and a shifted one read the same.",
        "types_with_an_empty_one_day_off_column": [],
        "one_day_off_detail": [],
        "sizing_under_v038": {
            "what_is_assumed": "A SIZING the CTO rules on, not a stamp. classes_admitted is, by the rule of this cell, the source's type values that are exchange-traded securities AND whose one-day-off column is empty; the source states no instrument type, so no value can be taken, classes_admitted is empty, no security is admitted to YAHOO_CLOSE (a security whose type the source does not state is in no admitted class), mutual funds are not admitted whatever a column reads, and the sizing equals the rule in force. The anchor grades every security it carries, as today. Nothing is re-graded in the product.",
            "classes_admitted": [], "mutual_funds_admitted": False,
            "account_days": {"present": tc["present"], "UNGRADEABLE": tc["UNGRADEABLE"], "ACCT_PRIOR_DATE": tc["ACCT_PRIOR_DATE"], "ACCT_OWN_DATE": tc["ACCT_OWN_DATE"], "NOTHING_TO_GRADE": tc["NOTHING_TO_GRADE"]},
            "serving_rule": {"eligible": sv["eligible"], "served": sv["served"], "blank": sv["blank"], "blank_share_percent": round(100.0 * sv["blank"] / sv["eligible"], 3),
                             "accounts_never_served": sum(1 for e, s_ in pa if s_ == 0), "accounts_with_eligible_days": len(pa)},
            "rule_in_force": {"blank_share_percent": 58.2, "accounts_never_served": 382, "of_accounts": 999, "equal_to_the_sizing": True},
            "withdrawn_figure_basis_for_reference_only": {"basis": "funds counted as graded by the reader (IB-pr-438's sizing under the withdrawn v0.37 text)", "blank_share_percent": 36.989, "accounts_never_served": 181,
                                                         "status": "WITHDRAWN by ADDENDUM v0.38; the blank share with two witnesses is not known and lies between 37.0 and 58.2 percent; with no class admitted it is the upper end, 58.2"},
            "fpnix_account_days": fp_ad,
            "fpnix_account_days_note": "account-days (one digested account on one of the 85 days) on which the account holds a PRICED row of the fund FPNIX (CUSIP %s) that the anchor does not carry that day (an outside-anchor row, the row kind that blocks the claim and for which the reader returned no data), under the cash rule: this run %s, the figure IB-pr-438 stated (12,115). Beside it, every kind of FPNIX row on any of the 85 days: %s (union of account-days %d); a no_price row (no usable market value or units) and a row the anchor grades do not wait on the reader." % (FPNIX_CUSIP, fp_ad, json.dumps({k: len(v) for k, v in sorted(fpn_by_type.items())}), fp_days),
            "fpnix_account_days_by_row_kind": {k: len(v) for k, v in sorted(fpn_by_type.items())}, "fpnix_account_days_any_row": fp_days,
        },
        "fund_transactions": ft,
        "fund_transactions_basis": "no instrument-type field exists, so a 'fund' is one of the nine funds of IB-pr-436 (matched by CUSIP); a purchase or redemption = Transaction Type Buy or Sale (Sub Type Buy, Sale or Redemption) with Price above 0, de-duplicated on TransactionID over every date partition of the table; 'inside the 85 days' = Trade Date is one of the 85 graded trading days. No transaction price was compared with any bar.",
        "control": {"planted": PLANTED, "read": ctl, "equal": ctl == PLANTED,
                    "what_it_is": "four planted securities over trading days d0..d6 (graded d1..d5): A reader one day LATE, B reader = anchor, C one missing bar and one wrong price, D reader one day EARLY; the shifted ones read one_day_off on the days the price moved, B reads equal"},
        "claims_regraded_in_product": False, "other_sources_asked": 0,
    }
    out.write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print("wrote", out, "rows_read", rows_read, "both", len(both_t), "tickers", len(tickers), "control equal", ctl == PLANTED, "fpnix", fp_days, fp_ad, "serving", doc["sizing_under_v038"]["serving_rule"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
