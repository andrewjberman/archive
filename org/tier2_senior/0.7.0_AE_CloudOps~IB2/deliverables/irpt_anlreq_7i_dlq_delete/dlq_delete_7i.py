"""IRPT_ANLREQ TO-DELETE-7I-DLQ-MESSAGE (applier 0.7.0_AE_CloudOps~IB2): delete run 7I's ONE synthetic message from irpt-generation-dlq by receipt handle.

  python dlq_delete_7i.py --go

R0 counts of both queues. Wait (attribute reads only; nothing is received from the source queue) until the SOURCE reads 0 visible, 0 in flight and 0 delayed and the DLQ
total has grown by one against R0, up to 06:00Z. Then enumerate the DLQ: every received message is held invisible (120 s) while all distinct messages are seen, its body
is tested for the 7I request id (yes or no; the body is never printed or kept), the 7I message is deleted by its receipt handle ONLY, and the others are returned to
visibility 0 together. No purge, no redrive, no attribute change.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
SRC, DLQ = "irpt-generation", "irpt-generation-dlq"
REQ = "REQ-0240fbdbf8c59e703e9fa3f0"
DEADLINE = datetime(2026, 10, 21, 6, 0, 0, tzinfo=timezone.utc)
OUT = []


def say(x):
    OUT.append(x)
    print(x, flush=True)


def counts(sqs, url):
    a = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible", "ApproximateNumberOfMessagesDelayed"])["Attributes"]
    return int(a["ApproximateNumberOfMessages"]), int(a["ApproximateNumberOfMessagesNotVisible"]), int(a["ApproximateNumberOfMessagesDelayed"])


def stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def finish(final):
    say(final)
    (HERE / "A_DLQ_DELETE.txt").write_text("\n".join(OUT) + "\n", encoding="ascii", errors="replace", newline="\n")


def main():
    sqs = boto3.client("sqs", region_name="us-east-1")
    src = sqs.get_queue_url(QueueName=SRC)["QueueUrl"]
    dlq = sqs.get_queue_url(QueueName=DLQ)["QueueUrl"]
    s0, d0 = counts(sqs, src), counts(sqs, dlq)
    before = sum(d0)
    say("R0 date=%s queues=%s,%s source visible=%d inflight=%d delayed=%d | dlq visible=%d inflight=%d delayed=%d" % (stamp(), SRC, DLQ, *s0, *d0))
    while True:
        s, d = counts(sqs, src), counts(sqs, dlq)
        if s == (0, 0, 0) and sum(d) >= before + 1:
            say("W waited_until=%s dlq_visible=%d (the source is empty and the DLQ total grew from %d to %d)" % (stamp(), d[0], before, sum(d)))
            break
        if datetime.now(timezone.utc) >= DEADLINE:
            say("W waited_until=%s dlq_visible=%d source_visible=%d source_inflight=%d" % (stamp(), d[0], s[0], s[1]))
            return finish("DLQ-DELETE-STOP the message had not reached the DLQ by 06:00Z (source or DLQ total did not move as expected); nothing deleted")
        time.sleep(120)
    held, seen, mine, deleted, empty = [], set(), 0, 0, 0
    for _ in range(40):
        r = sqs.receive_message(QueueUrl=dlq, MaxNumberOfMessages=10, WaitTimeSeconds=2, VisibilityTimeout=120)
        msgs = r.get("Messages", [])
        if not msgs:
            empty += 1
            if empty >= 3:
                break
            continue
        empty = 0
        for m in msgs:
            if m["MessageId"] in seen:
                continue
            seen.add(m["MessageId"])
            if REQ in (m.get("Body") or "") and not deleted:
                mine += 1
                sqs.delete_message(QueueUrl=dlq, ReceiptHandle=m["ReceiptHandle"])
                deleted += 1
            else:
                held.append(m["ReceiptHandle"])
    for h in held:
        sqs.change_message_visibility(QueueUrl=dlq, ReceiptHandle=h, VisibilityTimeout=0)
    say("M received=%d is7i=%d returned=%d (held invisible while the DLQ was enumerated, then returned together)" % (len(seen), mine, len(held)))
    if not deleted:
        return finish("DLQ-DELETE-STOP every distinct DLQ message was seen and none carries the 7I request id; nothing deleted")
    say("D deleted=1 by_receipt_handle")
    time.sleep(75)
    s, d = counts(sqs, src), counts(sqs, dlq)
    say("C dlq_before=%d dlq_after=%d source_visible=%d source_inflight=%d" % (before, sum(d), s[0], s[1]))
    return finish("DLQ-DELETE-DONE")


if __name__ == "__main__":
    if "--go" in sys.argv:
        main()
    else:
        print("USAGE dlq_delete_7i.py --go")
