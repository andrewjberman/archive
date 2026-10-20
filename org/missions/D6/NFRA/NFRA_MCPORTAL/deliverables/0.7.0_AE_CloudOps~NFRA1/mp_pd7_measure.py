#!/usr/bin/env python
"""MP-pd-7 pre-act measurements, READ ONLY (get-function, a download of the function's own code zip from the presigned URL, local builds into the scratch folder, git reads). Counts, member paths and short md5 only; no content, no ARN, no account number.
  1. the deployed function: CodeSha256, LastModified, size, runtime, the layer VERSION (not the ARN), the zip's members by short md5;
  2. the NEW package: build_package.py at the working tree (Lambda directory byte-equal to LAMBDA_COMMIT), the live release read from the manifest TWICE; members by short md5; the members that differ from the deployed zip;
  3. the ROLLBACK candidate: the Lambda directory of the commit whose lambda_function.py blob equals the deployed one, built against the SAME live release in a scratch worktree; compared per member with the deployed zip, with the new package as the NEGATIVE control.
usage: python mp_pd7_measure.py <out.json> <scratch dir>   (repository root)"""
from __future__ import annotations

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

OUT, SCR = sys.argv[1:3]
os.makedirs(SCR, exist_ok=True)
FN = "mcportal-grant-writer-lambda"
L = "infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"
LAMBDA_COMMIT, LIVE_BASE = "f3774ac1df8", "13917ef993207bee6b8df0124eec5444da4d62cd"


def git(*a, cwd=None):
    return subprocess.run(["git"] + list(a), capture_output=True, cwd=cwd)


def live_release():
    m = json.load(io.open("infra/aws/ec2/EC2_MANIFEST.json", encoding="utf-8"))
    return m["services"]["opal-gateway"]["deployed_commit"]


def members(zpath):
    with zipfile.ZipFile(zpath) as z:
        return {i.filename: hashlib.md5(z.read(i.filename)).hexdigest() for i in z.infolist() if not i.filename.endswith("/")}


def diff(a, b):
    return {"only_in_first": sorted(set(a) - set(b)), "only_in_second": sorted(set(b) - set(a)), "differ": sorted(k for k in set(a) & set(b) if a[k] != b[k]), "equal": sum(1 for k in set(a) & set(b) if a[k] == b[k])}


lam = boto3.client("lambda", region_name="us-east-1")
fn = lam.get_function(FunctionName=FN)
cfg, loc = fn["Configuration"], fn["Code"]["Location"]
dep_zip = os.path.join(SCR, "deployed.zip")
with urllib.request.urlopen(loc, timeout=60) as r, open(dep_zip, "wb") as fh:          # the function's OWN code zip, own plane; the presigned URL is never written
    fh.write(r.read())
dep = members(dep_zip)
layer_ver = re.search(r":layer:[^:]+:(\d+)$", (cfg.get("Layers") or [{}])[0].get("Arn", ""))
rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "live_release_first_read": live_release(), "live_base_expected": LIVE_BASE,
       "deployed": {"code_sha256": cfg["CodeSha256"], "last_modified": cfg["LastModified"], "code_size": cfg["CodeSize"], "runtime": cfg["Runtime"], "layer_version": int(layer_ver.group(1)) if layer_ver else None,
                    "members": len(dep), "zip_sha256_16": hashlib.sha256(open(dep_zip, "rb").read()).hexdigest()[:16],
                    "lambda_function_has_WIDEN_NO_CONFIRM": b"WIDEN-NO-CONFIRM" in zipfile.ZipFile(dep_zip).read("lambda_function.py"),
                    "lambda_function_has_widening_signoff": b"widening_signoff" in zipfile.ZipFile(dep_zip).read("lambda_function.py"),
                    "lambda_function_has_set_person_access": b"set_person_access" in zipfile.ZipFile(dep_zip).read("lambda_function.py")}}


