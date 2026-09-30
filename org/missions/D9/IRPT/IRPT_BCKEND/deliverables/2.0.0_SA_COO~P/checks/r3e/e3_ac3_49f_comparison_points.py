"""~E round 3 AC3 -- FWD-13 for 49F: every landed Black Diamond reporting_performance file has ONE comparison row
against the holdings-basis figure (PRD v0.19 ruling 8; 1.0.0_SA_CTO round-19 analysis section 6 item 4).

Usage: python e3_ac3_49f_comparison_points.py
Bronze: s3://opal-data-assets/blackdiamond/49f/bronze/reporting_performance/<pull date>/reporting_performance_<id>_<as-of>.json
(4 pull dates, 5,318 files at the cut). Gold: address("irpt", "49financial", "gold", "holdings_performance_comparison",
"date=<as-of>") for each distinct <as-of> in the file names. Pass, per as-of date: the partition's row count equals the
bronze file count carrying that as-of; every row carries source_key (the bronze key it compares) and EITHER both
vendor_return and opal_return with period_start and period_end, OR a non-empty not_comparable_reason; no source_key
appears twice.
"""
import collections
import io
import sys
from pathlib import Path

import boto3
import pandas as pd

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402

B, P = "opal-data-assets", "blackdiamond/49f/bronze/reporting_performance/"
s3 = boto3.client("s3")
keys = [o["Key"] for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P)
        for o in pg.get("Contents", []) if o["Key"].endswith(".json")]
by_asof = collections.defaultdict(set)
for k in keys:
    by_asof[k.rsplit("_", 1)[1][:-5]].add(k)
ok = bool(keys)
for asof, want in sorted(by_asof.items()):
    uri = opal_naming.address("irpt", "49financial", "gold", "holdings_performance_comparison", "date=%s" % asof)
    bucket, _, key = uri[len("s3://"):].partition("/")
    parts = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=key.rstrip("/") + "/").get("Contents", [])
             if o["Key"].endswith(".parquet")]
    df = pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read())) for k in parts]) if parts else None
    if df is None or "source_key" not in df.columns:
        print("as-of %s: bronze files %d | comparison rows 0" % (asof, len(want)))
        ok = False
        continue
    have = df["source_key"].astype(str)
    both = df[["vendor_return", "opal_return", "period_start", "period_end"]].notna().all(axis=1) if {"vendor_return", "opal_return", "period_start", "period_end"} <= set(df.columns) else pd.Series(False, index=df.index)
    named = df["not_comparable_reason"].fillna("").astype(str).str.len() > 0 if "not_comparable_reason" in df.columns else pd.Series(False, index=df.index)
    bad = int((~(both | named)).sum())
    missing = len(want - set(have))
    dup = int(have.duplicated().sum())
    print("as-of %s: bronze files %d | comparison rows %d | compared %d | named not-comparable %d | missing %d | dup %d | neither %d" % (
        asof, len(want), len(df), int(both.sum()), int(named.sum()), missing, dup, bad))
    ok = ok and len(df) == len(want) and not missing and not dup and not bad
print("E3-AC3 PASS" if ok else "E3-AC3 FAIL")
sys.exit(0 if ok else 1)
