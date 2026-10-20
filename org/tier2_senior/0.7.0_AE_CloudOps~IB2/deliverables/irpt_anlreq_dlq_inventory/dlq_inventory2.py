"""IRPT_ANLREQ TO-READ-DLQ-INVENTORY, AMENDMENT 1 (applier 0.7.0_AE_CloudOps~IB2): ONE MORE PASS of at most 8 zero-visibility receives, then the UNION of
every pass and of A_DLQ_WHY.txt. READ ONLY.

  python dlq_inventory2.py     prints the union rows and writes A_DLQ_INVENTORY.txt (the first pass's rows are kept in A_DLQ_INVENTORY_PASS1.txt)

A message is identified by the first 8 characters of its MessageId (the first pass printed only those). From a body only the closed kind word, the
request id and the tenant are parsed. For each request the request item's member NAMES are read first (names only); the acceptance time is the member
named like accept/created/submitted/received/filed whose value parses as a time. Nothing is deleted, purged, redriven or sent.
"""
from __future__ import annotations

import json
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
DLQ = "irpt-generation-dlq"
MAX_RECEIVES = 8
PASS1_RECEIVES = 4
# the two requests the earlier reads (A_RESOLVE_LIVE and A_DLQ_WHY) saw in the queue; their message ids were not recorded
EARLIER = (("REQ-8966d24ffefa1c28269ef26c", "cottonwood"), ("REQ-4b5155ac2ea9467ab771b414", "49financial"))