def build(workdir, tag):
    out, stage = os.path.join(SCR, tag + ".zip"), os.path.join(SCR, tag + "_stage")
    r = subprocess.run([sys.executable, os.path.join(workdir, L, "build_package.py"), "--out", out, "--stage-dir", stage], capture_output=True, text=True, cwd=workdir)
    return r.returncode, out, (r.stdout + r.stderr).strip().splitlines()[-1:]


rc, new_zip, tail = build(os.getcwd(), "new")
new = members(new_zip)
rec["new_package"] = {"build_rc": rc, "build_last_line": tail, "members": len(new), "zip_sha256_16": hashlib.sha256(open(new_zip, "rb").read()).hexdigest()[:16],
                      "lambda_function_has_WIDEN_NO_CONFIRM": b"WIDEN-NO-CONFIRM" in zipfile.ZipFile(new_zip).read("lambda_function.py"),
                      "lambda_function_has_widening_signoff": b"widening_signoff" in zipfile.ZipFile(new_zip).read("lambda_function.py"),
                      "lambda_dir_equals_LAMBDA_COMMIT": git("diff", "--quiet", LAMBDA_COMMIT, "HEAD", "--", L).returncode == 0}
rec["new_vs_deployed"] = diff(new, dep)

# the commit whose lambda_function.py equals the deployed one
want = rec["deployed"]
dep_lf = hashlib.md5(zipfile.ZipFile(dep_zip).read("lambda_function.py")).hexdigest()
match = None
for line in git("log", "--format=%h", "--", L + "/lambda_function.py").stdout.decode().split():
    blob = git("show", "%s:%s/lambda_function.py" % (line, L)).stdout
    if hashlib.md5(blob).hexdigest() == dep_lf:
        match = line
        break
rec["rollback_candidate_commit"] = match
if match:
    wt = os.path.join(SCR, "prevtree")
    git("worktree", "add", "--detach", wt, "HEAD")
    # only the handler differs between the two packages' Lambda inputs (build_package.py copies lambda_function.py from its own directory; the CURRENT build tooling, with --stage-dir, is what the Terraform build calls)
    data = git("show", "%s:%s/lambda_function.py" % (match, L)).stdout
    open(os.path.join(wt, L, "lambda_function.py"), "wb").write(data)
    rc2, prev_zip, tail2 = build(wt, "prev")
    prev = members(prev_zip)
    rec["rollback_package"] = {"built_from_lambda_commit": match, "live_release": live_release(), "build_rc": rc2, "build_last_line": tail2, "members": len(prev), "zip_sha256_16": hashlib.sha256(open(prev_zip, "rb").read()).hexdigest()[:16]}
    rec["rollback_vs_deployed"] = diff(prev, dep)
    rec["negative_control_new_vs_deployed_differs"] = bool(rec["new_vs_deployed"]["differ"] or rec["new_vs_deployed"]["only_in_first"] or rec["new_vs_deployed"]["only_in_second"])
    git("worktree", "remove", "--force", wt)
rec["live_release_second_read"] = live_release()
rec["live_release_stable_and_equals_LIVE_BASE"] = rec["live_release_first_read"] == rec["live_release_second_read"] == LIVE_BASE
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps({"deployed": {k: rec["deployed"][k] for k in ("code_sha256", "last_modified", "members", "lambda_function_has_set_person_access", "lambda_function_has_WIDEN_NO_CONFIRM")}, "new": {k: rec["new_package"][k] for k in ("build_rc", "members", "lambda_function_has_WIDEN_NO_CONFIRM", "lambda_dir_equals_LAMBDA_COMMIT")},
                  "new_vs_deployed": {k: (v if isinstance(v, int) else len(v)) for k, v in rec["new_vs_deployed"].items()}, "rollback_commit": match,
                  "rollback_vs_deployed": ({k: (v if isinstance(v, int) else len(v)) for k, v in rec["rollback_vs_deployed"].items()} if match else None), "live_stable": rec["live_release_stable_and_equals_LIVE_BASE"]}))
