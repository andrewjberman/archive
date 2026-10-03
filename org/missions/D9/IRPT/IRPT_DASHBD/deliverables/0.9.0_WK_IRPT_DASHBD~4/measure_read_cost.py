"""DB-b-17 read-cost measurement. S3 READS ONLY. Ids and counts only; no name, no custodian number printed.

Writes READ_COST_R9.json beside this file. Usage (from the repo root): python <this file>
"""
import gzip
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "reporting-publish"))

import boto3  # noqa: E402
import handler  # noqa: E402
from botocore.config import Config  # noqa: E402
from lib import opal_naming  # noqa: E402

DIRECTORY_BUCKET = "opal-data-bd"  # data/firm_registry.json: the publish firm's directory bucket
POINTER_KEY = "investor-reporting/directory/latest.json"
OUT = Path(__file__).resolve().parent / "READ_COST_R9.json"


def main():
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=32))
    _, firm = handler.resolve_firm()
    pb, pk = handler._split(opal_naming.address("irpt", firm, "platinum", "reporting", "account=0"))
    prefix = pk.rsplit("account=", 1)[0]

    t = time.time()
    raws = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=pb, Prefix=prefix, Delimiter="/"):
        for c in page.get("CommonPrefixes", []):
            tail = c["Prefix"][len(prefix):].strip("/")
            if tail.startswith("account="):
                raws.append(tail[len("account="):])
    t_list = time.time() - t

    t = time.time()
    ptr = json.loads(s3.get_object(Bucket=DIRECTORY_BUCKET, Key=POINTER_KEY)["Body"].read())
    body = s3.get_object(Bucket=DIRECTORY_BUCKET, Key=ptr["key"])["Body"].read()
    t_dir = time.time() - t
    t = time.time()
    directory = json.loads(body)
    t_parse = time.time() - t

    def one(raw):
        t0 = time.time()
        base = prefix + "account=%s/" % raw
        sb = s3.get_object(Bucket=pb, Key=base + "series.json.gz")["Body"].read()
        mb = s3.get_object(Bucket=pb, Key=base + "manifest.json")["Body"].read()
        t1 = time.time()
        series = json.loads(gzip.decompress(sb))
        json.loads(mb)
        return t1 - t0, time.time() - t1, len(sb), len(series["date"])

    t = time.time()
    seq = [one(r) for r in raws]
    t_seq = time.time() - t
    t = time.time()
    with ThreadPoolExecutor(16) as pool:
        list(pool.map(one, raws * 4))
    t_par = time.time() - t

    n = len(raws)
    out = {
        "published_accounts": n,
        "list_prefixes_seconds": round(t_list, 3),
        "list_pages_note": "1 page per 1000 prefixes",
        "directory_bytes": len(body),
        "directory_get_seconds": round(t_dir, 3),
        "directory_parse_seconds": round(t_parse, 3),
        "directory_clients": len(directory["entries"]),
        "seq_per_account_get_seconds_mean": round(sum(x[0] for x in seq) / n, 4),
        "seq_per_account_decode_seconds_mean": round(sum(x[1] for x in seq) / n, 5),
        "seq_total_seconds": round(t_seq, 3),
        "series_gz_bytes_mean": round(sum(x[2] for x in seq) / n),
        "series_days_mean": round(sum(x[3] for x in seq) / n, 1),
        "par16_accounts_read": n * 4,
        "par16_total_seconds": round(t_par, 3),
        "par16_seconds_per_account": round(t_par / (n * 4), 4),
        "vantage": "laptop (not in-region): an upper bound on per-request latency",
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
