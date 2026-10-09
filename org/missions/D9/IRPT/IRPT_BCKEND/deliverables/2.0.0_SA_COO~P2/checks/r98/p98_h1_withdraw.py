"""IRPT_BCKEND round 98 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- check of cell IB-pr-392: H1 WITHDRAWN before any apply (CTO msg 2621,
ruling @19c5067e12, on ~Y2 msg 2610; rescinds msg 2507). The stream mapping to the commentary Lambda and its kms:Decrypt grant are removed
from infra/aws/terraform/investor-reporting/core; IRPT_ANLREQ's I3 queue (AR-t-11) is the one trigger.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB98-1-AC1  no .tf in the core root declares an aws_lambda_event_source_mapping, names the commentary role, or grants kms:Decrypt to
              anything but what the root granted before IB-pr-388 (no `ready_consumer_stream`, no `ready_analysis`, no file
              ready_trigger.tf). Base: FAIL (IB-pr-388's ready_trigger.tf is present).
  IB98-1-AC2  `terraform fmt -check` passes on dynamodb.tf and outputs.tf. Base: PASS.
"""
import subprocess
import sys
from pathlib import Path

CORE = "infra/aws/terraform/investor-reporting/core"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB98-1"))
        sys.exit(1)

    core = root / CORE
    if cid == "IB98-1-AC1":
        if (core / "ready_trigger.tf").exists():
            fail("ready_trigger.tf still present")
        for p in sorted(core.glob("*.tf")):
            t = p.read_text(encoding="utf-8")
            for bad in ("aws_lambda_event_source_mapping", "ready_consumer_stream", "ready_analysis", "commentary"):
                if bad in t:
                    fail("%s still names %s" % (p.name, bad))
        print("OK: no event source mapping, no commentary grant in core")
    elif cid == "IB98-1-AC2":
        common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=str(root),
                                capture_output=True, text=True).stdout.strip()
        cands = [root / ".tools" / "terraform.exe"] + ([Path(common).parent / ".tools" / "terraform.exe"] if common else [])
        tf = next((str(c) for c in cands if c.is_file()), "terraform")
        p = subprocess.run([tf, "fmt", "-check", "-no-color", "dynamodb.tf", "outputs.tf"], cwd=str(core), capture_output=True, timeout=120)
        if p.returncode != 0:
            fail("fmt rc %d: %s" % (p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")[-200:]))
        print("OK: dynamodb.tf and outputs.tf formatted")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
