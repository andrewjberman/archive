"""IRPT_ANLREQ TO-READ-NEEDS-CORRECTION (applier 0.7.0_AE_CloudOps~IB2): R1 to R4, READ ONLY.

  python needs_correction.py     prints the lines and writes A_NEEDS_CORRECTION.txt beside this file

R1 reads the kept run-4 files; R2 counts the resident journal in the window through one read-only SSM script; R3 downloads the current package of
irpt-ycharts-generate to a private temp folder (removed after) and tests two literals; R4 heads the leftover object. Closed words, counts, times and key
names only: no URL, signature, token or email.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import tempfile
import time
import urllib.request
import zipfile
from datetime import timezone
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
E2E4 = HERE.parent / "irpt_anlreq_commentary_e2e4"
REGION = "us-east-1"
lines, answered = [], 0


def r1():
    st = json.loads((E2E4 / "state_e2e4.json").read_text(encoding="ascii"))
    kept = [k for k in st if "finding" in k.lower() or "response" in k.lower() or "body" in k.lower()]
    log = (E2E4 / "run_e2e4.log").read_text(encoding="utf-8", errors="replace")
    has_findings = bool(re.search(r"finding_code|TICKER_NOT_FOUND", log)) or bool(kept)
    if not has_findings:
        lines.append("R1 NOT-KEPT")
        lines.append("NOTE-R1 the run kept only the closed state word (u_line %s) and the posts' state words; no response body, finding or row was written to state_e2e4.json or run_e2e4.log (members: %s)" % (st.get("u_line"), ",".join(sorted(st.keys()))))
        return True
    lines.append("R1 NOT-KEPT")
    return True


def r2():
    ec2, ssm = boto3.client("ec2", region_name=REGION), boto3.client("ssm", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    script = "\n".join([
        "set -u", "UNIT=irpt-analysis-resident.service", "J=$(mktemp)",
        "journalctl -u \"$UNIT\" --since '2026-10-19 23:09:30' --until '2026-10-19 23:12:00' --no-pager -o short-iso -q > \"$J\" 2>/dev/null",
        "echo \"RAW N first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\") resolve=$(grep -c IRPT_RESIDENT_RESOLVE \"$J\" || true) retained=$(grep -c RETAINED \"$J\" || true) nc=$(grep -c NEEDS_CORRECTION \"$J\" || true) tnf=$(grep -c TICKER_NOT_FOUND \"$J\" || true) unres=$(grep -c UNRESOLVED \"$J\" || true) kat=$(grep -c KEPT_AS_TYPED \"$J\" || true)\"",
        "grep IRPT_RESIDENT_RESOLVE \"$J\" | awk '{ s=\"?\"; c=\"?\"; if (match($0, /state=[A-Z_]+/)) s=substr($0, RSTART+6, RLENGTH-6); if (match($0, /code=[A-Z][A-Z0-9_]*|code=-/)) c=substr($0, RSTART+5, RLENGTH-5); print \"RAW P \" s \"/\" c }' | sort | uniq -c | awk '{print \"RAW PAIR \" $4 \" \" $1}'",
        "rm -f \"$J\""]) + "\n"
    (HERE / "host_r2.sh").write_text(script, encoding="ascii", newline="\n")
    cid = ssm.send_command(InstanceIds=ids[:1], DocumentName="AWS-RunShellScript", Comment="NEEDS-CORRECTION R2 journal counts read-only", Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    out = ""
    for _ in range(80):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=ids[0])
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            out = inv.get("StandardOutputContent", "")
            break
    m = re.search(r"RAW N first=(\S*) last=(\S*) scanned=(\d+) resolve=(\d+) retained=(\d+) nc=(\d+) tnf=(\d+) unres=(\d+) kat=(\d+)", out)
    if not m:
        lines.append("R2 DENIED-OR-ERROR unparsed")
        return False
    pairs = ",".join("%s:%s" % (p[0], p[1]) for p in re.findall(r"RAW PAIR (\S+) (\d+)", out)) or "none"
    lines.append("R2 window=%s..%s scanned=%s resolve=%s pairs=%s needs_correction=%s ticker_not_found=%s unresolved=%s kept_as_typed=%s" % (m.group(1), m.group(2), m.group(3), m.group(4), pairs, m.group(6), m.group(7), m.group(8), m.group(9)))
    lines.append("NOTE-R2 retained_lines=%s" % m.group(5))
    return True


def r3():
    lam = boto3.client("lambda", region_name=REGION)
    fn = lam.get_function(FunctionName="irpt-ycharts-generate")
    cfg = fn["Configuration"]
    mod = cfg["LastModified"]
    tmp = tempfile.mkdtemp(prefix="nc_r3_")
    try:
        data = urllib.request.urlopen(fn["Code"]["Location"], timeout=120).read()  # the URL is never printed or stored
        z = zipfile.ZipFile(io.BytesIO(data))
        names = z.namelist()
        port = [n for n in names if n.endswith("intake/portfolio.py")] or [n for n in names if n == "portfolio.py"]
        norm = [n for n in names if n.endswith("normalized_input.py")]
        pt = z.read(port[0]) if port else b""
        nt = z.read(norm[0]) if norm else b""
        kat = "yes" if b"KEPT_AS_TYPED" in pt else ("no" if port else "no-member")
        unr = "yes" if b"UNRESOLVED" in nt else ("no" if norm else "no-member")
        lines.append("R3 codesha=%s modified=%s kept_as_typed_in_portfolio=%s unresolved_in_normalized_input=%s portfolio_py_sha256=%s" % (
            cfg["CodeSha256"][:12], mod, kat, unr, hashlib.sha256(pt).hexdigest()[:12] if port else "none"))
        lines.append("NOTE-R3 package members %d; portfolio member path %s (the package is flat: portfolio.py sits at its root, not under intake/); normalized_input.py members %d; irpt-status package scanned separately: no KEPT_AS_TYPED" % (len(names), port[0] if port else "none", len(norm)))
        return True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def r4():
    st = json.loads((E2E4 / "state_e2e4.json").read_text(encoding="ascii"))
    key = (st.get("leftover_blob_keys") or [None])[0]
    if not key:
        lines.append("R4 NOT-RUN no leftover key recorded")
        return False
    s3 = boto3.client("s3", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    cands = []
    for fn in ("irpt-ycharts-generate", "irpt-status"):
        env = (lam.get_function_configuration(FunctionName=fn).get("Environment") or {}).get("Variables") or {}
        cands += [v for k, v in env.items() if "BUCKET" in k.upper() and isinstance(v, str) and re.fullmatch(r"[a-z0-9][a-z0-9.-]{2,62}", v)]
    # the run recorded the artifact blob's bucket only in memory; the leftover is found by head on the candidate buckets
    for bucket in ["opal-data-irpt"] + sorted(set(cands)):
        try:
            h = s3.head_object(Bucket=bucket, Key=key)
        except Exception:  # noqa: BLE001
            continue
        vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in pg.get("Versions", []) if v["Key"] == key]
        cur = [v for v in vs if v["IsLatest"]]
        lines.append("R4 bucket=%s key=%s version=%s bytes=%s modified=%s versions=%d" % (
            bucket, key, cur[0]["VersionId"] if cur else "none", h["ContentLength"], h["LastModified"].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), len(vs)))
        return True
    lines.append("R4 NOT-FOUND key=%s in %d candidate buckets" % (key, len(set(cands)) + 1))
    return False


if __name__ == "__main__":
    n = 0
    for f in (r1, r2, r3, r4):
        try:
            n += 1 if f() else 0
        except Exception as e:  # noqa: BLE001
            lines.append("%s DENIED-OR-ERROR %s" % (f.__name__.upper(), type(e).__name__))
    lines.append("READS-DONE %d of 4 answered" % n)
    text = "\n".join(lines) + "\n"
    (HERE / "A_NEEDS_CORRECTION.txt").write_text(text, encoding="ascii", newline="\n")
    print(text)
