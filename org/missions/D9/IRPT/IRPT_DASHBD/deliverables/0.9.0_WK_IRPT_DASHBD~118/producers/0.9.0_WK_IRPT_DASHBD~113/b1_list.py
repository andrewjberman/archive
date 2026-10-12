"""~113 step 6: LIST-ONLY look at the shape of 49 Financial's silver_legacy/transactions prefix (same bucket/prefix ~108 read). Prints counts only.
Usage: python -I b1_list.py"""
import collections
import boto3
from botocore.config import Config

BUCKET = "opal-data-assets"
PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
s3 = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}))
tops = []
for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
    for cp in p.get("CommonPrefixes", []):
        tops.append(cp["Prefix"])
print("top-level partitions", len(tops))
shape = collections.Counter(t[len(PREFIX):].split("=")[0] for t in tops)
print("partition key names", dict(shape))
print("first/last partition token", tops[0][len(PREFIX):], tops[-1][len(PREFIX):])
objs = collections.Counter()
for t in tops[:5] + tops[-5:]:
    r = s3.list_objects_v2(Bucket=BUCKET, Prefix=t)
    objs[len(r.get("Contents", []))] += 1
    print(t[len(PREFIX):], [(o["Key"][len(t):], o["Size"]) for o in r.get("Contents", [])][:5])
