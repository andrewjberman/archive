"""Read-only census over ALL fact_transactions partitions (GET only): distinct External Flow vocabulary by Transaction Type, and the
column types. Prints counts and vocabulary words only; no account id, no amount."""
import io
from collections import Counter

import boto3
import pyarrow.parquet as pq

BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    prefix = SILVER + "fact_transactions/"
    dates, tok = [], None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=prefix, Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        dates += [c["Prefix"].rstrip("/").rsplit("date=", 1)[1] for c in r.get("CommonPrefixes", []) if "date=" in c["Prefix"]]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    dates = sorted(dates)
    reads = 1
    ef_vocab = Counter()       # (External Flow value, Transaction Type) -> count
    types = Counter()
    schema_types = {}
    mv_types = Counter()
    nulls_ef = 0
    rows = 0
    for d in dates:
        body = s3.get_object(Bucket=BUCKET, Key="%sfact_transactions/date=%s/data.parquet" % (SILVER, d))["Body"].read()
        reads += 1
        tb = pq.read_table(io.BytesIO(body), columns=["Transaction Type", "External Flow", "Market Value"])
        if not schema_types:
            schema_types = {f.name: str(f.type) for f in tb.schema}
        t = tb.to_pydict()
        for ty, ef, mv in zip(t["Transaction Type"], t["External Flow"], t["Market Value"]):
            rows += 1
            types[ty] += 1
            if ef is None:
                nulls_ef += 1
                ef_vocab[("<NULL>", ty)] += 1
            else:
                ef_vocab[(ef, ty)] += 1
            mv_types[type(mv).__name__] += 1
    print("fact_transactions partitions:", len(dates), "rows:", rows, "S3 reads:", reads)
    print("schema types of the three columns in the first partition:", schema_types)
    print("External Flow null rows:", nulls_ef)
    print("distinct External Flow values overall:")
    per_val = Counter()
    for (v, ty), n in ef_vocab.items():
        per_val[v] += n
    for v, n in per_val.most_common():
        print("  value %r rows %d" % (v, n))
    print("External Flow value by Transaction Type (counts):")
    for (v, ty), n in sorted(ef_vocab.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        print("  type %r value %r rows %d" % (ty, v, n))
    print("Market Value python types seen:", dict(mv_types))


if __name__ == "__main__":
    main()
