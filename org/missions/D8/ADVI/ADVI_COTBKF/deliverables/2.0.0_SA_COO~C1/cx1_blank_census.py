"""ADVI_COTBKF TO-CB-cx-1 (issuer's check): the census of blanks by reason on the SERVED FWD-3 tables, recomputed from the served objects.

Reads (read-only, one get each, at the pinned VersionIds; counts only) the served daily_returns, month_grades and account_day_value.
  python cx1_blank_census.py                -> prints three lines:
    CENSUS-DAYS total=<n> with_return=<n> blank=<n> unreasoned=<n> by_reason=<REASON:count,...sorted by reason>
    CENSUS-MONTHS total=<n> not_match=<n> unreasoned=<n> by_verdict=<VERDICT:count,...sorted; ABSENT = a null verdict>
    CENSUS-UNPRICED rows=<n> cusips=<n> never_priced_cusips=<n> never_priced_rows=<n> gap_cusips=<n> gap_rows=<n>
  python cx1_blank_census.py <record.json>  -> prints   CENSUS-CROSS days_equal=<bool> months_equal=<bool> unreasoned_equal=<bool> unpriced_equal=<bool>
    comparing the worker's record keys days, months, unreasoned, unpriced with this independent recompute.
Definitions: a blank day is a daily_returns row with a null return; unreasoned = blank with a null blank_reason (days) or a month that is
not MATCH and has a null reason and a non-null verdict (months). UNPRICED holding-days = account_day_value rows with a null close and a
null blank_reason (a held or regressed row carries its own reason and is not in this partition); a cusip is NEVER-PRICED when no row of the
table carries a close for it, GAP otherwise. No account, cusip or value is printed. Needs AWS read credentials.
"""
import io
import json
import sys

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
VERSIONS = {"daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N", "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC",
            "account_day_value": "ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a"}


def read(s3, t, cols):
    body = s3.get_object(Bucket=BUCKET, Key=BASE % t, VersionId=VERSIONS[t])["Body"].read()
    return pq.read_table(io.BytesIO(body), columns=cols).to_pandas()


def census():
    s3 = boto3.client("s3", region_name="us-east-1")
    dr = read(s3, "daily_returns", ["return", "blank_reason"])
    blank = dr[dr["return"].isna()]
    by_reason = blank["blank_reason"].fillna("NONE").astype(str).value_counts().to_dict()
    days = dict(total=int(len(dr)), with_return=int(len(dr) - len(blank)), blank=int(len(blank)),
                unreasoned=int(blank["blank_reason"].isna().sum()), by_reason={k: int(v) for k, v in sorted(by_reason.items())})
    mg = read(s3, "month_grades", ["verdict", "reason"])
    nm = mg[mg["verdict"] != "MATCH"]
    by_verdict = mg["verdict"].fillna("ABSENT").astype(str).value_counts().to_dict()
    months = dict(total=int(len(mg)), not_match=int(len(nm)), unreasoned=int((nm["verdict"].notna() & nm["reason"].isna()).sum()),
                  by_verdict={k: int(v) for k, v in sorted(by_verdict.items())})
    av = read(s3, "account_day_value", ["cusip", "close", "blank_reason"])
    priced_cusips = set(av.loc[av["close"].notna(), "cusip"].astype(str))
    un = av[av["close"].isna() & av["blank_reason"].isna()]
    uc = un["cusip"].astype(str)
    never = uc[~uc.isin(priced_cusips)]
    gap = uc[uc.isin(priced_cusips)]
    unpriced = dict(rows=int(len(un)), cusips=int(uc.nunique()), never_priced_cusips=int(never.nunique()), never_priced_rows=int(len(never)),
                    gap_cusips=int(gap.nunique()), gap_rows=int(len(gap)))
    return days, months, unpriced


days, months, unpriced = census()
if len(sys.argv) < 2:
    print("CENSUS-DAYS total=%d with_return=%d blank=%d unreasoned=%d by_reason=%s" % (
        days["total"], days["with_return"], days["blank"], days["unreasoned"], ",".join("%s:%d" % kv for kv in days["by_reason"].items())))
    print("CENSUS-MONTHS total=%d not_match=%d unreasoned=%d by_verdict=%s" % (
        months["total"], months["not_match"], months["unreasoned"], ",".join("%s:%d" % kv for kv in months["by_verdict"].items())))
    print("CENSUS-UNPRICED rows=%d cusips=%d never_priced_cusips=%d never_priced_rows=%d gap_cusips=%d gap_rows=%d" % (
        unpriced["rows"], unpriced["cusips"], unpriced["never_priced_cusips"], unpriced["never_priced_rows"], unpriced["gap_cusips"], unpriced["gap_rows"]))
else:
    w = json.load(open(sys.argv[1], encoding="utf-8"))
    print("CENSUS-CROSS days_equal=%s months_equal=%s unreasoned_equal=%s unpriced_equal=%s" % (
        w.get("days") == days, w.get("months") == months,
        w.get("unreasoned") == dict(days=days["unreasoned"], months=months["unreasoned"]), w.get("unpriced") == unpriced))
