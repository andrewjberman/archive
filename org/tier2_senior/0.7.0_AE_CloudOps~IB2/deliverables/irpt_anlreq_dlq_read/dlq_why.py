"""IRPT_ANLREQ TO-READ-DLQ-WHY (applier 0.7.0_AE_CloudOps~IB2): R1, R2, R3 and the closing line, READ ONLY.

  python dlq_why.py            prints the lines and writes A_DLQ_WHY.txt beside this file

One receive call with visibility timeout 0 on the dead letter queue; nothing is deleted, purged, redriven or sent. Closed words, counts, ages and
key NAMES only: no URL, host, email, token, signature or log line beyond the closed literals the order names.
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
REQS = (("REQ-8966d24ffefa1c28269ef26c", "cottonwood"), ("REQ-4b5155ac2ea9467ab771b414", "49financial"))
DLQ = "irpt-generation-dlq"
UPPER = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")
LOW, HIGH = datetime(2026, 10, 8, 20, 0, tzinfo=timezone.utc), datetime(2026, 10, 9, 23, 0, tzinfo=timezone.utc)
CUT = datetime(2026, 10, 8, 21, 0, tzinfo=timezone.utc)
lines, answered = [], 0


def utc_min(v):
    return v.strftime("%Y-%m-%dT%H:%MZ")


def from_attr(a):
    """A DynamoDB attribute value as an aware UTC datetime when it is an ISO string or an epoch number; else None."""
    if not a:
        return None
    s = a.get("S") or a.get("N")
    if not s:
        return None
    try:
        if re.fullmatch(r"\d+(\.\d+)?", s):
            x = float(s)
            return datetime.fromtimestamp(x / 1000.0 if x > 1e11 else x, timezone.utc)
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def r1(ddb):
    global answered
    ok = True
    for req, tenant in REQS:
        try:
            job = ddb.get_item(TableName="irpt-jobs", Key={"tenant": {"S": tenant}, "job": {"S": req}}, ConsistentRead=True).get("Item")
        except Exception:  # noqa: BLE001 -- the key names may differ; read them and retry once
            ks = [k["AttributeName"] for k in ddb.describe_table(TableName="irpt-jobs")["Table"]["KeySchema"]]
            try:
                job = ddb.get_item(TableName="irpt-jobs", Key={ks[0]: {"S": tenant}, ks[1]: {"S": req}}, ConsistentRead=True).get("Item")
            except Exception as e2:  # noqa: BLE001
                lines.append("R1 %s tenant=%s DENIED-OR-ERROR %s" % (req[4:16], tenant, type(e2).__name__))
                ok = False
                continue
        item = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": tenant}, "request_revision": {"S": "analysis#%s#1" % req}}, ConsistentRead=True).get("Item")
        state = (job or {}).get("state", {}).get("S") if job else None
        code = "none"
        code_member = None
        if job:
            for name, val in sorted(job.items()):
                s = val.get("S")
                if s and UPPER.match(s) and name != "state" and name not in ("tenant", "job"):
                    code, code_member = s, name
                    break
        attempts = "none"
        if job:
            for name, val in sorted(job.items()):
                if "attempt" in name.lower() and val.get("N"):
                    attempts = val["N"]
                    break
        upd = "none"
        if job:
            for name in ("updated_at", "updatedAt", "updated", "last_updated", "modified_at", "last_updated_at"):
                t = from_attr(job.get(name))
                if t:
                    upd = utc_min(t)
                    break
        acc = "none"
        if item:
            for name in ("accepted_at", "acceptedAt", "created_at", "createdAt", "accepted"):
                t = from_attr(item.get(name))
                if t:
                    acc = utc_min(t)
                    break
        lines.append("R1 %s tenant=%s job=%s state=%s code=%s attempts=%s updated=%s item=%s ticket=%s acceptedAt=%s" % (
            req[4:16], tenant, "exists" if job else "absent", state or "none", code, attempts, upd, "exists" if item else "absent",
            "yes" if item and (item.get("ticket_id") or {}).get("S") else "no", acc))
        lines.append("NOTE-R1 %s code_member=%s job_members=%s item_has_commentary_ref=%s" % (req[4:16], code_member or "none", ",".join(sorted(job.keys())) if job else "none", "yes" if item and "commentary_ref" in item else "no"))
    return ok


def r2(sqs):
    try:
        url = sqs.get_queue_url(QueueName=DLQ)["QueueUrl"]
        a = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=["ApproximateNumberOfMessages", "MessageRetentionPeriod"])["Attributes"]
        depth, ret = int(a["ApproximateNumberOfMessages"]), int(a["MessageRetentionPeriod"]) / 86400.0
        srcs = sqs.list_dead_letter_source_queues(QueueUrl=url).get("queueUrls", [])
        source, mrc, vis, sdepth, snv = "NOT FOUND", "?", "?", "?", "?"
        if srcs:
            surl = srcs[0]
            source = surl.rsplit("/", 1)[-1]
            sa = sqs.get_queue_attributes(QueueUrl=surl, AttributeNames=["RedrivePolicy", "VisibilityTimeout", "ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
            mrc = json.loads(sa.get("RedrivePolicy", "{}")).get("maxReceiveCount", "?")
            vis, sdepth, snv = sa.get("VisibilityTimeout"), sa.get("ApproximateNumberOfMessages"), sa.get("ApproximateNumberOfMessagesNotVisible")
        resp = sqs.receive_message(QueueUrl=url, VisibilityTimeout=0, MaxNumberOfMessages=10, WaitTimeSeconds=2, AttributeNames=["SentTimestamp", "ApproximateReceiveCount"])
        msgs = resp.get("Messages", [])
        ages, counts, ids = [], [], []
        now = time.time()
        for m in msgs:
            ages.append(round((now - int(m["Attributes"]["SentTimestamp"]) / 1000.0) / 86400.0, 1))
            counts.append(m["Attributes"]["ApproximateReceiveCount"])
            try:
                b = json.loads(m["Body"])
                rid = b.get("request_id") or (b.get("payload") or {}).get("request_id") or ""
                kind = b.get("kind") or ""
            except ValueError:
                rid, kind = "", ""
            ids.append("%s:%s" % ((rid[4:16] if rid.startswith("REQ-") else "none"), kind if UPPER.match(kind) or re.fullmatch(r"[a-z_]+", kind or "") else "kind?"))
        oldest = max(ages) if ages else None
        left = round(ret - oldest, 1) if oldest is not None else "none"
        lines.append("R2 dlq_depth=%d retention_days=%s source=%s max_receive=%s source_visibility_s=%s source_depth=%s source_not_visible=%s received=%d ages_days=%s receive_counts=%s oldest_retention_left_days=%s" % (
            depth, ("%g" % ret), source, mrc, vis, sdepth, snv, len(msgs), ",".join(str(x) for x in ages) or "none", ",".join(counts) or "none", left))
        lines.append("NOTE-R2 messages=%s" % (",".join(ids) or "none"))
        return True
    except Exception as e:  # noqa: BLE001
        lines.append("R2 DENIED-OR-ERROR %s" % type(e).__name__)
        return False


def host_journal_hits(ssm, ec2, req):
    """The resident unit's journal since 2026-10-08: first and last timestamp, total lines scanned, and the count of lines naming the request id (counts only)."""
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    script = "\n".join([
        "set -u", "UNIT=irpt-analysis-resident.service", "J=$(mktemp)",
        "journalctl -u \"$UNIT\" --since '2026-10-08 00:00:00' --no-pager -o short-iso -q > \"$J\" 2>/dev/null",
        "echo \"RAW J first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\") hits=$(grep -c '" + req + "' \"$J\" || true)\"",
        "rm -f \"$J\""]) + "\n"
    (HERE / "host_journal.sh").write_text(script, encoding="ascii", newline="\n")
    cid = ssm.send_command(InstanceIds=ids[:1], DocumentName="AWS-RunShellScript", Comment="DLQ-WHY R3 journal count read-only", Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=ids[0])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            m = re.search(r"RAW J first=(\S*) last=(\S*) scanned=(\d+) hits=(\d+)", inv.get("StandardOutputContent", ""))
            return {"window": "%s..%s" % (m.group(1), m.group(2)), "scanned": int(m.group(3)), "hits": int(m.group(4))} if m else {"error": "unparsed"}
    return {"error": "timeout"}


