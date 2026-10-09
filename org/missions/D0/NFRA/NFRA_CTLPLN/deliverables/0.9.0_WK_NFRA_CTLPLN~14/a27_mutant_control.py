"""AMENDMENT 27 mutant control (read-only simulation): dell2's and dell1's decision for the shell-script document sent to mdpf-daily-runner under
(a) the policy file as built, (b) the file as it stood at HEAD before this pass (without SendShellScriptToDailyRunner), and (c) the built file with the
PowerShell resource taken out of the Deny (so the PowerShell arm is shown to be refused BY that Deny, not by silence).
Run from the worktree root: python <this file>
"""
import json
import subprocess
import sys
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parents[7]
TESTS = ROOT / "infra" / "aws" / "terraform" / "nfra-ctlpln-identity" / "tests"
sys.path.insert(0, str(TESTS))
import derive_ssm_documents as dsd  # noqa: E402
import simulate_policy as sp  # noqa: E402

REL = "infra/aws/terraform/nfra-ctlpln-identity/dell2_ssm_policy.json"
iam = boto3.client("iam")
built = json.loads((ROOT / REL).read_text(encoding="utf-8"))
old = json.loads(subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:" + REL], capture_output=True, text=True, check=True).stdout)
no_ps_deny = json.loads(json.dumps(built))
for st in no_ps_deny["Statement"]:
    if st["Sid"] == "DenyShellDocuments":
        st["Resource"] = [r for r in st["Resource"] if "AWS-RunPowerShellScript" not in r]
group = sp.group_docs()
bus = {"dell1": sp.DELL1_BUS_POLICY, "dell2": sp.DELL2_BUS_POLICY}
shell = dsd.SHELL_SCRIPT_ARN
ps = "arn:aws:ssm:us-east-1::document/AWS-RunPowerShellScript"
for who in ("dell1", "dell2"):
    for label, doc in (("built", built), ("HEAD before this pass", old), ("built minus the PowerShell Deny", no_ps_deny)):
        pset = group + [json.dumps(json.loads(bus[who].read_text(encoding="utf-8"))), json.dumps(doc)]
        for what, res in (("shell-script", [shell, dsd.DAILY_RUNNER_ARN]), ("PowerShell", [ps, dsd.DAILY_RUNNER_ARN])):
            overall, per = sp.eval_pair(iam, pset, "ssm:SendCommand", res)
            print("%s %-34s %-12s -> mdpf-daily-runner: %s per-resource=%s" % (who, label, what, overall, [per[r][0] for r in res]))
