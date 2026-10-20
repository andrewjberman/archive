"""R22-DL1 precondition 2 (pair section 3): READ-ONLY. Every manifest entry PRESENT at its version, one version + no marker on its key,
no ObjectLockMode / legal hold / retention. Writes nothing."""
from __future__ import annotations

import json
import sys

import boto3
from botocore.exceptions import ClientError

M = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json"
objs = json.load(open(M, encoding="utf-8"))["objects"]
s3 = boto3.client("s3", region_name="us-east-1")
bad, rows = [], 0
for b in sorted({o["bucket"] for o in objs}):
    try:
        cfg = s3.get_object_lock_configuration(Bucket=b)["ObjectLockConfiguration"]
        print("bucket %s ObjectLockConfiguration: %s" % (b, json.dumps(cfg)))
    except ClientError as e:
        print("bucket %s object-lock config: %s" % (b, e.response["Error"]["Code"]))
for o in objs:
    b, k, v = o["bucket"], o["key"], o["version_id"]
    try:
        h = s3.head_object(Bucket=b, Key=k, VersionId=v)
    except ClientError as e:
        bad.append((k, "head %s" % e.response["Error"]["Code"]))
        continue
    lock = [h.get("ObjectLockMode"), h.get("ObjectLockLegalHoldStatus"), h.get("ObjectLockRetainUntilDate")]
    if any(lock):
        bad.append((k, "LOCK/RETENTION %s" % lock))
    vs = []
    for page in s3.get_paginator("list_object_versions").paginate(Bucket=b, Prefix=k):
        for ver in page.get("Versions", []):
            if ver["Key"] == k:
                vs.append(ver)
        for mark in page.get("DeleteMarkers", []):
            if mark["Key"] == k:
                bad.append((k, "delete marker present"))
    if len(vs) != 1 or vs[0]["VersionId"] != v:
        bad.append((k, "versions on key: %d" % len(vs)))
    rows += 1
print("entries %d, read clean %d, problems %d" % (len(objs), rows - len({b0[0] for b0 in bad}), len(bad)))
for k, why in bad:
    print("PROBLEM", k, why)
sys.exit(1 if bad else 0)