def parse_pass1():
    src = HERE / "A_DLQ_INVENTORY_PASS1.txt"
    if not src.exists():
        shutil.copyfile(HERE / "A_DLQ_INVENTORY.txt", src)
    seen = {}
    for ln in src.read_text(encoding="ascii").splitlines():
        m = re.match(r"M (\S{8}) kind=(\S+) request=(\S+) tenant=(\S+) sent=(\d{4}-\d\d-\d\d \d\d:\d\d) age_days=\S+ receive_count=(\d+)", ln)
        if m:
            sent = datetime.strptime(m.group(5), "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp()
            seen[m.group(1)] = {"kind": m.group(2), "rid": m.group(3), "tenant": m.group(4), "sent": sent, "count": int(m.group(6)), "pass": 1}
    return seen


def accepted_of(item):
    names = sorted(item.keys())
    for pat in ("accept", "created", "submitted", "received", "filed"):
        for n in names:
            if pat in n.lower():
                v = item[n]
                s = v.get("S") or v.get("N")
                if not s:
                    continue
                try:
                    if re.fullmatch(r"\d+(\.\d+)?", s):
                        x = float(s)
                        t = datetime.fromtimestamp(x / 1000.0 if x > 1e11 else x, timezone.utc)
                    else:
                        t = datetime.fromisoformat(s.replace("Z", "+00:00"))
                    return n, t.strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    continue
    return None, "NOT-READ"


def main():
    sqs = boto3.client("sqs", region_name=REGION)
    ddb = boto3.client("dynamodb", region_name=REGION)
    url = sqs.get_queue_url(QueueName=DLQ)["QueueUrl"]
    a = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
    depth, notvis = int(a["ApproximateNumberOfMessages"]), int(a["ApproximateNumberOfMessagesNotVisible"])
    seen = parse_pass1()
    p1 = len(seen)
    receives = 0
    while receives < MAX_RECEIVES and len(seen) < depth:
        receives += 1
        resp = sqs.receive_message(QueueUrl=url, VisibilityTimeout=0, MaxNumberOfMessages=10, WaitTimeSeconds=20, AttributeNames=["SentTimestamp", "ApproximateReceiveCount"])
        new = 0
        for m in resp.get("Messages", []):
            mid = m["MessageId"][:8]
            cnt = int(m["Attributes"]["ApproximateReceiveCount"])
            if mid in seen:
                seen[mid]["count"] = max(seen[mid]["count"], cnt)
                continue
            new += 1
            try:
                b = json.loads(m["Body"])
            except ValueError:
                b = {}
            p = b.get("payload") if isinstance(b.get("payload"), dict) else {}
            kind, rid, tenant = b.get("kind") or p.get("kind") or "", b.get("request_id") or p.get("request_id") or "", b.get("tenant") or p.get("tenant") or ""
            seen[mid] = {"kind": kind if re.fullmatch(r"[A-Za-z_]{1,40}", kind or "") else "kind?", "rid": rid if re.fullmatch(r"REQ-[0-9a-f]{24}", rid or "") else "none",
                         "tenant": tenant if re.fullmatch(r"[a-z0-9_-]{1,40}", tenant or "") else "none", "sent": int(m["Attributes"]["SentTimestamp"]) / 1000.0, "count": cnt, "pass": 2}
        print("pass2 receive %d returned %d messages, %d new, union distinct %d of depth %d" % (receives, len(resp.get("Messages", [])), new, len(seen), depth), flush=True)
        if new == 0:
            break
    now = time.time()
    rows = []
    for mid, v in sorted(seen.items(), key=lambda kv: kv[1]["sent"]):
        rows.append("M %s kind=%s request=%s tenant=%s sent=%s age_days=%.1f receive_count=%d seen_in_pass=%d" % (
            mid, v["kind"], v["rid"], v["tenant"], datetime.fromtimestamp(v["sent"], timezone.utc).strftime("%Y-%m-%d %H:%M"), (now - v["sent"]) / 86400.0, v["count"], v["pass"]))
    reqs = {}
    for v in seen.values():
        reqs[(v["rid"], v["tenant"])] = reqs.get((v["rid"], v["tenant"]), 0) + 1
    for rid, tenant in EARLIER:
        reqs.setdefault((rid, tenant), 0)  # messages=0 here means: seen in A_RESOLVE_LIVE / A_DLQ_WHY, no message id in this union
    names_printed = False
    for (rid, tenant), n in sorted(reqs.items()):
        acc, tick, members = "NOT-READ", "NOT-READ", None
        if rid != "none" and tenant != "none":
            it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": tenant}, "request_revision": {"S": "analysis#%s#1" % rid}}, ConsistentRead=True).get("Item")
            if it:
                members = ",".join(sorted(it.keys())) if not names_printed else None
                names_printed = True
                tick = "yes" if (it.get("ticket_id") or {}).get("S") else "no"
                _, acc = accepted_of(it)
            else:
                tick = "item-absent"
        src = [("pass1/pass2" if n else "A_RESOLVE_LIVE+A_DLQ_WHY only")]
        sent = sorted(v["sent"] for v in seen.values() if v["rid"] == rid)
        cnts = [str(v["count"]) for v in seen.values() if v["rid"] == rid]
        rows.append("Q %s tenant=%s messages=%d sent=%s receive_count=%s accepted=%s ticket=%s source=%s" % (
            rid, tenant, n, datetime.fromtimestamp(sent[0], timezone.utc).strftime("%Y-%m-%d %H:%M") if sent else "NOT-IN-UNION", ",".join(cnts) or "none", acc, tick, src[0]))
        if members:
            rows.append("NOTE-Q request item member names (names only): %s" % members)
    unseen = max(0, depth - len(seen))
    total_receives = PASS1_RECEIVES + receives
    rows.append("COUNTS depth=%d distinct_messages=%d distinct_requests=%d receives=%d unseen=%d" % (depth, len(seen), len([k for k in reqs if k[0] != "none"]), total_receives, unseen))
    complete = len(seen) == depth
    rows.append("INVENTORY-DONE complete=%s" % ("yes" if complete else "no"))
    rows.append("NOTE pass 1 saw %d messages (4 receives); pass 2 added %d (%d receives); depth now %d, not visible %d; the two requests of A_RESOLVE_LIVE and A_DLQ_WHY with no recorded message id are listed under Q with messages=0 and are not counted as messages" % (p1, len(seen) - p1, receives, depth, notvis))
    if not complete:
        rows.append("NOTE shortfall %d message(s) still UNSEEN after %d receives in all" % (unseen, total_receives))
    text = "\n".join(rows) + "\n"
    (HERE / "A_DLQ_INVENTORY.txt").write_text(text, encoding="ascii", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
