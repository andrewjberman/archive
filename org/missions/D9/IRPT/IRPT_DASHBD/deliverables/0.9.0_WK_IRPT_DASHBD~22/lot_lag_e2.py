"""IRPT_DASHBD TO-DB-b-38 (round 25, workstream B) -- the lot-lag measurement behind LEG_LAG_DAYS. LOCAL; S3 is READ, never written.

Over the SAME 91 graded accounts and window as round 24 (2026-09-01..2026-10-05), finds for every trade that opens or relieves a lot
(buy, sell, in-kind arrival, in-kind departure) the custodian lot row it produced and the lag in TRADING days between the day the
transaction posts in fact_trn and the day the lot row posts in the lot tables. Run from the worktree root:

    python <this file>                 # about 4 minutes cold; writes LOT_LAG_E2.json beside this file, nothing to S3

THE LAG. Both ends are the custodian's partition (business) days, because that is what the producer's pending-leg rule counts
(`di - leg["di"]`): the trading days in (transaction day, lot-row day]. A trade posted on a non-trading day counts from there.
  sell     fact_trn trade rows grouped (account, order_number, cusip), credit side; the lot row is fact_rld, same key, the first
           partition day on which the closing quantity reaches the trade quantity (1e-3).
  buy      fact_trn trade rows grouped (account, cusip, trade_date), debit side; the lot row is the open lot (fact_uln/fact_ult)
           or an already-closed lot (fact_rld) of the same account and security acquired on the trade date, first partition day
           on which their summed quantity reaches the trade quantity (1e-3).
  in kind  the producer's own matcher (`apply_inkind_reference`) with the bound removed (LEG_LAG_DAYS lifted to 30), so the lag it
           reports is the lag the data shows and not the bound under test; its `lag_trading_days` is read as is.
A trade with no lot row in the read window (the lot tables are read to 10 trading days past the window's last day) is `unmatched`.
ASCII only.
"""
import bisect
import json
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "lib"))
import account_activity_lots as aal  # noqa: E402
import account_return_daily as ard  # noqa: E402
import boto3  # noqa: E402
import pandas as pd  # noqa: E402
import trading_calendar as tc  # noqa: E402
from botocore.config import Config  # noqa: E402

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R23 = ROOT / D / "0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"
OUT = ROOT / D / "0.9.0_WK_IRPT_DASHBD~22/LOT_LAG_E2.json"
QTY = 1e-3
LIFTED_BOUND = 30
EXTEND_TRADING_DAYS = 10
PCTS = (50, 90, 95, 99)


