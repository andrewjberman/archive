#!/usr/bin/env python
"""OG-en-7 runner: upload en7_host.py to S3, run it ONCE on the gateway host (one SSM command, Rule 12), and write W/SMARTX_CROSSFIRM.json.
The live commit is the git-ref metadata of the deployed artifact, read before and after the host read; the record is written only if the two are equal.
usage: python en7_run.py   (from the repository root). No retry: a failure prints and stops."""
from __future__ import annotations

import datetime
import io
import json
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "ec2/opal-gateway/en7_host.py"
ART = "ec2/opal-gateway/opal-gateway-latest.tar.gz"
W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"

s3 = boto3.client("s3")


def live_ref() -> str:
    return s3.head_object(Bucket=BUCKET, Key=ART)["Metadata"].get("git-ref", "")


ref_before = live_ref()
s3.put_object(Bucket=BUCKET, Key=KEY, Body=io.open(W + "en7_host.py", "rb").read())
cmd = ("cd /opt/opal-gateway && rm -f /tmp/en7_host.py && aws s3 cp s3://%s/%s /tmp/en7_host.py --region us-east-1 >/dev/null && "
       "/opt/opal-gateway/.venv/bin/python /tmp/en7_host.py" % (BUCKET, KEY))
ssm = boto3.client("ssm")
cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=900)["Command"]["CommandId"]
inv = None
for _ in range(200):
    time.sleep(4)
    inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
    if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
        break
so = inv.get("StandardOutputContent", "")
ref_after = live_ref()
print("status=%s rc=%s stdout_chars=%d ref_before=%s ref_after=%s" % (inv["Status"], inv.get("ResponseCode"), len(so), ref_before[:10], ref_after[:10]))
if "EN7_JSON" not in so:
    raise SystemExit("no marker in the host output; stderr tail: " + inv.get("StandardErrorContent", "")[-400:])
doc = json.loads(so.split("EN7_JSON", 1)[1].strip())
print(json.dumps(doc, indent=1))
if "fatal" in doc or not doc.get("candidates"):
    raise SystemExit("host read did not produce a usable count; nothing recorded")
if ref_before != ref_after or not ref_after:
    raise SystemExit("the live ref moved or is unreadable during the read; nothing recorded")
n, k = doc["candidates"], doc["candidates_mapping_to_other_firm"]
rec = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "live_commit": ref_after,
    "method": ("On the gateway host, through the installed client_adapter_smartx: every distinct last4 on firm 49financial's accounts in the newest non-empty "
               "account map, grouped by the module's own _candidates_by_account; each candidate's account_id joined to its allocations and their roster rows, each "
               "advisor_name mapped through the context's own firm_roster(); a master_admin stand-in, read-only, audit sink stubbed."),
    "candidates_checked": n,
    "candidates_mapping_to_other_firm": k,
    "denominator": ("%d SmartX candidates (distinct account_ids of the firm, over %d distinct last4 values), built from %d firm allocations of %d roster rows and %d account-map rows; "
                    "the advisor-to-firm map holds %d names over %d firms." % (n, doc["distinct_last4"], doc["firm_allocations"], doc["roster_partition_rows"],
                                                                                 doc["account_map_partition_rows"], doc["firm_roster_names"], doc["firm_roster_firms"])),
    "expected": 0,
    "note": ("%d of %d candidates have an advisor mapped to another firm; %d have an unmapped advisor, %d an allocation without a roster row, %d sit on an account that also "
             "carries an allocation outside the firm's set; the served tool and the module agreed on %d of %d last4 values checked. The live commit is the deployed artifact's "
             "git-ref, equal before and after the read; host bytes were not walked." % (k, n, doc["candidates_with_unmapped_advisor"],
                                                                                          doc["candidates_with_an_allocation_lacking_a_roster_row"],
                                                                                          doc["candidates_on_a_shared_account"], doc["tool_crosscheck_agree"],
                                                                                          doc["tool_crosscheck_last4s"])),
    "command_id": cid,
}
io.open(W + "SMARTX_CROSSFIRM.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print("WROTE SMARTX_CROSSFIRM.json n=%d k=%d" % (n, k))
