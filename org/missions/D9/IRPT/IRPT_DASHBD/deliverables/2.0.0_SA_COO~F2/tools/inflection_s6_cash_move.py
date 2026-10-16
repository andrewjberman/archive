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
        df = read_day(bucket, pos_prefix, day, ["accountId", "currentValue", "isCustodialCash"])
        if df is None:
            continue
        df["currentValue"] = df["currentValue"].astype(float)
        total = df.groupby("accountId")["currentValue"].sum()
        cash = df[df["isCustodialCash"].fillna(False).astype(bool)].groupby("accountId")["currentValue"].sum()
        pos[day] = (total, cash)
        print("P", day, flush=True)
    out = {"latest_snapshot": latest, "events": len(events), "tolerance": TOL, "missing_positions": 0,
           "cash_change_vs_X": {"with_positive_income_partner": Counter(), "without_partner": Counter()},
           "total_change_vs_X": {"with_positive_income_partner": Counter(), "without_partner": Counter()}}
    for acct, d, x in events:
        day = dt.date.fromisoformat(str(d))
        d1, d0 = day.isoformat(), (day - dt.timedelta(days=1)).isoformat()
        if d1 not in pos or d0 not in pos:
            out["missing_positions"] += 1
            continue
        tot1, cash1 = pos[d1]
        tot0, cash0 = pos[d0]
        partner = "with_positive_income_partner" if (acct, d, x) in inc_pos else "without_partner"
        out["cash_change_vs_X"][partner][bucket_of(float(cash1.get(acct, 0.0)) - float(cash0.get(acct, 0.0)), x)] += 1
        out["total_change_vs_X"][partner][bucket_of(float(tot1.get(acct, 0.0)) - float(tot0.get(acct, 0.0)), x)] += 1
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
