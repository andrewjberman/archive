#!/usr/bin/env python
"""OG-ap-44 Phase B (the CTO's criterion and CT3): is the service's access log back? READ ONLY. Two sources, the SAME window, counts only (no principal, argument or row content is printed):
  journal:    the opal-gateway unit's lines between the start and the end: `POST /mcp` lines (the service's own), `POST /probe/` lines (the listener's), the total, and the INFO startup lines of the uvicorn servers
  audit lake: s3://opal-mcp-audit audit/dt=<day>/ records between the start and the end (the method of ap42_graphcounts.py), by tool
  baseline:   the same two counts for the 30 minutes before the OG-ap-40 deploy (the last window with a live access log)
usage: python ap44_accesslog.py <start_utc> <end_utc> <baseline_start_utc> <baseline_end_utc> <out.json>"""
from __future__ import annotations

import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-mcp-audit"


def journal(start, end):
    since, until = start.replace("T", " ").replace("Z", ""), end.replace("T", " ").replace("Z", "")
    base = "journalctl -u opal-gateway --since '%s UTC' --until '%s UTC' --no-pager 2>&1" % (since, until)
    cmd = ("echo BEGIN; %s | grep -c 'POST /mcp'; %s | grep -c 'POST /probe/'; %s | wc -l; "
           "%s | grep 'Started server process\\|Uvicorn running on' | sed 's/^.*uvicorn\\[[0-9]*\\]: //' | cut -c1-90; echo END" % (base, base, base, base))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
    inv = None
    for _ in range(40):
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    body = inv["StandardOutputContent"].split("BEGIN", 1)[-1].split("END", 1)[0].splitlines()
    nums = [x.strip() for x in body if x.strip().isdigit()][:3]
    lines = [x.strip() for x in body if x.strip() and not x.strip().isdigit()]
    return {"post_mcp_lines": int(nums[0]) if len(nums) > 0 else None, "post_probe_lines": int(nums[1]) if len(nums) > 1 else None, "journal_lines_total": int(nums[2]) if len(nums) > 2 else None,
            "uvicorn_startup_lines": lines, "ssm_command_id": cid}


def lake(start, end):
    s3 = boto3.client("s3", region_name="us-east-1")
    day = start[:10]
    keys, token, first = [], None, True
    while first or token:
        first = False
        kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day}
        kw.update({"ContinuationToken": token} if token else {"StartAfter": "audit/dt=%s/%s" % (day, start[:-1])})
        page = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in page.get("Contents", [])]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
    inwin = [k for k in keys if k.split("/")[-1][:19] <= end[:-1]]
    by, errors = {}, 0
    for k in inwin:
        try:
            for ln in s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if ln.strip():
                    rec = json.loads(ln)
                    tool = str(rec.get("tool"))
                    out = str(rec.get("outcome") or rec.get("verdict") or "unknown")[:24]
                    by.setdefault(tool, {})
                    by[tool][out] = by[tool].get(out, 0) + 1
        except Exception:
            errors += 1
    return {"objects_in_window": len(inwin), "read_errors": errors, "records_in_window": sum(sum(v.values()) for v in by.values()), "distinct_tools_seen": len(by), "by_tool_and_outcome": by}


def main():
    start, end, bstart, bend, out = sys.argv[1:6]
    rec = {"window_start_utc": start, "window_end_utc": end, "journal": journal(start, end), "audit_lake": lake(start, end),
           "baseline_window": {"start_utc": bstart, "end_utc": bend, "journal": journal(bstart, bend)},
           "method": "journalctl -u opal-gateway between the window's two times, grep -c 'POST /mcp' (the service) and 'POST /probe/' (the listener); the audit lake read object by object (key names start with the record's own UTC time); the same window for both"}
    with open(out, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps(rec, indent=1) + chr(10))
    print(json.dumps({"journal_post_mcp": rec["journal"]["post_mcp_lines"], "journal_post_probe": rec["journal"]["post_probe_lines"], "journal_total": rec["journal"]["journal_lines_total"], "lake_records": rec["audit_lake"]["records_in_window"],
                      "baseline_post_mcp": rec["baseline_window"]["journal"]["post_mcp_lines"], "startup_lines": rec["journal"]["uvicorn_startup_lines"]}))


if __name__ == "__main__":
    main()
