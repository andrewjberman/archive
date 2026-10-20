"""IRPT_ANLREQ TO-READ-PACKAGER-403 (applier 0.7.0_AE_CloudOps~IB2): R1 to R3, READ ONLY.

  python packager_403.py     prints the lines and writes A_PACKAGER_403.txt beside this file

R1 is the host read already run (ssm_r1_out.txt, host_r1.sh): its R1 line is copied in. R2 describes the gateway's authorizer and reads the authorizer Lambda's
log group for the two windows (closed words and times only). R3 reads the ticket service's users table for the subject svc-irpt-packager and the Lambda's
PACKAGE_ALLOWED_FIRMS setting (that one key only). No secret value, no POST.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
API = "7k3ed8px20"
SUBJECT = "svc-irpt-packager"
lines = []
answered = 0


def r1():
    text = (HERE / "ssm_r1_out.txt").read_text(encoding="utf-8")
    got = [ln for ln in text.splitlines() if ln.startswith("R1 members=")]
    if not got:
        lines.append("R1 DENIED-OR-ERROR no R1 line in ssm_r1_out.txt")
        return False
    lines.append(got[0].rstrip())
    return True


def ms(day, hms):
    return int(datetime.fromisoformat("%sT%s" % (day, hms)).replace(tzinfo=timezone.utc).timestamp() * 1000)


def r2():
    a = boto3.client("apigatewayv2", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    logs = boto3.client("logs", region_name=REGION)
    auths = a.get_authorizers(ApiId=API)["Items"]
    stages = a.get_stages(ApiId=API)["Items"]
    for x in auths:
        fn = x.get("AuthorizerUri", "").split(":function:")[-1].split("/")[0]
        lines.append("R2 authorizer name=%s type=%s identity_source=%s simple_responses=%s function=%s" % (x["Name"], x["AuthorizerType"], ",".join(x.get("IdentitySource", [])), x.get("EnableSimpleResponses"), fn))
    lines.append("R2 access_logging=%s (stages=%s)" % ("on" if any("AccessLogSettings" in s for s in stages) else "off", ",".join(s["StageName"] for s in stages)))
    fn = auths[0].get("AuthorizerUri", "").split(":function:")[-1].split("/")[0]
    lam.get_function_configuration(FunctionName=fn)
    group = "/aws/lambda/" + fn
    for lo, hi in (("08:02:30", "08:03:30"), ("08:57:30", "08:59:30")):
        n_all, hits = 0, []
        for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=group, startTime=ms("2026-10-20", lo), endTime=ms("2026-10-20", hi)):
            for ev in pg["events"]:
                n_all += 1
                m = ev["message"]
                t = datetime.fromtimestamp(ev["timestamp"] / 1000.0, timezone.utc).strftime("%H:%M:%S")
                if "Origin verification FAILED" in m:
                    hits.append((t, "ORIGIN_VERIFICATION_FAILED"))
        lines.append("NOTE-R2 window %s..%s log group %s holds %d events" % (lo, hi, group, n_all))
        for t, reason in hits:
            lines.append("R2 %sZ POST /package status=403 reason=%s" % (t, reason))
        if not hits:
            lines.append("R2 NOT-FOUND no origin-verification line in %s between %sZ and %sZ" % (group, lo, hi))
    lines.append("NOTE-R2 the authorizer logs print no path (path: undefined), so a line is tied to the package call by its time only; the 08:02:32Z line of the same window (a token verified for the run's synthetic login) is NOT a refusal")
    return True


def r3():
    ddb = boto3.client("dynamodb", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    cfg = lam.get_function_configuration(FunctionName="opal-ticket-api")
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    table = env.get("USERS_TABLE", "opal-users-v2")
    index = env.get("USERS_EMAIL_INDEX", "email-index")
    q = ddb.query(TableName=table, IndexName=index, KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": SUBJECT}})
    keys = [i for i in q.get("Items", []) if i.get("SK", {}).get("S") == "PROFILE"]
    g = ddb.get_item(TableName=table, Key={"PK": {"S": "USER#" + SUBJECT}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
    row = g
    if row is None and keys:
        row = ddb.get_item(TableName=table, Key={"PK": keys[0]["PK"], "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
    if row is None:
        lines.append("R3 row=absent members=- userType=- allowedFirmIds=- (table %s: index query for the subject returned %d PROFILE key(s); get-item on the subject's own PK returned none)" % (table, len(keys)))
    else:
        def closed(v):
            return isinstance(v, str) and re.fullmatch(r"[a-z]{1,16}", v) is not None

        ut =row.get("userType", {}).get("S") or row.get("role", {}).get("S")
        afi = row.get("allowedFirmIds")
        if afi is None:
            shown = "-"
        elif "L" in afi:
            shown = ",".join(sorted(x.get("S", "?") for x in afi["L"]))
        else:
            shown = (afi.get("S") or "?")
        lines.append("R3 row=present members=%s userType=%s allowedFirmIds=%s" % (",".join(sorted(row)), ut if closed(ut) else "-", shown))
    pa = env.get("PACKAGE_ALLOWED_FIRMS")
    lines.append("NOTE-R3 the Lambda's setting PACKAGE_ALLOWED_FIRMS (the source says the package principal needs no PROFILE row and is firm-bound by this setting): %s" % ("unset" if pa is None else (pa if re.fullmatch(r"[a-z0-9,]{0,80}", pa) else "<set, not a closed list>")))
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
    (HERE / "A_PACKAGER_403.txt").write_text(text, encoding="ascii", errors="replace", newline="\n")
    print(text)
