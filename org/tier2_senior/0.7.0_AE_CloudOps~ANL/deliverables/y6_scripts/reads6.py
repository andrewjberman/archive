"""Y6 reads: job-row states of the snapshot's READY ids, and the ticket_id count. READ-ONLY (get_item, scan).
usage: reads6.py jobs <snapshot.json> <out_jobs.json> | reads6.py count <out_count.json>
Prints ids, state strings, counts and error codes only; no record body, no ticket id value. ASCII only."""
import json
import re
import sys

import boto3
from botocore.exceptions import ClientError

ddb = boto3.client("dynamodb", region_name="us-east-1")
SK = re.compile(r"^analysis#(REQ-[0-9a-f]{24})#1$")


def jobs(snapshot, out):
    r4 = json.load(open(snapshot, encoding="utf-8"))["R4R5"]
    ids = sorted((k, v["tenant"]) for k, v in r4.items() if v.get("state") == "READY")
    states, denied = {}, []
    for rid, tenant in ids:
        try:
            it = ddb.get_item(TableName="irpt-jobs", Key={"tenant": {"S": tenant}, "job": {"S": rid}},
                              ConsistentRead=True, ProjectionExpression="#s", ExpressionAttributeNames={"#s": "state"}).get("Item")
            states[rid] = it["state"]["S"] if it and "state" in it else "NO_ROW"
        except ClientError as e:
            states[rid] = e.response["Error"]["Code"]
            denied.append(rid)
    json.dump({"ids": [i for i, _ in ids], "states": states, "errors": denied}, open(out, "w", encoding="ascii"), indent=1, sort_keys=True)
    for rid, _ in ids:
        print(rid, states[rid])
    ready = [i for i, _ in ids if states[i] == "READY"]
    print("READ_N_OF", len(ids) - len(denied), "of", len(ids), "| READY", len(ready), "| first_ready", ready[0] if ready else None)


def count(out):
    items = acc = w = wo = bad = 0
    by = {}
    try:
        for pg in ddb.get_paginator("scan").paginate(TableName="irpt-requests", ConsistentRead=True):
            for it in pg.get("Items", []):
                items += 1
                m = SK.match(it.get("request_revision", {}).get("S", ""))
                if not m:
                    continue
                t = it.get("tenant", {}).get("S", "?")
                acc += 1
                try:
                    rec = json.loads(it["record"]["S"])
                except Exception:
                    bad += 1
                    continue
                b = by.setdefault(t, {"with": 0, "without": 0})
                if "ticket_id" in rec:
                    w += 1
                    b["with"] += 1
                else:
                    wo += 1
                    b["without"] += 1
    except ClientError as e:
        print("SCAN_DENIED", e.response["Error"]["Code"])
        raise
    res = {"accepted_scanned": acc, "items_scanned": items, "with_ticket_id": w, "without_ticket_id": wo,
           "unreadable": bad, "by_tenant": by}
    json.dump(res, open(out, "w", encoding="ascii"), indent=1, sort_keys=True)
    print(json.dumps(res, sort_keys=True))


if sys.argv[1] == "jobs":
    jobs(sys.argv[2], sys.argv[3])
else:
    count(sys.argv[2])
