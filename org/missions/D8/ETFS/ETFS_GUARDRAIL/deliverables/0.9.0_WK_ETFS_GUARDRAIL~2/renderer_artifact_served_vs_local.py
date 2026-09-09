"""renderer_artifact_served_vs_local.py -- EG-s-6 S6-AC6: the 6 uploaded artifacts
(the renderer + the 3 committed coverage-package files + the 2 build-time copies
taken from lib/ and data/inf/scripts/silver/) match their local sources by
head-object ETag vs local md5 (ETag == md5 hex for a single-part, non-multipart
upload -- true here, every file well under the 8 MiB multipart threshold).

READ-ONLY: 6 lambda-artifacts-bucket head_object calls (via boto3 directly -- Python
spawning the .tools/aws bash shim as a subprocess is a known trap on this box,
CLAUDE.md Rule 16) + 6 local file reads. Prints each pair and ONE verdict line.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys

import boto3

HERE_REPO_ROOT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
).stdout.strip()

BUCKET = "opal-313476888478-lambda-artifacts"

# (local path, relative to repo root, S3 key)
PAIRS = [
    ("data/etfs/scripts/presentation/render_month_end.py", "ec2/etfs-reports/render_month_end.py"),
    ("data/etfs/scripts/coverage/__init__.py", "ec2/etfs-reports/coverage/__init__.py"),
    ("data/etfs/scripts/coverage/classifier.py", "ec2/etfs-reports/coverage/classifier.py"),
    ("data/etfs/scripts/coverage/remediate.py", "ec2/etfs-reports/coverage/remediate.py"),
    ("lib/trading_calendar.py", "ec2/etfs-reports/coverage/trading_calendar.py"),
    ("data/inf/scripts/silver/_orion_vendor_asof.py", "ec2/etfs-reports/coverage/_orion_vendor_asof.py"),
]


def main() -> int:
    s3 = boto3.client("s3")
    match_count = 0
    for local_rel, key in PAIRS:
        local_path = HERE_REPO_ROOT + "/" + local_rel
        local_bytes = open(local_path, "rb").read()
        local_md5 = hashlib.md5(local_bytes).hexdigest()
        try:
            head = s3.head_object(Bucket=BUCKET, Key=key)
            served_etag = head["ETag"].strip('"')
        except Exception as exc:
            print("PAIR %-70s -> MISSING (%s)" % (key, str(exc)[:150]))
            continue
        ok = served_etag == local_md5
        if ok:
            match_count += 1
        print("PAIR %-70s local_md5=%s served_etag=%s %s" % (
            key, local_md5, served_etag, "MATCH" if ok else "MISMATCH"))

    total = len(PAIRS)
    print("VERDICT: %s %d of %d" % ("MATCH" if match_count == total else "MISMATCH", match_count, total))
    return 0 if match_count == total else 1


if __name__ == "__main__":
    sys.exit(main())
