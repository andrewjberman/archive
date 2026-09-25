"""Shared S3 read instrument for HVST-s-1 AC0/AC2/AC3/AC4.

READ ONLY. Never puts, never deletes. Every count prints its own denominator.
"""

import io
import json
import pickle

import pyarrow.parquet as pq

import lib.research.harvest.store as store
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER

PUBLISHERS = tuple(sorted(SOURCE_FOR_PUBLISHER))


def _client():
    return store._default_client()


def _objects(prefix, client):
    keys = []
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            keys.append(obj["Key"])
    return keys


def snapshot(client=None):
    """{publisher: {...}} plus every silver listing_hit ROW, read fresh from S3 at call time."""
    client = client or _client()
    out = {}
    all_rows = []
    for publisher in PUBLISHERS:
        source = SOURCE_FOR_PUBLISHER[publisher]
        silver_prefix = store.table_prefix(source, "silver", "listing_hit")
        bronze_prefix = store.table_prefix(source, "bronze", "news_listing")
        silver_keys = [k for k in _objects(silver_prefix, client) if k.endswith(".parquet")]
        bronze_keys = _objects(bronze_prefix, client)
        rows = []
        for key in silver_keys:
            resp = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
            raw = resp["Body"].read() if hasattr(resp["Body"], "read") else resp["Body"]
            for row in pq.read_table(io.BytesIO(raw)).to_pylist():
                row["_source_object"] = key
                rows.append(row)
        for row in rows:
            all_rows.append(row)
        out[publisher] = {
            "source": source,
            "silver_prefix": silver_prefix,
            "bronze_prefix": bronze_prefix,
            "silver_listing_hit_parts": len(silver_keys),
            "silver_listing_hit_rows": len(rows),
            "bronze_news_listing_objects": len(bronze_keys),
        }
    return out, all_rows


def dump(path, counts, rows):
    with open(path, "wb") as fh:
        pickle.dump({"counts": counts, "rows": rows}, fh)


def load(path):
    with open(path, "rb") as fh:
        blob = pickle.load(fh)
    return blob["counts"], blob["rows"]


def print_counts(label, counts):
    print("%s -- silver listing_hit rows per publisher (denominator: %d publishers, the five in "
          "SOURCE_FOR_PUBLISHER)" % (label, len(PUBLISHERS)))
    total_rows = 0
    total_bronze = 0
    for publisher in PUBLISHERS:
        c = counts[publisher]
        total_rows += c["silver_listing_hit_rows"]
        total_bronze += c["bronze_news_listing_objects"]
        print("  %-8s silver listing_hit rows=%-6d (parts=%d)   bronze news_listing objects=%d"
              % (publisher, c["silver_listing_hit_rows"], c["silver_listing_hit_parts"],
                 c["bronze_news_listing_objects"]))
    print("  TOTAL    silver listing_hit rows=%d across %d publishers; bronze news_listing objects=%d "
          "across %d publishers" % (total_rows, len(PUBLISHERS), total_bronze, len(PUBLISHERS)))
    print("  sa EXPLICIT: silver listing_hit rows = %d ; bronze news_listing objects = %d"
          % (counts["sa"]["silver_listing_hit_rows"], counts["sa"]["bronze_news_listing_objects"]))


def json_counts(counts):
    return json.dumps(counts, indent=1, sort_keys=True)
