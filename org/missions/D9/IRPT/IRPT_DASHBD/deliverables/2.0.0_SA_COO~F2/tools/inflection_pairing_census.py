"""IRPT_DASHBD (workstream F-SHIP, ~F2): the GLOBAL, VALUES-FREE refinement of the two round-132 Inflection censuses (CTO msg 9342 rulings 1 and 4), over
EVERY partition. The first run (inflection_round132_census.py) paired inside one partition and matched Reversed keys without looking at dates; this one
does not limit the partner to the partition.

  python <this file> <out.json>

(A) S6 PAIRING (ruling 4): the Complete rows of `Dividend Paid from Cash` and `Income Paid` are keyed (accountId, transDate, abs(transAmount)); the
    Complete rows of every INCOME-class description (the contract's mapping) are scanned across ALL partitions; a row is PAIRED when its key occurs
    among the INCOME-class rows. Reported per description with the denominator, and the number of distinct keys matched.
(B) REVERSED OFFSETS (ruling 1): each Reversed row is keyed (accountId, ticker, noUnits, transAmount) with its transDate; a Complete row whose
    (accountId, ticker, noUnits, -transAmount) equals such a key is an OFFSET CANDIDATE. Reported: the Reversed rows and distinct keys; the candidate
    rows; per matched key the number of Reversed originals and of candidate rows (a real reversal pair is one original to one offset); the day gap
    between a candidate and the nearest original (zero, within 7 days, more), and the candidates per description.

Counts only: no account id, amount, symbol or identifier is kept or written. GET requests only. Run from the repository root with the box's AWS
credentials; needs boto3, pandas, numpy and pyarrow.
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

S6 = ("Dividend Paid from Cash", "Income Paid")
KEY = ["accountId", "ticker", "noUnits", "transAmount"]
COLS = ["status", "transDate", "accountId", "ticker", "noUnits", "transAmount", "transactionDescription"]
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
    s6_frames, rev_frames = [], []
    for day in days:
        df = read_day(bucket, prefix, day)
        if df is None or not len(df):
            continue
        s = df[(df["status"] == "Complete") & df["transactionDescription"].isin(S6)]
        if len(s):
            s6_frames.append(pd.DataFrame({"accountId": s["accountId"], "transDate": s["transDate"], "amt": s["transAmount"].astype(float).abs().round(6),
                                           "desc": s["transactionDescription"]}))
        r = df[df["status"] == "Reversed"]
        if len(r):
            rev_frames.append(pd.DataFrame({"accountId": r["accountId"], "ticker": r["ticker"], "noUnits": r["noUnits"].astype(float),
                                            "amt": (-r["transAmount"].astype(float)), "rdate": pd.to_datetime(r["transDate"])}))
        print("A", day, flush=True)
    s6 = pd.concat(s6_frames, ignore_index=True)
    rev = pd.concat(rev_frames, ignore_index=True)
    s6_keys = s6[["accountId", "transDate", "amt"]].drop_duplicates()
    s6_keys["_hit"] = True
    matched_s6 = []
    cand_frames = []
    rev_keys = rev[["accountId", "ticker", "noUnits", "amt"]].drop_duplicates()
    for day in days:
        df = read_day(bucket, prefix, day)
        if df is None or not len(df):
            continue
        c = df[df["status"] == "Complete"]
        inc = c[c["transactionDescription"].isin(income)]
        if len(inc):
            k = pd.DataFrame({"accountId": inc["accountId"], "transDate": inc["transDate"], "amt": inc["transAmount"].astype(float).abs().round(6)}).drop_duplicates()
            m = k.merge(s6_keys, on=["accountId", "transDate", "amt"], how="inner")
            if len(m):
                matched_s6.append(m[["accountId", "transDate", "amt"]])
        cc = pd.DataFrame({"accountId": c["accountId"], "ticker": c["ticker"], "noUnits": c["noUnits"].astype(float), "amt": c["transAmount"].astype(float),
                           "cdate": pd.to_datetime(c["transDate"]), "desc": c["transactionDescription"]})
        m = cc.merge(rev_keys, on=["accountId", "ticker", "noUnits", "amt"], how="inner")
        if len(m):
            cand_frames.append(m)
        print("B", day, flush=True)
    matched = pd.concat(matched_s6, ignore_index=True).drop_duplicates() if matched_s6 else pd.DataFrame(columns=["accountId", "transDate", "amt"])
    matched["_m"] = True
    s6m = s6.merge(matched, on=["accountId", "transDate", "amt"], how="left")
    s6_out = {}
    for d in S6:
        x = s6m[s6m["desc"] == d]
        paired = int(x["_m"].notna().sum())
        s6_out[d] = {"rows": int(len(x)), "paired_in_any_partition": paired, "share_paired": round(paired / len(x), 6) if len(x) else None}
    cand = pd.concat(cand_frames, ignore_index=True) if cand_frames else pd.DataFrame(columns=["accountId", "ticker", "noUnits", "amt", "cdate", "desc"])
    per_key_cand = cand.groupby(["accountId", "ticker", "noUnits", "amt"]).size() if len(cand) else pd.Series(dtype=int)
    per_key_orig = rev.groupby(["accountId", "ticker", "noUnits", "amt"]).size()
    gaps = {"same_day": 0, "within_7_days": 0, "more_than_7_days": 0}
    if len(cand):
        joined = cand.merge(rev, on=["accountId", "ticker", "noUnits", "amt"], how="left")
        joined["gap"] = (joined["cdate"] - joined["rdate"]).abs().dt.days
        nearest = joined.groupby(["accountId", "ticker", "noUnits", "amt", "cdate", "desc"])["gap"].min()
        gaps = {"same_day": int((nearest == 0).sum()), "within_7_days": int(((nearest > 0) & (nearest <= 7)).sum()), "more_than_7_days": int((nearest > 7).sum())}
    pairs_1to1 = 0
    if len(per_key_cand):
        for key, n in per_key_cand.items():
            if n == 1 and per_key_orig.get(key, 0) == 1:
                pairs_1to1 += 1
    out = {"firm": "inflection", "read_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "partitions_read": len(days),
           "income_class_descriptions": len(income),
           "s6_pairing": s6_out,
           "reversed": {"rows": int(len(rev)), "distinct_keys": int(len(rev_keys)), "offset_candidate_rows": int(len(cand)),
                        "distinct_keys_with_a_candidate": int(len(per_key_cand)),
                        "keys_with_one_original_and_one_candidate": pairs_1to1,
                        "originals_per_matched_key_max": int(per_key_orig[per_key_cand.index].max()) if len(per_key_cand) else 0,
                        "candidates_per_matched_key_max": int(per_key_cand.max()) if len(per_key_cand) else 0,
                        "candidate_day_gap_to_nearest_original": gaps,
                        "candidates_per_description": {str(k): int(v) for k, v in cand["desc"].value_counts().items()} if len(cand) else {}},
           "reader": "values-free: counts only; no account id, amount, symbol or identifier is kept or written"}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: out[k] for k in ("s6_pairing", "reversed")}))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
