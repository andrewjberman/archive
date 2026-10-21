"""IRPT_ANLREQ TO-DELETE-7H-DLQ-MESSAGE (applier 0.7.0_AE_CloudOps~IB2): delete run 7H's ONE synthetic message from irpt-generation-dlq by receipt handle.

  python dlq_delete_7h.py --go

R0 counts of both queues; wait (attribute reads only, nothing received from the source queue) until the DLQ shows a visible message or the source reads 0 visible and
0 in flight, up to 04:00Z; then receive from the DLQ (up to 10, wait 2 s), decide is7h by the request id inside the body (yes or no, the body is never printed or
kept), return every other message to visibility at once, delete the 7H message by its receipt handle only; print the counts after. No purge, no redrive, no
attribute change.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
SRC, DLQ = "irpt-generation", "irpt-generation-dlq"
REQ = "REQ-e90c581652f6c90d3e33af23"
DEADLINE = datetime(2026, 10, 21, 4, 0, 0, tzinfo=timezone.utc)
OUT = []
MAX_RECEIVES = 6  # the DLQ already held other messages at R0, so two receives of a batch cannot be shown to cover it; every non-7H message goes back at once


def say(line):
    OUT.append(line)
    print(line, flush=True)


def counts(sqs, url):
    a = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible", "ApproximateNumberOfMessagesDelayed"])["Attributes"]
    return int(a["ApproximateNumberOfMessages"]), int(a["ApproximateNumberOfMessagesNotVisible"]), int(a["ApproximateNumberOfMessagesDelayed"])


def now():
    return datetime.now(timezone.utc)


def finish(final):
    say(final)
    (HERE / "A_DLQ_DELETE.txt").write_text("\n".join(OUT) + "\n", encoding="ascii", errors="replace", newline="\n")


def main():
    sqs = boto3.client("sqs", region_name=REGION)
    src = sqs.get_queue_url(QueueName=SRC)["QueueUrl"]
    dlq = sqs.get_queue_url(QueueName=DLQ)["QueueUrl"]
    s0, d0 = counts(sqs, src), counts(sqs, dlq)
    say("R0 date=%s queues=%s,%s source visible=%d inflight=%d delayed=%d | dlq visible=%d inflight=%d delayed=%d" % (now().strftime("%Y-%m-%dT%H:%M:%SZ"), SRC, DLQ, *s0, *d0))
    dlq_before = d0[0] + d0[1] + d0[2]
    while True:
        s, d = counts(sqs, src), counts(sqs, dlq)
        if s == (0, 0, 0) and d[0] + d[1] + d[2] > dlq_before:
            say("W waited_until=%s dlq_visible=%d (the source queue is empty and the DLQ total grew from %d to %d)" % (now().strftime("%Y-%m-%dT%H:%M:%SZ"), d[0], dlq_before, d[0] + d[1] + d[2]))
            break
        if s == (0, 0, 0):
            say("W waited_until=%s dlq_visible=%d source_empty=yes dlq_total_unchanged=%d" % (now().strftime("%Y-%m-%dT%H:%M:%SZ"), d[0], dlq_before))
            return finish("DLQ-DELETE-STOP the source queue is empty but the DLQ total did not grow; nothing deleted")
        if now() >= DEADLINE:
            say("W waited_until=%s dlq_visible=%d source_visible=%d source_inflight=%d" % (now().strftime("%Y-%m-%dT%H:%M:%SZ"), d[0], s[0], s[1]))
            return finish("DLQ-DELETE-STOP the message had not reached the DLQ by 04:00Z; the source queue still holds it; nothing deleted")
        time.sleep(120)
    received = is7h = returned = deleted = 0
    for _ in range(MAX_RECEIVES):
        r = sqs.receive_message(QueueUrl=dlq, MaxNumberOfMessages=10, WaitTimeSeconds=2, VisibilityTimeout=60)
        msgs = r.get("Messages", [])
        for m in msgs:
            received += 1
            mine = REQ in (m.get("Body") or "")
            if mine and deleted == 0:
                is7h += 1
                sqs.delete_message(QueueUrl=dlq, ReceiptHandle=m["ReceiptHandle"])
                deleted += 1
            else:
                if mine:
                    is7h += 1
                sqs.change_message_visibility(QueueUrl=dlq, ReceiptHandle=m["ReceiptHandle"], VisibilityTimeout=0)
                returned += 1
        if deleted:
            break
    say("M received=%d is7h=%d returned=%d" % (received, is7h, returned))
    if not deleted:
        return finish("DLQ-DELETE-STOP no 7H message in the DLQ after the receives; nothing deleted")
    say("D deleted=1 by_receipt_handle")
    time.sleep(75)
    s, d = counts(sqs, src), counts(sqs, dlq)
    say("C dlq_before=%d dlq_after=%d source_visible=%d source_inflight=%d" % (dlq_before, d[0] + d[1] + d[2], s[0], s[1]))
    return finish("DLQ-DELETE-DONE")


if __name__ == "__main__":
    if "--go" in sys.argv:
        main()
    else:
        print("USAGE dlq_delete_7h.py --go")
