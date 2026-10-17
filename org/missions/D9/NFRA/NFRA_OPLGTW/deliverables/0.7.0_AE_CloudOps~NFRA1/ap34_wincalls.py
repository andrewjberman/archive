#!/usr/bin/env python
"""OG-ap-34 Phase B, CTO CT1 Amendment 1 point 3: how many /mcp calls did the SERVICE serve in the read-back window, and how many of them were window reads?
READ-ONLY. Two of the service's own logs, counts only (no principal, argument or row content is printed):
  journal: the uvicorn access lines of the opal-gateway unit, `POST /mcp` between the start and the end (the service's stdout log; it names no tool)
  audit lake: s3://opal-mcp-audit audit/dt=<day>/ records the service wrote (key names start with the record's own UTC timestamp); records between the start and the end whose
              tool is client_get_transactions or client_get_fees, plus the total records and the distinct tools seen
usage: python ap34_wincalls.py <start_utc> <end_utc> <out.json>      e.g. 2026-10-17T05:19:28Z 2026-10-17T05:50:00Z"""
from __future__ import annotations

import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-mcp-audit"
WINDOW_TOOLS = ("client_get_transactions", "client_get_fees")


def journal_count(start, end):
    since, until = start.replace("T", " ").replace("Z", ""), end.replace("T", " ").replace("Z", "")
    cmd = ("echo BEGIN; journalctl -u opal-gateway --since '%s UTC' --until '%s UTC' --no-pager 2>&1 | grep -c 'POST /mcp'; "
           "journalctl -u opal-gateway --since '%s UTC' --until '%s UTC' --no-pager 2>&1 | grep 'POST /mcp' | grep -c ' 200 '; echo END" % (since, until, since, until))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
    for _ in range(40):
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    nums = [x.strip() for x in inv["StandardOutputContent"].split("BEGIN", 1)[-1].split("END", 1)[0].splitlines() if x.strip().isdigit()]
    return {"post_mcp_lines": int(nums[0]) if nums else None, "post_mcp_status_200": int(nums[1]) if len(nums) > 1 else None, "ssm_command_id": cid}


def audit_counts(start, end):
    s3 = boto3.client("s3", region_name="us-east-1")
    day = start[:10]
    keys, token = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day, "StartAfter": "audit/dt=%s/%s" % (day, start[:-1])}
        if token:
            kw = {"Bucket": BUCKET, "Prefix": "audit/dt=%s/" % day, "ContinuationToken": token}
        r = s3.list_objects_v2(**kw)
        keys += [o["Key"] for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            break
        token = r["NextContinuationToken"]
    inwin = [k for k in keys if k.split("/")[-1][:19] <= end[:-1]]
    tools, errors = {}, 0
    for k in inwin:
        try:
            for ln in s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if ln.strip():
                    t = json.loads(ln).get("tool")
                    tools[t] = tools.get(t, 0) + 1
        except Exception:
            errors += 1
    return {"objects_listed_after_start": len(keys), "objects_in_window": len(inwin), "read_errors": errors, "records_in_window": sum(tools.values()),
            "distinct_tools_seen": len(tools), "window_tool_calls": {t: tools.get(t, 0) for t in WINDOW_TOOLS}, "window_tool_calls_total": sum(tools.get(t, 0) for t in WINDOW_TOOLS)}


def main():
    start, end, out = sys.argv[1:4]
    rec = {"window_start_utc": start, "window_end_utc": end, "journal": journal_count(start, end), "audit_lake": audit_counts(start, end)}
    with open(out, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps(rec, indent=1) + chr(10))
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
