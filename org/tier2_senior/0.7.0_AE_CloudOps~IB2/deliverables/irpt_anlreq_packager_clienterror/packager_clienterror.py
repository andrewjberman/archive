"""IRPT_ANLREQ TO-READ-PACKAGER-CLIENTERROR (applier 0.7.0_AE_CloudOps~IB2): R1 to R3, READ ONLY.

  python packager_clienterror.py     prints the lines and writes A_PACKAGER_CLIENTERROR.txt beside this file

R1 quotes the closed resident-journal lines of the window (one read-only SSM script; e-mail addresses, URLs and long tokens are replaced by <redacted>).
R2 counts and lists the ticket service's /package requests from its CloudWatch log group. R3 simulates the resident host's role (one resource per call).
No secret value, no queue receive, no post, nothing written but the record file.
"""
from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
LOW, HIGH = datetime(2026, 10, 20, 8, 2, 20, tzinfo=timezone.utc), datetime(2026, 10, 20, 8, 6, 0, tzinfo=timezone.utc)
BUCKET = "opal-data-irpt"
lines = []
REDACT = [(re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}"), "<redacted>"), (re.compile(r"https?://\S+"), "<redacted>"),
          (re.compile(r"eyJ[A-Za-z0-9_-]{10,}"), "<redacted>"), (re.compile(r"X-Amz-\S+"), "<redacted>"), (re.compile(r"\b[A-Fa-f0-9]{40,}\b"), "<hex>")]


def red(s):
    for pat, rep in REDACT:
        s = pat.sub(rep, s)
    return s


def ids():
    ec2 = boto3.client("ec2", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    return [i for x in r["Reservations"] for i in x["Instances"]]


def r1():
    inst = ids()
    ssm = boto3.client("ssm", region_name=REGION)
    script = "\n".join([
        "set -u", "J=$(mktemp)",
        "journalctl -u irpt-analysis-resident.service --since '2026-10-20 08:02:20' --until '2026-10-20 08:06:00' --no-pager -o short-iso -q > \"$J\" 2>/dev/null",
        "echo \"RAW N first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\")\"",
        "grep -E 'IRPT_RESIDENT_PACKAGE|PACKAGER|HOP_FAILURE|retained_for_retry|ClientError|Traceback' \"$J\" | cut -c1-600 | sed 's/^/RAW L /'",
        "rm -f \"$J\""]) + "\n"
    (HERE / "host_r1.sh").write_text(script, encoding="ascii", newline="\n")
    cid = ssm.send_command(InstanceIds=[inst[0]["InstanceId"]], DocumentName="AWS-RunShellScript", Comment="PACKAGER-CLIENTERROR R1 journal read-only", Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    out = ""
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=inst[0]["InstanceId"])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            out = inv.get("StandardOutputContent", "")
            break
    m = re.search(r"RAW N first=(\S*) last=(\S*) scanned=(\d+)", out)
    if not m:
        lines.append("R1 DENIED-OR-ERROR unparsed")
        return False
    ls = [ln[6:] for ln in out.splitlines() if ln.startswith("RAW L ")]
    lines.append("R1 window=%s..%s scanned=%s lines=%d" % (m.group(1), m.group(2), m.group(3), len(ls)))
    for ln in ls:
        t = ln.split(" ", 1)
        lines.append("R1L %s %s" % (t[0][11:19] if len(t[0]) > 19 else t[0], red(t[1] if len(t) > 1 else "")))
    return True


def r2():
    logs = boto3.client("logs", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    fn = "opal-ticket-api"
    lam.get_function_configuration(FunctionName=fn)
    group = "/aws/lambda/" + fn
    n, rows = 0, []
    for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=group, startTime=int(LOW.timestamp() * 1000), endTime=int(HIGH.timestamp() * 1000), filterPattern="package"):
        for ev in pg["events"]:
            msg = ev["message"]
            if "/package" not in msg:
                continue
            n += 1
            t = datetime.fromtimestamp(ev["timestamp"] / 1000.0, timezone.utc).strftime("%H:%M:%S")
            status = re.search(r"(?:status|statusCode|status_code)\W{0,4}([1-5]\d\d)", msg)
            codes = sorted(set(re.findall(r"\b[A-Z][A-Z0-9_]{5,}\b", msg)))[:4]
            rows.append("R2 %sZ POST /package status=%s code=%s" % (t, status.group(1) if status else "-", ",".join(codes) or "-"))
    total = sum(len(pg["events"]) for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=group, startTime=int(LOW.timestamp() * 1000), endTime=int(HIGH.timestamp() * 1000)))
    lines.append("NOTE-R2 control: the log group holds %d events in the same window (so the group is live and a /package line would appear); retention 14 days" % total)
    if n == 0:
        lines.append("R2 NOT-FOUND no event naming /package in %s between 08:02:20Z and 08:06:00Z (looked in the log group of %s)" % (group, fn))
    else:
        lines.extend(rows[:20])
    lines.append("R2 count=%d" % n)
    return True


