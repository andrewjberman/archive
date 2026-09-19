#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-12 third pass -- ARM (e)'s ACT: apply the 6 roots the packet signs (K-CODE x 6), and nothing else.

Packet NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-12.md, blob 9d273fb8517a00288ec13d8dd0814a47af8782fa; halves COO @71d5098fd9, CTO
@f62dd3e5bb. Run under ledger irpt-bckend-ib-rtf-12-apply (sentinel committed before this runs).

  PRE-APPLY (packet section 9) -- EVERY check must hold before ANY apply; a single miss applies NOTHING:
    - both halves at HEAD naming the packet blob (2 of 2); the packet blob at HEAD == the worktree == the signed blob;
    - every built artifact the LATEST at its built sha (the build-store version == the packet's BUILT version, its
      content-sha256 == the built sha), 6 of 6;
    - per root (7): init + plan -out=<planfile> with the vendored terraform; canonical digest == packet section 4;
      0 to destroy; each code-carrying update == its function's built sha; ycharts "No changes".
  APPLY: `.tools/safe-apply.sh -chdir=<root> apply -input=false -no-color <THAT planfile>` for the 6 roots that carry a
    change, in packet order -- the bytes applied are the bytes digested; ycharts (0 changes, S102) is not applied.
    The first failure STOPS the loop (NEVER-2: finish or roll back in-session; this script names which roots landed).
  POST-APPLY: per root, a fresh plan must read "No changes." (0-diff), 7 of 7.
Prints no credential. Writes IB-rtf-12_apply_output.txt beside itself.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import subprocess
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(WS, ".tools"))
from git_bash_resolver import bash_argv  # noqa: E402

OUTPUT_PATH = os.path.join(HERE, "IB-rtf-12_apply_output.txt")
TF = os.path.join(WS, ".tools", "terraform.exe")
TF_ROOT = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting")
PLAN_DIR = os.path.join(WS, ".scratch", "plans_apply12")
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-12.md"
PACKET_BLOB = "9d273fb8517a00288ec13d8dd0814a47af8782fa"
HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-12_RAW_KEYS_STAGED.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-12_RAW_KEYS_STAGED.md",
}
BUILT = {  # function -> (built sha256, build-store version), packet section 1
    "irpt-directory-search": ("PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=", "DOwCkAXXw1oLuzL_yzf2AqNJ0v.WnYDF"),
    "irpt-status": ("O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=", "z8VnRXEPFTioTwjwWlR_TCCQYiqU6mmV"),
    "irpt-holdings": ("uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=", "U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg"),
    "irpt-narrative": ("o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8=", "jM9scOJ005ovgidfDS3DBRHRmjvLzUwn"),
    "irpt-export-render": ("9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=", "dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH"),
    "irpt-performance-adapter": ("IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=", "38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF"),
}
ADDR = {  # the one code-carrying address per root -> its function
    "module.irpt_directory_search.aws_lambda_function.this": "irpt-directory-search",
    "module.irpt_status.aws_lambda_function.this": "irpt-status",
    "module.irpt_holdings.aws_lambda_function.this": "irpt-holdings",
    "module.irpt_narrative.aws_lambda_function.this": "irpt-narrative",
    "module.irpt_export_render.aws_lambda_function.this": "irpt-export-render",
    "module.irpt_performance_adapter.aws_lambda_function.this": "irpt-performance-adapter",
}
EXPECTED = {  # packet section 4, in apply order
    "directory": "d26db7c034ca5461325881af8a70c66790aab8b1f592112ed9f00170eed0cadc",
    "ops": "82b6c8efa3ce899dbc6621d160b8e668beae5d7dbd687bf7b17bb7852fa30b75",
    "holdings": "9635d3b90fdb76daf49f124bfe591b7a890a54e4cf928537ea79879ae47d331a",
    "narrative": "a292e3786a24963e2e0426b0b4698311972c2b68ea0029b5af9f7ef093f1d9c9",
    "export": "328dab19b150d19a9b8df1d54041901a1aeaeb8d0f98bb9cc48aec7997c12425",
    "performance": "3ab3ce3d3b266411dbc00496e260fef59bb51a9a6cf810412df7261b5b736cff",
    "ycharts": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
}
APPLY_ROOTS = ["directory", "ops", "holdings", "narrative", "export", "performance"]
LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=120)
    return out.returncode, out.stdout


