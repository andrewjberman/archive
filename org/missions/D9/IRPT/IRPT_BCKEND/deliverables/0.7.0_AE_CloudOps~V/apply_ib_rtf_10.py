#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-10 fourth pass -- ARM (e)'s ACT: apply the 7 roots the packet signs, and nothing else.

Packet NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md, blob c3a44074d2dabe4292bfc648d855be4b99fe48db; halves COO @025607941e,
CTO @b6af01c2f4. Run under ledger irpt-bckend-ib-rtf-10-apply (sentinel committed before this runs).

  PRE-APPLY (packet section 11) -- EVERY check must hold before ANY apply; a single miss applies NOTHING:
    - both halves at HEAD naming the packet blob (2 of 2); the packet blob at HEAD == the worktree == the signed blob;
    - data/firm_registry.json blob at HEAD == 99b8eeb54f... (the ARN list's vintage);
    - the latest irpt-directory-search.zip version == hk9OUfwH... with content-sha256 == HOpXPDo... (K-CODE);
    - per root: init + plan -out=<planfile> with the vendored terraform; canonical digest == packet section 6;
      0 to destroy; the only code-carrying update is K-CODE's own.
  APPLY: `.tools/safe-apply.sh -chdir=<root> apply -input=false -no-color <THAT planfile>` per root, in packet order --
    the bytes applied are the bytes digested, never a re-plan. The first failure STOPS the loop (NEVER-2: the
    operator finishes or rolls back in-session; this script names which roots landed).
  POST-APPLY: per root, a fresh plan must read "No changes." (0-diff), 7 of 7.
Prints no credential. Writes IB-rtf-10_apply_output.txt beside itself.
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

OUTPUT_PATH = os.path.join(HERE, "IB-rtf-10_apply_output.txt")
TF = os.path.join(WS, ".tools", "terraform.exe")
TF_ROOT = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting")
PLAN_DIR = os.path.join(WS, ".scratch", "plans_apply")
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md"
PACKET_BLOB = "c3a44074d2dabe4292bfc648d855be4b99fe48db"
HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-10_SERVING_ROLES_GRANTED.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-10_SERVING_ROLES_GRANTED.md",
}
REGISTRY_BLOB = "99b8eeb54fb08a7ea6e4b89b64f300ee6cab3200"
KCODE_KEY = "investor-reporting/irpt-directory-search.zip"
KCODE_VERSION = "hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd"
KCODE_SHA = "HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI="
KCODE_ADDRESS = "module.irpt_directory_search.aws_lambda_function.this"
EXPECTED = {  # packet section 6, in apply order
    "directory": "0f66bef1d322a6d04916673b741ec794b86109d74e36bb313f337bc19eaad7ff",
    "ops": "a9197cc1b8bb4f796fbcff7522be08bdfab3b813814bf7b5a3a8458af8ee0e19",
    "holdings": "450a1ab86a6981a5d1269d65dfb32dbcc3442d8801a0973ab6ff96a5f12c1654",
    "narrative": "5e0e1ed7317bdacdfd8b744e52f34331b7361cedd2c8bcb13ca914e4ea96973c",
    "export": "527c2a500d1d1e32324ee6f3cc0e8d2f60b4e7357b3ae2672ae87df2f6caf80c",
    "performance": "5059fda3e68f5f5f2cd729f1d7845aaea3ee4044b5ee95cd53371d1c3ce60d37",
    "ycharts": "063b9919d876ea86f8f4d3831d30ff8aa853070438b107e67721cfe12c212aeb",
}
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
    rc, reg = git("rev-parse", "--verify", "--quiet", "HEAD:data/firm_registry.json")
    r_ok = rc == 0 and reg.strip() == REGISTRY_BLOB
    ok &= r_ok
    emit("  registry blob at HEAD %s vs %s -> %s" % (reg.strip(), REGISTRY_BLOB, "EQUAL" if r_ok else "DIFFERS"))
    h = boto3.client("s3", region_name="us-east-1").head_object(Bucket="opal-313476888478-lambda-artifacts", Key=KCODE_KEY)
    meta = (h.get("Metadata") or {}).get("content-sha256")
    k_ok = h.get("VersionId") == KCODE_VERSION and meta == KCODE_SHA
    ok &= k_ok
    emit("  K-CODE artifact latest version %s content-sha256 %s -> %s" % (h.get("VersionId"), meta, "EQUAL" if k_ok else "DIFFERS"))
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
        code_ok = all(addr == KCODE_ADDRESS and h2 == KCODE_SHA for addr, h2 in code) and len(code) == (1 if root == "directory" else 0)
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
    for root in EXPECTED:
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
    emit("  applied: %d of %d" % (len(landed), len(EXPECTED)))
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
    emit("IB-rtf-10 ARM (e) APPLY -- run at %s as %s -- worktree HEAD %s" % (
        now(), boto3.client("sts").get_caller_identity()["Arn"], git("rev-parse", "HEAD")[1].strip()))
    emit("")
    rc = 1
    if precheck():
        landed = apply_all()
        if len(landed) == len(EXPECTED):
            rc = 0 if post() else 1
    emit("")
    emit("APPLY RESULT: %s" % ("7 of 7 applied, 0-diff 7 of 7" if rc == 0 else "NOT COMPLETE -- see above"))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
