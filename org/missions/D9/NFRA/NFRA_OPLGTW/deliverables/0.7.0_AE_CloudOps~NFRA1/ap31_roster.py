#!/usr/bin/env python
"""OG-ap-31 Phase A: READ-ONLY. How many entries does the host's MASTER_ADMIN_EMAILS hold, and is each of the three roster addresses the order names a member?
Booleans and a count only; no other value from .env is printed. usage: python ap31_roster.py <out.json>"""
import json
import sys
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
NAMED = {"andrew": "andrew@opalinvest.com", "opalbloomberg": "opalbloomberg@opalinvest.com", "alyssa": "alyssa@opalinvest.com"}
cmd = ("cd /opt/opal-gateway && echo BEGIN && (grep -E '^MASTER_ADMIN_EMAILS=' .env || echo ABSENT) | cut -d= -f2- | tr ',' ' ' | tr -d '\"' | tr '[:upper:]' '[:lower:]' | tr ' ' '\\n' | sed '/^$/d' | sort && echo END")
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
for _ in range(60):
    time.sleep(3)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
if inv["Status"] != "Success":
    raise SystemExit("SSM did not succeed: " + inv["Status"])
out = inv["StandardOutputContent"]
if "BEGIN" not in out or "END" not in out:
    raise SystemExit("output not bracketed")
entries = [x.strip() for x in out.split("BEGIN", 1)[1].split("END", 1)[0].splitlines() if x.strip()]
absent = entries == ["ABSENT"]
res = {"env_key_present": not absent, "entries": 0 if absent else len(entries), "members": {k: (v in entries) for k, v in NAMED.items()},
       "default_if_absent": "the code default is andrew@opalinvest.com only (app/config.py)", "ssm_command_id": cid}
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res))
