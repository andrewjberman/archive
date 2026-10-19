#!/usr/bin/env python
"""OG-ev-10 STEP 1: is the per-identity refusal's audit write failing? READ-ONLY (journalctl on the host over SSM; the audit lake listed and read; nothing written but the local record). Counts only: no log line,
principal, address or email is printed or stored.
  python ev10_step1.py <out.json> <journal_since_utc 'YYYY-MM-DD HH:MM:SS'>      (repository root of the worktree that holds this file)
Journal: the unit's lines since the given UTC time (the OG-ap-44 restart). Lake: s3://opal-mcp-audit audit/dt=<day>/ objects from the first access line to now, each object read, records with event gw_ratelimit counted.
The OG-ev-7 limb: the records of 2026-10-18T21:08:03Z to 21:08:59Z not labelled probe, as (label, tool or event) pairs (the same window rule as ev7_run.py lake_labels)."""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-mcp-audit"
OUT, SINCE = sys.argv[1], sys.argv[2]
ssm = boto3.client("ssm", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
E7_START, E7_END = "2026-10-18T21:08:03Z", "2026-10-18T21:08:59Z"
BASE = "journalctl -u opal-gateway --since '%s UTC' --utc --no-pager -o short-iso" % SINCE


def journal():
    cmd = ("echo BEGIN; %(b)s | grep -E 'POST /mcp' | head -1 | cut -d' ' -f1; %(b)s | tail -1 | cut -d' ' -f1; "
           "%(b)s | grep -cE '\"POST /mcp[^\"]*\" 429'; %(b)s | grep -c 'ratelimit-audit WARN: refusal row not recorded'; "
           "%(b)s | grep -cE '\"POST /mcp'; %(b)s | wc -l; %(b)s | head -1 | cut -d' ' -f1; echo END" % {"b": BASE})
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
    inv = None
    for _ in range(90):
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    body = [x.strip() for x in inv["StandardOutputContent"].split("BEGIN", 1)[-1].split("END", 1)[0].splitlines() if x.strip()]
    first, last, n429, warn, mcp_all, total, earliest = body[:7]
    return {"first_access_line_ts": first, "last_line_ts": last, "post_mcp_429_lines": int(n429), "ratelimit_audit_warn_lines": int(warn), "post_mcp_lines": int(mcp_all), "journal_lines_total": int(total),
            "journal_earliest_line_ts": earliest, "ssm_command_id": cid}


def iso_z(ts):
    return dt.datetime.fromisoformat(ts.replace("+0000", "+00:00")).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def list_keys(start_z, end_z):
    keys = []
    d0 = dt.date.fromisoformat(start_z[:10])
    d1 = dt.date.fromisoformat(end_z[:10])
    day = d0
    while day <= d1:
        token, first = None, True
        while first or token:
            first = False
            kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day.isoformat()}
            if token:
                kw["ContinuationToken"] = token
            elif day == d0:
                kw["StartAfter"] = "audit/dt=%s/%s" % (day.isoformat(), start_z[:-1])
            page = s3.list_objects_v2(**kw)
            keys += [o["Key"] for o in page.get("Contents", [])]
            token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
        day += dt.timedelta(days=1)
    return [k for k in keys if k.split("/")[-1][:19] <= end_z[:-1]]


def read_one(key):
    try:
        out = []
        for ln in s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8", "replace").splitlines():
            if ln.strip():
                rec = json.loads(ln)
                label = "none"
                if "probe:" in ln:
                    label = ln[ln.index("probe:"):].split('"')[0].split()[0][:24]
                out.append((rec.get("event") or "", rec.get("tool") or "", label))
        return key, out, None
    except Exception as exc:                                    # a counted read error, never a silent zero
        return key, [], type(exc).__name__


