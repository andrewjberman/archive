#!/usr/bin/env python
"""OG-ap-32 Phase B step 1 (CTO CT2): the gateway's worker and process count on the host, plus host memory and CPU. READ-ONLY. Names, counts and percentages only.
usage: python ap32_workers.py <out.json>"""
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
cmd = ("echo BEGIN; ps -eo pid,ppid,rss,comm,args --sort=pid | grep -E 'uvicorn|gunicorn' | grep -v grep | "
       "sed -E 's/ --env-file[^ ]*//; s/(--[a-z-]*(key|token|secret)[a-z-]*)[= ][^ ]*/\\1 <redacted>/Ig'; echo ---; systemctl show opal-gateway -p MainPID -p NRestarts -p ActiveState 2>/dev/null; "
       "echo ---; nproc; free -m | sed -n 2p; echo END")
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
for _ in range(30):
    time.sleep(3)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
out = inv["StandardOutputContent"]
body = out.split("BEGIN", 1)[1].split("END", 1)[0] if "BEGIN" in out else out
procs = [ln for ln in body.split("---")[0].splitlines() if ln.strip()]
res = {"ssm_command_id": cid, "status": inv["Status"], "uvicorn_or_gunicorn_processes": len(procs),
       "process_lines_sanitised": [" ".join(p.split()[:3]) + " " + " ".join(a for a in p.split()[3:] if a.startswith("--") or a in ("uvicorn", "gunicorn") or a.endswith(":app"))[:160] for p in procs],
       "workers_flag_seen": any("--workers" in p for p in procs), "rest": [x.strip() for x in body.split("---")[1:] if x.strip()]}
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
