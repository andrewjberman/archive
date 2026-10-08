"""TO19 read-only AWS evidence; never emits message/cursor contents or signed URLs."""

import base64
import datetime as dt
import hashlib
import json
import pathlib
import sys
import urllib.request
import boto3

OUT = pathlib.Path(__file__).resolve().parent
def NOW():
    return dt.datetime.now(dt.timezone.utc)
FN = [
    "teams-global-chat-assist-handler-lambda",
    "teams-global-chat-assist-ingress-lambda",
]


def save(name, value):
    p = OUT / name
    p.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return p


def digest(b):
    return {
        "sha256": hashlib.sha256(b).hexdigest(),
        "sha256_base64": base64.b64encode(hashlib.sha256(b).digest()).decode(),
        "bytes": len(b),
    }


def functions():
    client = boto3.client("lambda", region_name="us-east-1")
    return client, [
        {k: d[k] for k in ("FunctionName", "CodeSha256", "LastModified", "RevisionId")}
        for d in [client.get_function_configuration(FunctionName=n) for n in FN]
    ]


def before():
    client, rows = functions()
    assert len({r["CodeSha256"] for r in rows}) == 1, "Live function hashes disagree"
    url = client.get_function(FunctionName=FN[0])["Code"]["Location"]
    with urllib.request.urlopen(url) as response:
        data = response.read()
    proof = digest(data)
    assert proof["sha256_base64"] == rows[0]["CodeSha256"], (
        "Downloaded live zip hash mismatch"
    )
    (OUT / "before-live-package.zip").write_bytes(data)
    s3 = boto3.client("s3", region_name="us-east-1")
    obj = s3.get_object(
        Bucket="opal-data-transcripts",
        Key="teams/transcripts/state/chat_assist/global/cursor.json",
    )
    cursor = obj["Body"].read()
    (OUT / "before-cursor.json").write_bytes(cursor)
    result = {
        "read_utc": NOW().isoformat(),
        "functions": rows,
        "package": proof,
        "cursor": digest(cursor),
    }
    save("before-metadata.json", result)
    print(json.dumps(result, indent=2))


def events(group, start, end):
    client = boto3.client("logs", region_name="us-east-1")
    args = dict(
        logGroupName=group,
        startTime=int(start.timestamp() * 1000),
        endTime=int(end.timestamp() * 1000),
    )
    for page in client.get_paginator("filter_log_events").paginate(**args):
        for row in page.get("events", []):
            yield row


def parsed(row):
    raw = row["message"]
    try:
        return json.loads(raw[raw.index("{") :])
    except (ValueError, TypeError):
        return {}


def eod():
    end = NOW()
    start = end - dt.timedelta(minutes=60)
    sqs = boto3.client("sqs", region_name="us-east-1")
    url = sqs.get_queue_url(QueueName="teams-global-chat-assist-queue.fifo")["QueueUrl"]
    attrs = sqs.get_queue_attributes(
        QueueUrl=url, AttributeNames=["ApproximateNumberOfMessagesNotVisible"]
    )["Attributes"]
    pending = {}
    completed = 0
    total = 0
    control = 0
    kinds = {}
    for row in events("/aws/lambda/" + FN[0], start, end):
        total += 1
        if "REPORT RequestId:" in row["message"]:
            control += 1
        d = parsed(row)
        kind = d.get("kind", "")
        if not isinstance(kind, str) or not kind.startswith("eod."):
            continue
        # Old live tenant logs lack object hashes. The runtime processes records
        # sequentially in each invocation/stream; match the next completion of
        # the same kind within that stream, never across streams.
        event = d.get("event")
        key = (row["logStreamName"], kind)
        kinds[event] = kinds.get(event, 0) + 1
        if event == "ldo_event":
            if pending.get(key):
                pending[key].pop(0)
            if not pending.get(key):
                pending.pop(key, None)
            completed += 1
        else:
            pending.setdefault(key, []).append(row["timestamp"])
    result = {
        "read_utc": end.isoformat(),
        "window_start": start.isoformat(),
        "queue": attrs,
        "log_event_count": total,
        "positive_control_REPORT": control,
        "eod_counts_by_event": kinds,
        "completed_eod": completed,
        "unmatched_eod_count": len(pending),
        "after_2145Z": end >= dt.datetime(2026, 10, 8, 21, 45, tzinfo=dt.timezone.utc),
    }
    result["gate_clear"] = (
        result["after_2145Z"]
        and attrs["ApproximateNumberOfMessagesNotVisible"] == "0"
        and not pending
        and control > 0
    )
    save("eod-gate.json", result)
    print(json.dumps(result, indent=2))


def after():
    _, rows = functions()
    data = pathlib.Path(
        "infra/aws/lambda/teams-chat-assist/dist/teams-chat-assist.zip"
    ).read_bytes()
    result = {
        "read_utc": NOW().isoformat(),
        "functions": rows,
        "built": digest(data),
        "matches": all(r["CodeSha256"] == digest(data)["sha256_base64"] for r in rows),
    }
    save("after-metadata.json", result)
    print(json.dumps(result, indent=2))


def ingress():
    start = dt.datetime.fromisoformat(sys.argv[2])
    end = min(NOW(), start + dt.timedelta(minutes=5))
    counts = {}
    steps = {}
    polls = 0
    lines = 0
    control = 0
    for row in events("/aws/lambda/" + FN[1], start, end):
        lines += 1
        if "REPORT RequestId:" in row["message"]:
            control += 1
        d = parsed(row)
        event = d.get("event")
        if event:
            counts[event] = counts.get(event, 0) + 1
        if event == "ingress_poll" and all(
            k in d for k in ["chats_read", "pages", "messages"]
        ):
            polls += 1
        if event == "ingress_step_failed":
            step = d.get("step", "unknown")
            steps[step] = steps.get(step, 0) + 1
    result = {
        "start_utc": start.isoformat(),
        "end_utc": end.isoformat(),
        "lines": lines,
        "positive_control_REPORT": control,
        "events": counts,
        "failed_steps": steps,
        "polls_with_new_fields": polls,
        "gate_clear": polls > 0 and steps.get("chats", 0) == 0 and control > 0,
    }
    save("after-ingress-counts.json", result)
    print(json.dumps(result, indent=2))


def trail():
    start = dt.datetime.fromisoformat(sys.argv[2])
    client = boto3.client("cloudtrail", region_name="us-east-1")
    rows = []
    for fn in FN:
        for page in client.get_paginator("lookup_events").paginate(
            LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": fn}],
            StartTime=start,
        ):
            for event in page.get("Events", []):
                d = json.loads(event["CloudTrailEvent"])
                name = d.get("requestParameters", {}).get("functionName", "")
                if name == fn and d["eventName"].startswith("UpdateFunctionCode"):
                    rows.append(
                        {
                            "function": name,
                            "event_time": d["eventTime"],
                            "event_id": d["eventID"],
                            "event_name": d["eventName"],
                        }
                    )
    save("cloudtrail.json", rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    {"before": before, "eod": eod, "after": after, "ingress": ingress, "trail": trail}[
        sys.argv[1]
    ]()
