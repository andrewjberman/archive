"""IRPT_ANLREQ TO-RUN-FWD1 window 3 (0.7.0_AE_CloudOps~AQ2): after-reads F2, F5 and the packager secret (READ ONLY, statuses and counts only).

  python after_run3.py <since-epoch-seconds>

F2: opal-tickets tickets created at or after the run's start by the run address (status-index query on open and in_progress, filtered on created_at and requester); F5: the count of WE_DL_SENT
lines in the ticket Lambda's log group since the run start; F6: describe-secret LastAccessedDate of the packager secret (never get-secret-value).
"""
from __future__ import annotations

import datetime as dt
import sys


def main(argv):
    import boto3
    since = dt.datetime.fromtimestamp(float(argv[0]), dt.timezone.utc)
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    n_new, n_run = 0, 0
    for st in ("open", "in_progress", "completed"):
        r = ddb.query(TableName="opal-tickets", IndexName="status-index", KeyConditionExpression="#s = :s AND created_at >= :c",
                      ExpressionAttributeNames={"#s": "status"}, ExpressionAttributeValues={":s": {"S": st}, ":c": {"S": since.strftime("%Y-%m-%dT%H:%M:%S")}})
        for it in r.get("Items", []):
            n_new += 1
            req = it.get("requester", {}).get("M", {})
            if "fwd1-staff-r41b" in str(req):
                n_run += 1
        print("F2 status %s: tickets created since %s: %d" % (st, since.strftime("%H:%M:%SZ"), len(r.get("Items", []))))
    print("F2 tickets created since the run start: %d; of them by the run address: %d" % (n_new, n_run))
    logs = boto3.client("logs", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")
    fn = "opal-ticket-api"
    grp = "/aws/lambda/" + lam.get_function_configuration(FunctionName=fn)["FunctionName"]
    tot = 0
    kw = dict(logGroupName=grp, startTime=int(since.timestamp() * 1000), filterPattern="WE_DL_SENT")
    while True:
        r = logs.filter_log_events(**kw)
        tot += len(r.get("events", []))
        if "nextToken" not in r:
            break
        kw["nextToken"] = r["nextToken"]
    print("F5 WE_DL_SENT lines in %s since the run start: %d" % (grp, tot))
    sm = boto3.client("secretsmanager", region_name="us-east-1")
    d = sm.describe_secret(SecretId="opal/ticketing/svc-irpt-packager")
    print("F6 packager secret LastAccessedDate after: %s" % d.get("LastAccessedDate", "NEVER"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
