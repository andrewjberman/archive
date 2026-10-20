"""TO-APPLY-MODELGRANT G4: send host_g4.sh (read only) to the YCharts runner host through SSM and print its closed output.

The script is a shell file (aws CLI, gzip, python3 -m json.tool): no code is inlined or written on the host. The output is also written to G4_OUTPUT_r2.txt.
"""
from __future__ import annotations

import time
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"


def main():
    ec2 = boto3.client("ec2", region_name=REGION)
    ssm = boto3.client("ssm", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    if len(ids) != 1:
        raise SystemExit("STOP: running irpt-ycharts-runner count %d" % len(ids))
    script = (HERE / "host_g4.sh").read_text(encoding="ascii")
    cid = ssm.send_command(InstanceIds=ids, DocumentName="AWS-RunShellScript", Comment="MODELGRANT G4 read only", Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    out = ""
    for _ in range(60):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=ids[0])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            out = "status=%s\n%s" % (inv["Status"], inv.get("StandardOutputContent", ""))
            break
    print(out)
    (HERE / "G4_OUTPUT_r2.txt").write_text(out, encoding="ascii", errors="replace", newline="\n")


if __name__ == "__main__":
    main()
