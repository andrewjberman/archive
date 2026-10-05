"""IRPT_BCKEND round 57 (workstream ~P, issuer 2.0.0_SA_COO~P) -- S335, CTO batch 264 @f49b5958b0: a second directory refresh
schedule 10 minutes after the first (09:40 America/New_York), same target and input, plus the never-widen packet for the first
successful fire.

Usage: python <this file> <repo_root> <criterion_id>
  IB57-1-AC1  schedule.tf declares a SECOND aws_scheduler_schedule targeting module.irpt_directory_refresh.function_arn with the
              same role and the same input `kind`, expression cron(40 9 ? * MON-FRI *) in America/New_York, ENABLED; the first
              schedule (cron(30 9 ...)) is unchanged; `terraform fmt -check` passes on the file. Base: FAIL.
  IB57-1-AC2  PACKET exists with, per firm (49financial, inflection, cottonwood): bucket, the latest.json key, its current
              VersionId, LastModified, its entry count; the writer named; both branches; the rollback per key. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TF = "infra/aws/terraform/investor-reporting/directory/schedule.tf"
PACKET = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~128/S335_SECOND_FIRE_PACKET.json"
FIRMS = ("49financial", "inflection", "cottonwood")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB57-1"))
        sys.exit(1)

    if cid == "IB57-1-AC1":
        s = (root / TF).read_bytes().decode("utf-8")
        blocks = re.findall(r'resource "aws_scheduler_schedule" "(\w+)" \{(.*?)\n\}', s, re.S)
        refresh = [(n, b) for n, b in blocks if "module.irpt_directory_refresh.function_arn" in b]
        if len(refresh) != 2:
            fail("%d schedules target irpt_directory_refresh; want 2" % len(refresh))
        exprs = sorted(re.search(r'schedule_expression\s*=\s*"([^"]+)"', b).group(1) for _n, b in refresh)
        if exprs != ["cron(30 9 ? * MON-FRI *)", "cron(40 9 ? * MON-FRI *)"]:
            fail("expressions %s" % exprs)
        for n, b in refresh:
            if 'state                        = "ENABLED"' not in b and not re.search(r'state\s*=\s*"ENABLED"', b):
                fail("%s not ENABLED" % n)
            if "America/New_York" not in b or "aws_iam_role.irpt_directory_refresh_scheduler.arn" not in b or "irpt_directory_refresh" not in b:
                fail("%s lacks the zone, the scheduler role or the input kind" % n)
        r = subprocess.run(["terraform", "fmt", "-check", str(root / TF)], capture_output=True, text=True)
        if r.returncode:
            fail("terraform fmt -check: %s" % (r.stdout + r.stderr)[-200:])
        print("OK: two refresh schedules (09:30 and 09:40 ET), both ENABLED; fmt clean")
    elif cid == "IB57-1-AC2":
        p = root / PACKET
        if not p.is_file():
            fail("no %s" % PACKET)
        c = json.loads(p.read_bytes().decode("utf-8"))
        firms = {f.get("firm"): f for f in c.get("firms") or []}
        for fm in FIRMS:
            f = firms.get(fm)
            if not f or not all(f.get(k) is not None for k in ("bucket", "key", "version_id", "last_modified", "entry_count", "rollback")):
                fail("firm %s incomplete: %r" % (fm, f))
        for k in ("writer", "branches"):
            if not c.get(k):
                fail("packet lacks %r" % k)
        print("OK: packet covers %d firms with version ids, counts and rollback" % len(FIRMS))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
