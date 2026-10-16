#!/usr/bin/env python
"""OG-en-11 runner: upload en11_host.py, run it ONCE on the gateway host (one SSM command, Rule 12), and write W/BD49F_SERVED.json.
The host's raw answer is kept OUTSIDE the repo (argv[1], default the system temp dir) so the classification can be re-derived without a second host read.
The live commit is the deployed artifact's S3 git-ref, read before and after; the record is written only if the two are equal.
usage: python en11_run.py [raw_out_path]   (from the repository root). No retry."""
from __future__ import annotations

import datetime
import io
import json
import os
import re
import sys
import tempfile
import time

import boto3

INSTANCE = "i-07dccb1615503ac99"
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "ec2/opal-gateway/en11_host.py"
ART = "ec2/opal-gateway/opal-gateway-latest.tar.gz"
W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(tempfile.gettempdir(), "en11_raw.json")
s3 = boto3.client("s3")


def live_ref() -> str:
    return s3.head_object(Bucket=BUCKET, Key=ART)["Metadata"].get("git-ref", "")


def mask(s):
    return re.sub(r"\d{8,}", "<acct>", s) if isinstance(s, str) else s


def klass(bucket):
    if not bucket:
        return "none"
    b = mask(bucket)
    if re.search(r"(^|-)data-bd$", b) or b == "opal-data-bd":
        return "opal-data-bd"
    if re.search(r"(^|-)data-assets$", b) or b == "opal-data-assets":
        return "opal-data-assets"
    return "other"


def main():
    ref_before = live_ref()
    s3.put_object(Bucket=BUCKET, Key=KEY, Body=io.open(W + "en11_host.py", "rb").read())
    cmd = ("cd /opt/opal-gateway && rm -f /tmp/en11_host.py && aws s3 cp s3://%s/%s /tmp/en11_host.py --region us-east-1 >/dev/null && "
           "/opt/opal-gateway/.venv/bin/python /tmp/en11_host.py" % (BUCKET, KEY))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=600)["Command"]["CommandId"]
    inv = None
    for _ in range(120):
        time.sleep(4)
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    ref_after = live_ref()
    print("status=%s rc=%s stdout_chars=%d ref_before=%s ref_after=%s" % (inv["Status"], inv.get("ResponseCode"), len(so), ref_before[:10], ref_after[:10]))
    if "EN11_JSON" not in so:
        raise SystemExit("no marker in the host output; stderr tail: " + inv.get("StandardErrorContent", "")[-400:])
    io.open(RAW, "w", encoding="utf-8", newline="\n").write(so)
    doc = json.loads(so.split("EN11_JSON", 1)[1].strip())
    print(json.dumps(doc, indent=1))
    if ref_before != ref_after or not ref_after:
        raise SystemExit("the live ref moved or is unreadable during the read; nothing recorded")
    build(doc, ref_after, cid)


def build(doc, ref, cid=None):
    if "fatal" in doc:
        raise SystemExit("host failed: " + doc["fatal"][:300])
    tools = []
    roles = set()
    for t in doc.get("tools", []):
        cb = t.get("catalog_bucket")
        cls = klass(cb)
        obs = [klass(b) for b in t.get("observed_buckets", [])]
        roles.update(t.get("session_roles", []))
        note = "catalog row bucket class %s; the S3 helpers were handed %s" % (cls, ("class " + ", ".join(sorted(set(obs)))) if obs else "no bucket under that prefix")
        if cls == "none":
            note = "no source key (%s)" % (t.get("absent_reason") or t.get("code") or t.get("error") or "empty answer")
        elif obs and set(obs) != {cls}:
            note += " -- DISAGREES with the catalog row"
        tools.append({"tool": t["tool"], "bucket": mask(cb) if cb else None, "bucket_class": cls,
                      "source_prefix": t.get("source_prefix"), "partition_date": t.get("partition_date"), "rows": t.get("rows", 0), "note": note})
    classes = {t["tool"]: t["bucket_class"] for t in tools}
    if all(c == "opal-data-bd" for c in classes.values()) and len(classes) == 4:
        finding = "all four read opal-data-bd"
    else:
        finding = "; ".join("%s read %s" % (k, v) for k, v in classes.items() if v != "opal-data-bd") or "no tool answered"
    rec = {"read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_commit": ref,
           "method": ("On the gateway host, through the installed registered tools as a master_admin stand-in: client_resolve_account for firm 49financial, then the four client "
                      "tools on one Black Diamond account it returned; per tool the bucket of the first source key is the DATA_CATALOG row the context resolves for it, cross-read "
                      "against the bucket the typed_scope S3 helpers were handed; the role is the STS caller identity of the client the adapter used."),
           "role_assumed": ", ".join(sorted(roles)) if roles else "unread",
           "tools": tools, "finding": finding}
    if doc.get("finding_hint"):
        rec["finding"] = doc["finding_hint"]
    io.open(W + "BD49F_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print("WROTE BD49F_SERVED.json:", rec["finding"])


if __name__ == "__main__":
    main()
