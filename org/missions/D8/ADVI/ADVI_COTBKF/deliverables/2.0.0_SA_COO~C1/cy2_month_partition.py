"""ADVI_COTBKF TO-CB-cy-2 (issuer's check): the UNGRADABLE months of the served month_grades as DISJOINT categories, recomputed from the served objects.

Reads (read-only, one get each, pinned VersionIds; counts only) the served daily_returns and month_grades. Every UNGRADABLE account-month falls in
exactly one category, assigned in this order:
  no_daily            the month has no daily_returns row at all (reason text 'no daily returns for the month')
  blank_only_unpriced the month has blank days, EVERY blank day is UNPRICED, and the month's reason text carries no reported-side clause
  blank_only_other    the month has blank days, at least one blank day is not UNPRICED, and no reported-side clause
  blank_and_reported  the month has blank days and a reported-side clause
  reported_only       the month has no blank day and a reported-side clause
  other               anything else (expected 0)
A reported-side clause is any of: 'no reported monthly return', 'reported span', 'reported rows disagree', 'not finite' (the month_grades reason text).
Blank days come from daily_returns (return null), by month = the first 7 characters of the date.
  python cy2_month_partition.py                -> MONTH-PARTITION ungradable=<n> no_daily=<a> blank_only_unpriced=<b> blank_only_other=<c>
                                                  blank_and_reported=<d> reported_only=<e> other=<f> sum_equals=<bool> text_blank_mismatch=<g>
  python cy2_month_partition.py <record.json>  -> MONTH-CROSS partition_equal=<bool> fill_bound_equal=<bool>
                                                  comparing the worker's record keys partition ({no_daily, blank_only_unpriced, blank_only_other,
                                                  blank_and_reported, reported_only, other}) and fill_upper_bound (= blank_only_unpriced) with this recompute.
text_blank_mismatch counts UNGRADABLE months whose reason text mentions blank days but daily_returns shows none, or the reverse (expected 0).
Reads counts only; no account, name or dollar value is printed. Needs AWS read credentials.
"""
import io
import json
import sys

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
VERSIONS = {"daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N", "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC"}
REPORTED = ("no reported monthly return", "reported span", "reported rows disagree", "not finite")


def read(s3, t, cols):
    body = s3.get_object(Bucket=BUCKET, Key=BASE % t, VersionId=VERSIONS[t])["Body"].read()
    return pq.read_table(io.BytesIO(body), columns=cols).to_pandas()


def partition():
    s3 = boto3.client("s3", region_name="us-east-1")
    dr = read(s3, "daily_returns", ["account", "date", "return", "blank_reason"])
    mg = read(s3, "month_grades", ["account", "month", "verdict", "reason"])
    dr["month"] = dr["date"].astype(str).str.slice(0, 7)
    bl = dr[dr["return"].isna()].copy()
    bl["unpriced"] = bl["blank_reason"].astype(str) == "UNPRICED"
    g = bl.groupby(["account", "month"])["unpriced"].agg(["size", "all"]).reset_index()
    info = {(str(a), str(m)): (int(n), bool(al)) for a, m, n, al in zip(g["account"], g["month"], g["size"], g["all"])}
    has_daily = set(zip(dr["account"].astype(str), dr["month"].astype(str)))
    ug = mg[mg["verdict"] == "UNGRADABLE"]
    out = dict(no_daily=0, blank_only_unpriced=0, blank_only_other=0, blank_and_reported=0, reported_only=0, other=0)
    mismatch = 0
    for a, m, r in zip(ug["account"].astype(str), ug["month"].astype(str), ug["reason"].astype(str)):
        text = r.lower()
        rep = any(k in text for k in REPORTED)
        nblank, allunp = info.get((a, m), (0, False))
        text_blank = "blank day" in text
        if text_blank != (nblank > 0):
            mismatch += 1
        if (a, m) not in has_daily:
            out["no_daily"] += 1
        elif nblank > 0 and rep:
            out["blank_and_reported"] += 1
        elif nblank > 0 and allunp:
            out["blank_only_unpriced"] += 1
        elif nblank > 0:
            out["blank_only_other"] += 1
        elif rep:
            out["reported_only"] += 1
        else:
            out["other"] += 1
    return len(ug), out, mismatch


n, part, mism = partition()
if len(sys.argv) < 2:
    print("MONTH-PARTITION ungradable=%d no_daily=%d blank_only_unpriced=%d blank_only_other=%d blank_and_reported=%d reported_only=%d other=%d sum_equals=%s text_blank_mismatch=%d"
          % (n, part["no_daily"], part["blank_only_unpriced"], part["blank_only_other"], part["blank_and_reported"], part["reported_only"],
             part["other"], sum(part.values()) == n, mism))
else:
    w = json.load(open(sys.argv[1], encoding="utf-8"))
    print("MONTH-CROSS partition_equal=%s fill_bound_equal=%s" % (w.get("partition") == part, w.get("fill_upper_bound") == part["blank_only_unpriced"]))
