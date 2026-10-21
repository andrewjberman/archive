"""IRPT_ANLREQ TO-DELETE-7H-DLQ-MESSAGE, attempt 3 (0.7.0_AE_CloudOps~IB2): the DLQ holds 11 messages (10 older, the 7H one arrived).

Attempts 1 and 2 returned every non-7H message at once, so the repeated receives could keep drawing the same few. This pass holds each received message invisible
(120 s) while the whole DLQ is enumerated, tests each body for the 7H request id (yes or no, the body is never printed or kept), deletes the 7H message by its
receipt handle ONLY, then returns every other held message to visibility 0 together. No purge, no redrive, no attribute change.
"""
from __future__ import annotations

import time
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REQ = "REQ-e90c581652f6c90d3e33af23"
sqs = boto3.client("sqs", region_name="us-east-1")
dlq = sqs.get_queue_url(QueueName="irpt-generation-dlq")["QueueUrl"]
src = sqs.get_queue_url(QueueName="irpt-generation")["QueueUrl"]
OUT = []


def say(x):
    OUT.append(x)
    print(x, flush=True)


def cnt(url):
    a = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible", "ApproximateNumberOfMessagesDelayed"])["Attributes"]
    return int(a["ApproximateNumberOfMessages"]), int(a["ApproximateNumberOfMessagesNotVisible"]), int(a["ApproximateNumberOfMessagesDelayed"])


before = cnt(dlq)
say("R0 attempt3 dlq visible=%d inflight=%d delayed=%d | source %s" % (*before, cnt(src)))
held, seen_ids, is7h, deleted, empty_streak = [], set(), 0, 0, 0
for _ in range(40):
    r = sqs.receive_message(QueueUrl=dlq, MaxNumberOfMessages=10, WaitTimeSeconds=2, VisibilityTimeout=120)
    msgs = r.get("Messages", [])
    if not msgs:
        empty_streak += 1
        if empty_streak >= 3:
            break
        continue
    empty_streak = 0
    for m in msgs:
        if m["MessageId"] in seen_ids:
            continue
        seen_ids.add(m["MessageId"])
        if REQ in (m.get("Body") or "") and not deleted:
            is7h += 1
            sqs.delete_message(QueueUrl=dlq, ReceiptHandle=m["ReceiptHandle"])
            deleted += 1
        else:
            held.append(m["ReceiptHandle"])
returned = 0
for h in held:
    sqs.change_message_visibility(QueueUrl=dlq, ReceiptHandle=h, VisibilityTimeout=0)
    returned += 1
say("M distinct_received=%d is7h=%d returned=%d (held invisible while the DLQ was enumerated, then returned together)" % (len(seen_ids), is7h, returned))
if deleted:
    say("D deleted=1 by_receipt_handle")
time.sleep(75)
after = cnt(dlq)
s = cnt(src)
say("C dlq_before=%d dlq_after=%d source_visible=%d source_inflight=%d" % (sum(before), sum(after), s[0], s[1]))
say("DLQ-DELETE-DONE" if deleted else "DLQ-DELETE-STOP all %d distinct DLQ messages enumerated and none carries the 7H request id in its body; nothing deleted" % len(seen_ids))
(HERE / "A_DLQ_DELETE.txt").write_text("\n".join(OUT) + "\n", encoding="ascii", errors="replace", newline="\n")
