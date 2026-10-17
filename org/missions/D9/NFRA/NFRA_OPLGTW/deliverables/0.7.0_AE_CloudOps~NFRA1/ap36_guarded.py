#!/usr/bin/env python
"""OG-ap-36 Phase B step 7 (after the 17:21Z host OOM): run the 27-tool served harness on the gateway host UNDER A HARD GUARD, so a runaway call cannot take the host down again.
One file, two roles:
  python ap36_guarded.py <out.txt> [as_cap_mb] [harness.py]   -> the RUNNER (repository root): uploads itself to S3, runs once over SSM (Rule 12), writes the raw output
  python ap36_guarded.py --host <as_cap_mb>      -> the HOST wrapper: sets oom_score_adj 1000 (this process is the kernel's first victim), caps the address space
                                                   (a runaway allocation raises MemoryError here instead of killing the host), dumps every thread's stack every 15 s to stderr,
                                                   then runs /tmp/ap23_served_harness.py (already pulled by ap23_run_served.py) as __main__.
READ-ONLY. Counts, names and stack frames only."""
from __future__ import annotations

import faulthandler
import io
import os
import runpy
import sys
import time


def host(cap_mb: int) -> None:
    import resource                     # Linux only: imported on the host
    with open("/proc/self/oom_score_adj", "w") as fh:
        fh.write("1000")
    resource.setrlimit(resource.RLIMIT_AS, (cap_mb * 1024 * 1024, cap_mb * 1024 * 1024))
    faulthandler.dump_traceback_later(15, repeat=True, file=sys.stderr)
    sys.argv = ["/tmp/ap23_served_harness.py"]
    sys.path.insert(0, "/opt/opal-gateway")
    try:
        runpy.run_path("/tmp/ap23_served_harness.py", run_name="__main__")
    except MemoryError:
        import traceback
        print("AP36_GUARD_MEMORYERROR")
        traceback.print_exc(limit=-14, file=sys.stdout)
        sys.exit(4)


def runner(outp: str, cap_mb: int, harness: str = "") -> None:
    import boto3
    instance, bucket, key = "i-07dccb1615503ac99", "opal-313476888478-lambda-artifacts", "ec2/opal-gateway/ap36_guarded.py"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=io.open(os.path.abspath(__file__), "rb").read())
    pull = ""
    if harness:                                                    # an alternative harness: pulled over /tmp/ap23_served_harness.py
        hkey = "ec2/opal-gateway/ap36_served_harness.py"
        boto3.client("s3").put_object(Bucket=bucket, Key=hkey, Body=io.open(harness, "rb").read())
        pull = "rm -f /tmp/ap23_served_harness.py && aws s3 cp s3://%s/%s /tmp/ap23_served_harness.py --region us-east-1 >/dev/null && " % (bucket, hkey)
    cmd = ("cd /opt/opal-gateway && " + pull + "rm -f /tmp/ap36_guarded.py && aws s3 cp s3://%s/%s /tmp/ap36_guarded.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/ap36_guarded.py --host %d" % (bucket, key, cap_mb))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=900)["Command"]["CommandId"]
    inv = None
    for _ in range(300):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so, se = inv.get("StandardOutputContent", ""), inv.get("StandardErrorContent", "")
    io.open(outp, "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR (tail) ---\n%s\n" % (inv["Status"], so, se[-6000:]))
    print("status=%s stdout=%d bytes stderr=%d bytes" % (inv["Status"], len(so), len(se)))


if __name__ == "__main__":
    if "--host" in sys.argv:
        host(int(sys.argv[sys.argv.index("--host") + 1]))
    else:
        runner(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1500, sys.argv[3] if len(sys.argv) > 3 else "")
