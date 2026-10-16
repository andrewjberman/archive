"""IRPT_DASHBD (workstream F-SHIP, ~F2): READ-ONLY, VALUES-FREE censuses for the CTO's round-131 rulings (msg 9342), over EVERY Inflection partition.

  python <this file> <out.json>

Three censuses, counts only (no account id, amount, symbol or identifier is kept or written; GET requests only):

 (1) FUND FAMILY (ruling 2): over Complete rows that carry units and a positive navPrice, the rows with a non-blank `fundFamilyName` (price served)
     and the rows without one (price null, reason NAV_PRICE_FUND_ONLY), and within the fund-family rows how many have navPrice * noUnits within one
     percent of transAmount.
 (2) REVERSED OFFSETS (ruling 1): the Reversed rows (the originals) are keyed by (accountId, ticker, noUnits, transAmount); a Complete row whose
     (accountId, ticker, noUnits, -transAmount) equals an original's key is an OFFSET. Reported over all days (an upper bound), with the
     denominators: Reversed rows, distinct Reversed keys, Complete rows scanned; and the offsets per transactionDescription.
 (3) S6 PAIRING (ruling 4): for the rows of `Dividend Paid from Cash` and `Income Paid` (Complete), how many have, in the SAME partition, a Complete
     row of an INCOME-class description (the contract's mapping) with the same account, the same transDate and the same absolute amount; per
     description. Pairing is looked for inside the partition (a partner in another partition counts as unpaired, so the share is a lower bound).

Run from the repository root with the box's AWS credentials; needs boto3, pandas and pyarrow.
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from pathlib import Path

import boto3
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402

S6_DESCRIPTIONS = ("Dividend Paid from Cash", "Income Paid")
KEY = ["accountId", "ticker", "noUnits", "transAmount"]
COLS = ["status", "transDate", "accountId", "ticker", "noUnits", "transAmount", "navPrice", "fundFamilyName", "transactionDescription"]
s3 = boto3.client("s3", config=Config(max_pool_connections=8, retries={"max_attempts": 5}))


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_day(bucket, prefix, day):
    tables = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)):
        for o in page.get("Contents", []) or []:
            if o["Key"].endswith(".parquet"):
                tables.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read()), columns=COLS))
    return pa.concat_tables(tables, promote_options="default").to_pandas() if tables else None


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    con = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
    income = {m["source_value"] for m in con["source_mapping"] if m["firm"] == "inflection" and m["flow_class"] == "INCOME"}
    days = ard.partition_days(s3, bucket, prefix)
    fund = {"unit_bearing_positive_nav_rows": 0, "with_fund_family": 0, "without_fund_family": 0, "fund_rows_within_1pct": 0}
    s6 = {d: {"rows": 0, "paired_in_partition": 0} for d in S6_DESCRIPTIONS}
    rev_frames = []
    rev_by_desc = {}
    complete_rows = 0
    rev_rows = 0
    for day in days:
        df = read_day(bucket, prefix, day)
        if df is None or not len(df):
            continue
        rev = df[df["status"] == "Reversed"]
        if len(rev):
            rev_frames.append(rev[KEY].drop_duplicates())
            for d, n in rev["transactionDescription"].value_counts().items():
                rev_by_desc[str(d)] = rev_by_desc.get(str(d), 0) + int(n)
            rev_rows += len(rev)
        c = df[df["status"] == "Complete"]
        complete_rows += len(c)
        units = c["noUnits"].astype(float)
        nav = c["navPrice"].astype(float)
        usable = (units != 0) & (nav > 0)
        fam = c["fundFamilyName"].notna() & (c["fundFamilyName"].astype(str).str.strip() != "")
        fund["unit_bearing_positive_nav_rows"] += int(usable.sum())
        fund["with_fund_family"] += int((usable & fam).sum())
        fund["without_fund_family"] += int((usable & ~fam).sum())
        diff = (units * nav - c["transAmount"].astype(float)).abs()
        tol = c["transAmount"].astype(float).abs() * 0.01 + 0.01
        fund["fund_rows_within_1pct"] += int((usable & fam & (diff <= tol)).sum())
        inc = c[c["transactionDescription"].isin(income)]
        inc_keys = set(zip(inc["accountId"].tolist(), inc["transDate"].tolist(), inc["transAmount"].astype(float).abs().round(6).tolist()))
        for d in S6_DESCRIPTIONS:
            rows = c[c["transactionDescription"] == d]
            s6[d]["rows"] += len(rows)
            keys = zip(rows["accountId"].tolist(), rows["transDate"].tolist(), rows["transAmount"].astype(float).abs().round(6).tolist())
            s6[d]["paired_in_partition"] += sum(1 for k in keys if k in inc_keys)
        print("A", day, flush=True)
    rev_keys = pd.concat(rev_frames, ignore_index=True).drop_duplicates() if rev_frames else pd.DataFrame(columns=KEY)
    rev_keys["transAmount"] = -rev_keys["transAmount"].astype(float)
    rev_keys = rev_keys.assign(_k=1)
    off_all = 0
    matched_keys = set()
    off_by_desc = {}
    for day in days:
        df = read_day(bucket, prefix, day)
        if df is None or not len(df):
            continue
        c = df[df["status"] == "Complete"][KEY + ["transDate", "transactionDescription"]].copy()
        c["transAmount"] = c["transAmount"].astype(float)
        m = c.merge(rev_keys, on=KEY, how="inner")
        off_all += len(m)
        if len(m):
            for d, n in m["transactionDescription"].value_counts().items():
                off_by_desc[str(d)] = off_by_desc.get(str(d), 0) + int(n)
            matched_keys.update(zip(m["accountId"].tolist(), m["ticker"].tolist(), m["noUnits"].tolist(), m["transAmount"].tolist()))
        print("B", day, flush=True)
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "partitions_read": len(days),
           "rows_complete": complete_rows, "income_class_descriptions": len(income),
           "fund_family": fund,
           "reversed": {"rows": rev_rows, "distinct_keys": int(len(rev_keys)), "rows_per_description": dict(sorted(rev_by_desc.items())),
                        "complete_rows_whose_negated_key_matches_a_reversed_key": off_all, "distinct_reversed_keys_matched": len(matched_keys),
                        "offset_rows_per_description": dict(sorted(off_by_desc.items()))},
           "s6_pairing": {d: dict(v, share_paired=round(v["paired_in_partition"] / v["rows"], 6) if v["rows"] else None) for d, v in s6.items()},
           "reader": "values-free: counts only; no account id, amount, symbol or identifier is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, default=lambda o: int(o) if isinstance(o, (np.integer,)) else str(o))
    print(json.dumps({k: out[k] for k in ("fund_family", "reversed", "s6_pairing")}, default=str)[:1800])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
