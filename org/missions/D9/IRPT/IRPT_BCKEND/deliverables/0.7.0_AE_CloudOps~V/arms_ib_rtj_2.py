#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtj-2 arms (d)/(e) -- run ONLY after both never-widen halves are at HEAD and the role is applied.

Assumes irpt-fence-probe-l4-role as user/Andrew_Berman (the trust policy's one principal), then, under that ONE
session:
  POSITIVE ARM      list-objects-v2 on the control opal-313476888478-lambda-artifacts  -> must SUCCEED
  NEGATIVE ARMS     list-objects-v2 on each fenced firm bucket (the registry selector's 2) -> must be AccessDenied,
                    ATTRIBUTED by S3's own error context to "an explicit deny in a resource-based policy"
  ATTRIBUTION CTRL  list-objects-v2 on opal-data-assets (not granted, no ListBucket Deny) -> AccessDenied attributed
                    to "no identity-based policy allows" -- proves the wording discriminates the two causes
Prints key COUNTS only (no key names), the session ARN, and each denial's Code + Message verbatim.
Writes IB-rtj-2_arms_output.txt beside itself. Exit 0 only if every arm lands as expected.
"""
from __future__ import annotations

import datetime
import json
import os
import sys

import boto3
from botocore.exceptions import ClientError

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUT = os.path.join(HERE, "IB-rtj-2_arms_output.txt")
ROLE_ARN = "arn:aws:iam::313476888478:role/irpt-fence-probe-l4-role"
CONTROL = "opal-313476888478-lambda-artifacts"
ATTR_CONTROL = "opal-data-assets"
RESOURCE_DENY = "explicit deny in a resource-based policy"
IDENTITY_NONE = "no identity-based policy allows"
LINES: list[str] = []


def emit(s: str = "") -> None:
    LINES.append(s)
    print(s, flush=True)


def fenced_buckets() -> list[str]:
    reg = json.load(open(os.path.join(WS, "infra", "logic", "registry", "scopes.json"), encoding="utf-8"))
    return [s["bucket"] for s in reg["scopes"]
            if s.get("class") == "FIRM" and s.get("bucket_managed_by", "") == "s3-lgic-firm-buckets.tf"]


def list_as(s3, bucket: str) -> tuple[str, str]:
    try:
        r = s3.list_objects_v2(Bucket=bucket, MaxKeys=5)
        return "OK", "KeyCount %d IsTruncated %s (key names not printed)" % (r.get("KeyCount", 0), r.get("IsTruncated"))
    except ClientError as e:
        err = e.response.get("Error", {})
        return err.get("Code", "?"), err.get("Message", "")


def main() -> int:
    emit("IB-rtj-2 arms -- run at %s" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    base = boto3.client("sts", region_name="us-east-1")
    emit("operator identity: %s" % base.get_caller_identity()["Arn"])
    cred = base.assume_role(RoleArn=ROLE_ARN, RoleSessionName="ib-rtj-2-l4-probe", DurationSeconds=900)["Credentials"]
    sess = boto3.Session(aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"],
                         aws_session_token=cred["SessionToken"], region_name="us-east-1")
    emit("assumed session: %s (expires %s)" % (sess.client("sts").get_caller_identity()["Arn"], cred["Expiration"]))
    s3 = sess.client("s3")
    ok = True

    code, msg = list_as(s3, CONTROL)
    pos = code == "OK"
    ok &= pos
    emit("")
    emit("POSITIVE ARM  %s -> %s: %s  => %s" % (CONTROL, code, msg, "PASS" if pos else "FAIL (instrument/assumption/grant broken; negatives NOT meaningful)"))

    fb = fenced_buckets()
    emit("")
    emit("NEGATIVE ARMS over the registry selector's fenced buckets: %d: %s" % (len(fb), fb))
    n = 0
    for b in fb:
        code, msg = list_as(s3, b)
        att = code == "AccessDenied" and RESOURCE_DENY in msg
        n += att
        emit("  %s -> %s" % (b, code))
        emit("     S3 error context: %s" % msg)
        emit("     => %s" % ("DENIED, ATTRIBUTED to the resource-policy explicit Deny" if att else
                              ("FENCE LEAK -- the role LISTED this bucket" if code == "OK" else "DENIED but NOT attributed to the resource policy")))
    emit("  attributed denials: %d of %d" % (n, len(fb)))
    ok &= len(fb) == 2 and n == len(fb)

    code, msg = list_as(s3, ATTR_CONTROL)
    ac = code == "AccessDenied" and IDENTITY_NONE in msg and RESOURCE_DENY not in msg
    ok &= ac
    emit("")
    emit("ATTRIBUTION CONTROL  %s -> %s" % (ATTR_CONTROL, code))
    emit("     S3 error context: %s" % msg)
    emit("     => %s" % ("DENIED for the OTHER cause (no identity grant) -- the wording discriminates" if ac else "UNEXPECTED"))

    emit("")
    emit("ARMS RESULT: %s" % ("ALL HOLD" if ok else "NOT ALL HOLD"))
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
