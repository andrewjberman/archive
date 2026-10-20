#!/usr/bin/env python
"""MP-pd-7: the act, in supervised steps (run from the repository root; each step prints its verdict and exits non-zero on a STOP).
  python mp_pd7_act.py gate          both halves SIGNED at HEAD on the ask's sha256 and none refused, the ask unchanged, the deadline not passed, the live release equal to LIVE_BASE (read now)
  python mp_pd7_act.py plan          re-read the live release (second read), build the PLAN with -out (scratch), require exactly "0 to add, 1 to change, 0 to destroy" on the one function
  python mp_pd7_act.py apply         ONE safe-apply of that saved plan; record the start/stop times
  python mp_pd7_act.py post          the post-apply reads: CodeSha256, the two no-header invokes, the code zip downloaded and compared per member with the package built here
  python mp_pd7_act.py rollback      the rollback: the old handler laid in the working tree (uncommitted), plan, safe-apply, restore
Counts, hashes and times only; no account number, ARN or presigned URL is written."""
from __future__ import annotations

import glob
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import zipfile

import boto3

M = "org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.7.0_AE_CloudOps~NFRA1/"
SCR = "C:/tmp/ap50_scratch/mp/"
ASK_SHA16 = "f0098d2b67ab"
LIVE_BASE, LAMBDA_COMMIT, OLD_COMMIT = "13917ef993207bee6b8df0124eec5444da4d62cd", "f3774ac1df8", "30d9b99758d"
DEADLINE = "2026-10-21T05:30:00Z"
TF_DIR = "infra/aws/terraform/opal-gateway"
L = "infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
FN, TARGET = "mcportal-grant-writer-lambda", "aws_lambda_function.mcportal_grant_writer"
step = sys.argv[1]


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True)


def live_release():
    return json.load(io.open("infra/aws/ec2/EC2_MANIFEST.json", encoding="utf-8"))["services"]["opal-gateway"]["deployed_commit"]


def stop(msg):
    print("STOP: " + msg)
    sys.exit(3)


def market_root():
    sys.path.insert(0, os.getcwd())
    from lib.opal_naming import address
    return address("sharepoint", "transcripts", "bronze", "market_update", "date=X")[:-len("date=X")]


def tf(*args, out=None):
    cmd = ["terraform", "-chdir=" + TF_DIR] + list(args)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if out:
        io.open(out, "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


def members(zpath):
    with zipfile.ZipFile(zpath) as z:
        return {i.filename: hashlib.md5(z.read(i.filename)).hexdigest() for i in z.infolist() if not i.filename.endswith("/")}


if step == "gate":
    half_cto = sorted(glob.glob("org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_MP-pd-7_*.md"))
    half_coo = sorted(glob.glob("org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/NEVER_WIDEN_HALF_COO_MP-pd-7_*.md"))
    ok = True
    for who, files in (("CTO", half_cto), ("COO", half_coo)):
        if not files:
            print("%s half: ABSENT" % who)
            ok = False
            continue
        t = io.open(files[-1], encoding="utf-8").read()
        refused = bool(re.search(r"(?i)\bREFUSED\b", t)) and not re.search(r"(?i)\bSIGNED\b", t)
        signed = bool(re.search(r"(?i)\bSIGNED\b", t)) and ASK_SHA16 in t
        print("%s half: %s (SIGNED at the ask's sha256 prefix: %s; refused: %s)" % (who, os.path.basename(files[-1]), signed, refused))
        ok = ok and signed and not refused
    ask_sha = hashlib.sha256(open(M + "NEVER_WIDEN_ASK_MP-pd-7.md", "rb").read()).hexdigest()
    print("ask sha256 prefix %s (signed %s): %s" % (ask_sha[:12], ASK_SHA16, "unchanged" if ask_sha.startswith(ASK_SHA16) else "CHANGED"))
    lr = live_release()
    print("live release now %s (LIVE_BASE %s): %s; now %s, deadline %s" % (lr[:10], LIVE_BASE[:10], "equal" if lr == LIVE_BASE else "DIFFERS", now(), DEADLINE))
    ok = ok and ask_sha.startswith(ASK_SHA16) and lr == LIVE_BASE and now() < DEADLINE
    print("GATE: %s" % ("OPEN" if ok else "CLOSED"))
    sys.exit(0 if ok else 3)

if step == "plan":
    if live_release() != LIVE_BASE:
        stop("the live release differs from LIVE_BASE at the second read")
    if git("diff", "--quiet", LAMBDA_COMMIT, "HEAD", "--", L).returncode != 0:
        stop("the Lambda directory is not byte-equal to LAMBDA_COMMIT")
    rc, out = tf("plan", "-target=" + TARGET, "-lock=false", "-no-color", "-input=false", "-out=" + SCR + "act.tfplan", "-var", "market_update_s3_root=" + market_root(), out=SCR + "act_plan.txt")
    m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out)
    changed = re.findall(r"# (\S+) will be (updated in-place|created|destroyed|replaced)", out)
    print("plan rc=%s: %s; resources %s" % (rc, m.group(0) if m else "NO PLAN LINE", changed))
    if rc != 0 or not m or m.groups() != ("0", "1", "0") or changed != [(TARGET, "updated in-place")]:
        stop("the plan is not exactly the one in-place update of the one function")
    print("PLAN OK")

