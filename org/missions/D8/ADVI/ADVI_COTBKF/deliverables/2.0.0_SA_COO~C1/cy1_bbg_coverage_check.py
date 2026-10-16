"""ADVI_COTBKF TO-CB-cy-1 (issuer's check): how much of the served UNPRICED holding-days do the Bloomberg closes ALREADY IN OPAL'S STORE cover?

The worker names, in its record, where returned Bloomberg price history lives (key `bloomberg`: bucket, prefix, columns {cusip, date, close}).
This script re-counts that independently. READ-ONLY, counts only; it never calls Bloomberg and never writes.
  python cy1_bbg_coverage_check.py <record.json>
    reads the record's bloomberg.bucket / bloomberg.prefix, lists every .parquet object under it (list-objects, paginated), reads ONLY the three named
    columns of each, and keeps (cusip, date) pairs whose close is a positive finite number. Then, on the served account_day_value (pinned VersionId):
    UNPRICED holding-days = rows with a null close and a null blank_reason; a holding-day is COVERED when its (cusip, date) is in the Bloomberg set.
    Prints  BBG-COVERAGE objects=<n> bbg_points=<p> bbg_cusips=<c> unpriced_cusips_covered=<k> unpriced_rows_covered=<r> unpriced_rows=<u>
    and, on the SAME line,   objects_equal=<bool> points_equal=<bool> cusips_covered_equal=<bool> rows_covered_equal=<bool>
    comparing record keys bloomberg.objects, bloomberg.points, coverage.securities_covered, coverage.holding_days_covered.
An empty or absent prefix gives objects=0 and every count 0 (that is the answer, not an error). No cusip, account or value is printed.
Needs AWS read credentials.
"""
import io
import json
import sys

import boto3
import pyarrow.parquet as pq

if len(sys.argv) < 2:
    raise SystemExit("usage: cy1_bbg_coverage_check.py <record.json>")
w = json.load(open(sys.argv[1], encoding="utf-8"))
bb = w.get("bloomberg") or {}
bucket, prefix, cols = bb.get("bucket"), bb.get("prefix"), bb.get("columns") or {}
s3 = boto3.client("s3", region_name="us-east-1")

keys = []
if bucket and prefix is not None:
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith(".parquet")]

pts = set()
for k in keys:
    t = pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read()), columns=[cols["cusip"], cols["date"], cols["close"]]).to_pandas()
    t = t[t[cols["close"]].notna() & (t[cols["close"]] > 0)]
    pts.update(zip(t[cols["cusip"]].astype(str).str.strip(), t[cols["date"]].astype(str).str.slice(0, 10)))

body = s3.get_object(Bucket="opal-data-assets", Key="commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/part-00000.parquet",
                     VersionId="ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a")["Body"].read()
av = pq.read_table(io.BytesIO(body), columns=["cusip", "date", "close", "blank_reason"]).to_pandas()
un = av[av["close"].isna() & av["blank_reason"].isna()]
key = list(zip(un["cusip"].astype(str).str.strip(), un["date"].astype(str).str.slice(0, 10)))
hit = [k in pts for k in key]
covered = un[hit]
k_cov = int(covered["cusip"].astype(str).nunique())
r_cov = int(len(covered))
cov = w.get("coverage") or {}
print("BBG-COVERAGE objects=%d bbg_points=%d bbg_cusips=%d unpriced_cusips_covered=%d unpriced_rows_covered=%d unpriced_rows=%d objects_equal=%s points_equal=%s cusips_covered_equal=%s rows_covered_equal=%s"
      % (len(keys), len(pts), len({p[0] for p in pts}), k_cov, r_cov, len(un), bb.get("objects") == len(keys), bb.get("points") == len(pts),
         cov.get("securities_covered") == k_cov, cov.get("holding_days_covered") == r_cov))
