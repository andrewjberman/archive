"""IRPT_ANLREQ TO-APPLY-YFDEPS step 4 (0.7.0_AE_CloudOps~AQ2): D1, the upload of the 17 approved wheels to 17 NEW keys.

  python upload_yf.py --selftest
  python upload_yf.py --live --go

Reads the approved list (yf_wheels.json: file name, sha256, size) and the collection folder. PHASE 1 (no write): the folder's 17 wheels
are re-hashed against the list, and every one of the 17 keys must read 404 (head_object); any key that exists, or any difference, STOPS with
nothing uploaded. PHASE 2: put_object of each wheel from the collection folder (the named list only; receipts never travel), then a
get_object of that VersionId read back and its sha256 and size compared with the table. Prints one line per key (name, VersionId, size,
EQUAL) and the 17 VersionIds. Writes nothing else; deletes nothing.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REGION = "us-east-1"
BUCKET = "opal-313476888478-lambda-artifacts"
PREFIX = "ec2/investor-reporting-ycharts/resident/pydeps-wheels/yfinance-1.2.0/"
LIST = Path("org/tier1_exec/2.0.0_SA_COO~G2/deliverables/yf/yf_wheels.json")
FOLDER = Path("C:/opal-intake/inbound/yfinance-linux-cp312")


def load_list(path):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = rows if isinstance(rows, list) else rows.get("wheels", rows)
    out = {}
    for r in rows:
        out[r.get("file") or r.get("file_name") or r.get("name")] = (r["sha256"], int(r.get("size") or r.get("bytes")))
    return out


def equal(raw, sha, size):
    return hashlib.sha256(raw).hexdigest() == sha and len(raw) == size


def selftest():
    raw = b"abc"
    sha = hashlib.sha256(raw).hexdigest()
    assert equal(raw, sha, 3) and not equal(raw, sha, 4) and not equal(b"abd", sha, 3)
    want = load_list(LIST)
    assert len(want) == 17 and all(k.endswith(".whl") for k in want)
    print("SELFTEST OK equal() (match, wrong size, wrong bytes) and the approved list reads 17 wheels")
    return 0


def live():
    import boto3
    from botocore.exceptions import ClientError
    s3 = boto3.client("s3", region_name=REGION)
    want = load_list(LIST)
    blobs = {}
    for name, (sha, size) in sorted(want.items()):
        raw = (FOLDER / name).read_bytes()
        if not equal(raw, sha, size):
            print("STOP: %s differs from the approved list; nothing uploaded" % name)
            return 2
        blobs[name] = raw
    print("PHASE 1a: %d of %d collected wheels equal the approved list" % (len(blobs), len(want)))
    exist = []
    for name in sorted(want):
        try:
            s3.head_object(Bucket=BUCKET, Key=PREFIX + name)
            exist.append(name)
        except ClientError as e:
            if e.response["Error"]["Code"] not in ("404", "NoSuchKey", "NotFound"):
                print("STOP: head_object %s answered %s, not 404; nothing uploaded" % (name, e.response["Error"]["Code"]))
                return 2
    if exist:
        print("STOP: %d key(s) already exist %s; nothing uploaded" % (len(exist), exist))
        return 2
    print("PHASE 1b: %d of %d keys read 404 before any write" % (len(want), len(want)))
    vids, bad = [], 0
    for name in sorted(want):
        sha, size = want[name]
        r = s3.put_object(Bucket=BUCKET, Key=PREFIX + name, Body=blobs[name])
        vid = r.get("VersionId")
        got = s3.get_object(Bucket=BUCKET, Key=PREFIX + name, VersionId=vid)["Body"].read()
        ok = equal(got, sha, size)
        bad += not ok
        vids.append((name, vid))
        print("D1 %s VersionId %s size %d %s" % (name, vid, len(got), "EQUAL" if ok else "DIFFERENT"))
    print("D1 RESULT: %d of %d uploaded and read back equal" % (len(want) - bad, len(want)))
    print("VERSIONIDS " + json.dumps(dict(vids), sort_keys=True))
    return 0 if not bad else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--live" in sys.argv and "--go" in sys.argv:
        sys.exit(live())
    print(__doc__)
    sys.exit(2)