def main():
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    j = journal()
    start = iso_z(j["first_access_line_ts"])
    end = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    keys = list_keys(start, end)
    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(read_one, keys))
    errors = sum(1 for _k, _o, e in res if e)
    rl_rows = sum(1 for _k, o, _e in res for ev, _t, _l in o if ev == "gw_ratelimit")
    total = sum(len(o) for _k, o, _e in res)
    e7keys = {k for k in list_keys(E7_START, E7_END) if k.split("/")[-1][:19] >= E7_START[:-1]}
    pairs = {}
    e7_total = 0
    for k, o, _e in res:
        if k in e7keys:
            for ev, tool, label in o:
                e7_total += 1
                if label.startswith("probe:"):
                    continue
                pairs[(label, tool or ev or "unknown")] = pairs.get((label, tool or ev or "unknown"), 0) + 1
    e7_pairs = [{"label": a, "tool": b, "n": n} for (a, b), n in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0]))]
    body = {
        "journal": {"source": "ssm send-command on the host: " + BASE + " | grep -cE '\"POST /mcp[^\"]*\" 429' ; | grep -c 'ratelimit-audit WARN: refusal row not recorded' (counts only; first access line = first 'POST /mcp' line)",
                    "first_access_line_ts": j["first_access_line_ts"], "last_line_ts": j["last_line_ts"], "post_mcp_429_lines": j["post_mcp_429_lines"], "ratelimit_audit_warn_lines": j["ratelimit_audit_warn_lines"],
                    "post_mcp_lines": j["post_mcp_lines"], "journal_lines_total": j["journal_lines_total"], "journal_earliest_line_ts": j["journal_earliest_line_ts"]},
        "lake": {"source": "s3://%s audit/dt=<day>/ listed (StartAfter the window start) and every object read, records with event gw_ratelimit counted; %d records read" % (BUCKET, total),
                 "window_start": start, "window_end": end, "gw_ratelimit_rows": rl_rows, "denominator": len(keys), "read_errors": errors},
        "counter_exposed": False,
        "counter_evidence": "Grep audit_failure_count|_audit_failures over infra/aws/ec2/opal-gateway/**/*.py: 7 hits, none a route or health read: app/ratelimit.py:199 (the variable), :202 and :204 (the reader function), :222 (docstring), :223 and :246 (the writer's own global and increment); tests/test_og_en10.py:57, :154, :164 (the tests).",
        "controlled_refusal": None,
        "ev7_unlabelled": {"window_start": E7_START, "window_end": E7_END, "records": sum(p["n"] for p in e7_pairs), "pairs": e7_pairs,
                           "source": "s3://%s audit/dt=2026-10-18/ objects after 2026-10-18T21:08:03 up to 21:08:59 (the ev7_run.py lake_labels rule), each object read; %d records in the window, probe-labelled ones excluded; label = the probe:<order> token or none, tool = the record's tool or event" % (BUCKET, e7_total)},
        "read_at": {"start": t0, "end": end},
    }
    n429, warn = j["post_mcp_429_lines"], j["ratelimit_audit_warn_lines"]
    if warn >= 1:
        body["verdict"], body["reason"] = "FAILS", "the writer's own WARN line is in the journal (%d)" % warn
    elif n429 >= 1 and rl_rows == 0:
        body["verdict"], body["reason"] = "FAILS", "%d POST /mcp lines answered 429 and the lake holds 0 gw_ratelimit rows for the window" % n429
    elif n429 >= 1 and rl_rows >= 1:
        body["verdict"], body["reason"] = "WRITES", "%d 429 lines in the journal and %d gw_ratelimit rows in the lake" % (n429, rl_rows)
    else:
        body["verdict"], body["reason"] = "NOT_EXPOSED", "no POST /mcp line answered 429 in the retained window and no route exposes the counter; %d lake rows" % rl_rows
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"body": body}, indent=1) + "\n")
    print(json.dumps({"verdict": body["verdict"], "429": n429, "warn": warn, "post_mcp": j["post_mcp_lines"], "lake_rows": rl_rows, "objects": len(keys), "errors": errors, "e7_records": body["ev7_unlabelled"]["records"], "e7_pairs": e7_pairs}))


if __name__ == "__main__":
    main()
