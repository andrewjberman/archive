"""Scratch control: the shellpar allowed arms evaluated with the PRE-CHANGE dell2_ssm_policy.json (git HEAD) read explicitDeny; and with the new file minus its Allow of the shell-script document read denied."""
import json
import subprocess
import sys
from pathlib import Path

import boto3

TESTS = Path(sys.argv[1])
sys.path.insert(0, str(TESTS))
import simulate_policy as sp  # noqa: E402

iam = boto3.client("iam", region_name="us-east-1")
sg = sp.dsd.send_grant()
shell, f1 = sg["shell_arn"], "arn:aws:ec2:us-east-1:313476888478:instance/" + sg["f1_id"]
old = subprocess.run(["git", "show", "HEAD:infra/aws/terraform/nfra-ctlpln-identity/dell2_ssm_policy.json"], capture_output=True, text=True, check=True).stdout
g = sp.group_docs()
bus = sp.load(sp.DELL2_BUS_POLICY)
new = json.loads(sp.DELL2_SSM_POLICY.read_text(encoding="utf-8"))
no_allow = json.loads(json.dumps(new))
no_allow["Statement"][0]["Resource"] = [r for r in no_allow["Statement"][0]["Resource"] if "AWS-RunShellScript" not in r]
no_deny_session = json.loads(json.dumps(new))
no_deny_session["Statement"] = [s for s in no_deny_session["Statement"] if s["Sid"] != "DenyStartSessionOnShellScriptDocument"]
for label, doc, action, res in (
        ("PRE-CHANGE file: shell + F1", old, "ssm:SendCommand", [shell, f1]),
        ("NEW file minus the shell-script Allow resource: shell + F1", json.dumps(no_allow), "ssm:SendCommand", [shell, f1]),
        ("NEW file: shell + F1", json.dumps(new), "ssm:SendCommand", [shell, f1]),
        ("NEW file minus DenyStartSessionOnShellScriptDocument: StartSession on shell", json.dumps(no_deny_session), "ssm:StartSession", [shell]),
        ("NEW file: StartSession on shell", json.dumps(new), "ssm:StartSession", [shell])):
    dec, per = sp.eval_pair(iam, g + [bus, json.dumps(json.loads(doc))], action, res)
    print("CONTROL %-80s -> %s %s" % (label, dec, sorted({s for _d, sids in per.values() for s in sids})))
