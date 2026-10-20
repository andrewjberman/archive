#!/usr/bin/env python
"""OG-ev-13: the audit lake leg after a day of production traffic. READ ONLY (journalctl over SSM, S3 list and get on s3://opal-mcp-audit). COUNTS ONLY: no principal, e-mail, account or object value is printed or kept.
  python ev13_run.py journal <scratch>     host journal: per-hour `POST /mcp` lines, `audit-lake WARN: lake put failed` lines, last count=, exception classes, first journal line time
  python ev13_run.py lake <scratch>        per-hour lake objects (LIST only) for every whole hour touching the window
  python ev13_run.py anomaly <scratch>     read EVERY body of the 2026-10-19T02:00Z hour, histogram by the record's tool (or event) name (background; progress in <scratch>/anomaly_progress.txt)
  python ev13_run.py build <scratch>       assemble W/AUDIT_LEG_24H.json from the three scratch records
The window is 2026-10-19T07:44:53Z (the OG-ap-48 close) to 2026-10-20T07:48:00Z (the issuer's GO); the first and last hour buckets are taken whole, the last capped at window_end for BOTH counts."""
from __future__ import annotations

import collections
import concurrent.futures
import datetime
import io
import json
import os
import subprocess
import sys
import time

import boto3

INSTANCE, BUCKET = "i-07dccb1615503ac99", "opal-mcp-audit"
WS, WE = "2026-10-19T07:44:53Z", "2026-10-20T07:48:00Z"
HOUR0 = datetime.datetime(2026, 10, 19, 7, 0, 0, tzinfo=datetime.timezone.utc)
HOURS = [(HOUR0 + datetime.timedelta(hours=i)).strftime("%Y-%m-%dT%H:00:00Z") for i in range(25)]
W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
ANOMALY_HOUR = "2026-10-19T02:00:00Z"
SOURCE = ("TZ=UTC journalctl -u opal-gateway -q --since '2026-10-19 07:00:00' --until '2026-10-20 07:48:00' --no-pager -o short-iso | grep -c 'POST /mcp' (per hour via awk on the first 13 characters); "
          "the same window | grep 'audit-lake WARN: lake put failed'")


def save(scratch, name, obj):
    io.open(os.path.join(scratch, name), "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1) + "\n")


def load(scratch, name):
    return json.load(io.open(os.path.join(scratch, name), encoding="utf-8"))


def journal(scratch):
    base = "TZ=UTC journalctl -u opal-gateway -q --since '2026-10-19 07:00:00' --until '2026-10-20 07:48:00' --no-pager -o short-iso"
    cmd = ("echo ---FIRST; TZ=UTC journalctl -u opal-gateway -q --no-pager -o short-iso | head -1 | cut -c1-25; "
           "echo ---PERHOUR; %(b)s | grep 'POST /mcp' | awk '{print substr($1,1,13)}' | sort | uniq -c; "
           "echo ---WARN; %(b)s | grep 'audit-lake WARN: lake put failed' > /tmp/ev13_warn.txt; echo LINES=$(grep -c . /tmp/ev13_warn.txt); echo LASTCOUNT=$(grep -o 'count=[0-9]*' /tmp/ev13_warn.txt | tail -1 | cut -d= -f2); "
           "echo CLASSES=$(grep -oE 'lake put failed \\(([A-Za-z0-9_.]+)\\)' /tmp/ev13_warn.txt | sed 's/.*(\\(.*\\))/\\1/' | sort -u | tr '\\n' ' '); rm -f /tmp/ev13_warn.txt; "
           "echo ---SHA; cat /opt/opal-gateway/.deployed_commit; echo ---END" % {"b": base})
    ssm = boto3.client("ssm", region_name="us-east-1")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=300)["Command"]["CommandId"]
    inv = None
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv["StandardOutputContent"]
    sec = {}
    for blk in so.split("---")[1:]:
        name, _, rest = blk.partition("\n")
        sec[name.strip()] = rest.strip()
    per = {}
    for ln in sec.get("PERHOUR", "").splitlines():
        n, hh = ln.split()
        per[hh + ":00:00Z"] = int(n)
    kv = dict(ln.split("=", 1) for ln in sec.get("WARN", "").splitlines() if "=" in ln)
    first = sec.get("FIRST", "").strip()[:19]
    doc = {"ssm_command_id": cid, "ssm_status": inv["Status"], "first_line_ts": (first + "Z") if first else None, "post_mcp_per_hour": per, "warn_lines": int(kv.get("LINES", "0") or 0), "last_count": int(kv.get("LASTCOUNT", "0") or 0),
           "classes": [c for c in kv.get("CLASSES", "").split() if c], "code_sha": sec.get("SHA", "").strip(), "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    save(scratch, "journal.json", doc)
    print(json.dumps({k: v for k, v in doc.items() if k != "post_mcp_per_hour"}), "hours with lines:", len(per), "total:", sum(per.values()))


def list_keys(s3, prefix):
    keys, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        if not page.get("IsTruncated"):
            return keys
        token = page.get("NextContinuationToken")


def lake(scratch):
    s3 = boto3.client("s3", region_name="us-east-1")
    keys = []
    for day in ("2026-10-19", "2026-10-20"):
        keys += list_keys(s3, "audit/dt=%s/" % day)
    cap = WE[:-1]
    per = collections.Counter()
    for k in keys:
        t = k.split("/")[-1][:19]
        if t[:13] + ":00:00Z" in HOURS and t < cap:
            per[t[:13] + ":00:00Z"] += 1
    sample = k.split("/")[-1] if (k := keys[0]) else ""
    doc = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "listed_keys_two_days": len(keys), "lake_objects_per_hour": dict(per), "key_shape": "audit/dt=<day>/<19-char iso time>" + sample[19:20] + "...", "listed_only": True}
    save(scratch, "lake.json", doc)
    print(json.dumps({"keys": len(keys), "hours": len(per), "in_window_total": sum(per.values())}))


