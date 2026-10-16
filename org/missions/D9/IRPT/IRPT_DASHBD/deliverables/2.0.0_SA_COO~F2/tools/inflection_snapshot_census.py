"""IRPT_DASHBD (workstream F-SHIP, ~F2): the CORRECTED DOMAIN of the Inflection transaction censuses. READ-ONLY, VALUES-FREE, counts only (no account id, amount,
symbol or identifier is kept or written; GET requests only).

  python <this file> <out.json>

FINDING that this tool measures (round 135): every Orion silver `fact_transactions` partition is a CUMULATIVE SNAPSHOT of the whole transaction history (the row count
grows from 1.25 million to 1.52 million over 155 partitions, and each partition reaches back about 6.4 years), so a census "over every partition" counts each
transaction roughly 140 times. The earlier round-131 and round-132 Inflection censuses (status, Reversed offsets, the S6 pairing, price agreement, duplicate keys)
were SNAPSHOT-WEIGHTED, not distinct-transaction counts. This tool measures:

 (A) the DISTINCT transactions: the distinct `id` values across all snapshots, how many appear in the latest snapshot, how many were seen but are gone from it;
 (B) STATUS MOVEMENT by id: for ids seen in at least two snapshots, the number whose status changed between the first snapshot they appear in and the latest
     snapshot they appear in, by (first status, last status) pair;
 (C) the LATEST snapshot alone, the proper domain of a gold run: rows; rows per status; Complete rows; rolled Complete rows (non-trading transDate); the S6
     description rows and how many pair with an INCOME-class row of the same account, day and absolute amount; the Reversed rows and the Complete offset
     candidates (account, symbol, units, negated amount); the non-unique natural-key census (account, transDate, description, symbol, units, amount).
"""
import datetime as dt
import importlib.util
import io
import json
import sys
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
import trading_calendar as tc  # noqa: E402

S6 = ("Dividend Paid from Cash", "Income Paid")
COLS = ["id", "status", "transDate", "accountId", "ticker", "noUnits", "transAmount", "transactionDescription"]
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


def main(out_path):
    iar = load("iar", "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py")
    bucket, _, rest = iar.ORION_SILVER[len("s3://"):].partition("/")
    prefix = rest + "fact_transactions/"
    con = json.loads((ROOT / "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json").read_text(encoding="utf-8"))
    income = {m["source_value"] for m in con["source_mapping"] if m["firm"] == "inflection" and m["flow_class"] == "INCOME"}
    days = ard.partition_days(s3, bucket, prefix)
    # (A) and (B): one frame indexed by id, first and last status and the number of snapshots the id appears in
    state = pd.DataFrame(columns=["first", "last", "n"])
    state.index.name = "id"
    for day in days:
        df = read_day(bucket, prefix, day, ["id", "status"])
        df = df.drop_duplicates("id").set_index("id")["status"]
        cur = pd.DataFrame({"s": df})
        joined = state.join(cur, how="outer")
        new = joined["first"].isna()
        joined.loc[new, "first"] = joined.loc[new, "s"]
        joined.loc[new, "n"] = 0
        present = joined["s"].notna()
        joined.loc[present, "last"] = joined.loc[present, "s"]
        joined.loc[present, "n"] = joined.loc[present, "n"].astype(int) + 1
        state = joined[["first", "last", "n"]]
        print("A", day, len(state), flush=True)
    latest = days[-1]
    lf = read_day(bucket, prefix, latest, COLS)
    in_latest = set(lf["id"].tolist())
    seen_not_latest = int((~state.index.isin(in_latest)).sum())
    multi = state[state["n"].astype(int) >= 2]
    moves = multi[multi["first"] != multi["last"]]
    pair_counts = {"%s -> %s" % k: int(v) for k, v in moves.groupby(["first", "last"]).size().items()}
    out_a = {"snapshots": len(days), "distinct_ids_ever_seen": int(len(state)), "ids_in_latest_snapshot": int(len(in_latest)), "ids_seen_but_absent_from_latest": seen_not_latest,
             "ids_seen_in_two_or_more_snapshots": int(len(multi)), "ids_whose_status_changed_first_to_last": int(len(moves)), "status_changes_by_first_and_last": pair_counts}
    # (C) the latest snapshot alone
    rows = int(len(lf))
    per_status = {str(k): int(v) for k, v in lf["status"].value_counts().items()}
    c = lf[lf["status"] == "Complete"].copy()
    cache = {}

    def nontrading(d):
        if d not in cache:
            cache[d] = not tc.is_trading_day(dt.date.fromisoformat(str(d)))
        return cache[d]

    rolled = int(c["transDate"].map(nontrading).sum())
    c["amt"] = c["transAmount"].astype(float).round(6)
    inc = c[c["transactionDescription"].isin(income)]
    inc_keys = set(zip(inc["accountId"].tolist(), inc["transDate"].tolist(), inc["amt"].abs().tolist()))
    s6 = {}
    for d in S6:
        x = c[c["transactionDescription"] == d]
        keys = list(zip(x["accountId"].tolist(), x["transDate"].tolist(), x["amt"].abs().tolist()))
        s6[d] = {"rows": int(len(x)), "paired_with_income_class_row": sum(1 for k in keys if k in inc_keys)}
    a_keys = set(zip(c[c["transactionDescription"] == S6[0]]["accountId"], c[c["transactionDescription"] == S6[0]]["transDate"], c[c["transactionDescription"] == S6[0]]["amt"].abs()))
    b_keys = set(zip(c[c["transactionDescription"] == S6[1]]["accountId"], c[c["transactionDescription"] == S6[1]]["transDate"], c[c["transactionDescription"] == S6[1]]["amt"].abs()))
    rev = lf[lf["status"] == "Reversed"]
    rkeys = set(zip(rev["accountId"], rev["ticker"], rev["noUnits"].astype(float), -rev["transAmount"].astype(float)))
    cand = c[[k in rkeys for k in zip(c["accountId"], c["ticker"], c["noUnits"].astype(float), c["transAmount"].astype(float))]]
    keycols = ["accountId", "transDate", "transactionDescription", "ticker", "noUnits", "transAmount"]
    sizes = c.groupby(keycols, dropna=False).size()
    out_c = {"latest_snapshot": latest, "rows": rows, "rows_per_status": per_status, "complete_rows": int(len(c)), "complete_rolled_rows": rolled,
             "s6_rows_and_pairing": s6, "s6_distinct_keys_a": len(a_keys), "s6_distinct_keys_b": len(b_keys), "s6_keys_in_both": len(a_keys & b_keys),
             "reversed_rows": int(len(rev)), "reversed_distinct_keys": len(rkeys), "offset_candidate_rows": int(len(cand)),
             "offset_candidate_descriptions": {str(k): int(v) for k, v in cand["transactionDescription"].value_counts().items()},
             "complete_rows_in_non_unique_keys": int(sizes[sizes > 1].sum()), "complete_non_unique_keys": int((sizes > 1).sum())}
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "table": "fact_transactions",
           "finding": "each partition is a cumulative snapshot of the whole history; earlier censuses over every partition were snapshot-weighted",
           "distinct_and_movement": out_a, "latest_snapshot": out_c,
           "reader": "values-free: counts only; no account id, amount, symbol or identifier is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps({"distinct_and_movement": out_a, "latest_snapshot": out_c})[:3500])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
