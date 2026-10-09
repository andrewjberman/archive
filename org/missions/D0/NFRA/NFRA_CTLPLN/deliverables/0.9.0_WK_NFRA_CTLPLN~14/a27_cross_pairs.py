"""AMENDMENT 27 control: which documents each Dell may send to mdpf-daily-runner besides the shell-script document (read-only simulation).

IAM authorises ssm:SendCommand against the document and the instance separately, so an Allow that names the instance for the shell document also
admits any document another Allow names, sent to that instance. This prints the decision for three such pairs, for both users, with the policies as built.
Run from the worktree root: python <this file>
"""
import sys
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "nfra-ctlpln-identity" / "tests"))
import derive_ssm_documents as dsd  # noqa: E402
import simulate_policy as sp  # noqa: E402

iam = boto3.client("iam")
sets = sp.user_sets()
pairs = (
    ("irpt-ycharts-run -> mdpf", [dsd.DAILY_RUNNER_ARN, dsd.doc_arn("irpt-ycharts-run")]),
    ("irpt-ycharts-deploy -> mdpf", [dsd.DAILY_RUNNER_ARN, dsd.doc_arn("irpt-ycharts-deploy")]),
    ("a group-Allow document -> mdpf", [dsd.DAILY_RUNNER_ARN, dsd.send_grant()["document_arns"][0]]),
)
for who in ("dell1", "dell2"):
    for label, res in pairs:
        overall, per = sp.eval_pair(iam, sets[who], "ssm:SendCommand", res)
        print(who, label, overall, [per[r][0] for r in res])
