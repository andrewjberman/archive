"""OFFLINE adapter: account_return_daily for ONE custody source (IRPT_DASHBD.TO-DB-b-71, FWD-11).

Reads the declaration beside this file (adapter_source.json), resolves the firm and every address from the
naming registry, READS the custodian's silver holdings and transactions from S3, and writes ONE parquet to the
path given on the command line. It never writes to S3 and never calls the vendor. No firm token appears here:
the firm is lookup(registry_key)['firm'] at run time (C-ADAPTERS).

THE METHOD (the PRD's, same as the 49 Financial producer):  r_t = (V_t - F_t) / V_(t-1) - 1
  V_t   whole-account value at the end of trading day t (declaration: value_rule)
  F_t   net EXTERNAL flow, capital-in positive, over the vendor-dated window (prev trading day, t]
  t-1   the prior TRADING day (lib/trading_calendar.py); a trading day with no source partition has no value,
        and the day after it is NOT_MEASURABLE (the geometric link BREAKS with a stated gap).

Usage: python adapter_returns.py <repo_root> <out.parquet>
"""
import datetime as dt
import io
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
METHOD_VERSION = 1
SCHEMA_VERSION = "1.0"


def load_decl(root):
    doc = json.loads((HERE / "adapter_source.json").read_bytes().decode("utf-8"))
    entries = [(k, v) for k, v in doc.items() if isinstance(v, dict) and not k.startswith("_")]
    if len(entries) != 1:
        raise SystemExit("ERROR: expected exactly one custody source in the declaration, found %d" % len(entries))
    return entries[0]


def setup(root):
    sys.path.insert(0, str(Path(root) / "lib"))
    import opal_naming
    import trading_calendar
    return opal_naming, trading_calendar


def read_object(s3, uri):
    """READ one parquet object; None if the key does not exist (an absence, never a zero)."""
    import pyarrow.parquet as pq
    bucket, key = uri[len("s3://"):].split("/", 1)
    try:
        body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    except s3.exceptions.NoSuchKey:
        return None
    return pq.read_table(io.BytesIO(body)).to_pandas()


def days_between(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def build(root, out_path):
    import boto3
    naming, cal = setup(root)
    name, decl = load_decl(root)
    firm = naming.lookup(decl["registry_key"])["firm"]
    vendor = naming.lookup(decl["registry_key"])["vendor"]
    s3 = boto3.client("s3")

    def uri(table, day):
        return naming.address(vendor, firm, "silver", table, "date=%s" % day.isoformat(), object=decl["object"])

    # coverage: probe a calendar-day range wide enough to hold the source (the source's own first/last partition is MEASURED here)
    lo, hi = dt.date(2026, 5, 1), dt.date.today()
    hold, first_part = {}, None
    for d in days_between(lo, hi):
        t = read_object(s3, uri(decl["holdings_table"], d))
        if t is None:
            continue
        acc, val = decl["account_column"], decl["value_column"]
        hold[d] = t.groupby(acc)[val].sum(min_count=1).dropna()
        first_part = first_part or d
    last_part = max(hold)
    txn_frames = []
    for d in days_between(lo, hi):
        t = read_object(s3, uri(decl["transactions_table"], d))
        if t is None:
            continue
        t = t[[decl["transaction_key_column"], decl["account_column"], decl["flow_column"], decl["flow_amount_column"],
               decl["flow_date_column"], decl["income_column"], decl["income_type_column"]]].copy()
        t["_part"] = d
        txn_frames.append(t)
    tx = pd.concat(txn_frames).sort_values("_part").drop_duplicates(decl["transaction_key_column"], keep="last")
    tx["_rd"] = pd.to_datetime(tx[decl["flow_date_column"]], format="%m/%d/%Y").dt.date
    amt = decl["flow_amount_column"]
    flow = tx[tx[decl["flow_column"]].isin(decl["flow_values"])]
    inc = tx[tx[decl["income_type_column"]].isin(decl["income_types"])]

    accounts = sorted(set().union(*[set(s.index) for s in hold.values()]))
    tdays = [d for d in days_between(first_part, last_part) if cal.is_trading_day(d)]
    flow_by = {(r, a): v for (r, a), v in flow.groupby(["_rd", decl["account_column"]])[amt].sum().items()}
    inc_by = {(r, a): v for (r, a), v in inc.groupby(["_rd", decl["account_column"]])[decl["income_column"]].sum().items()}
    parts = sorted(hold)
    first_acc = set(hold[first_part].index)

    rows = []
    for a in accounts:
        for t in tdays:
            v = hold.get(t, pd.Series(dtype=float)).get(a)
            if v is None:
                continue
            lo_d = cal.prev_trading_day(t)
            win = [d for d in days_between(lo_d + dt.timedelta(days=1), t)]
            f = sum(flow_by.get((d, a), 0.0) for d in win)
            i = sum(inc_by.get((d, a), 0.0) for d in win)
            carried = max(1, sum(1 for p in parts if lo_d < p <= t))
            pv = hold.get(lo_d, pd.Series(dtype=float)).get(a) if lo_d >= first_part else None
            if pv is None or pv <= 0:
                r, ir, basis, q = None, None, "NOT_MEASURABLE", "NOT_MEASURABLE"
            else:
                r = (v - f) / pv - 1.0
                ir = i / pv
                share = abs(f) / pv
                basis = "TWR"
                q = "LARGE_FLOW" if share > decl["large_flow_share"] else "MEASURED"
            rows.append({
                "firm": firm, "account_id": a, "business_date": t.isoformat(),
                "market_value_eod": float(v), "external_flow": float(f), "income_received": float(i),
                "income_return": ir, "total_return_daily": r, "return_basis": basis,
                "holdings_price_return": None, "holdings_price_return_reason": "NO_HOLDINGS_ROW",
                "fee_amount": None, "fee_amount_reason": "FEE_RAIL_UNUSED",
                "day_quality": q, "guard_state": "GUARD_NOT_REACHED",
                "history_scope": "PARTIAL_HISTORY" if a in first_acc else "FULL",
                "carried_days": carried, "method_version": METHOD_VERSION, "schema_version": SCHEMA_VERSION,
            })
    frame = pd.DataFrame(rows)
    con = json.loads((Path(root) / "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json").read_bytes().decode("utf-8"))
    cols = [c["name"] for c in con["columns"]]
    frame = frame[cols]
    for c in con["columns"]:
        if c["type"] == "int64":
            frame[c["name"]] = frame[c["name"]].astype("int64")
        elif c["type"] == "double":
            frame[c["name"]] = frame[c["name"]].astype("float64")
    frame.to_parquet(out_path, index=False)
    print("OK: wrote %d rows, %d accounts, %d trading days (%s..%s) to %s"
          % (len(frame), frame.account_id.nunique(), len(tdays), first_part, last_part, out_path))
    print("source partitions: first %s last %s; day_quality %s" % (first_part, last_part, frame.day_quality.value_counts().to_dict()))


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
