"""IRPT_ANLREQ TO-READ-DLQ-INVENTORY (applier 0.7.0_AE_CloudOps~IB2): every message of irpt-generation-dlq, ids and counts only. READ ONLY.

  python dlq_inventory.py     prints the rows and writes A_DLQ_INVENTORY.txt beside this file

At most 8 receives, each with visibility timeout 0, max 10 messages, wait 20 s; stops at the first receive with nothing new or when the distinct set
reaches the depth read first. MessageId is held in memory and printed as its first 8 characters. From a body only the closed kind word, the
request id and the tenant are parsed. Nothing is deleted, purged, redriven or sent.
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
DLQ = "irpt-generation-dlq"
MAX_RECEIVES = 8


def main():
    sqs = boto3.client("sqs", region_name=REGION)
    ddb = boto3.client("dynamodb", region_name=REGION)
    url = sqs.get_queue_url(QueueName=DLQ)["QueueUrl"]
    a = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
    depth = int(a["ApproximateNumberOfMessages"])
    notvis = int(a["ApproximateNumberOfMessagesNotVisible"])
    seen, receives = {}, 0
    while receives < MAX_RECEIVES and len(seen) < depth:
        receives += 1
        resp = sqs.receive_message(QueueUrl=url, VisibilityTimeout=0, MaxNumberOfMessages=10, WaitTimeSeconds=20, AttributeNames=["SentTimestamp", "ApproximateReceiveCount"])
        new = 0
        for m in resp.get("Messages", []):
            if m["MessageId"] in seen:
                # keep the highest receive count seen for the message
                seen[m["MessageId"]]["count"] = max(seen[m["MessageId"]]["count"], int(m["Attributes"]["ApproximateReceiveCount"]))
                continue
            new += 1
            try:
                b = json.loads(m["Body"])
            except ValueError:
                b = {}
            p = b.get("payload") if isinstance(b.get("payload"), dict) else {}
            kind = b.get("kind") or p.get("kind") or ""
            rid = b.get("request_id") or p.get("request_id") or ""
            tenant = b.get("tenant") or p.get("tenant") or ""
            seen[m["MessageId"]] = {"kind": kind if re.fullmatch(r"[A-Za-z_]{1,40}", kind or "") else "kind?", "rid": rid if re.fullmatch(r"REQ-[0-9a-f]{24}", rid or "") else "none",
                                    "tenant": tenant if re.fullmatch(r"[a-z0-9_-]{1,40}", tenant or "") else "none",
                                    "sent": int(m["Attributes"]["SentTimestamp"]) / 1000.0, "count": int(m["Attributes"]["ApproximateReceiveCount"])}
        print("receive %d returned %d messages, %d new, distinct %d of depth %d" % (receives, len(resp.get("Messages", [])), new, len(seen), depth), flush=True)
        if new == 0:
            break
    now = time.time()
    rows = []
    for mid, v in sorted(seen.items(), key=lambda kv: kv[1]["sent"]):
        rows.append("M %s kind=%s request=%s tenant=%s sent=%s age_days=%.1f receive_count=%d" % (
            mid[:8], v["kind"], v["rid"], v["tenant"], datetime.fromtimestamp(v["sent"], timezone.utc).strftime("%Y-%m-%d %H:%M"), (now - v["sent"]) / 86400.0, v["count"]))
    reqs = {}
    for v in seen.values():
        reqs.setdefault((v["rid"], v["tenant"]), 0)
        reqs[(v["rid"], v["tenant"])] += 1
    for (rid, tenant), n in sorted(reqs.items()):
        acc, tick = "NOT-READ", "NOT-READ"
        if rid != "none" and tenant != "none":
            it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": tenant}, "request_revision": {"S": "analysis#%s#1" % rid}}, ConsistentRead=True).get("Item")
            if it:
                tick = "yes" if (it.get("ticket_id") or {}).get("S") else "no"
                for name in ("accepted_at", "acceptedAt", "created_at", "createdAt", "accepted"):
                    s = (it.get(name) or {}).get("S") or (it.get(name) or {}).get("N")
                    if s:
                        try:
                            t = datetime.fromtimestamp(float(s) / (1000.0 if float(s) > 1e11 else 1.0), timezone.utc) if re.fullmatch(r"\d+(\.\d+)?", s) else datetime.fromisoformat(s.replace("Z", "+00:00"))
                            acc = t.strftime("%Y-%m-%d %H:%M")
                        except ValueError:
                            acc = "unparsed"
                        break
            else:
                tick = "item-absent"
        rows.append("Q %s tenant=%s messages=%d accepted=%s ticket=%s" % (rid, tenant, n, acc, tick))
    rows.append("COUNTS depth=%d distinct_messages=%d distinct_requests=%d receives=%d" % (depth, len(seen), len(reqs), receives))
    complete = len(seen) == depth
    rows.append("INVENTORY-DONE complete=%s" % ("yes" if complete else "no"))
    if not complete:
        rows.append("NOTE shortfall %d message(s) not returned (not visible to this reader: %d reported not visible at the start)" % (depth - len(seen), notvis))
    text = "\n".join(rows) + "\n"
    (HERE / "A_DLQ_INVENTORY.txt").write_text(text, encoding="ascii", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
