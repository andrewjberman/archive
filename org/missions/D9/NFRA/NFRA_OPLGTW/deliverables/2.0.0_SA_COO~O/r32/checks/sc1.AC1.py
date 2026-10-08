"""OPLGTW OG-sc-1 AC1 (round 32 item 4, PRD v2.0 items 1-2): the exact column list of seven silver tables, both masters.

Re-derives every fact from live S3, independently of the worker:
  - for each master x table, the newest `date=YYYY-MM-DD/` partition (a delimiter listing of the table prefix);
  - that partition's `data.parquet` schema, read from the FOOTER ONLY (two ranged GETs; no row group is read, and no
    column statistics are read or printed);
and compares them with the worker's record: the newest date, the key, and the column names IN ORDER with their Arrow
types. The record must carry no key named like a statistic (min, max, statistics, null_count, distinct).

  python sc1.AC1.py <record.json>
"""
import io
import json
import re
import struct
import sys

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
MASTERS = ("08242234", "08335338")
TABLES = ("fact_acc", "fact_uln", "fact_ult", "fact_rld", "fact_rly", "fact_rty", "fact_trn")
STAT_KEY = re.compile(r"^(min|max|statistics|stats|null_count|distinct_count|min_value|max_value)$", re.I)


def newest_date(s3, master, table):
    prefix = "schwab/%s/silver/%s/" % (master, table)
    dates, token = [], None
    while True:
        args = {"Bucket": BUCKET, "Prefix": prefix, "Delimiter": "/"}
        if token:
            args["ContinuationToken"] = token
        page = s3.list_objects_v2(**args)
        for cp in page.get("CommonPrefixes") or []:
            m = re.match(re.escape(prefix) + r"date=(\d{4}-\d{2}-\d{2})/$", cp["Prefix"])
            if m:
                dates.append(m.group(1))
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
        if not token:
            break
    return max(dates) if dates else None, len(dates)


def footer_schema(s3, key):
    size = s3.head_object(Bucket=BUCKET, Key=key)["ContentLength"]
    tail = s3.get_object(Bucket=BUCKET, Key=key, Range="bytes=%d-%d" % (size - 8, size - 1))["Body"].read()
    if tail[4:] != b"PAR1":
        raise ValueError("not a parquet tail")
    flen = struct.unpack("<I", tail[:4])[0]
    footer = s3.get_object(Bucket=BUCKET, Key=key, Range="bytes=%d-%d" % (size - 8 - flen, size - 9))["Body"].read()
    sch = pq.read_schema(io.BytesIO(b"PAR1" + footer + tail))
    return [(f.name, str(f.type)) for f in sch]


def stat_keys(obj, path=""):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if STAT_KEY.match(str(k)):
                found.append(path + "/" + str(k))
            found += stat_keys(v, path + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += stat_keys(v, "%s[%d]" % (path, i))
    return found


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        rec = json.load(open(argv[1], encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("record unreadable: %s (%s)" % (argv[1], type(exc).__name__))
        print("RESULT: FAIL")
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    ok, cells = True, 0
    for master in MASTERS:
        for table in TABLES:
            cells += 1
            got = ((rec.get("tables") or {}).get(master) or {}).get(table)
            try:
                live_date, n_parts = newest_date(s3, master, table)
            except Exception as exc:
                print("FAIL: %s/%s: listing failed (%s)" % (master, table, type(exc).__name__))
                ok = False
                continue
            if live_date is None:
                print("FAIL: %s/%s: no partition on S3" % (master, table))
                ok = False
                continue
            key = "schwab/%s/silver/%s/date=%s/data.parquet" % (master, table, live_date)
            if not isinstance(got, dict):
                print("FAIL: %s/%s: absent from the record (live newest %s)" % (master, table, live_date))
                ok = False
                continue
            try:
                live_cols = footer_schema(s3, key)
            except Exception as exc:
                print("FAIL: %s/%s: footer read failed at %s (%s)" % (master, table, key, type(exc).__name__))
                ok = False
                continue
            rec_cols = [(c.get("name"), c.get("type")) for c in got.get("columns") or []]
            same = got.get("newest_date") == live_date and got.get("key") == key and rec_cols == live_cols
            print("%s %s/%s: newest %s of %d partitions, %d columns live, %d in record" % (
                "OK  " if same else "FAIL", master, table, live_date, n_parts, len(live_cols), len(rec_cols)))
            ok = ok and same
    bad = stat_keys(rec)
    if bad:
        print("FAIL: the record carries statistic-like keys: %s" % bad[:10])
        ok = False
    print("cells checked: %d of %d" % (cells, len(MASTERS) * len(TABLES)))
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
