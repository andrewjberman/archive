"""Round 24 AC1 (IB-pr-241) -- the diagnosis names the Inflection RAW bronze writer and why it stopped after 2026-09-27
(row S216; 1.0.0_SA_CTO 102969: diagnose before restarting anything).

Usage: python p24_1_ac1_raw_writer_diagnosis.py <worktree root>
Reads `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~81/RAW_WRITER_DIAGNOSIS.json` and checks it
against the live world (read-only):
  (1) fields present: raw_writer (kind + name), last_raw_date, stop_cause (one sentence), evidence (>= 3 items, each
      naming a log group / S3 key / commit), restart_path (what a restart would change, under which ledger);
  (2) last_raw_date equals the newest date for which opal-data-inf bronze/positions/<date>.jsonl.gz exists (S3 list);
  (3) raw_writer names a thing that exists: a Lambda function (get_function) or an EC2 launch template / SSM document
      (describe), per its kind.
Pass: all three.
"""
import json
import sys
from pathlib import Path

import boto3

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
rec = root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~81/RAW_WRITER_DIAGNOSIS.json"
if not rec.is_file():
    print("diagnosis record absent:", rec)
    print("P24-1-AC1 FAIL")
    sys.exit(1)
d = json.loads(rec.read_text(encoding="utf-8"))
need = ("raw_writer", "last_raw_date", "stop_cause", "evidence", "restart_path")
fields = all(k in d and d[k] for k in need) and isinstance(d.get("evidence"), list) and len(d["evidence"]) >= 3 \
    and isinstance(d.get("raw_writer"), dict) and d["raw_writer"].get("kind") and d["raw_writer"].get("name")
print("fields present:", bool(fields))
s3 = boto3.client("s3", region_name="us-east-1")
dates = []
for page in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-inf", Prefix="bronze/positions/"):
    dates += [o["Key"].rsplit("/", 1)[-1][:10] for o in page.get("Contents", []) if o["Key"].endswith(".jsonl.gz")]
newest = max(dates) if dates else None
date_ok = bool(fields) and d.get("last_raw_date") == newest
print("newest raw positions date in S3: %s | record says %s | equal: %s" % (newest, d.get("last_raw_date"), date_ok))
exists = False
if fields:
    kind, name = d["raw_writer"]["kind"].lower(), d["raw_writer"]["name"]
    try:
        if "lambda" in kind:
            boto3.client("lambda", region_name="us-east-1").get_function(FunctionName=name)
            exists = True
        elif "launch" in kind:
            boto3.client("ec2", region_name="us-east-1").describe_launch_templates(LaunchTemplateNames=[name])
            exists = True
        elif "ssm" in kind:
            boto3.client("ssm", region_name="us-east-1").describe_document(Name=name)
            exists = True
        elif "ec2" in kind or "instance" in kind:
            r = boto3.client("ec2", region_name="us-east-1").describe_instances(InstanceIds=[name])
            exists = bool(r["Reservations"])
    except Exception as exc:  # noqa: BLE001 -- the check reports the refusal by name
        print("raw_writer lookup refused:", type(exc).__name__, str(exc)[:120])
print("raw_writer exists: %s" % exists)
ok = bool(fields) and date_ok and exists
print("P24-1-AC1 PASS" if ok else "P24-1-AC1 FAIL")
sys.exit(0 if ok else 1)
