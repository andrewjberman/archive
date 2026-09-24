"""AMGT_CORPUS d-5 re-fire -- the one-version-per-run discriminator (CTO R-49/R-51, NEVER-1).

READ-ONLY: prints the served crosswalk key's version list (count, latest VersionId, size,
ETag, sha256 of the body) and the raw bronze identity partition count. Run BEFORE the fire and
AFTER it; the pair's blast radius is ONE new version of the key (or none, when nothing landed).

  PYTHONPATH="$(pwd)" python org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~X/refire_versions_probe.py [as_of] [label]
"""
import datetime
import hashlib
import json
import sys

import boto3

AS_OF = sys.argv[1] if len(sys.argv) > 1 else "2026-09-24"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "probe"
BUCKET = "opal-data-harvest"
KEY = "crosswalk/v1/%s.json" % AS_OF
RAW_PREFIX = "bloomberg/harvest/bronze/identity/"

client = boto3.client("s3", region_name="us-east-1")
now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

versions = []
markers = 0
for page in client.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=KEY):
    versions.extend(v for v in page.get("Versions", []) if v["Key"] == KEY)
    markers += sum(1 for m in page.get("DeleteMarkers", []) if m["Key"] == KEY)
versions.sort(key=lambda v: v["LastModified"])
latest = [v for v in versions if v["IsLatest"]]
head = client.head_object(Bucket=BUCKET, Key=KEY)
body = client.get_object(Bucket=BUCKET, Key=KEY)["Body"].read()
doc = json.loads(body.decode("utf-8"))
den = doc.get("denominators", {})

raw_objects = 0
raw_partitions = set()
for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=RAW_PREFIX):
    for obj in page.get("Contents", []):
        raw_objects += 1
        raw_partitions.add(obj["Key"].split("/")[4] if obj["Key"].count("/") >= 5 else obj["Key"])

out = {
    "label": LABEL,
    "read_at": now,
    "key": "s3://%s/%s" % (BUCKET, KEY),
    "versions": len(versions),
    "delete_markers": markers,
    "latest_version_id": latest[0]["VersionId"] if latest else None,
    "latest_last_modified": latest[0]["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ") if latest else None,
    "size": head["ContentLength"],
    "etag": head["ETag"],
    "sha256": hashlib.sha256(body).hexdigest(),
    "meta_document_sha256": head.get("Metadata", {}).get("document-sha256"),
    "denominators": {k: den.get(k) for k in ("records", "MEASURED", "UNRESOLVED", "registered", "universe_registered")},
    "raw_identity_objects": raw_objects,
    "raw_identity_partitions": len(raw_partitions),
}
print(json.dumps(out, indent=1))
