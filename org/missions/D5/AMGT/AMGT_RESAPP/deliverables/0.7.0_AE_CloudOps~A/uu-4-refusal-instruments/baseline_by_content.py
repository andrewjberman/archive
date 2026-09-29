"""uu-4 step 1 -- the BASELINE, IDENTIFIED BY CONTENT, never by filename.

Reads the live function config and the artifact key FRESH (a VersionId pinned at signing would be
stale by the apply), downloads the object AT the prior VersionId, and proves it is the bytes that
are running: sha256(b64) of the downloaded object == its own content-sha256 metadata == the live
CodeSha256, and its length == the live CodeSize. Prints every figure with its denominator.
Writes the object to <outdir>/deployed.zip. No AWS write of any kind.
usage: python step1_baseline.py <outdir>
"""
import base64
import hashlib
import json
import os
import sys

import boto3

BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "research/opal-amgt-scoped-api.zip"
FUNCTION = "opal-amgt-scoped-api"
REGION = "us-east-1"
GO_PRIOR_VERSION = "0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS"
GO_PRIOR_SHA = "vBSCqd71wGn1GNOpaWGKr+KdI6t+zo3QVovzEd9Mrew="

outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)

lam = boto3.client("lambda", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)

cfg = lam.get_function_configuration(FunctionName=FUNCTION)
live_sha = cfg["CodeSha256"]
live_size = cfg["CodeSize"]
print("LIVE FUNCTION: CodeSha256=%s CodeSize=%d LastModified=%s LastUpdateStatus=%s Runtime=%s"
      % (live_sha, live_size, cfg["LastModified"], cfg.get("LastUpdateStatus"), cfg.get("Runtime")))
print("GO's prior sha:      %s  -> live==GO? %s" % (GO_PRIOR_SHA, live_sha == GO_PRIOR_SHA))

head = s3.head_object(Bucket=BUCKET, Key=KEY)
cur_ver = head["VersionId"]
print("ARTIFACT HEAD (current): VersionId=%s Size=%d ETag=%s meta=%s"
      % (cur_ver, head["ContentLength"], head["ETag"], json.dumps(head.get("Metadata", {}))))
print("GO's prior VersionId: %s  -> current==GO? %s" % (GO_PRIOR_VERSION, cur_ver == GO_PRIOR_VERSION))

obj = s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=GO_PRIOR_VERSION)
body = obj["Body"].read()
dl_sha = base64.b64encode(hashlib.sha256(body).digest()).decode()
meta_sha = obj.get("Metadata", {}).get("content-sha256")
path = os.path.join(outdir, "deployed.zip")
with open(path, "wb") as fh:
    fh.write(body)

print("\nDOWNLOADED AT VersionId %s: %d bytes -> %s" % (GO_PRIOR_VERSION, len(body), path))
print("  sha256(b64) of downloaded bytes : %s" % dl_sha)
print("  its own content-sha256 metadata : %s" % meta_sha)
print("  live Lambda CodeSha256          : %s" % live_sha)
print("  live Lambda CodeSize            : %d   downloaded length: %d" % (live_size, len(body)))

checks = {
    "downloaded sha == its own metadata": dl_sha == meta_sha,
    "downloaded sha == live CodeSha256": dl_sha == live_sha,
    "downloaded length == live CodeSize": len(body) == live_size,
    "live CodeSha256 == the GO's prior sha": live_sha == GO_PRIOR_SHA,
}
for k, v in checks.items():
    print("  %-40s %s" % (k, "OK" if v else "*** FALSE ***"))

# NEGATIVE CONTROL: a bogus VersionId must be refused, so the successful read is a real read.
try:
    s3.get_object(Bucket=BUCKET, Key=KEY, VersionId="ZZZZnoSuchVersionId999999999999")
    print("  CONTROL BROKEN: a bogus VersionId RESOLVED")
    ctl = False
except Exception as exc:
    print("  CONTROL OK: bogus VersionId refused (%s)" % type(exc).__name__)
    ctl = True

ok = all(checks.values()) and ctl
print("\nBASELINE %s -- these are%s the bytes that are running" % ("ESTABLISHED" if ok else "REFUSED", "" if ok else " NOT provably"))
sys.exit(0 if ok else 1)