def tf_env() -> dict:
    env = dict(os.environ, TF_IN_AUTOMATION="1", AWS_REGION="us-east-1",
               TF_PLUGIN_CACHE_DIR=os.path.join(WS, ".scratch", "tf-plugin-cache"))
    os.makedirs(env["TF_PLUGIN_CACHE_DIR"], exist_ok=True)
    return env


def tf(root: str, *args: str, timeout: int = 1200) -> subprocess.CompletedProcess:
    return subprocess.run([TF, "-chdir=" + os.path.join(TF_ROOT, root), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=tf_env(), timeout=timeout)


def plan(root: str, pf: str) -> tuple[bool, str, list, str]:
    i = tf(root, "init", "-input=false", "-no-color", timeout=900)
    if i.returncode != 0:
        return False, "init rc %d: %s" % (i.returncode, (i.stderr or i.stdout)[-300:].replace("\n", " ")), [], ""
    p = tf(root, "plan", "-input=false", "-no-color", "-out=" + pf)
    if p.returncode != 0:
        return False, "plan rc %d: %s" % (p.returncode, (p.stderr or p.stdout)[-300:].replace("\n", " ")), [], ""
    line = next((ln.strip() for ln in p.stdout.splitlines() if ln.startswith("Plan:") or "No changes." in ln), "?")
    j = json.loads(tf(root, "show", "-json", pf, timeout=600).stdout)
    rcs = [c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]]
    canon = [{"address": c["address"], "actions": c["change"]["actions"], "before": c["change"].get("before"),
              "after": c["change"].get("after")} for c in rcs]
    return True, line, rcs, hashlib.sha256(json.dumps(canon, sort_keys=True).encode("utf-8")).hexdigest()


def precheck() -> bool:
    emit("PRE-APPLY -- every check must hold before any apply (packet section 11)")
    ok = True
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    _, wt = git("hash-object", PACKET_REL)
    pk = rc == 0 and head.strip() == PACKET_BLOB == wt.strip()
    ok &= pk
    emit("  packet blob at HEAD %s, worktree %s, signed %s -> %s" % (head.strip(), wt.strip(), PACKET_BLOB, "EQUAL" if pk else "DIFFERS"))
    n = 0
    for who, path in HALVES.items():
        rc, text = git("show", "HEAD:" + path)
        hit = rc == 0 and PACKET_BLOB in text
        n += hit
        emit("  %s half at HEAD (%s): names the blob=%s" % (who, path, hit))
    ok &= n == 2
    emit("  halves: %d of 2" % n)
    s3c = boto3.client("s3", region_name="us-east-1")
    n_art = 0
    for fn, (sha, ver) in BUILT.items():
        h = s3c.head_object(Bucket="opal-313476888478-lambda-artifacts", Key="investor-reporting/%s.zip" % fn)
        meta = (h.get("Metadata") or {}).get("content-sha256")
        a_ok = h.get("VersionId") == ver and meta == sha
        n_art += a_ok
        emit("  built artifact %-26s latest version %s content-sha256 %s -> %s" % (fn, h.get("VersionId"), meta, "EQUAL" if a_ok else "DIFFERS"))
    ok &= n_art == len(BUILT)
    emit("  built artifacts the latest at their built sha: %d of %d" % (n_art, len(BUILT)))
    os.makedirs(PLAN_DIR, exist_ok=True)
    for root, want in EXPECTED.items():
        pf = os.path.join(PLAN_DIR, root + ".tfplan")
        good, line, rcs, digest = plan(root, pf)
        destroys = sum("delete" in c["change"]["actions"] for c in rcs)
        code = []
        for c in rcs:
            if c["type"] == "aws_lambda_function" and "update" in c["change"]["actions"]:
                b, a = c["change"]["before"] or {}, c["change"]["after"] or {}
                if b.get("source_code_hash") != a.get("source_code_hash"):
                    code.append((c["address"], a.get("source_code_hash")))
        code_ok = all(addr in ADDR and BUILT[ADDR[addr]][0] == h2 for addr, h2 in code) and len(code) == (0 if root == "ycharts" else 1)
        r = good and digest == want and destroys == 0 and code_ok
        ok &= r
        emit("  %-11s %s | destroy %d | code changes %s | canonical digest %s -> %s" % (
            root, line, destroys, code or "none", digest, "EQUAL" if digest == want else "DIFFERS from %s" % want))
    emit("PRE-APPLY: %s" % ("ALL HOLD -- applying" if ok else "A CHECK FAILED -- NOTHING APPLIED (STOP)"))
    return ok


