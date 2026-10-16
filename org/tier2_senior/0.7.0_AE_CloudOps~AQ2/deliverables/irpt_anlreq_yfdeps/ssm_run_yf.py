"""IRPT_ANLREQ TO-APPLY-YFDEPS (0.7.0_AE_CloudOps~AQ2): send ONE signed host script to the resident host by Systems Manager, as ec2-user.

  python ssm_run_yf.py <script.sh> <out-file> [--expect-sha256 <hex>] [--as-root]

The script bytes are sent unchanged (base64 inside the command text, decoded on the host and run as `sudo -u ec2-user bash -c`, or, with --as-root, as the Systems Manager agent's own user, root, via `bash -c`), after the
sender re-checks the file's sha256 against --expect-sha256. Polls the invocation until a terminal status. Writes <out-file>: the sha256 sent,
the command id, Status, ResponseCode, then StandardOutputContent and StandardErrorContent as returned (Systems Manager truncates each at
24000 characters; the file says so when the returned length reaches it). Prints the Status and ResponseCode. No other AWS call.
"""
from __future__ import annotations

import base64
import hashlib
import sys
import time
from pathlib import Path

REGION = "us-east-1"
INSTANCE = "i-0167fd745ad906a66"


def build_command(raw, as_root=False):
    b64 = base64.b64encode(raw).decode()
    if as_root:
        return "bash -c \"$(echo %s | base64 -d)\"" % b64
    return "sudo -u ec2-user HOME=/home/ec2-user bash -c \"$(echo %s | base64 -d)\"" % b64


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    import boto3
    script, out = Path(argv[0]), Path(argv[1])
    raw = script.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if "--expect-sha256" in argv and sha != argv[argv.index("--expect-sha256") + 1]:
        print("REFUSED: sha256 of %s is %s, not the expected value; nothing sent" % (script, sha))
        return 3
    ssm = boto3.client("ssm", region_name=REGION)
    r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", TimeoutSeconds=900,
                         Parameters={"commands": [build_command(raw, "--as-root" in argv)], "executionTimeout": ["900"]},
                         Comment="IRPT_ANLREQ TO-APPLY-YFDEPS " + script.name)
    cid = r["Command"]["CommandId"]
    print("sent %s sha256 %s command %s" % (script.name, sha, cid), flush=True)
    time.sleep(3)
    while True:
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            time.sleep(2)
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
        time.sleep(4)
    so, se = inv.get("StandardOutputContent", ""), inv.get("StandardErrorContent", "")
    note = []
    if len(so) >= 24000:
        note.append("STDOUT may be truncated at 24000 characters")
    if len(se) >= 24000:
        note.append("STDERR may be truncated at 24000 characters")
    out.write_text("script %s sha256 %s\ncommand %s\nStatus %s\nResponseCode %s\n%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n"
                   % (script.name, sha, cid, inv["Status"], inv.get("ResponseCode"), "; ".join(note), so, se), encoding="utf-8")
    print("Status %s ResponseCode %s -> %s" % (inv["Status"], inv.get("ResponseCode"), out))
    return 0 if inv["Status"] == "Success" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