if step == "apply":
    t0 = now()
    t_start = time.monotonic()
    env = dict(os.environ, HALT_ACK="1", AGENT_NAME="0.7.0_AE_CloudOps~NFRA1")
    r = subprocess.run(["bash", ".tools/safe-apply.sh", "-chdir=" + TF_DIR, "apply", "-input=false", "-no-color", SCR + "act.tfplan"], capture_output=True, text=True, env=env)
    secs = round(time.monotonic() - t_start, 1)
    io.open(SCR + "act_apply.txt", "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
    m = re.search(r"Apply complete! Resources: (\d+) added, (\d+) changed, (\d+) destroyed", r.stdout)
    rec = {"apply_started_utc": t0, "apply_finished_utc": now(), "apply_seconds": secs, "rc": r.returncode, "apply_result": m.group(0) if m else "NO APPLY LINE"}
    io.open(M + "MP-pd-7_APPLY.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print(json.dumps(rec))
    sys.exit(0 if (r.returncode == 0 and m and m.groups() == ("0", "1", "0")) else 3)

if step in ("post", "post_quiet"):
    lam = boto3.client("lambda", region_name="us-east-1")
    fn = lam.get_function(FunctionName=FN)
    cfg = fn["Configuration"]
    zp = SCR + "after.zip"
    with urllib.request.urlopen(fn["Code"]["Location"], timeout=60) as r, open(zp, "wb") as fh:
        fh.write(r.read())
    after = members(zp)
    built = members(SCR + "new.zip")
    z = zipfile.ZipFile(zp)
    src = z.read("lambda_function.py").decode("utf-8")
    inv = {}
    for action in ("narrow", "set_person_access"):
        r = lam.invoke(FunctionName=FN, Payload=json.dumps({"action": action, "tid": "-", "oid": "-"}).encode())
        j = json.loads(r["Payload"].read().decode("utf-8", "replace"))
        inv[action] = {"status_code": r["StatusCode"], "function_error": r.get("FunctionError"), "answer": {k: j.get(k) for k in ("verdict", "reason", "record")}}
    rec = {"read_at": now(), "when": "after the apply", "code_sha256_after": cfg["CodeSha256"], "last_modified": cfg["LastModified"], "members_after": len(after), "members_built_here": len(built),
           "member_md5_equal_to_built": after == built, "members_differing": sorted(k for k in set(after) | set(built) if after.get(k) != built.get(k)),
           "lambda_function_has_WIDEN_NO_CONFIRM": "WIDEN-NO-CONFIRM" in src, "lambda_function_has_widening_signoff": "widening_signoff" in src, "invokes": inv,
           "both_refused_no_owner_header": all(v["answer"]["verdict"] == "REFUSED" and v["answer"]["reason"] == "NO-OWNER-HEADER" for v in inv.values())}
    io.open(M + "MP-pd-7_AFTER.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in ("code_sha256_after", "members_after", "member_md5_equal_to_built", "members_differing", "lambda_function_has_WIDEN_NO_CONFIRM", "lambda_function_has_widening_signoff", "both_refused_no_owner_header")}))
    print("ROLL BACK AT ONCE (python mp_pd7_act.py rollback)" if not rec["both_refused_no_owner_header"] else "POST OK" if rec["member_md5_equal_to_built"] else "POST: the deployed-bytes read missed (graded FAIL as measured; a row; the issuer decides)")
    sys.exit(0 if rec["both_refused_no_owner_header"] else 3)

if step == "rollback":
    t_start = time.monotonic()
    path = L + "/lambda_function.py"
    cur = git("show", "HEAD:" + path).stdout
    old = git("show", "%s:%s" % (OLD_COMMIT, path)).stdout
    try:
        open(path, "wb").write(old)
        rc, out = tf("plan", "-target=" + TARGET, "-lock=false", "-no-color", "-input=false", "-out=" + SCR + "rb.tfplan", "-var", "market_update_s3_root=" + market_root(), out=SCR + "rb_plan.txt")
        m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out)
        print("rollback plan rc=%s: %s" % (rc, m.group(0) if m else "NO PLAN LINE"))
        if rc != 0 or not m or m.groups() != ("0", "1", "0"):
            stop("the rollback plan is not the one in-place update")
        env = dict(os.environ, HALT_ACK="1", AGENT_NAME="0.7.0_AE_CloudOps~NFRA1")
        r = subprocess.run(["bash", ".tools/safe-apply.sh", "-chdir=" + TF_DIR, "apply", "-input=false", "-no-color", SCR + "rb.tfplan"], capture_output=True, text=True, env=env)
        io.open(SCR + "rb_apply.txt", "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
        print("rollback apply rc=%s: %s" % (r.returncode, (re.search(r"Apply complete! Resources: .*", r.stdout) or [""])[0]))
    finally:
        open(path, "wb").write(cur)
    print("rollback seconds (plan + apply): %.1f; the working tree handler restored: %s" % (time.monotonic() - t_start, git("diff", "--quiet", "HEAD", "--", path).returncode == 0))
