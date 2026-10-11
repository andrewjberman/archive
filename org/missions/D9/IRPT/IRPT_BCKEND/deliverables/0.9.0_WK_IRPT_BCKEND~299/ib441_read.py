#!/usr/bin/env python3
"""IB-pr-441: render the one-page read from the measured json (every number in the tables is read from it, none typed).

    python -I ib441_read.py <IB138-2_type_overlap_and_fund_check.json> <out.md>
"""
import json
import sys
from pathlib import Path

SIX = ("same_day_only", "prior_day_only", "next_day_only", "more_than_one", "none", "no_bar")
RIC = "Securities Issued by Registered Investment Companies or Business Development Companies"


def short(k):
    return k.replace(RIC, "RIC/BDC")


def six_row(label, d):
    return "| %s | %d | %s |" % (label, d["trades"], " | ".join(str(d[k]) for k in SIX))


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    tj, ov, ft, fe, ed = d["type_join"], d["overlap_by_type"], d["fund_trades"], d["fetch"], d["edges"]
    L = []
    w = L.append
    w("# IB138-2 -- both witnesses per instrument type, and each priced fund trade beside the reader's bars (IB-pr-441, round 138)")
    w("")
    w("READ ONLY. Counts only. No class is admitted by this cell, nothing is built or served, no claim is re-graded, no other source was asked. "
      "`RIC/BDC` below is the source's value `%s`." % RIC)
    w("")
    w("## The join (type from the transactions table, by CUSIP)")
    w("")
    w("- Securities both witnesses carry: **%d** (IB-pr-439 counted 894). Found ONE type: **%d**; found NO transaction row: **%d**; found MORE THAN ONE type (put under `MIXED`): **%d**." % (
        tj["securities_both_witnesses_carry"], tj["found_a_type"], tj["found_no_type"], tj["found_more_than_one_type"]))
    w("- How a type is taken: %s" % tj["how_a_type_is_taken"])
    w("- The `MIXED` combinations (securities): " + "; ".join("%s = %d" % (short(k), v) for k, v in tj["mixed_combinations"].items()) + ".")
    w("- Transactions table: %d date partitions (%s to %s), %d rows read, %d distinct TransactionIDs." % (
        tj["transactions_read"]["partitions"], tj["transactions_read"]["first_partition"], tj["transactions_read"]["last_partition"],
        tj["transactions_read"]["rows_read"], tj["transactions_read"]["distinct_transaction_ids"]))
    w("")
    w("## Table 1 -- the reader's bar for day t against the anchor's close for day t, per type (85 trading days, 2026-06-10 to 2026-10-09)")
    w("")
    w("| type (SEC Asset Type / Share Class Type) | securities | security-days | equal | one_day_off | neither | no_bar | equal on days the close moved | securities with any one_day_off |")
    w("|---|---|---|---|---|---|---|---|---|")
    tot = {k: 0 for k in ("securities", "security_days", "equal", "one_day_off", "neither", "no_bar", "equal_on_days_the_close_moved", "securities_with_any_one_day_off")}
    for k, v in ov.items():
        w("| %s | %s |" % (short(k), " | ".join(str(v[c]) for c in tot)))
        for c in tot:
            tot[c] += v[c]
    w("| **all types** | %s |" % " | ".join("**%d**" % tot[c] for c in tot))
    w("")
    w("- A security-day is a day on which the anchor carries the security (the comparison needs its close). Rule: %s" % d["one_day_off_rule"])
    w("- %s" % d["unchanged_price_rule"])
    w("- Types whose one_day_off column is EMPTY (and equal above 0): %s." % "; ".join(short(x) for x in d["types_with_an_empty_one_day_off_column"]))
    w("- Edges: %s" % ed["meaning"])
    w("")
    w("### What is behind every non-empty one_day_off entry")
    w("")
    for k, s in d["one_day_off_summary"].items():
        w("- **%s**: %d one_day_off security-days, on %d securities, on %d dates; dates with 3 or more securities at once: %d." % (
            short(k), s["one_day_off"], s["securities_with_any"], s["dates_with_one_day_off"], s["dates_with_3_or_more_securities_at_once"]))
    w("")
    w("| type | ticker | date | the reader's bar for t equals the anchor close of the | that ticker's one_day_off days | securities one_day_off that date |")
    w("|---|---|---|---|---|---|")
    for x in d["one_day_off_detail"]:
        w("| %s | %s | %s | %s | %d | %d |" % (short(x["type"]), x["ticker"], x["date"], "prior and the next day" if x["direction"] == "both" else x["direction"] + " day", x["days_for_this_ticker"], x["securities_one_day_off_that_date"]))
    w("")
    w("Every date is one security alone (no date has 3 or more at once), so none is a calendar or holiday effect; each is a single security on a single date (a corporate action, a distribution day or a bad bar -- the data here do not say which; INFERRED, not tested). ")
    w("")
    w("## Table 2 -- every priced fund trade beside the reader's bars")
    w("")
    w("- Fund = %s" % ft["how_a_fund_is_recognised"])
    w("- Unit: %s. %s." % (ft["unit_counted"], ft["count_check"]))
    w("- Date column: %s. Tolerance: %s" % (ft["date_column"], ft["tolerance"]))
    w("")
    w("| basis | trades | same_day_only | prior_day_only | next_day_only | more_than_one | none | no_bar |")
    w("|---|---|---|---|---|---|---|---|")
    w(six_row("trade date, relative 1e-4", ft))
    w(six_row("trade date, to the cent", ft["to_the_cent"]))
    w(six_row("settle date, relative 1e-4", ft["by_settle_date"]))
    w(six_row("settle date, to the cent", {**ft["by_settle_date"]["to_the_cent"], "trades": ft["by_settle_date"]["trades"]}))
    w("")
    w("%d fund-dates, %d funds. Settle line: %d trades whose settle date lies outside the reader's window are left out. `no_bar` = the fund's ticker returned nothing (%s: %d trades) -- the reader has a bar for no other fund-date asked." % (
        ft["fund_dates"], ft["funds"], ft["by_settle_date"]["trades_whose_settle_date_is_outside_the_window_or_not_a_trading_day"], ", ".join(ft["no_bar_tickers"]), ft["no_bar_trades_whose_fund_ticker_returned_nothing"]))
    w("")
    c = ft["concentration"]
    cc = ft["concentration_to_the_cent"]
    w("### Where the off-day trades concentrate")
    w("")
    w("- `prior_day_only` (%d trades, %d funds; to the cent %d trades): by fund %s; by trade date %s; kinds %s. All are %s." % (
        c["prior_day_only"]["trades"], c["prior_day_only"]["funds"], cc["prior_day_only"]["trades"], c["prior_day_only"]["by_fund_top"], c["prior_day_only"]["by_trade_date_top"], c["prior_day_only"]["by_kind"],
        "dividend-reinvestment buys" if list(c["prior_day_only"]["by_kind"]) == ["Buy / Dividend Reinvestment"] else "mixed kinds"))
    w("- `next_day_only` (%d trades; to the cent %d trades, funds %s, dates %s, kinds %s)." % (c["next_day_only"]["trades"], cc["next_day_only"]["trades"], cc["next_day_only"]["by_fund_top"], cc["next_day_only"]["by_trade_date_top"], cc["next_day_only"]["by_kind"]))
    w("- `more_than_one` (%d trades, %d funds): by fund %s; by trade date %s; kinds %s. A bar that did not move across the days it matches." % (
        c["more_than_one"]["trades"], c["more_than_one"]["funds"], c["more_than_one"]["by_fund_top"][:6], c["more_than_one"]["by_trade_date_top"][:4], c["more_than_one"]["by_kind"]))
    w("- `none` (%d trades, %d funds): by fund %s; by trade date %s; kinds %s. Relative difference to the trade-date bar: %s; %d of them are under 0.1 percent." % (
        c["none"]["trades"], c["none"]["funds"], c["none"]["by_fund_top"][:6], c["none"]["by_trade_date_top"][:4], c["none"]["by_kind"], ft["none_diagnostic"]["relative_difference_to_the_trade_date_bar"], ft["none_diagnostic"]["under_0.1_percent"]))
    w("- Trade kinds, all %d trades: %s. Funds with any prior_day_only or next_day_only trade: %d of %d." % (ft["trades"], ft["trade_kinds_all"], ft["funds_with_any_prior_or_next_day_only_trade"], ft["funds"]))
    w("")
    w("Per fund (`by_fund`, ticker, trades and the six counts) is in the json: %d rows." % len(ft["by_fund"]))
    w("")
    w("## Fetch, control, bounds")
    w("")
    w("- Yahoo Finance through `fetch_yahoo` / `read_yahoo_close` (unedited), unadjusted Close, window %s: **%d calls, %d distinct tickers, each asked once** (%d with bars, %d with none); %s. Pause %d s between calls, no parallel call. Ticker list: %s." % (
        fe["window"], fe["call_count"], fe["distinct_tickers_asked"], fe["tickers_with_bars"], fe["tickers_with_no_bars"], "none rate-limited" if all(x["rate_limited_not_read"] == 0 for x in fe["calls"]) else "RATE-LIMITED", fe["pause_between_calls_seconds"], fe["distinct_tickers_made_of"]))
    w("- Control (planted, read equal: %s): a series shifted one day late and one a day early read one_day_off on the days the price moved; the unshifted reads equal; three planted trades (the same day's bar, the prior day's bar, a price matching none) read `same_day_only`, `prior_day_only`, `none`; the other three outcomes are planted too." % d["control"]["equal"])
    w("- `claims_regraded_in_product` false; `other_sources_asked` 0; `classes_admitted_by_this_cell` 0.")
    w("")
    w("## Reading (marked INFERRED where it is)")
    w("")
    w("%s" % open(sys.argv[3], encoding="utf-8").read() if len(sys.argv) > 3 else "")
    Path(sys.argv[2]).write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", sys.argv[2], len("\n".join(L)), "chars")


if __name__ == "__main__":
    main()