def percentile(sorted_vals, p):
    """Nearest-rank percentile of a sorted list of ints."""
    k = max(1, -(-len(sorted_vals) * p // 100))
    return sorted_vals[int(k) - 1]


def main():
    rec = json.loads(R23.read_bytes().decode("utf-8"))
    days, sample = rec["days"], rec["accounts"]
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    pad = int(src.get("account_id_zero_pad") or 0)

    # ---- the 91 graded accounts and the in-kind legs, by the producer with the bound lifted
    aal.LEG_LAG_DAYS = LIFTED_BOUND
    tables, run = aal.compute_local(s3, days, sample, workers=12)
    rows = tables[aal.TABLE_ACTIVITY]
    graded = []
    for a in sorted({r["account_id"] for r in rows}):
        mine = sorted(r["business_date"] for r in rows if r["account_id"] == a)
        if aal.window_reconciliation(rows, a, mine[0], days[-1]):
            graded.append(a)
    keep = set(graded)
    inkind = run["inkind"]

    # ---- own reads: trades in the window, lot tables to 10 trading days past it
    first_prev = str(tc.prev_trading_day(days[0]))[:10]
    end_ext = str(tc.trading_days_between(days[-1], str(pd.Timestamp(days[-1]) + pd.Timedelta(days=30))[:10])[EXTEND_TRADING_DAYS])[:10]
    cal = [str(d)[:10] for d in tc.trading_days_between("2026-08-01", "2026-12-31")]

    def tdays(a, b):
        return bisect.bisect_right(cal, b) - bisect.bisect_right(cal, a)

    trn_days = [d for d in ard.partition_days(s3, src["bucket"], src["transactions_prefix"]) if first_prev < d <= days[-1]]
    ur, rl = aal.LOT_SOURCE["unrealized"], aal.LOT_SOURCE["realized"]
    uln_days = {t: [d for d in ard.partition_days(s3, src["bucket"], aal.lot_prefix(src, t)) if first_prev <= d <= end_ext]
                for t in ur["tables"]}
    rld_days = [d for d in ard.partition_days(s3, src["bucket"], aal.lot_prefix(src, rl["table"])) if first_prev < d <= end_ext]
    lot_days = sorted(set(uln_days["fact_uln"]) | set(uln_days["fact_ult"]))

    def norm(frame):
        acct = frame["account_id"].astype(str).str.strip().str.zfill(pad)
        return frame[acct.isin(keep)].assign(account_id=acct[acct.isin(keep)])

    tcols = ["account_id", "tr_cd", "sb_cd", "debit_credit", "cusip", "quantity", "net_amount", "trade_date", "order_number"]

    def one_trn(day):
        f = aal.read_day(s3, src, "fact_trn", day, columns=tcols)
        if f is None:
            return day, None
        f = norm(f)
        return day, f[f["tr_cd"].astype(str).str.strip().str.upper() == "TR"]

    ucols = ["account_id", "cusip", "current_quantity", "acquired_date", "orgpurch_date"]

    def one_lots(args):
        table, day = args
        f = aal.read_day(s3, src, table, day, columns=ucols)
        return table, day, None if f is None else norm(f)

    rcols = ["account_id", "cusip", "closing_quantity", "acquired_date", "orgpurch_date", "order_number", "closing_date"]

    def one_rld(day):
        f = aal.read_day(s3, src, rl["table"], day, columns=rcols)
        return day, None if f is None else norm(f)

    with ThreadPoolExecutor(12) as pool:
        trn = dict(pool.map(one_trn, trn_days))
        lots = defaultdict(dict)
        for table, day, f in pool.map(one_lots, [(t, d) for t in ur["tables"] for d in uln_days[t]]):
            lots[day][table] = f
        rld = dict(pool.map(one_rld, rld_days))

    # open-lot quantity per (day, account, cusip, acquired_date)
    open_q = defaultdict(float)               # keyed by acquired_date
    open_o = defaultdict(float)               # keyed by orgpurch_date (a reinvested lot carries the trade date there)
    for day, by_t in lots.items():
        for f in by_t.values():
            if f is None:
                continue
            q = pd.to_numeric(f["current_quantity"], errors="coerce").fillna(0.0)
            for a, c, ad, od, v in zip(f["account_id"], f["cusip"].astype(str).str.strip(), f["acquired_date"].astype(str).str[:10],
                                       f["orgpurch_date"].astype(str).str[:10], q):
                open_q[(day, a, c, ad)] += float(v)
                open_o[(day, a, c, od)] += float(v)
    closed_q = defaultdict(float)             # (day, account, cusip, acquired_date) -> quantity closed that day
    closed_o = defaultdict(float)             # the same keyed by orgpurch_date
    sell_q = defaultdict(float)               # (day, account, order, cusip) -> quantity closed that day
    for day, f in rld.items():
        if f is None:
            continue
        q = pd.to_numeric(f["closing_quantity"], errors="coerce").fillna(0.0)
        for a, c, ad, od, o, v in zip(f["account_id"], f["cusip"].astype(str).str.strip(), f["acquired_date"].astype(str).str[:10],
                                      f["orgpurch_date"].astype(str).str[:10], f["order_number"].astype(str).str.strip(), q):
            closed_q[(day, a, c, ad)] += float(v)
            closed_o[(day, a, c, od)] += float(v)
            sell_q[(day, a, o, c)] += float(v)

    # ---- trades -> groups
    sells, buys = {}, {}
    for day, f in trn.items():
        if f is None or not len(f):
            continue
        q = pd.to_numeric(f["quantity"], errors="coerce").fillna(0.0).abs()
        for a, dc, c, o, td, v in zip(f["account_id"], f["debit_credit"].astype(str).str.strip().str.upper().str[:1],
                                      f["cusip"].astype(str).str.strip(), f["order_number"].astype(str).str.strip(),
                                      f["trade_date"].astype(str).str[:10], q):
            if dc == "C":
                g = sells.setdefault((a, o, c), {"day": day, "q": 0.0})
            else:
                g = buys.setdefault((a, c, td), {"day": day, "q": 0.0})
            g["day"] = min(g["day"], day)
            g["q"] += float(v)

    counts = {"sell": Counter(), "buy": Counter(), "in_kind_arrival": Counter(), "in_kind_departure": Counter()}
    unmatched = {"sell": [], "buy": [], "in_kind_arrival": [], "in_kind_departure": []}
    totals = {k: 0 for k in counts}
    via = Counter()

    for (a, o, c), g in sells.items():
        totals["sell"] += 1
        cum, hit = 0.0, None
        for d in rld_days:
            if d < g["day"]:
                continue
            cum += sell_q.get((d, a, o, c), 0.0)
            if cum + QTY >= g["q"] and cum > 0:
                hit = d
                break
        if hit is None:
            unmatched["sell"].append("%s/%s/%s@%s" % (a, o, c, g["day"]))
        else:
            counts["sell"][tdays(g["day"], hit)] += 1

    for (a, c, td), g in buys.items():
        totals["buy"] += 1
        hit = None
        for keyed, o_q, c_q in (("acquired", open_q, closed_q), ("orgpurch", open_o, closed_o)):
            for d in lot_days:
                if d < g["day"]:
                    continue
                have = o_q.get((d, a, c, td), 0.0) + sum(c_q.get((x, a, c, td), 0.0) for x in rld_days if g["day"] <= x <= d)
                if have > 0 and have + QTY >= g["q"]:
                    hit = d
                    break
            if hit is not None:
                break
        if hit is None:
            unmatched["buy"].append("%s/%s/%s@%s" % (a, c, td, g["day"]))
        else:
            counts["buy"][tdays(g["day"], hit)] += 1
            via[keyed] += 1

    for m in inkind["matched_arrivals"]:
        totals["in_kind_arrival"] += 1
        counts["in_kind_arrival"][int(m["lag_trading_days"])] += 1
    for m in inkind["matched_departures"]:
        totals["in_kind_departure"] += 1
        counts["in_kind_departure"][int(m["lag_trading_days"])] += 1
    for u in inkind["unmatched"]:
        if u.get("reason") == "IN_KIND_DEPARTURE_QUANTITY" or (u.get("reason") == "IN_KIND_LEG_NOT_POSTED_BY_THE_LAST_DAY" and u.get("side") == -1):
            totals["in_kind_departure"] += 1
            unmatched["in_kind_departure"].append("%s/%s@%s:%s" % (u.get("account_id"), u.get("cusip"), u.get("day"), u["reason"]))
        elif u.get("reason") in ("IN_KIND_ARRIVAL_QUANTITY", "IN_KIND_LEG_NOT_POSTED_BY_THE_LAST_DAY"):
            totals["in_kind_arrival"] += 1
            unmatched["in_kind_arrival"].append("%s/%s@%s:%s" % (u.get("account_id"), u.get("cusip"), u.get("day"), u["reason"]))

    allc = Counter()
    for c in counts.values():
        allc.update(c)
    lags = sorted(k for k, v in allc.items() for _ in range(v))
    n = len(lags)
    pct = {"p%d" % p: percentile(lags, p) for p in PCTS}
    pct["max"] = lags[-1]
    un_all = [x for k in unmatched for x in unmatched[k]]
    # THE CHOICE: the smallest whole number of trading days that covers every matched lag. The bound only decides when an unposted
    # in-kind leg is LISTED as unmatched (a leg is never bent to fit), so no margin is added on top of what the data shows.
    cover = 100.0
    k = next(d for d in range(0, lags[-1] + 1) if 100.0 * sum(1 for x in lags if x <= d) / n >= cover)
    share = 100.0 * sum(1 for x in lags if x <= k) / n
    out = {
        "task_order": "IRPT_DASHBD.TO-DB-b-38", "worker": "0.9.0_WK_IRPT_DASHBD~22", "window": "%s..%s" % (days[0], days[-1]),
        "accounts_graded": len(graded), "lot_tables_read_to": end_ext,
        "lags": {"n": n, "percentiles": pct, "counts_by_days": {str(k): allc[k] for k in sorted(allc)}},
        "by_kind": {k: {"trades": totals[k], "matched": sum(counts[k].values()), "unmatched": len(unmatched[k]),
                        "counts_by_days": {str(d): counts[k][d] for d in sorted(counts[k])}} for k in counts},
        "unmatched": {"count": len(un_all), "examples": un_all[:20],
                      "by_kind": {k: len(v) for k, v in unmatched.items()}},
        "leg_lag_days": k, "covered_percentile": round(share, 4),
        "choice_rule": "the smallest whole number of trading days k with 100% of the matched lags at or under k (k = the maximum "
                       "matched lag); no margin added, because a leg past the bound is listed unmatched and never bent",
        "buys_matched_by": dict(via),
        "producer_bound_lifted_to": LIFTED_BOUND,
        "inkind_audit_unmatched_reasons": dict(Counter(u.get("reason") for u in inkind["unmatched"])),
    }
    OUT.write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    print("accounts", len(graded), "n", n, pct)
    print("by kind", {k: (totals[k], sum(counts[k].values()), len(unmatched[k])) for k in counts})
    print("choice", k, share, "buys matched by", dict(via))
    print("counts", out["lags"]["counts_by_days"])
    print("unmatched examples", un_all[:6], "inkind reasons", out["inkind_audit_unmatched_reasons"])


if __name__ == "__main__":
    main()
