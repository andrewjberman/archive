"""Read-only: do consecutive transaction partitions of the 49 Financial (Schwab fact_trn) and Inflection (Orion fact_transactions) silver repeat rows? Counts only."""
import hashlib
import io
import sys

sys.path.insert(0, "C:/dev/ajb_workspace/data/assets/scripts/gold/irpt_reporting/adapters")
sys.path.insert(0, "C:/dev/ajb_workspace/lib")
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def list_parts(bucket, prefix):
    days, tok = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix, "Delimiter": "/"}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        days += [c["Prefix"][len(prefix):].strip("/") for c in r.get("CommonPrefixes", [])]
        tok = r.get("NextContinuationToken")
        if not tok:
            break
    return sorted(d[5:] for d in days if d.startswith("date="))


def read_part(bucket, prefix, day):
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, day)).get("Contents", []) if o["Key"].endswith(".parquet")]
    tabs = [pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read())) for k in keys]
    return tabs


def measure(label, bucket, prefix, date_cols, n=12):
    parts = list_parts(bucket, prefix)
    print(label, "partitions", len(parts), "last", parts[-3:])
    seen = set()
    total = dup = 0
    for p in parts[-n:]:
        tabs = read_part(bucket, prefix, p)
        rows = 0
        datevals = set()
        for t in tabs:
            cols = t.column_names
            dc = [c for c in date_cols if c in cols]
            if dc:
                datevals |= {str(x)[:10] for x in t.column(dc[0]).to_pylist()}
            d = t.to_pydict()
            keys = list(d)
            for i in range(t.num_rows):
                h = hashlib.sha1(("|".join(str(d[k][i]) for k in keys)).encode("utf-8")).hexdigest()
                rows += 1
                if h in seen:
                    dup += 1
                seen.add(h)
        total += rows
        print("  ", p, "rows", rows, "distinct date values", len(datevals), "range", (min(datevals), max(datevals)) if datevals else "-")
    print(label, "sampled rows", total, "rows identical to a row of an earlier sampled partition", dup)


import inflection_account_dim as iad  # noqa: E402

orion = [pfx for pfx in iad.GRANTED_PREFIXES if "/orion/" in pfx][0]
ob, op = orion[len("s3://"):].split("/", 1)
measure("INFLECTION fact_transactions", ob, op + "silver/fact_transactions/", ["transDate"])
measure("49F fact_trn", "opal-data-assets", "schwab/08335338/silver/fact_trn/", ["trade_date", "tran_dt", "td_dt", "proc_dt"])
