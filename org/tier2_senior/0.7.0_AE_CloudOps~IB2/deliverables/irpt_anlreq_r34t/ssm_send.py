"""IRPT_ANLREQ TO-APPLY-R34T: send ONE shell script file to the resident host through Systems Manager (AWS-RunShellScript, which runs as root) and save its output.

  python ssm_send.py <script> <out_file> [--export NAME=VALUE ...] [--wait SECONDS]

The script is a file of the release (or the V2 script of the repository): its sha256 is printed and written at the top of the output file, so the bytes sent are the
bytes verified. --export puts `export NAME=VALUE` lines in front of the script text (the order sends the V2 script with V2S_WANT_ROOT set); the script bytes are
not changed. Nothing secret is printed. The output file format is the one of the earlier releases: script and sha256, command id, status, response code, stdout, stderr.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
from pathlib import Path

import boto3

REGION = "us-east-1"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--export", action="append", default=[])
    ap.add_argument("--wait", type=int, default=600)
    a = ap.parse_args(argv)
    raw = Path(a.script).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    prefix = "".join("export %s\n" % e for e in a.export)
    ec2 = boto3.client("ec2", region_name=REGION)
    ssm = boto3.client("ssm", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    if len(ids) != 1:
        print("STOP: running irpt-ycharts-runner count %d" % len(ids))
        return 2
    cid = ssm.send_command(InstanceIds=ids, DocumentName="AWS-RunShellScript", Comment=("R34T " + Path(a.script).name)[:100],
                           Parameters={"commands": [prefix + text], "executionTimeout": [str(min(a.wait, 3600))]}, TimeoutSeconds=max(a.wait, 30))["Command"]["CommandId"]
    inv = None
    t0 = time.time()
    while time.time() - t0 < a.wait + 60:
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=ids[0])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    if inv is None:
        print("STOP: no invocation read for command %s" % cid)
        return 3
    body = "script %s sha256 %s\ncommand %s\nStatus %s\nResponseCode %s\n\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (
        Path(a.script).name, sha, cid, inv["Status"], inv.get("ResponseCode"), inv.get("StandardOutputContent", ""), inv.get("StandardErrorContent", ""))
    Path(a.out).write_text(body, encoding="utf-8", newline="\n")
    print("script %s sha256 %s | command %s | status %s | response code %s | output %d bytes -> %s" % (Path(a.script).name, sha, cid, inv["Status"], inv.get("ResponseCode"), len(body), a.out))
    return 0 if inv["Status"] == "Success" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