def apply_all() -> list:
    emit("")
    emit("APPLY -- .tools/safe-apply.sh per root, the SAVED planfile (the bytes digested above)")
    landed = []
    env = dict(tf_env(), OPAL_AGENT_SERIAL=os.environ.get("OPAL_AGENT_SERIAL", ""))
    emit("  ycharts: 0 changes (S102, deferred) -- not applied; its post-apply plan is read below")
    for root in APPLY_ROOTS:
        pf = os.path.join(PLAN_DIR, root + ".tfplan").replace("\\", "/")
        chdir = "infra/aws/terraform/investor-reporting/" + root
        t0 = now()
        p = subprocess.run(bash_argv(".tools/safe-apply.sh", "-chdir=" + chdir, "apply", "-input=false", "-no-color", pf),
                           cwd=WS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=1800)
        summary = next((ln.strip() for ln in (p.stdout or "").splitlines() if ln.startswith("Apply complete!")), None)
        emit("  %-11s %s -> %s rc=%d %s" % (root, t0, now(), p.returncode, summary or "NO 'Apply complete!' LINE"))
        if p.returncode != 0 or not summary:
            tail = ((p.stderr or "") + (p.stdout or ""))[-1200:]
            emit("  APPLY FAILED on %s -- STOP. Landed before it: %s. NEVER-2: finish or roll back in-session." % (root, landed or "none"))
            for ln in tail.splitlines():
                emit("    | " + ln)
            return landed + ["FAILED:" + root]
        landed.append(root)
    emit("  applied: %d of %d" % (len(landed), len(APPLY_ROOTS)))
    return landed


def post() -> bool:
    emit("")
    emit("POST-APPLY -- a fresh plan per root must read 'No changes.' (0-diff)")
    n = 0
    for root in EXPECTED:
        pf = os.path.join(PLAN_DIR, root + ".post.tfplan")
        good, line, rcs, _ = plan(root, pf)
        zero = good and not rcs
        n += zero
        emit("  %-11s %s | changes %d -> %s" % (root, line, len(rcs), "0-DIFF" if zero else "NOT 0-DIFF: %s" % [c["address"] for c in rcs]))
    emit("  0-diff: %d of %d" % (n, len(EXPECTED)))
    return n == len(EXPECTED)


def main() -> int:
    emit("IB-rtf-12 ARM (e) APPLY -- run at %s as %s -- worktree HEAD %s" % (
        now(), boto3.client("sts").get_caller_identity()["Arn"], git("rev-parse", "HEAD")[1].strip()))
    emit("")
    rc = 1
    if precheck():
        landed = apply_all()
        if len(landed) == len(APPLY_ROOTS):
            rc = 0 if post() else 1
    emit("")
    emit("APPLY RESULT: %s" % ("6 of 6 applied, 0-diff 7 of 7" if rc == 0 else "NOT COMPLETE -- see above"))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
