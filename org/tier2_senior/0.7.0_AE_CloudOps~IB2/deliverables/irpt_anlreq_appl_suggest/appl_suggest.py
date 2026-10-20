"""IRPT_ANLREQ TO-READ-APPL-SUGGEST (applier 0.7.0_AE_CloudOps~IB2): R1 to R3, READ ONLY.

  python appl_suggest.py     prints the lines and writes A_APPL_SUGGEST.txt beside this file

R1 and R2 read the resident journal in two windows (one read-only SSM script each) and quote only the closed IRPT_RESIDENT_SUGGEST and IRPT_RESIDENT_KIMI lines.
R3 describes the advisory's secret (never get-secret-value) and simulates the resident role against its ARN. No secret value is read.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
SECRET = "astn/kimi/api-key"
lines = []
REDACT = [(re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}"), "<redacted>"), (re.compile(r"https?://\S+"), "<redacted>"), (re.compile(r"eyJ[A-Za-z0-9_-]{10,}"), "<redacted>")]


def red(s):
    for pat, rep in REDACT:
        s = pat.sub(rep, s)
    return s


def instance():
    ec2 = boto3.client("ec2", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    return [i for x in r["Reservations"] for i in x["Instances"]][0]


def window(tag, since, until):
    inst = instance()
    ssm = boto3.client("ssm", region_name=REGION)
    script = "\n".join([
        "set -u", "J=$(mktemp)",
        "journalctl -u irpt-analysis-resident.service --since '%s' --until '%s' --no-pager -o short-iso -q > \"$J\" 2>/dev/null" % (since, until),
        "echo \"RAW N first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\") resolve=$(grep -c IRPT_RESIDENT_RESOLVE \"$J\" || true)\"",
        "grep -E 'IRPT_RESIDENT_SUGGEST|IRPT_RESIDENT_KIMI' \"$J\" | cut -c1-400 | sed 's/^/RAW L /'",
        "rm -f \"$J\""]) + "\n"
    cid = ssm.send_command(InstanceIds=[inst["InstanceId"]], DocumentName="AWS-RunShellScript", Comment="APPL-SUGGEST %s journal read-only" % tag, Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    out = ""
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=inst["InstanceId"])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            out = inv.get("StandardOutputContent", "")
            break
    m = re.search(r"RAW N first=(\S*) last=(\S*) scanned=(\d+) resolve=(\d+)", out)
    if not m:
        lines.append("%s DENIED-OR-ERROR unparsed" % tag)
        return False
    ls = [red(ln[6:]) for ln in out.splitlines() if ln.startswith("RAW L ")]
    sug = [x for x in ls if "IRPT_RESIDENT_SUGGEST" in x]
    kim = [x for x in ls if "IRPT_RESIDENT_KIMI" in x]
    lines.append("%s window=%s..%s scanned=%s suggest=%s kimi=%d lines resolve=%s" % (tag, m.group(1), m.group(2), m.group(3), ("%d line(s)" % len(sug)) if sug else "none", len(kim), m.group(4)))
    for x in sug + kim:
        lines.append("%sL %s" % (tag, red(x.split(": ", 1)[-1])[:380] if ": " in x else x[:380]))
    return True


def r3():
    sm, iam = boto3.client("secretsmanager", region_name=REGION), boto3.client("iam", region_name=REGION)
    try:
        d = sm.describe_secret(SecretId=SECRET)
        present, changed, deleted, arn = "present", d["LastChangedDate"].strftime("%Y-%m-%dT%H:%M:%SZ"), "yes" if d.get("DeletedDate") else "no", d["ARN"]
        rot = d.get("RotationEnabled", False)
    except Exception as e:  # noqa: BLE001
        lines.append("R3 secret=ERROR %s" % type(e).__name__)
        return False
    inst = instance()
    prof = inst["IamInstanceProfile"]["Arn"].rsplit("/", 1)[-1]
    role = iam.get_instance_profile(InstanceProfileName=prof)["InstanceProfile"]["Roles"][0]
    r = iam.simulate_principal_policy(PolicySourceArn=role["Arn"], ActionNames=["secretsmanager:GetSecretValue"], ResourceArns=[arn])["EvaluationResults"][0]
    stm = ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"
    lines.append("R3 secret=%s changed=%s deleted=%s role=%s get_secret_value=%s matched=%s rotation=%s" % (present, changed, deleted, role["RoleName"], "allowed" if r["EvalDecision"] == "allowed" else "denied(%s)" % r["EvalDecision"], stm, rot))
    return True


if __name__ == "__main__":
    n = 0
    for f in (lambda: window("R1", "2026-10-20 02:03:30", "2026-10-20 02:06:30"), lambda: window("R2", "2026-10-20 02:33:00", "2026-10-20 02:34:30"), r3):
        try:
            n += 1 if f() else 0
        except Exception as e:  # noqa: BLE001
            lines.append("READ DENIED-OR-ERROR %s" % type(e).__name__)
    lines.append("READS-DONE %d of 3 answered" % n)
    text = "\n".join(lines) + "\n"
    (HERE / "A_APPL_SUGGEST.txt").write_text(text, encoding="ascii", errors="replace", newline="\n")
    print(text)
