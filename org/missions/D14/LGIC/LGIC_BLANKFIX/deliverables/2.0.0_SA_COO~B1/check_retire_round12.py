"""LGIC_BLANKFIX round 12, cell BF-aa-1: the two empty Terraform roots are retired in git, with the proof that they were empty.

Reads, never writes. Last line: RETIRE ok=<bool> roots=2 absent=N state_empty=N aws_owned_zero=N remote_state_left=N
  absent             the root folder has no tracked file at HEAD (git ls-files)
  state_empty        the evidence file has 'STATE-LIST <root> count=0' (terraform state list printed, no address)
  aws_owned_zero     the evidence file has 'AWS-OWNED <root> count=0'
  remote_state_left  the evidence file has 'REMOTE-STATE <root> s3://<bucket>/<key> LEFT' (the backend object stays: Andrew's act)
Evidence file: org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.7.0_AE_CloudOps~DELL1/RETIRE_EVIDENCE_round12.md
"""
import os
import re
import subprocess
import sys

ROOTS = ("canonical-schwab-si2-schedule", "opal-assets-absence")
EVIDENCE = "org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.7.0_AE_CloudOps~DELL1/RETIRE_EVIDENCE_round12.md"


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip() or os.getcwd()


def main():
    root = repo_root()
    absent = 0
    for r in ROOTS:
        out = subprocess.run(["git", "-C", root, "ls-files", "infra/aws/terraform/%s" % r], capture_output=True, text=True)
        tracked = [ln for ln in out.stdout.splitlines() if ln.strip()]
        print("ROOT %s tracked_files=%d" % (r, len(tracked)))
        if out.returncode == 0 and not tracked:
            absent += 1
    try:
        with open(os.path.join(root, *EVIDENCE.split("/")), "r", encoding="utf-8") as fh:
            ev = fh.read()
    except OSError:
        ev = ""
        print("EVIDENCE absent: %s" % EVIDENCE)
    state_empty = sum(1 for r in ROOTS if re.search(r"^STATE-LIST %s count=0\b" % re.escape(r), ev, re.M))
    owned_zero = sum(1 for r in ROOTS if re.search(r"^AWS-OWNED %s count=0\b" % re.escape(r), ev, re.M))
    left = sum(1 for r in ROOTS if re.search(r"^REMOTE-STATE %s s3://\S+ LEFT\b" % re.escape(r), ev, re.M))
    ok = absent == len(ROOTS) and state_empty == len(ROOTS) and owned_zero == len(ROOTS) and left == len(ROOTS)
    print("RETIRE ok=%s roots=%d absent=%d state_empty=%d aws_owned_zero=%d remote_state_left=%d"
          % (ok, len(ROOTS), absent, state_empty, owned_zero, left))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
