"""IRPT_ANLREQ TO-RUN-FWD1 window 4: R0 (b), (d), (f), (g), (g2), (h) -- READ ONLY. Prints words, hashes and counts; never a secret value.

  python r0_aws.py
"""
import datetime as dt
import sys

import boto3

R = "us-east-1"
lam, ddb, sqs, sm = (boto3.client(x, region_name=R) for x in ("lambda", "dynamodb", "sqs", "secretsmanager"))
rc = 0


def line(tag, ok, text):
    global rc
    print("%s %s %s" % (tag, "OK" if ok else "RED", text))
    if not ok:
        rc = 3


# (b) the four addresses ABSENT by a ConsistentRead and by the email GSI
for addr in ("fwd1-staff-r41b@opal.invalid", "irpt-r3p-iv-20261016@opal.invalid", "irpt-r3q-iv-20261016@opal.invalid", "irpt-r3r-iv-20261016@opal.invalid"):
    item = ddb.get_item(TableName="opal-users-v2", Key={"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
    cnt = ddb.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]
    line("R0b", item is None and cnt == 0, "%s consistent=%s gsi_count=%d" % (addr, "ABSENT" if item is None else "PRESENT", cnt))

# (d) the two function hashes
for fn, want in (("irpt-ycharts-generate", "kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE="), ("irpt-status", "+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=")):
    got = lam.get_function(FunctionName=fn)["Configuration"]["CodeSha256"]
    line("R0d", got == want, "%s CodeSha256 %s" % (fn, got))

# (f) the commentary function and the two pull functions
got = lam.get_function(FunctionName="outlook-global-commentary-draft-lambda")["Configuration"]
line("R0f", got["CodeSha256"] == "I/6mirBTU5+JPCUUx6Xrmd1bn1vGAjvZTL75LhOm3HY=", "outlook-global-commentary-draft-lambda CodeSha256 %s LastModified %s" % (got["CodeSha256"], got["LastModified"]))
for fn in ("teams-global-transcripts-pull-lambda", "outlook-global-transcripts-pull-lambda"):
    got = lam.get_function(FunctionName=fn)["Configuration"]["CodeSha256"]
    line("R0f", got == "hUZY39qNcHdJf0fgQRHS4ckuFBT+8rU/K7VhGscaeYc=", "%s CodeSha256 %s" % (fn, got))

# queue depths (every queue whose name starts with irpt or carries analysis/commentary)
urls = []
for pg in sqs.get_paginator("list_queues").paginate():
    urls += pg.get("QueueUrls", [])
shown = 0
for u in sorted(urls):
    name = u.rsplit("/", 1)[-1]
    if any(t in name.lower() for t in ("irpt", "analysis", "commentary", "resident")):
        a = sqs.get_queue_attributes(QueueUrl=u, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible", "ApproximateNumberOfMessagesDelayed"])["Attributes"]
        print("R0f queue %s visible=%s in_flight=%s delayed=%s" % (name, a["ApproximateNumberOfMessages"], a["ApproximateNumberOfMessagesNotVisible"], a["ApproximateNumberOfMessagesDelayed"]))
        shown += 1
print("R0f queues listed=%d (denominator: all queues in the account=%d)" % (shown, len(urls)))

# (g2) the ticket service and (g) its mail map
t = lam.get_function(FunctionName="opal-ticket-api")["Configuration"]
line("R0g2", t["CodeSha256"].startswith("JwdnACONAnxw") and t["LastModified"].startswith("2026-10-16T17:57:13"), "opal-ticket-api CodeSha256 %s LastModified %s" % (t["CodeSha256"], t["LastModified"]))
env = (t.get("Environment") or {}).get("Variables") or {}
dl = env.get("TICKET_DL_MAP", "<absent>")
line("R0g", dl.strip() in ("{}", ""), "TICKET_DL_MAP=%s (variables present: %d)" % (dl if len(dl) < 80 else dl[:80] + "...", len(env)))

# (h) the packager secret: describe only
d = sm.describe_secret(SecretId="opal/ticketing/svc-irpt-packager")
print("R0h packager secret LastAccessedDate before=%s" % (d.get("LastAccessedDate").isoformat() if d.get("LastAccessedDate") else "NEVER"))
now = dt.datetime.now(dt.timezone.utc)
last = dt.datetime(2026, 10, 16, 18, 26, 53, tzinfo=dt.timezone.utc)
line("R0h2", (now - last).total_seconds() >= 390, "clock %s, %d s since the paced read's last lookup 18:26:53Z" % (now.strftime("%Y-%m-%dT%H:%M:%SZ"), (now - last).total_seconds()))
sys.exit(rc)