def anomaly(scratch):
    s3 = boto3.client("s3", region_name="us-east-1")
    keys = [k for k in list_keys(s3, "audit/dt=2026-10-19/") if "2026-10-19T02:" in k.split("/")[-1][:19]]
    prog = os.path.join(scratch, "anomaly_progress.txt")
    hist, errors, read, key_names = collections.Counter(), 0, 0, []

    def one(k):
        for attempt in range(3):
            try:
                body = s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace")
                return [json.loads(ln) for ln in body.splitlines() if ln.strip()]
            except Exception:
                time.sleep(1 + attempt)
        return None

    with concurrent.futures.ThreadPoolExecutor(16) as ex:
        for i, recs in enumerate(ex.map(one, keys), 1):
            if recs is None:
                errors += 1
            else:
                read += 1
                for r in recs:
                    if len(key_names) < 2:
                        key_names.append(sorted(r.keys()))
                    hist[str(r.get("tool") or r.get("event") or "unnamed")] += 1
            if i % 100 == 0 or i == len(keys):
                io.open(prog, "w", encoding="utf-8").write("%d of %d objects, errors %d\n" % (i, len(keys), errors))
    doc = {"hour_start": ANOMALY_HOUR, "objects": len(keys), "read": read, "read_errors": errors, "records": sum(hist.values()), "sample_record_key_names": key_names,
           "tools": [{"tool": t, "n": n} for t, n in hist.most_common()], "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    save(scratch, "anomaly.json", doc)
    io.open(prog, "w", encoding="utf-8").write("DONE %d of %d objects, errors %d, records %d\n" % (read, len(keys), errors, doc["records"]))


def build(scratch):
    j, lk, an = load(scratch, "journal.json"), load(scratch, "lake.json"), load(scratch, "anomaly.json")
    git_sha = j["code_sha"]
    hours = [{"hour_start": h, "lake_objects": lk["lake_objects_per_hour"].get(h, 0), "post_mcp_lines": j["post_mcp_per_hour"].get(h, 0)} for h in HOURS]
    busy = [h for h in hours if h["post_mcp_lines"] >= 20]
    keeps = all(h["lake_objects"] >= 0.5 * h["post_mcp_lines"] for h in busy)
    warn_every = float(subprocess.run(["git", "show", "%s:infra/aws/ec2/opal-gateway/app/audit.py" % git_sha], capture_output=True).stdout.decode().split("_LAKE_WARN_EVERY_S = ", 1)[1].split()[0])
    if j["warn_lines"] >= 1:
        verdict = "FAILS_SEEN"
    elif keeps and j["first_line_ts"] and j["first_line_ts"] <= WS:
        verdict = "HOLDS"
    else:
        verdict = "UNDETERMINED"
    samp = [json.loads(ln) for ln in io.open(W + "rz2_pb/sampler.jsonl", encoding="utf-8") if ln.strip()]
    samp401 = collections.Counter(s["t"][:13] + ":00:00Z" for s in samp if s.get("code") == 401)
    body = {"window_start": WS, "window_end": WE, "code_sha": git_sha, "warn_every_s": warn_every,
            "journal": {"source": SOURCE, "first_line_ts": j["first_line_ts"], "warn_lines": j["warn_lines"], "last_count": j["last_count"], "classes": j["classes"]},
            "hours": hours, "anomaly_hour": {"hour_start": ANOMALY_HOUR, "objects": an["objects"], "read": an["read"], "read_errors": an["read_errors"], "tools": an["tools"], "explanation": "EXPLAIN"},
            "verdict": verdict, "evidence": ["EVIDENCE1", "EVIDENCE2"],
            "_scratch_for_authoring": {"busy_hours": len(busy), "keeps_pace": keeps, "sampler_probes_by_hour": dict(samp401), "total_post_mcp": sum(h["post_mcp_lines"] for h in hours), "total_lake": sum(h["lake_objects"] for h in hours), "anomaly_records": an["records"],
                                       "worst_busy_ratio": min((h["lake_objects"] / h["post_mcp_lines"] for h in busy), default=None)}}
    save(scratch, "build_draft.json", {"body": body})
    print(json.dumps(body["_scratch_for_authoring"]), verdict, "first line", j["first_line_ts"])


if __name__ == "__main__":
    {"journal": journal, "lake": lake, "anomaly": anomaly, "build": build}[sys.argv[1]](sys.argv[2])
