"""IRPT_ANLREQ TO-APPLY-R34L step 3 (the r34l release) (0.7.0_AE_CloudOps~IB2, adapted from the AQ2 r34e script): D1, the upload of the three r34l artifacts to three NEW keys.

  python upload_r34l.py --live --go

PHASE 1 (no write): the three stage files (C:/dev/irpt-release-r35d) are re-hashed against the order's values, and every one of the three keys
must read 404 (head_object); any key that exists, or any difference, STOPS with nothing uploaded. PHASE 2: put_object of each file from the
stage folder, then a get_object of that VersionId read back and its sha256 and size compared. Prints one line per key and the VersionIds.
Deletes nothing and touches no earlier release key.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REGION = "us-east-1"
BUCKET = "opal-313476888478-lambda-artifacts"
PREFIX = "ec2/investor-reporting-ycharts/resident/"
STAGE = Path("C:/dev/irpt-release-r35d")
ITEMS = (
    ("irpt-resident-0485393f3a-r34l.tar.gz", STAGE / "irpt-resident-0485393f3a-r34l.tar.gz", "e1466cb8a0465572e4e0f9a42d79e193313c8afea5fbc2f3370a9ec015a33b6c"),
    ("irpt-resident-0485393f3a-r34l.package.SHA256SUMS", STAGE / "irpt-resident-0485393f3a-r34l.package.SHA256SUMS", "d5aa71aa6614baa9dc49c897e3b1d1f7ab25e830defc726127fbc9d89c1f8057"),
    ("resident_host_install_0485393f3a-r34l.sh", STAGE / "scripts" / "resident_host_install_0485393f3a-r34l.sh", "e4b73ff0c60b9f31c7d534e05304dab54a55d1cfb4f4e45b335c329f39c59e1d"),
)


def live():
    import boto3
    from botocore.exceptions import ClientError
    s3 = boto3.client("s3", region_name=REGION)
    blobs = {}
    for key, path, sha in ITEMS:
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha:
            print("STOP: %s differs from the order's sha256; nothing uploaded" % key)
            return 2
        blobs[key] = raw
    print("PHASE 1a: %d of %d stage files equal the order's sha256" % (len(blobs), len(ITEMS)))
    for key, _, _ in ITEMS:
        try:
            s3.head_object(Bucket=BUCKET, Key=PREFIX + key)
            print("STOP: key %s already exists; nothing uploaded" % key)
            return 2
        except ClientError as e:
            if e.response["Error"]["Code"] not in ("404", "NoSuchKey", "NotFound"):
                print("STOP: head_object %s answered %s, not 404; nothing uploaded" % (key, e.response["Error"]["Code"]))
                return 2
    print("PHASE 1b: %d of %d keys read 404 before any write" % (len(ITEMS), len(ITEMS)))
    bad = 0
    for key, _, sha in ITEMS:
        r = s3.put_object(Bucket=BUCKET, Key=PREFIX + key, Body=blobs[key])
        vid = r.get("VersionId")
        got = s3.get_object(Bucket=BUCKET, Key=PREFIX + key, VersionId=vid)["Body"].read()
        ok = hashlib.sha256(got).hexdigest() == sha and len(got) == len(blobs[key])
        bad += not ok
        print("D1 %s VersionId %s size %d sha256 %s %s" % (key, vid, len(got), hashlib.sha256(got).hexdigest(), "EQUAL" if ok else "DIFFERENT"))
    print("D1 RESULT: %d of %d uploaded and read back equal" % (len(ITEMS) - bad, len(ITEMS)))
    return 0 if not bad else 1


if __name__ == "__main__":
    if "--live" in sys.argv and "--go" in sys.argv:
        sys.exit(live())
    print(__doc__)
    sys.exit(2)
