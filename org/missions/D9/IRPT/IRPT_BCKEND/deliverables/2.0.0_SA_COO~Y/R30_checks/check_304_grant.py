#!/usr/bin/env python3
"""IB-yr-304 AC2 -- the irpt-ycharts-generate role is DECLARED one read on etf-classifications, and nothing wider.

Reads infra/aws/terraform/investor-reporting/ycharts/generate.tf as text (no terraform, no AWS call). A policy
statement is the text from one `Sid` to the next. PASS iff:
  (a) exactly ONE statement in the file names the action "dynamodb:Scan";
  (b) that statement's Action list is exactly ["dynamodb:Scan"];
  (c) its Resource names `table/etf-classifications` closed by the quote (no `/index`, no `*`), and no other
      `table/` resource;
  (d) CONTROL: the two canonical-profile statements the role already holds are still present
      (ReadCanonicalUserProfileByEmailIndexAndKey, ReadCanonicalUserProfileRow).
This is the DESIRED state only: the apply is a served act under its own never-widen halves and is not this cell's.
Base run (before the cut): FAIL -- 0 statements name dynamodb:Scan; (d) holds.
Issuer 2.0.0_SA_COO~Y, round 30. ASCII only.
"""
import os
import re
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R30_checks; the repo root is parents[8]
TF = os.path.join(ROOT, "infra", "aws", "terraform", "investor-reporting", "ycharts", "generate.tf")


def main():
    with open(TF, "r", encoding="utf-8") as fh:
        text = "\n".join(line for line in fh.read().splitlines() if not line.lstrip().startswith("#"))
    statements = re.split(r"(?=\bSid\s*=)", text)[1:]
    scans = [s for s in statements if '"dynamodb:Scan"' in s]
    control = all(('"%s"' % sid) in text for sid in
                  ("ReadCanonicalUserProfileByEmailIndexAndKey", "ReadCanonicalUserProfileRow"))
    if len(scans) != 1 or not control:
        print("FAIL: %d statements name dynamodb:Scan (need exactly 1); canonical-profile control %s"
              % (len(scans), control))
        return 1
    block = scans[0]
    action = re.search(r"Action\s*=\s*\[([^\]]*)\]", block)
    actions = re.findall(r'"([^"]+)"', action.group(1)) if action else []
    tables = re.findall(r'table/([^"\s]*)"', block)
    if actions == ["dynamodb:Scan"] and tables == ["etf-classifications"]:
        print("PASS: one Scan statement on table etf-classifications only")
        return 0
    print("FAIL: the Scan statement carries actions %r and table resources %r" % (actions, tables))
    return 1


if __name__ == "__main__":
    sys.exit(main())
