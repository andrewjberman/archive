"""Count-only: how repeated AccountID rows in fact_allocations relate (identical values or distinct components). GET and LIST only."""
import io
import sys
from collections import Counter
from pathlib import Path

import boto3
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402

reg = opal_naming.load_registry()
row = opal_naming.lookup("cottonwood")
BUCKET = reg["tiers"]["homes"][row["tenancy"]]["silver"]["bucket"]
SRC, SCOPES = list(row["monolith_scopes"].items())[0]
ROOT_SILVER = "%s/%s/silver/" % (SRC, SCOPES[0])


def main():
    s3 = boto3.client("s3", region_name="us-east-1")
    prefix = ROOT_SILVER + "fact_allocations/"
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
    dates = sorted(d for d in dates if "2026-06-22" <= d <= "2026-10-13")
    combo = Counter()
    reads = 1
    for d in dates:
        body = s3.get_object(Bucket=BUCKET, Key=prefix + "date=%s/data.parquet" % d)["Body"].read()
        reads += 1
        t = pq.read_table(io.BytesIO(body), columns=["AccountID", "Account Market Value", "Cash Market Value", "Account Number", "Relationship ID"]).to_pydict()
        groups = {}
        for a, v, c, n, rel in zip(t["AccountID"], t["Account Market Value"], t["Cash Market Value"], t["Account Number"], t["Relationship ID"]):
            groups.setdefault(a, []).append((v, c, n, rel))
        for a, rows in groups.items():
            k = len(rows)
            distinct_v = len(set(r[0] for r in rows))
            distinct_full = len(set(rows))
            combo[(min(k, 5), "values_identical" if distinct_v == 1 else "values_differ", "full_rows_identical" if distinct_full == 1 else "full_rows_differ")] += 1
    print("fact_allocations window partitions read:", len(dates), "S3 reads:", reads)
    print("(rows per account-day, value pattern, full-row pattern) -> account-days:")
    for k, n in sorted(combo.items()):
        print("  ", k, n)


if __name__ == "__main__":
    main()
