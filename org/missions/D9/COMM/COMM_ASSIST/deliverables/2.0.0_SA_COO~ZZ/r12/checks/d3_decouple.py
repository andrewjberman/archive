"""COMM_ASSIST CA-d-3 AC1 (round 12, CTO fold UB-e9bc @cfef5928ad): the KMS decoupling holds, read from the committed file
and the worker's saved preview plan.

PASS needs all of:
  1. chat_assist.tf at HEAD declares data "aws_kms_key" "ldo_001_transcripts" with key_id = "alias/${local.bucket}" (the STRING);
  2. chat_assist.tf at HEAD names no aws_kms_alias.* and no aws_kms_key.transcripts (the module's edge to the key resource is gone);
  3. the saved preview PLAN_D3.txt (variable "" plus the A3 foreign -var) reads "Plan: 0 to add, 2 to change, 0 to destroy";
  4. the plan carries no aws_kms_key.transcripts, no silver_reader, no second_reader address, and no LDO_KMS_KEY_ARN diff line.
Prints one line per check and RESULT: PASS|FAIL. Reads files only.
"""
import os
import re
import subprocess
import sys

TF = "infra/aws/terraform/transcripts/chat_assist.tf"
PLAN = "org/missions/D9/COMM/COMM_ASSIST/deliverables/0.7.0_AE_CloudOps~CA/PLAN_D3.txt"


def main():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8").stdout.strip()
    os.chdir(root)
    ok = True
    head = subprocess.run(["git", "show", "HEAD:" + TF], capture_output=True, text=True, encoding="utf-8").stdout
    m = re.search(r'data\s+"aws_kms_key"\s+"ldo_001_transcripts"\s*\{[^}]*key_id\s*=\s*"alias/\$\{local\.bucket\}"', head, re.S)
    print("CHECK data source keyed on the alias STRING: %s" % bool(m))
    ok &= bool(m)
    leaks = re.findall(r"aws_kms_alias\.|aws_kms_key\.transcripts", head)
    print("CHECK chat_assist.tf names no aws_kms_alias.* / aws_kms_key.transcripts: %s (found %d)" % (not leaks, len(leaks)))
    ok &= not leaks
    plan = open(PLAN, encoding="utf-8", errors="replace").read() if os.path.isfile(PLAN) else ""
    summary = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", plan)
    good_sum = bool(summary) and summary.groups() == ("0", "2", "0")
    print("CHECK plan summary 0/2/0: %s (%s)" % (good_sum, summary.group(0) if summary else "no plan file or no summary"))
    ok &= good_sum
    bad = [t for t in ("aws_kms_key.transcripts", "silver_reader", "second_reader") if re.search(r"#\s+\S*" + re.escape(t), plan)]
    env_diff = re.search(r"[~+-]\s+\"?LDO_KMS_KEY_ARN\"?\s*=", plan)
    print("CHECK plan has no key/reader address: %s %s" % (not bad and bool(plan), bad))
    print("CHECK plan has no LDO_KMS_KEY_ARN diff: %s" % (not env_diff and bool(plan)))
    ok &= bool(plan) and not bad and not env_diff
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
