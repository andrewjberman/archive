"""TO-RUN-b11 metadata-only pre/post version and literal key-set checks."""

import datetime
import json
import pathlib
import subprocess
import sys

import boto3

out = pathlib.Path(__file__).resolve().parent
phase = sys.argv[1]
assert phase in ("before", "after")
bucket = "opal-data-transcripts"
prefix = "teams/transcripts/silver/research_meeting/"
expected = set(
    json.loads((out.parent / "research_x9_20261008/RESULT_FOR_DELL2.json").read_text())[
        "keys"
    ]
)
s3 = boto3.client("s3", region_name="us-east-1")
assert s3.get_bucket_versioning(Bucket=bucket)["Status"] == "Enabled"
listed = {
    r["Key"]
    for page in s3.get_paginator("list_objects_v2").paginate(
        Bucket=bucket, Prefix=prefix
    )
    for r in page.get("Contents", [])
}
assert len(listed) == 29 and listed == expected, "STOP: literal keyset differs"
versions = {
    r["Key"]: r["VersionId"]
    for page in s3.get_paginator("list_object_versions").paginate(
        Bucket=bucket, Prefix=prefix
    )
    for r in page.get("Versions", [])
    if r["IsLatest"]
}
assert set(versions) == expected, "STOP: latest versions differ"
trees = {
    pin: subprocess.check_output(
        ["git", "rev-parse", pin + ":research_transcripts/structured"], text=True
    ).strip()
    for pin in ("9f8dddcb9b", "HEAD")
}
assert len(set(trees.values())) == 1, "STOP: input tree mismatch"
if phase == "after":
    prior = json.loads((out / "before-versions.json").read_text())["versions"]
    assert all(versions[k] != prior[k] for k in expected), (
        "STOP: version did not change"
    )
result = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "count": len(listed),
    "exact_keyset": True,
    "versioning": "Enabled",
    "trees": trees,
    "versions": versions,
}
(out / (phase + "-versions.json")).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "versions"}, indent=2))
