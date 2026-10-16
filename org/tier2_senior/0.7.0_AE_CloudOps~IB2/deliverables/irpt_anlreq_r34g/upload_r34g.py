"""IRPT_ANLREQ TO-APPLY-R34G step 3 (the r34g release) (0.7.0_AE_CloudOps~IB2, adapted from the AQ2 r34e script): D1, the upload of the three r34g artifacts to three NEW keys.

  python upload_r34g.py --live --go

PHASE 1 (no write): the three stage files (C:/dev/irpt-release-r34m) are re-hashed against the order's values, and every one of the three keys
must read 404 (head_object); any key that exists, or any difference, STOPS with nothing uploaded. PHASE 2: put_object of each file from the
stage folder, then a get_object of that VersionId read back and its sha256 and size compared. Prints one line per key and the VersionIds.
Deletes nothing and touches no r34 (first attempt) key.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REGION = "us-east-1"
BUCKET = "opal-313476888478-lambda-artifacts"
PREFIX = "ec2/investor-reporting-ycharts/resident/"
STAGE = Path("C:/dev/irpt-release-r34m")
ITEMS = (
    ("irpt-resident-0485393f3a-r34g.tar.gz", STAGE / "irpt-resident-0485393f3a-r34g.tar.gz", "1e5b3ef4120b8799ebd5f1cf620044b01b5e1bfeac2e1d4169d3f576a802580b"),
    ("irpt-resident-0485393f3a-r34g.package.SHA256SUMS", STAGE / "irpt-resident-0485393f3a-r34g.package.SHA256SUMS", "31813fd356336524b9ee76daa6411bef60ac57dba5bd53806c537f11396f3936"),
    ("resident_host_install_0485393f3a-r34g.sh", STAGE / "scripts" / "resident_host_install_0485393f3a-r34g.sh", "ef1e4999f585d640ec738992a7705771a716179286a2ab05186f0e7c21769b1a"),
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
