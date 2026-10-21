"""TCKT_VNEXT TO-R22-DL1 (cell R22-dl-1): the ONE delete pass for the fabric's synthetic S3 residue (0.7.0_AE_CloudOps~TV2).

For each chunk of 12 manifest entries: assume that chunk's throwaway role for exactly 900 s (credentials held in memory, never printed or written),
delete each exact (bucket, key, VersionId) in that session only, then read each version ABSENT (a 404 only) and each key's versions and markers empty
with this seat's OWN read rights. A non-204 delete, an assume that never succeeds, or any other error stops the pass at once; nothing is retried
blindly. Writes only deleted.json (the per-entry record). The Terraform destroy and the result file are separate steps.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time

import boto3
from botocore.exceptions import ClientError

MANIFEST = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json"
OUT = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/deleted.json"
ACCOUNT = "313476888478"
CHUNK = 12
DURATION = 900
REGION = "us-east-1"


def iso():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(msg):
    print("%s %s" % (iso(), msg), flush=True)


def absent(s3, bucket, key, version_id):
    """True only when the version reads 404 and the key lists no version or delete marker."""
    try:
        s3.head_object(Bucket=bucket, Key=key, VersionId=version_id)
        return False
    except ClientError as e:
        status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status != 404:
            raise
    for page in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key):
        for ver in page.get("Versions", []):
            if ver["Key"] == key:
                return False
        for mark in page.get("DeleteMarkers", []):
            if mark["Key"] == key:
                return False
    return True


def assume(sts, idx):
    role_arn = "arn:aws:iam::%s:role/opal-ticket-residue-delete-%d-role" % (ACCOUNT, idx)
    last = None
    for attempt in range(1, 9):
        try:
            r = sts.assume_role(RoleArn=role_arn, RoleSessionName="tv2-r22-dl1-%d" % idx, DurationSeconds=DURATION)
            return r["Credentials"]
        except ClientError as e:
            last = e.response["Error"]["Code"]
            say("assume role %d attempt %d: %s" % (idx, attempt, last))
            time.sleep(6)
    raise RuntimeError("assume role %d never succeeded (%s)" % (idx, last))


def main():
    objs = json.load(open(MANIFEST, encoding="utf-8"))["objects"]
    own = boto3.client("s3", region_name=REGION)
    sts = boto3.client("sts", region_name=REGION)
    record = []
    stopped = None
    n_chunks = -(-len(objs) // CHUNK)
    for idx in range(n_chunks):
        chunk = objs[idx * CHUNK:(idx + 1) * CHUNK]
        try:
            cred = assume(sts, idx)
        except RuntimeError as e:
            stopped = str(e)
            break
        s3a = boto3.client("s3", region_name=REGION, aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"],
                           aws_session_token=cred["SessionToken"])
        say("role %d assumed for %ds; %d entries" % (idx, DURATION, len(chunk)))
        for o in chunk:
            try:
                r = s3a.delete_object(Bucket=o["bucket"], Key=o["key"], VersionId=o["version_id"])
                status = r["ResponseMetadata"]["HTTPStatusCode"]
            except ClientError as e:
                stopped = "delete refused for ...%s: %s" % (o["key"][-48:], e.response["Error"]["Code"])
                break
            at = iso()
            gone = absent(own, o["bucket"], o["key"], o["version_id"])
            record.append({"bucket": o["bucket"], "key": o["key"], "version_id": o["version_id"], "deleted_at": at, "http_status": status,
                           "absent_after": gone})
            say("DELETE %s ...%s -> %s, read ABSENT=%s" % (o["bucket"], o["key"][-40:], status, gone))
            if status != 204 or not gone:
                stopped = "entry ...%s status %s absent %s" % (o["key"][-40:], status, gone)
                break
        del cred
        del s3a
        if stopped:
            break
    json.dump({"stopped": stopped, "deleted": record}, open(OUT, "w", encoding="utf-8"), indent=1)
    say("deleted %d of %d; stopped=%s" % (len(record), len(objs), stopped))
    return 1 if stopped else 0


if __name__ == "__main__":
    sys.exit(main())
