"""HVST-cb-2 start condition 1.c: newest LastModified per wsj/barrons bronze and silver prefix.

Prefixes are derived with store.table_prefix (the table segment is cut, never typed). Listing is paginated and
counted client-side; the denominator (objects scanned) is printed beside every newest-LastModified value.
Read only. Usage: python cb2_s3_lastmodified.py <bucket> <cutoff ISO Z>
"""
from __future__ import annotations

import sys
import datetime

sys.path.insert(0, ".")
from lib.research.harvest import store  # noqa: E402

import boto3  # noqa: E402


def main(bucket, cutoff_iso):
    cutoff = datetime.datetime.strptime(cutoff_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    client = boto3.client("s3", region_name="us-east-1")
    print("BUCKET=%s CUTOFF=%s" % (bucket, cutoff_iso))
    bad = 0
    for source in ("wsj", "barrons"):
        for tier in ("bronze", "silver"):
            tp = store.table_prefix(source, tier, "ZZTABLE")
            prefix = tp[: -len("ZZTABLE/")]
            n = 0
            newest = None
            newest_key = None
            after = 0
            pages = 0
            for page in client.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
                pages += 1
                for obj in page.get("Contents", []) or []:
                    n += 1
                    lm = obj["LastModified"]
                    if newest is None or lm > newest:
                        newest, newest_key = lm, obj["Key"]
                    if lm > cutoff:
                        after += 1
            if newest is None:
                verdict = "EMPTY_PREFIX"
            elif after:
                verdict = "WRITTEN_AFTER_CUTOFF"
                bad += 1
            else:
                verdict = "OLDER_THAN_CUTOFF"
            print(
                "%s %s prefix=%s objects=%d pages=%d newest=%s after_cutoff=%d %s newest_key=%s"
                % (source, tier, prefix, n, pages,
                   newest.strftime("%Y-%m-%dT%H:%M:%SZ") if newest else "none", after, verdict, newest_key)
            )
    print("PREFIXES_WRITTEN_AFTER_CUTOFF=%d" % bad)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
