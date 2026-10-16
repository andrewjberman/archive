"""HVST-cb-9 start condition 1.d: for each publisher, the earliest and newest object written after the site Z cutoff.

Prefixes come from store.table_prefix (table segment cut, never typed); the bucket is store.HARVEST_BUCKET (read, not typed).
Paginated list_objects_v2, counted client-side, denominator printed. Read only.
Usage: python cb9_s3_writers.py <cutoff ISO Z> <publisher> [<publisher> ...]
"""
from __future__ import annotations

import datetime
import sys

sys.path.insert(0, ".")
from lib.research.harvest import store  # noqa: E402

import boto3  # noqa: E402


def _fmt(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ") if d else "none"


def main(cutoff_iso, publishers):
    cutoff = datetime.datetime.strptime(cutoff_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    client = boto3.client("s3", region_name="us-east-1")
    print("BUCKET=%s (store.HARVEST_BUCKET) CUTOFF=%s" % (store.HARVEST_BUCKET, cutoff_iso))
    for source in publishers:
        for tier in ("bronze", "silver"):
            tp = store.table_prefix(source, tier, "ZZTABLE")
            prefix = tp[: -len("ZZTABLE/")]
            n = pages = after = 0
            newest = earliest_after = None
            for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
                pages += 1
                for obj in page.get("Contents", []) or []:
                    n += 1
                    lm = obj["LastModified"]
                    if newest is None or lm > newest:
                        newest = lm
                    if lm > cutoff:
                        after += 1
                        if earliest_after is None or lm < earliest_after:
                            earliest_after = lm
            print("%s %s prefix=%s objects=%d pages=%d newest=%s after_cutoff=%d earliest_after_cutoff=%s" % (
                source, tier, prefix, n, pages, _fmt(newest), after, _fmt(earliest_after)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
