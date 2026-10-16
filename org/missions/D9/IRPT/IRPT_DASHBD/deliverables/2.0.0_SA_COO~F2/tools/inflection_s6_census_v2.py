"""IRPT_DASHBD (workstream F-SHIP, ~F2): the S6 CENSUS v2 the CTO asked for (ADDENDUM 1 of CTO_ROUND_ANALYSIS_IRPT_DASHBD_F-SHIP_ROUND_131, msg 9359),
READ-ONLY and VALUES-FREE, over EVERY Inflection partition.

  python <this file> <out.json>

The Complete rows of the two descriptions `Dividend Paid from Cash` (A) and `Income Paid` (B) are read SEPARATELY. Counts only (description names are a
vendor enum; no account id, amount, symbol or identifier is kept or written; GET requests only):

 (1) per description: the rows; the rows paired with an INCOME-class row (the contract's mapping) of the same account, same transDate and same absolute
     amount; and how many rows of one description sit on the same account, transDate and absolute amount as a row of the OTHER description (two legs
     of one event, or a reader fault).
 (2) for the rows of each description that are NOT paired with an INCOME-class row: the number with (a) an INCOME-class row on the same account and day
     within one cent, (b) one with the same absolute amount within one day, (c) one within one cent and one day, (d) none of those; and, over the
     descriptions present on the same account on the same day, the day before and the day after, how many of the unpaired rows have at least one row
     of each description (the descriptions are the vendor's).

Run from the repository root with the box's AWS credentials; needs boto3, pandas and pyarrow.
"""
import datetime as dt
import importlib.util
import io
import json
import sys
from collections import Counter
from pathlib import Path

import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
import account_return_daily as ard  # noqa: E402

S6 = ("Dividend Paid from Cash", "Income Paid")
COLS = ["status", "transDate", "accountId", "transAmount", "transactionDescription"]
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


def pm1(day):
    d = dt.date.fromisoformat(day)
    return [(d - dt.timedelta(days=1)).isoformat(), day, (d + dt.timedelta(days=1)).isoformat()]


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    con = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
    income = {m["source_value"] for m in con["source_mapping"] if m["firm"] == "inflection" and m["flow_class"] == "INCOME"}
    days = ard.partition_days(s3, bucket, prefix)
    frames = []
    for day in days:
        df = read_day(bucket, prefix, day)
        if df is None or not len(df):
            continue
        s = df[(df["status"] == "Complete") & df["transactionDescription"].isin(S6)]
        if len(s):
            frames.append(pd.DataFrame({"acct": s["accountId"], "day": s["transDate"], "amt": s["transAmount"].astype(float).abs().round(6),
                                        "desc": s["transactionDescription"]}))
        print("A", day, flush=True)
    s6 = pd.concat(frames, ignore_index=True)
    accounts = set(s6["acct"].tolist())
    dates = set()
    for d in set(s6["day"].tolist()):
        dates.update(pm1(d))
    kept = []
    for day in days:
        df = read_day(bucket, prefix, day)
        if df is None or not len(df):
            continue
        c = df[(df["status"] == "Complete") & df["accountId"].isin(accounts) & df["transDate"].isin(dates)]
        if len(c):
            kept.append(pd.DataFrame({"acct": c["accountId"], "day": c["transDate"], "amt": c["transAmount"].astype(float).abs().round(6),
                                      "desc": c["transactionDescription"]}))
        print("B", day, flush=True)
    near = pd.concat(kept, ignore_index=True)
    inc = near[near["desc"].isin(income)]
    by_acct_day = {}
    for a, d, m, x in zip(near["acct"].tolist(), near["day"].tolist(), near["amt"].tolist(), near["desc"].tolist()):
        by_acct_day.setdefault((a, d), []).append((m, x))
    inc_by_acct_day = {}
    for a, d, m in zip(inc["acct"].tolist(), inc["day"].tolist(), inc["amt"].tolist()):
        inc_by_acct_day.setdefault((a, d), []).append(m)
    keys_by_desc = {d: set(zip(g["acct"], g["day"], g["amt"])) for d, g in s6.groupby("desc")}
    out_desc = {}
    for d in S6:
        g = s6[s6["desc"] == d]
        other = keys_by_desc[S6[1] if d == S6[0] else S6[0]]
        o = {"rows": int(len(g)), "paired_with_income_class_row": 0, "same_key_as_a_row_of_the_other_description": 0,
             "unpaired": 0, "unpaired_income_same_day_within_1_cent": 0, "unpaired_income_same_amount_within_1_day": 0,
             "unpaired_income_within_1_cent_and_1_day": 0, "unpaired_with_none_of_those": 0,
             "unpaired_rows_with_a_row_of_description_same_day": Counter(), "unpaired_rows_with_a_row_of_description_day_before": Counter(),
             "unpaired_rows_with_a_row_of_description_day_after": Counter()}
        for a, day, amt in zip(g["acct"].tolist(), g["day"].tolist(), g["amt"].tolist()):
            if (a, day, amt) in other:
                o["same_key_as_a_row_of_the_other_description"] += 1
            if any(abs(m - amt) < 5e-7 for m in inc_by_acct_day.get((a, day), [])):
                o["paired_with_income_class_row"] += 1
                continue
            o["unpaired"] += 1
            same = inc_by_acct_day.get((a, day), [])
            cent = any(abs(m - amt) <= 0.0100001 for m in same)
            day_before, day_after = pm1(day)[0], pm1(day)[2]
            side = [inc_by_acct_day.get((a, x), []) for x in (day_before, day_after)]
            amount_1day = any(abs(m - amt) < 5e-7 for lst in side for m in lst) or any(abs(m - amt) < 5e-7 for m in same)
            cent_1day = any(abs(m - amt) <= 0.0100001 for lst in side + [same] for m in lst)
            o["unpaired_income_same_day_within_1_cent"] += 1 if cent else 0
            o["unpaired_income_same_amount_within_1_day"] += 1 if amount_1day else 0
            o["unpaired_income_within_1_cent_and_1_day"] += 1 if cent_1day else 0
            o["unpaired_with_none_of_those"] += 0 if (cent or amount_1day or cent_1day) else 1
            for label, x in (("same_day", day), ("day_before", day_before), ("day_after", day_after)):
                present = {desc for _, desc in by_acct_day.get((a, x), [])}
                for desc in present:
                    o["unpaired_rows_with_a_row_of_description_" + label][desc] += 1
        for k in ("same_day", "day_before", "day_after"):
            o["unpaired_rows_with_a_row_of_description_" + k] = dict(o["unpaired_rows_with_a_row_of_description_" + k].most_common(12))
        o["share_paired"] = round(o["paired_with_income_class_row"] / o["rows"], 6) if o["rows"] else None
        out_desc[d] = o
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "partitions_read": len(days),
           "income_class_descriptions": len(income), "accounts_with_an_s6_row": len(accounts), "per_description": out_desc,
           "reader": "values-free: counts only; description names are a vendor enum; no account id, amount, symbol or identifier is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps(out_desc)[:3000])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
