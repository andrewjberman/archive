"""IRPT_DASHBD (workstream F-SHIP, ~F2): the S6 CASH-MOVE read the CTO asked for (msg 9640), READ-ONLY and VALUES-FREE (counts only; GET only; no account id or amount is kept
or written).

  python <this file> <out.json>

For each of the S6 events on the LATEST Orion transactions snapshot (the Complete lines of `Dividend Paid from Cash`, keyed on account, transDate and absolute amount X),
it reads the account's positions on the event day and on the day before (the Orion silver `fact_positions` daily partitions: `currentValue`, `isCustodialCash`) and
compares the change across the event day with X, within one cent:

  cash change    = sum of currentValue of the account's custodial-cash positions on the event day minus the same on the day before;
  total change   = sum of currentValue of ALL the account's positions on the event day minus the day before (it also carries market moves).

Each change is bucketed as: about -2X, about -X, about 0, about +X, about +2X, or other (within 0.01 of the target); and the events whose positions are missing on either day
are counted apart. The same bucketing is printed for the events that have a positive income-class partner and for those that have none.

Round 135 (CTO msg 9649): the events whose cash change on the event day is NOT about -X are RE-READ one trading day either side (the window shifted to the previous and to the
next trading day: the cash change across that day, against the same X). `agreement` prints the events whose cash fell by about X on the event day, and the total once
the shifted windows are counted; below 90 of the events stops the Inflection release.

Round 135 (CTO msg 9659): `reinvestment_by_cash_group` counts, for each event group (cash fell by about X; cash flat; other), the events with a Complete `Income Reinvested` line, a
Complete `Buy Exchange` line, either, or neither, on the SAME account and day with an absolute amount within one cent of X (one snapshot).
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from collections import Counter
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402
import trading_calendar as tc  # noqa: E402

TOL = 0.01
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_day(bucket, prefix, day, columns):
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                tables.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()), columns=columns))
    return pa.concat_tables(tables, promote_options="default").to_pandas() if tables else None


def bucket_of(change, x):
    for label, target in (("-2X", -2 * x), ("-X", -x), ("0", 0.0), ("+X", x), ("+2X", 2 * x)):
        if abs(change - target) <= TOL:
            return label
    return "other"


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    tx_prefix, pos_prefix = rest + "fact_transactions/", rest + "fact_positions/"
    con = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
    income = {m["source_value"] for m in con["source_mapping"] if m["firm"] == "inflection" and m["flow_class"] == "INCOME"}
    latest = ard.partition_days(s3, bucket, tx_prefix)[-1]
    lf = read_day(bucket, tx_prefix, latest, ["status", "transDate", "accountId", "transAmount", "transactionDescription"])
    c = lf[lf["status"] == "Complete"]
    a = c[c["transactionDescription"] == "Dividend Paid from Cash"]
    inc = c[c["transactionDescription"].isin(income)]
    inc_pos = {(r.accountId, r.transDate, round(abs(r.transAmount), 6)) for r in inc.itertuples() if r.transAmount > 0}
    events = [(r.accountId, r.transDate, round(abs(r.transAmount), 6)) for r in a.itertuples()]
    need_days = set()
    for _, d, _ in events:
        day = dt.date.fromisoformat(str(d))
        need_days.update([day.isoformat(), (day - dt.timedelta(days=1)).isoformat()])
    pos = {}
    for day in sorted(need_days):
        df = read_day(bucket, pos_prefix, day, ["accountId", "currentValue", "isCustodialCash", "productCategory", "assetClass"])
        if df is None:
            continue
        df["currentValue"] = df["currentValue"].astype(float)
        total = df.groupby("accountId")["currentValue"].sum()
        cash = df[df["isCustodialCash"].fillna(False).astype(bool)].groupby("accountId")["currentValue"].sum()
        broad = df[df["isCustodialCash"].fillna(False).astype(bool) | (df["productCategory"] == "Money Market") | (df["assetClass"] == "Cash or Equivalent")].groupby("accountId")["currentValue"].sum()
        pos[day] = (total, cash, broad)
        print("P", day, flush=True)
    def cash_of(day_iso):
        if day_iso not in pos:
            df = read_day(bucket, pos_prefix, day_iso, ["accountId", "currentValue", "isCustodialCash", "productCategory", "assetClass"])
            if df is None:
                pos[day_iso] = None
            else:
                df["currentValue"] = df["currentValue"].astype(float)
                cust = df["isCustodialCash"].fillna(False).astype(bool)
                pos[day_iso] = (df.groupby("accountId")["currentValue"].sum(), df[cust].groupby("accountId")["currentValue"].sum(),
                                df[cust | (df["productCategory"] == "Money Market") | (df["assetClass"] == "Cash or Equivalent")].groupby("accountId")["currentValue"].sum())
        return pos[day_iso]

    out = {"latest_snapshot": latest, "events": len(events), "tolerance": TOL, "missing_positions": 0,
           "cash_change_vs_X": {"with_positive_income_partner": Counter(), "without_partner": Counter()},
           "total_change_vs_X": {"with_positive_income_partner": Counter(), "without_partner": Counter()}}
    lines_by_day = {}
    for r in c.itertuples():
        lines_by_day.setdefault((r.accountId, r.transDate), []).append((r.transactionDescription, round(abs(float(r.transAmount)), 6)))
    reinvest = {"cash_fell_by_about_X": Counter(), "cash_flat": Counter(), "other": Counter()}
    on_day = shifted_hit = shifted_miss = 0
    broad_on_day = broad_shifted = 0
    for acct, d, x in events:
        day = dt.date.fromisoformat(str(d))
        d1, d0 = day.isoformat(), (day - dt.timedelta(days=1)).isoformat()
        if d1 not in pos or d0 not in pos:
            out["missing_positions"] += 1
            continue
        b1, b0 = float(pos[d1][2].get(acct, 0.0)), float(pos[d0][2].get(acct, 0.0))
        c1, c0 = float(pos[d1][1].get(acct, 0.0)), float(pos[d0][1].get(acct, 0.0))
        group = {"-X": "cash_fell_by_about_X", "0": "cash_flat"}.get(bucket_of(c1 - c0, x), "other")
        same_day = lines_by_day.get((acct, d), [])
        has_ir = any(desc == "Income Reinvested" and abs(m - x) <= TOL for desc, m in same_day)
        has_buy = any(desc == "Buy Exchange" and abs(m - x) <= TOL for desc, m in same_day)
        reinvest[group]["events"] += 1
        reinvest[group]["income_reinvested_line"] += 1 if has_ir else 0
        reinvest[group]["buy_line"] += 1 if has_buy else 0
        reinvest[group]["either"] += 1 if (has_ir or has_buy) else 0
        reinvest[group]["neither"] += 0 if (has_ir or has_buy) else 1
        broad_hit_day = abs((b1 - b0) + x) <= TOL
        broad_on_day += 1 if broad_hit_day else 0
        if abs((c1 - c0) + x) <= TOL:
            on_day += 1
        else:
            prev_t, next_t = tc.prev_trading_day(day), tc.first_trading_day_on_or_after(day + dt.timedelta(days=1))
            hit = False
            broad_hit = broad_hit_day
            for t1 in (prev_t, next_t):
                a1, a0 = cash_of(t1.isoformat()), cash_of(tc.prev_trading_day(t1).isoformat())
                if a1 is None or a0 is None:
                    continue
                if abs((float(a1[1].get(acct, 0.0)) - float(a0[1].get(acct, 0.0))) + x) <= TOL:
                    hit = True
                if abs((float(a1[2].get(acct, 0.0)) - float(a0[2].get(acct, 0.0))) + x) <= TOL:
                    broad_hit = True
            broad_shifted += 1 if (broad_hit and not broad_hit_day) else 0
            shifted_hit += 1 if hit else 0
            shifted_miss += 0 if hit else 1
        tot1, cash1, _ = pos[d1]
        tot0, cash0, _ = pos[d0]
        partner = "with_positive_income_partner" if (acct, d, x) in inc_pos else "without_partner"
        out["cash_change_vs_X"][partner][bucket_of(float(cash1.get(acct, 0.0)) - float(cash0.get(acct, 0.0)), x)] += 1
        out["total_change_vs_X"][partner][bucket_of(float(tot1.get(acct, 0.0)) - float(tot0.get(acct, 0.0)), x)] += 1
    out["agreement"] = {"events": len(events), "cash_fell_by_about_X_on_the_event_day": on_day, "re_read_one_trading_day_either_side": on_day + shifted_hit + shifted_miss - on_day,
                        "agreeing_on_a_shifted_window": shifted_hit, "agreeing_in_total": on_day + shifted_hit, "not_agreeing": shifted_miss, "release_floor": 90,
                        "broader_cash_definition": "custodial cash, money-market products and the Cash or Equivalent asset class",
                        "broader_cash_fell_by_about_X_on_the_event_day": broad_on_day, "broader_cash_agreeing_on_a_shifted_window_only": broad_shifted,
                        "broader_cash_agreeing_in_total": broad_on_day + broad_shifted}
    out["reinvestment_by_cash_group"] = {g: dict(v) for g, v in reinvest.items()}
    for k in ("cash_change_vs_X", "total_change_vs_X"):
        out[k] = {p: dict(v) for p, v in out[k].items()}
    out["read_at_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out["reader"] = "values-free: counts of buckets only; no account id or amount is kept or written"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
