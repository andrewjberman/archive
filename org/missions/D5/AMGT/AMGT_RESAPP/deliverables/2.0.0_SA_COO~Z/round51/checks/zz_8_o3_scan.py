"""AMGT_RESAPP round 51, zz-8 CTO half condition 3 -- HARVST o-3's POPULATION, measured before the GO.
Over every source's served silver `article` (every part-*.parquet under store.table_prefix(source, "silver", "article") for every
source in SOURCE_FOR_PUBLISHER), read the four columns /timeline/day serves from silver (publication_gold._TIMELINE_SILVER_COLUMNS:
article_key, fetched_at, title, published_precision) and, per article_key, the rows at its latest fetched_at.
Prints: parts read, rows, distinct keys; keys whose latest fetched_at is shared by >= 2 rows (TIED); among them keys whose tied rows
differ in `title` or `published_precision` (DIFFERING), each listed. 0 DIFFERING = o-3 cannot move a served body anywhere.
usage: python <this>   (from the repo root; S3 LIST/GET only)"""
import collections
import io
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402
from lib.research.harvest import publication_gold, store  # noqa: E402

COLS = publication_gold._TIMELINE_SILVER_COLUMNS
cl = boto3.client("s3", region_name="us-east-1")


def read(key):
    raw = cl.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
    names = set(pq.read_schema(io.BytesIO(raw)).names)
    return pq.read_table(io.BytesIO(raw), columns=[c for c in COLS if c in names]).to_pylist()


def main():
    keys = []
    per_source = {}
    for source in sorted(set(SOURCE_FOR_PUBLISHER.values())):
        prefix = store.table_prefix(source, "silver", "article")
        n = 0
        for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith(".parquet"):
                    keys.append(o["Key"])
                    n += 1
        per_source[source] = n
    with ThreadPoolExecutor(10) as ex:
        parts = list(ex.map(read, keys))
    by_key = collections.defaultdict(list)
    rows = 0
    for part in parts:
        for r in part:
            rows += 1
            by_key[r.get("article_key")].append(r)
    tied, differing = 0, []
    for k, rs in by_key.items():
        top = max(str(r.get("fetched_at")) for r in rs)
        at_top = [r for r in rs if str(r.get("fetched_at")) == top]
        if len(at_top) >= 2:
            tied += 1
            if len({(r.get("title"), r.get("published_precision")) for r in at_top}) > 1:
                differing.append(k)
    print("sources %d (parts per source %s)" % (len(per_source), per_source))
    print("parts read %d; rows %d; distinct article_keys %d" % (len(keys), rows, len(by_key)))
    print("TIED keys (latest fetched_at shared by >= 2 rows): %d" % tied)
    print("DIFFERING keys (tied rows differ in title or published_precision): %d %s" % (len(differing), sorted(differing)[:20]))
    print("O-3 CANNOT MOVE A SERVED /timeline/day BODY: %s" % ("YES" if not differing else "NO -- the listed keys are the expected diff"))
    return 0 if not differing else 1


if __name__ == "__main__":
    sys.exit(main())