def r3(ssm, ec2, logs):
    req = REQS[0][0]
    ok = True
    try:
        jw = host_journal_hits(ssm, ec2, req)
    except Exception as e:  # noqa: BLE001
        jw = {"error": type(e).__name__}
        ok = False
    groups, hits, lits = [], 0, {}
    try:
        names = ["/aws/lambda/irpt-ycharts-generate"]
        extra = [g["logGroupName"] for g in logs.describe_log_groups(logGroupNamePrefix="/aws/lambda/irpt-").get("logGroups", []) if "resident" in g["logGroupName"]]
        for g in names + extra:
            try:
                d = logs.describe_log_groups(logGroupNamePrefix=g)["logGroups"]
                d = [x for x in d if x["logGroupName"] == g]
                if not d:
                    groups.append("%s:absent" % g.rsplit("/", 1)[-1])
                    continue
                ret = d[0].get("retentionInDays", "never-expires")
                streams = logs.describe_log_streams(logGroupName=g, orderBy="LastEventTime", descending=False, limit=1).get("logStreams", [])
                first = streams[0].get("firstEventTimestamp") if streams else None
                before = (datetime.fromtimestamp(first / 1000.0, timezone.utc) < CUT) if first else None
                groups.append("%s:%s:earliest_before_21z=%s" % (g.rsplit("/", 1)[-1], ret, "yes" if before else ("no" if before is False else "no-events")))
                n = 0
                for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=g, startTime=int(LOW.timestamp() * 1000), endTime=int(HIGH.timestamp() * 1000), filterPattern='"%s"' % req):
                    for ev in pg["events"]:
                        n += 1
                        if n <= 20:
                            toks = ev["message"].strip().split()
                            if toks and re.match(r"^[A-Z][A-Z0-9_]+", toks[0]):
                                lit = re.match(r"^[A-Z][A-Z0-9_]+", toks[0]).group(0)
                                if len(toks) > 1 and UPPER.match(toks[1]):
                                    lit += "/" + toks[1]
                                lits[lit] = lits.get(lit, 0) + 1
                hits += n
            except Exception as e:  # noqa: BLE001
                groups.append("%s:ERROR_%s" % (g.rsplit("/", 1)[-1], type(e).__name__))
                ok = False
    except Exception as e:  # noqa: BLE001
        groups.append("ERROR_%s" % type(e).__name__)
        ok = False
    cw = ",".join(groups) or "none"
    if groups and all(("earliest_before_21z=no" in x or "absent" in x or "no-events" in x) for x in groups):
        cw += " LOGS-NOT-RETAINED"
    lines.append("R3 journal_window=%s scanned=%s journal_hits=%s cw_groups=%s cw_hits=%d literals=%s" % (
        jw.get("window", "none"), jw.get("scanned", "none"), jw.get("hits", jw.get("error", "none")), cw, hits, ",".join("%s:%d" % kv for kv in sorted(lits.items())) or "none"))
    return ok


if __name__ == "__main__":
    ddb, sqs = boto3.client("dynamodb", region_name=REGION), boto3.client("sqs", region_name=REGION)
    ssm, ec2, logs = boto3.client("ssm", region_name=REGION), boto3.client("ec2", region_name=REGION), boto3.client("logs", region_name=REGION)
    n = 0
    n += 1 if r1(ddb) else 0
    n += 1 if r2(sqs) else 0
    n += 1 if r3(ssm, ec2, logs) else 0
    lines.append("READS-DONE %d of 3 answered" % n)
    text = "\n".join(lines) + "\n"
    (HERE / "A_DLQ_WHY.txt").write_text(text, encoding="ascii", newline="\n")
    print(text)
