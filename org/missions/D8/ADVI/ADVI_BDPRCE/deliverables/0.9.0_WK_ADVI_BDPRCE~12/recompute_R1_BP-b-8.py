#!/usr/bin/env python3
"""recompute_R1_BP-b-8.py -- ADVI_BDPRCE BP-b-8: the R1 carry-forward for the chosen unlisted holding.

READ-ONLY. boto3 get_object on silver/transactions/<date>.parquet for 2026-10-02 .. 2026-10-10 (one call each,
read into memory, nothing written). Imports the merged R1 module (bd_price_rule.py) and calls price_for_date
(variant A) on the observation date, then carry_forward. Prints only the asset's own rows and figures.
Prints no client, account or advisor name.

Run:  cd <worktree> && timeout 300 python -I org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~12/recompute_R1_BP-b-8.py
"""
import importlib.util
import io
from pathlib import Path

import boto3
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
RULE = ROOT / "data" / "black_diamond" / "scripts" / "silver" / "bd_price_rule.py"
BUCKET = "opal-data-bd"
ASSET = "ALLSPRING CORE BOND CIT CLASS E2"
TARGET = "2026-10-09"
WINDOW = ["2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06", "2026-10-07",
          "2026-10-08", "2026-10-09", "2026-10-10"]
COLS = ["transaction_id", "transaction_type", "price", "trade_date", "asset_name"]

spec = importlib.util.spec_from_file_location("bd_price_rule", str(RULE))
R1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R1)

s3 = boto3.client("s3", region_name="us-east-1")
parts = []
for d in WINDOW:
    body = s3.get_object(Bucket=BUCKET, Key="silver/transactions/%s.parquet" % d)["Body"].read()
    df = pd.read_parquet(io.BytesIO(body), columns=COLS)
    parts.append(df[df["asset_name"] == ASSET])
rows = pd.concat(parts, ignore_index=True)
rows["trade_date"] = pd.to_datetime(rows["trade_date"], errors="coerce").dt.date.astype(str)
bs = rows[rows["transaction_type"].isin(["Buy", "Sale"])]
print("asset rows in window", len(rows), "Buy/Sale rows", len(bs))
before = sorted(set(bs[bs["trade_date"] < TARGET]["trade_date"]))
obs = before[-1]
print("last Buy/Sale trade date before", TARGET, "=", obs)
print("Buy/Sale rows on", TARGET, "=", int((bs["trade_date"] == TARGET).sum()), "(shape a fails when 0)")
r = R1.price_for_date(bs, obs)[ASSET]
print("R1 variant A on", obs, "price", r["price"], "distinct_trade_ids", r["trade_ids"], "conflicting_ids", r["conflicting_ids"])
c = R1.carry_forward((r["price"], obs))
print("R1 carry-forward for", TARGET, "price", c["price"], "observed_date", c["observed_date"], "source", c["source"])
print("served price 10.3525 equals carry:", abs(c["price"] - 10.3525) <= 1e-6 * max(1.0, 10.3525))
