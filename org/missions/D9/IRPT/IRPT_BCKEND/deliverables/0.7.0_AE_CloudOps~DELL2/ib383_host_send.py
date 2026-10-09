"""Send one shell script to one host through SSM AWS-RunShellScript and print what came back.

Generalised from org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/live_walk/host_read.py, whose
INSTANCE is hard-coded to the ycharts resident host i-0167fd745ad906a66. IB-pr-383's seeding runs on
the mdpf-daily-runner host instead, so the instance is an argument here rather than a constant.

boto3, not the .tools/aws shim: that shim is a bash script and a python subprocess cannot exec it
(WinError 2).

Usage: python ib383_host_send.py <script-path> <instance-id> "<comment>"
Output: the SSM command id, its terminal status, stdout, and stderr when there is any.
"""
import io
import sys
import time

import boto3

TERMINAL = ("Success", "Failed", "Cancelled", "TimedOut", "Cancelling")


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    script = io.open(argv[1], "r", encoding="utf-8").read()
    instance = argv[2]
    comment = (argv[3] if len(argv) > 3 else "0.7.0_AE_CloudOps~DELL2 host send")[:100]

    ssm = boto3.client("ssm", region_name="us-east-1")
    sent = ssm.send_command(
        InstanceIds=[instance],
        DocumentName="AWS-RunShellScript",
        Comment=comment,
        Parameters={"commands": [script]},
        TimeoutSeconds=600,
    )
    cid = sent["Command"]["CommandId"]
    print("ssm %s sent to %s" % (cid, instance))
    sys.stdout.flush()

    # The runner build is minutes, not seconds; poll to the document's own timeout.
    inv = None
    for _ in range(240):
        time.sleep(5)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=instance)
        except Exception as exc:  # the invocation is not registered for a moment after send
            print("  (waiting: %s)" % type(exc).__name__)
            continue
        if inv.get("Status") in TERMINAL:
            break
    if inv is None:
        print("ERROR: no invocation came back for %s" % cid)
        return 1

    print("ssm %s status %s rc %s" % (cid, inv.get("Status"), inv.get("ResponseCode")))
    out = inv.get("StandardOutputContent") or ""
    err = inv.get("StandardErrorContent") or ""
    print(out.rstrip("\n"))
    if err.strip():
        print("--- stderr ---")
        print(err.rstrip("\n"))
    return 0 if inv.get("Status") == "Success" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