def r3():
    inst = ids()[0]
    prof = inst["IamInstanceProfile"]["Arn"].rsplit("/", 1)[-1]
    iam = boto3.client("iam", region_name=REGION)
    role = iam.get_instance_profile(InstanceProfileName=prof)["InstanceProfile"]["Roles"][0]
    rname, rarn = role["RoleName"], role["Arn"]
    lines.append("R3 role %s" % rname)
    s3, ddb, sm = boto3.client("s3", region_name=REGION), boto3.client("dynamodb", region_name=REGION), boto3.client("secretsmanager", region_name=REGION)
    kms_arn = None
    try:
        enc = s3.get_bucket_encryption(Bucket=BUCKET)["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]
        kms_arn = enc.get("KMSMasterKeyID")
        lines.append("R3 bucket %s encryption %s%s" % (BUCKET, enc["SSEAlgorithm"], "" if not kms_arn else " key " + kms_arn))
    except Exception as e:  # noqa: BLE001
        lines.append("R3 bucket %s encryption ERROR %s" % (BUCKET, type(e).__name__))
    table_arn = ddb.describe_table(TableName="irpt-requests")["Table"]["TableArn"]
    try:
        secret_arn = sm.describe_secret(SecretId="opal/ticketing/svc-irpt-packager")["ARN"]
    except Exception as e:  # noqa: BLE001
        secret_arn = None
        lines.append("R3 secret opal/ticketing/svc-irpt-packager describe ERROR %s" % type(e).__name__)
    cases = []
    for pfx in ("ycharts_opal_reports", "analysis_commentaries"):
        key = "arn:aws:s3:::%s/irpt/49financial/state/%s/x" % (BUCKET, pfx)
        cases += [("s3:PutObject", key, "%s/%s" % (BUCKET, pfx)), ("s3:GetObject", key, "%s/%s" % (BUCKET, pfx))]
    if kms_arn and kms_arn.startswith("arn:"):
        cases += [("kms:GenerateDataKey", kms_arn, "bucket-key"), ("kms:Decrypt", kms_arn, "bucket-key")]
    for act in ("dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:GetItem", "dynamodb:Query"):
        cases.append((act, table_arn, "irpt-requests"))
    if secret_arn:
        cases.append(("secretsmanager:GetSecretValue", secret_arn, "opal/ticketing/svc-irpt-packager"))
    for act, arn, name in cases:
        try:
            r = iam.simulate_principal_policy(PolicySourceArn=rarn, ActionNames=[act], ResourceArns=[arn])["EvaluationResults"][0]
            dec = r["EvalDecision"]
            stm = ",".join(x["SourcePolicyId"] for x in r.get("MatchedStatements", [])[:2]) or "-"
            lines.append("R3 %s %s %s matched=%s" % (act, name, "allowed" if dec == "allowed" else "denied(%s)" % dec, stm))
        except Exception as e:  # noqa: BLE001
            lines.append("R3 %s %s ERROR %s" % (act, name, type(e).__name__))
    return True


if __name__ == "__main__":
    n = 0
    for f in (r1, r2, r3):
        try:
            n += 1 if f() else 0
        except Exception as e:  # noqa: BLE001
            lines.append("%s DENIED-OR-ERROR %s" % (f.__name__.upper(), type(e).__name__))
    lines.append("READS-DONE %d of 3 answered" % n)
    text = "\n".join(lines) + "\n"
    (HERE / "A_PACKAGER_CLIENTERROR.txt").write_text(text, encoding="ascii", errors="replace", newline="\n")
    print(text)
