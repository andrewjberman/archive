#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-10 second pass -- the S95 BUILD-STORE RESTORE (COO ruling on S95, msg 98244).

For each function whose plan carried a CODE change (irpt-status, irpt-narrative, irpt-export-render,
irpt-performance-adapter): download the LIVE zip (get-function Code.Location), verify its sha256(b64) == the live
CodeSha256 (a mismatch is a STOP for that function, nothing uploaded), then upload THOSE bytes to the manifest's
artifact key in the versioned build store with content-sha256 metadata == the live CodeSha256, and read the new
version back (length, metadata, re-downloaded sha256). The artifact at rest then equals what AWS serves, so the
yang-lambda module's source_code_hash (the latest version's content-sha256) equals the live CodeSha256 and the
re-plan carries no code change.

Touches the BUILD STORE ONLY -- never a function (no update-function-code, no apply). The displaced version (the
07:29-07:31Z build) is recorded by VersionId and stays in the versioned bucket. Run under the ledger
irpt-bckend-ib-rtf-10-build-store-restore. Prints no URL (the presigned Code.Location is never printed).
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import os
import sys
import urllib.request

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-10_build_store_restore_output.txt")
BUCKET = "opal-313476888478-lambda-artifacts"
FUNCS = ("irpt-status", "irpt-narrative", "irpt-export-render", "irpt-performance-adapter")
# The versions the first pass measured as the latest at each key; a different latest now is a STOP for that key
# (someone else wrote the build store after the ruling was made against this state).
EXPECTED_DISPLACED = {
    "irpt-status": "Fp_QWlcKDid_IrVgxtdbSHZoTcu5iHLx",
    "irpt-narrative": "xJmLYKYZ6Ad5W6NMIusKtOh3QbY_IIvM",
    "irpt-export-render": "4SHjHG9.poTQt9USOtnNtLqg393Ww1b_",
    "irpt-performance-adapter": "b_FS5lpcphi04WwjjlTTXT_NxIkCFomi",
}
LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def b64sha(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def main() -> int:
    lam = boto3.client("lambda", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    sts = boto3.client("sts")
    emit("IB-rtf-10 S95 build-store restore -- run at %s -- as %s" % (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), sts.get_caller_identity()["Arn"]))
    ok_n = 0
    for fn in FUNCS:
        key = "investor-reporting/%s.zip" % fn
        live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        loc = lam.get_function(FunctionName=fn)["Code"]["Location"]
        body = urllib.request.urlopen(loc, timeout=120).read()  # URL never printed
        got = b64sha(body)
        before = s3.head_object(Bucket=BUCKET, Key=key)
        displaced = before.get("VersionId")
        emit("%s: live CodeSha256 %s; downloaded %d bytes sha256(b64) %s -> %s; latest at %s is version %s "
             "(content-sha256 %s, uploaded %s)" % (fn, live, len(body), got, "EQUAL" if got == live else "DIFFERS",
                                                   key, displaced, (before.get("Metadata") or {}).get("content-sha256"),
                                                   before["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")))
        if got != live:
            emit("  STOP for %s: the downloaded bytes are not the served bytes -- nothing uploaded" % fn)
            continue
        if displaced != EXPECTED_DISPLACED[fn]:
            emit("  STOP for %s: the latest version is %s, not the %s the ruling was made against -- nothing uploaded"
                 % (fn, displaced, EXPECTED_DISPLACED[fn]))
            continue
        put = s3.put_object(Bucket=BUCKET, Key=key, Body=body, ServerSideEncryption="AES256",
                            Metadata={"content-sha256": live})
        new_v = put["VersionId"]
        after = s3.head_object(Bucket=BUCKET, Key=key, VersionId=new_v)
        back = s3.get_object(Bucket=BUCKET, Key=key, VersionId=new_v)["Body"].read()
        latest = s3.head_object(Bucket=BUCKET, Key=key).get("VersionId")
        live_after = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        good = (after["ContentLength"] == len(body) and (after.get("Metadata") or {}).get("content-sha256") == live
                and b64sha(back) == live and latest == new_v and live_after == live)
        ok_n += good
        emit("  uploaded -> version %s (latest=%s); ContentLength %d; content-sha256 %s; read-back sha256(b64) %s; "
             "function CodeSha256 after %s (unchanged=%s) -> %s" % (
                 new_v, latest == new_v, after["ContentLength"], (after.get("Metadata") or {}).get("content-sha256"),
                 b64sha(back), live_after, live_after == live, "RESTORED" if good else "NOT VERIFIED"))
        emit("  displaced version %s stays in the versioned bucket" % displaced)
    emit("RESTORED %d of %d" % (ok_n, len(FUNCS)))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 0 if ok_n == len(FUNCS) else 1


if __name__ == "__main__":
    sys.exit(main())
