"""List every object VERSION (and delete markers) under a name's four prefixes. usage: py -3.12 list_prefixes.py <KEY> <out.json>"""
import json
import sys

import boto3
B = "opal-data-harvest"
key, out = sys.argv[1:3]
prefixes = ["sec/harvest/silver/filing_source/", "filings/v1/%s/" % key, "drafting/v1/%s." % key,
            "amgt/harvest/state/filing_attempt/security_key=%s/" % key]
s3 = boto3.client("s3", region_name="us-east-1")
res = {}
for p in prefixes:
    rows = []
    for page in s3.get_paginator("list_object_versions").paginate(Bucket=B, Prefix=p):
        for v in page.get("Versions", []):
            rows.append({"key": v["Key"], "version_id": v["VersionId"], "last_modified": v["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), "size": v["Size"], "is_latest": v["IsLatest"]})
        for v in page.get("DeleteMarkers", []):
            rows.append({"key": v["Key"], "version_id": v["VersionId"], "last_modified": v["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), "size": -1, "is_latest": v["IsLatest"], "delete_marker": True})
    res[p] = rows
json.dump(res, open(out, "w"), indent=1)
for p, r in res.items():
    print(p, len(r), "versions;", sum(1 for x in r if x["is_latest"]), "latest")
