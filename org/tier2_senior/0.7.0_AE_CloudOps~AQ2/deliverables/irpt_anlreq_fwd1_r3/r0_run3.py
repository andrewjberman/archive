"""IRPT_ANLREQ TO-RUN-FWD1 window 3 (0.7.0_AE_CloudOps~AQ2): R0, the READ-ONLY start-state reads that need AWS.

  python r0_run3.py <label>

Prints, writes nothing to AWS and no secret value: (b) both addresses ABSENT (ConsistentRead and the email-index count), (d) the CodeSha256 of
irpt-ycharts-generate and irpt-status and the status key's latest S3 version hashed against the r35L zip sha256, (f) the commentary function and
both pull functions' digests, the five queues' depths (visible, in flight), (g) TICKET_DL_MAP of opal-ticket-api (a routing map, not a secret),
(h) the packager secret's LastAccessedDate by describe-secret only. Account ids are masked in what is printed.
"""
from __future__ import annotations

import hashlib
import re
import sys

REGION = "us-east-1"
USERS = "opal-users-v2"
ADDRS = ("fwd1-staff-r41b@opal.invalid", "irpt-r3p-iv-%s@opal.invalid", "irpt-r3q-iv-%s@opal.invalid")
STATUS_ZIP_SHA = "f937190d69b013bbafdec530a2cdbe8e7d656cac908a42bed779cd0730faab80"
WANT = {"irpt-ycharts-generate": "kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=", "irpt-status": "+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A="}
BUCKET = "opal-313476888478-lambda-artifacts"
QUEUES = {
    "analysis_ready": "outlook-global-commentary-draft-analysis-ready-queue",
    "commentary_ready": "outlook-global-commentary-draft-commentary-ready-queue",
}


def mask(text):
    return re.sub(r"\d{12}", "<acct>", str(text))


def main(argv):
    import boto3
    date = argv[0] if argv else "20261016"
    ddb = boto3.client("dynamodb", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    sqs = boto3.client("sqs", region_name=REGION)
    sm = boto3.client("secretsmanager", region_name=REGION)
    bad = []
    for a in ADDRS:
        addr = a % date if "%s" in a else a
        item = ddb.get_item(TableName=USERS, Key={"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
        n = ddb.query(TableName=USERS, IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]
        ok = item is None and n == 0
        bad += [] if ok else ["R0b " + addr]
        print("R0b %s ConsistentRead %s, email-index count %d -> %s" % (addr, "ABSENT" if item is None else "PRESENT", n, "ABSENT" if ok else "RED"))
    for fn, want in WANT.items():
        got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        print("R0d %s CodeSha256 %s want %s %s" % (fn, got, want, "EQUAL" if got == want else "DIFFERENT"))
        if got != want:
            bad.append("R0d " + fn)
    key = "investor-reporting/irpt-status.zip"
    vers = s3.list_object_versions(Bucket=BUCKET, Prefix=key)
    latest = [v for v in vers.get("Versions", []) if v["Key"] == key and v["IsLatest"]][0]
    raw = s3.get_object(Bucket=BUCKET, Key=key, VersionId=latest["VersionId"])["Body"].read()
    ok = hashlib.sha256(raw).hexdigest() == STATUS_ZIP_SHA
    print("R0d irpt-status key latest VersionId %s sha256 %s want %s %s (versions listed %d, truncated %s)" % (latest["VersionId"], hashlib.sha256(raw).hexdigest(), STATUS_ZIP_SHA, "EQUAL" if ok else "DIFFERENT", len(vers.get("Versions", [])), vers.get("IsTruncated")))
    if not ok:
        bad.append("R0d status key")
    for fn in ("outlook-global-commentary-draft-lambda", "teams-global-transcripts-pull-lambda", "outlook-global-transcripts-pull-lambda"):
        c = lam.get_function_configuration(FunctionName=fn)
        print("R0f %s CodeSha256 %s LastModified %s" % (fn, c["CodeSha256"], c["LastModified"]))
    esm = lam.list_event_source_mappings(FunctionName="outlook-global-commentary-draft-lambda")["EventSourceMappings"]
    names = dict(QUEUES)
    for m in esm:
        names["draft_queue(" + m["State"] + ")"] = m["EventSourceArn"].rsplit(":", 1)[-1]
    seen = {}
    for label, qn in list(names.items()):
        url = sqs.get_queue_url(QueueName=qn)["QueueUrl"]
        at = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible", "RedrivePolicy"])["Attributes"]
        seen[label] = (qn, at)
        print("R0e queue %s: visible %s in flight %s" % (label, at["ApproximateNumberOfMessages"], at["ApproximateNumberOfMessagesNotVisible"]))
        rp = at.get("RedrivePolicy")
        if rp:
            dlq = re.search(r'"deadLetterTargetArn":"[^"]*:([^":]+)"', rp)
            if dlq:
                du = sqs.get_queue_url(QueueName=dlq.group(1))["QueueUrl"]
                da = sqs.get_queue_attributes(QueueUrl=du, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
                print("R0e queue %s DLQ %s: visible %s in flight %s" % (label, dlq.group(1), da["ApproximateNumberOfMessages"], da["ApproximateNumberOfMessagesNotVisible"]))
    tm = lam.get_function_configuration(FunctionName="opal-ticket-api").get("Environment", {}).get("Variables", {}).get("TICKET_DL_MAP")
    print("R0g TICKET_DL_MAP of opal-ticket-api: %s" % mask(tm))
    d = sm.describe_secret(SecretId="opal/ticketing/svc-irpt-packager")
    print("R0h packager secret LastAccessedDate before: %s" % d.get("LastAccessedDate", "NEVER"))
    print("R0 AWS READS %s" % ("GREEN" if not bad else "RED " + str(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
