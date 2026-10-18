#!/usr/bin/env python
"""OG-ap-42 Phase B (the CTO's CT4): during the read-back window, how many Graph-backed tool calls succeeded or failed, and how many GraphHostRefused errors did the service log? READ ONLY.
Two of the service's own logs, counts only (no principal, argument or row content is printed):
  journal:    the opal-gateway unit's lines between the start and the end that contain GraphHostRefused, and its POST /mcp lines
  audit lake: s3://opal-mcp-audit audit/dt=<day>/ records between the start and the end, counted by tool and outcome word; a tool is GRAPH-BACKED by a static reading of the release tree's app/ (stated as such):
              (1) a function in app/tools.py that calls graph.call, or calls (by name, transitively) a function that does; (2) the audited route names of every other app module that imports graph
              (audit.log_call(<identity>, "<name>", ...) literals, e.g. hx_teams in teams_route.py and hx_msgs in mail_route.py). The first version of this script only looked at each tool function's own
              source and so counted 1 call (whoami); it missed the tools that reach Graph through a helper and the hx routes (see "supersedes" in the record).
usage: python ap42_graphcounts.py <start_utc> <end_utc> <out.json>"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-mcp-audit"
TOOLS_PY = "C:/tmp/og-rel-batch10/infra/aws/ec2/opal-gateway/app/tools.py"


def graph_backed_tools():
    src = open(TOOLS_PY, encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            direct, called = False, set()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Attribute) and sub.attr == "call" and isinstance(sub.value, ast.Name) and sub.value.id == "graph":
                    direct = True
                if isinstance(sub, ast.Call):
                    f = sub.func
                    called.add(f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else ""))
            funcs[node.name] = (direct, called)
    marked = {n for n, (d, _c) in funcs.items() if d}
    changed = True
    while changed:
        changed = False
        for n, (_d, called) in funcs.items():
            if n not in marked and called & marked:
                marked.add(n)
                changed = True
    out = set(marked)
    app_dir = os.path.dirname(TOOLS_PY)
    for fn in sorted(os.listdir(app_dir)):
        if not fn.endswith(".py") or fn in ("tools.py", "graph.py"):
            continue
        text = open(os.path.join(app_dir, fn), encoding="utf-8", errors="replace").read()
        if re.search(r"^from \. import [^\n]*\bgraph\b|^import graph", text, re.M):
            out |= set(re.findall(r'audit\.log_call\(\s*[^,]+,\s*"([A-Za-z_]+)"', text))
    return out


def journal_counts(start, end):
    since, until = start.replace("T", " ").replace("Z", ""), end.replace("T", " ").replace("Z", "")
    cmd = ("echo BEGIN; journalctl -u opal-gateway --since '%s UTC' --until '%s UTC' --no-pager 2>&1 | grep -c 'GraphHostRefused'; "
           "journalctl -u opal-gateway --since '%s UTC' --until '%s UTC' --no-pager 2>&1 | grep -c 'POST /mcp'; echo END" % (since, until, since, until))
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
    nums = [x.strip() for x in inv["StandardOutputContent"].split("BEGIN", 1)[-1].split("END", 1)[0].splitlines() if x.strip().isdigit()]
    return {"graph_host_refused_lines": int(nums[0]) if nums else None, "post_mcp_lines": int(nums[1]) if len(nums) > 1 else None, "ssm_command_id": cid}


def lake_counts(start, end):
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
    by, errors, refused_lines = {}, 0, 0
    for k in inwin:
        try:
            for ln in s3.get_object(Bucket=BUCKET, Key=k)["Body"].read().decode("utf-8", "replace").splitlines():
                if ln.strip():
                    rec = json.loads(ln)
                    tool = str(rec.get("tool"))
                    out = str(rec.get("outcome") or rec.get("verdict") or "unknown")[:24]
                    by.setdefault(tool, {})
                    by[tool][out] = by[tool].get(out, 0) + 1
                    refused_lines += "GraphHostRefused" in ln
        except Exception:
            errors += 1
    gb = graph_backed_tools()
    gcalls = {t: v for t, v in by.items() if t in gb}
    ok = sum(n for v in gcalls.values() for o, n in v.items() if o in ("ok", "allowed", "success"))
    allc = sum(n for v in gcalls.values() for n in v.values())
    return {"objects_in_window": len(inwin), "read_errors": errors, "records_in_window": sum(sum(v.values()) for v in by.values()), "distinct_tools_seen": len(by),
            "graph_backed_tool_names_in_tools_py": len(gb), "graph_backed_tools_called": sorted(gcalls), "graph_backed_calls": allc, "graph_backed_calls_ok": ok, "graph_backed_calls_not_ok": allc - ok,
            "graph_backed_by_outcome": gcalls, "audit_records_naming_GraphHostRefused": refused_lines, "all_tools_by_outcome": by}


def main():
    start, end, out = sys.argv[1:4]
    rec = {"window_start_utc": start, "window_end_utc": end, "journal": journal_counts(start, end), "audit_lake": lake_counts(start, end),
           "method": "graph-backed = a tools.py function that calls graph.call or (transitively, by name) a function that does, plus the audited route names of the other app modules that import graph (static reading)",
           "supersedes": {"first_count": {"graph_backed_calls": 1, "tools": ["whoami"], "how": "only each tool function's own source was searched for 'graph'"},
                          "why_wrong": "tools that reach Graph through a helper (read_channel_messages, poll_addressed_teams_messages) and the hx route names (hx_teams, hx_msgs) were not counted"}}
    with open(out, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps(rec, indent=1) + chr(10))
    print(json.dumps({k: rec["audit_lake"][k] for k in ("records_in_window", "distinct_tools_seen", "graph_backed_tools_called", "graph_backed_calls", "graph_backed_calls_ok", "graph_backed_calls_not_ok", "audit_records_naming_GraphHostRefused")}), json.dumps(rec["journal"]))


if __name__ == "__main__":
    main()
