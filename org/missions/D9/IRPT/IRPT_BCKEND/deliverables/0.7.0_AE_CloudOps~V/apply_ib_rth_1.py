#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rth-1 arm (d) -- the subtraction-gated APPLY of the loaders.py fix, 6 roots, and nothing else.

Packet NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md blob 19389dc50b6e3bfb7436681328cb2721c9c11802 (the worker's, in
deliverables/0.9.0_WK_IRPT_BCKEND~1/); halves COO @6298e74db4, CTO @5fce993215. Build: ledger
irpt-bckend-ib-rth-1-build, commit 2c7cff46b0 -- 6 of 7 built; irpt-ycharts-generate refused by the builder
(row IRPT_BCKEND-S111 = ARMED S102), so its root must plan EMPTY and is not applied.

  --plan   PRE-APPLY, read-only. Every check must hold or NOTHING is applied:
             - packet blob at HEAD == worktree == signed; both halves at HEAD naming it (2 of 2);
             - each built artifact is the build-store LATEST at its built version + content-sha256 (6 of 6), and
               ycharts-generate's latest is still its pre-change version;
             - every function's live CodeSha256 == the packet s4 pre-change value (7 of 7);
             - per root (10 of 10): init + plan -out=<planfile> (vendored terraform); THE SUBTRACTION GATE: data-source
               reads are subtracted and printed; what remains must be EXACTLY one managed update on the root's own
               aws_lambda_function for each of the 6 roots whose function was built -- changed attributes a subset
               of {s3_object_version, source_code_hash}, source_code_hash pre-change -> built, s3_object_version ->
               built version -- and NOTHING for the other 4 roots (api, core, intake, ycharts); 0 destroy anywhere.
           Writes a digest of each saved planfile's managed changes so --apply can refuse a moved plan.
  --apply  Re-verifies each saved planfile's digest, then `.tools/safe-apply.sh -chdir=<root> apply <planfile>` per
           root in order; the first failure STOPS (NEVER-2: this script names what landed). POST: a fresh plan per
           root must read 'No changes.' 10 of 10, and served CodeSha256 == built 6 of 6, ycharts-generate unchanged.
Prints no credential. Appends to IB-rth-1_apply_output.txt beside itself.
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

OUTPUT_PATH = os.path.join(HERE, "IB-rth-1_apply_output.txt")
TF = os.path.join(WS, ".tools", "terraform.exe")
TF_ROOT = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting")
PLAN_DIR = os.path.join(WS, ".scratch", "plans_rth1")
DIGESTS = os.path.join(PLAN_DIR, "digests.json")
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md"
PACKET_BLOB = "19389dc50b6e3bfb7436681328cb2721c9c11802"
HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rth-1_ACCESSDENIED_AS_ABSENT.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rth-1_ACCESSDENIED_AS_ABSENT.md",
}
BUCKET = "opal-313476888478-lambda-artifacts"
PRE = {  # packet s4 pre-change CodeSha256
    "irpt-directory-search": "76LeVyYNfhdyDnQNXR3LzrqSv7k7Vr3POSjpcBzww6E=",
    "irpt-status": "B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0=",
    "irpt-holdings": "rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=",
    "irpt-narrative": "o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8=",
    "irpt-export-render": "cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=",
    "irpt-performance-adapter": "W4rYXgZz/LmZ1zO9I6eiKWc7PgSH+eKAUYXzttCmRTA=",
    "irpt-ycharts-generate": "1L60sG1G9IaFfwe+LPNdE84DarlWCHKkdE8M5CyVI8o=",
}
BUILT = {  # function -> (built sha256, build-store version), ledger irpt-bckend-ib-rth-1-build
    "irpt-directory-search": ("cmh6XwybmdXSiWQkQZMeer7wtw0QW/1lXnAIJlPjJKg=", "4FHLOwjjMQh5LNUWnJRG6La1dJxen2kD"),
    "irpt-status": ("Hos/bFiiIjqK/pPFtaGwbWqTRasDFoA4HHfdfBQoajE=", "ofsQf6Q6ApAwAET9ykgqZIl7.jfChFzF"),
    "irpt-holdings": ("1XkzWP6p8OfobrSCI8ZrRCyMxfWgSK6sPZeYjdON50I=", "QHzwDQDRggw06hA4MAwmGgR0NVmGVH5F"),
    "irpt-narrative": ("es/S9azussVLY2DfTj6hRjV1pqhZ8EaVCnaVcELqhPc=", "ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ"),
    "irpt-export-render": ("2gSDyxxBQ3t4tupQUf/NV4EegOhxqpA2EPBLSKdInsY=", "DwdTG9SqmfEJtA5TwBnxL.gJtyZfvY4x"),
    "irpt-performance-adapter": ("jVktMAiRK+2mYPXEzyst6HjSFFv4xR3Kxm47hAyulyw=", "028gVFz77L5vMQGJSIkt0JqSZCk5V4rB"),
}
NOT_BUILT = {"irpt-ycharts-generate": "D6hl_ey9azxF8RJRQ01YkDlO.axHKuHw"}
ROOT_FN = {  # the 6 roots whose function was built, apply order
    "directory": "irpt-directory-search",
    "ops": "irpt-status",
    "holdings": "irpt-holdings",
    "narrative": "irpt-narrative",
    "export": "irpt-export-render",
    "performance": "irpt-performance-adapter",
}
EMPTY_ROOTS = ["api", "core", "intake", "ycharts"]
ALLOWED_ATTRS = {"s3_object_version", "source_code_hash"}
# KNOWN PRE-EXISTING DRIFT on a root this act does NOT apply -- the one exact change tolerated, nothing wider:
# the ycharts runner host 2.0.0_SA_COO~B started for the render-latency measurement (drive_log_20260921T1350Z.md
# @038ad3bd53: "a stop needs his word, not mine or the CTO's, per CLAUDE.md's EC2-stop rule"). Applying the ycharts
# root would STOP that instance, which is exactly why this act never applies it. Measured by the first --plan run
# (14:51Z): the gate refused on it, correctly, before this entry existed.
KNOWN_DRIFT = {("ycharts", "aws_ec2_instance_state.runner", "i-0167fd745ad906a66", "running", "stopped")}


def is_known_drift(root: str, c: dict) -> bool:
    b, a = c["change"].get("before") or {}, c["change"].get("after") or {}
    return (root, c["address"], b.get("instance_id"), b.get("state"), a.get("state")) in KNOWN_DRIFT \
        and c["change"]["actions"] == ["update"] and b.get("instance_id") == a.get("instance_id")
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


def managed_digest(managed: list) -> str:
    canon = [{"address": c["address"], "actions": c["change"]["actions"], "before": c["change"].get("before"),
              "after": c["change"].get("after")} for c in managed]
    return hashlib.sha256(json.dumps(canon, sort_keys=True).encode("utf-8")).hexdigest()


def plan(root: str, pf: str) -> tuple[bool, str, list, list]:
    i = tf(root, "init", "-input=false", "-no-color", timeout=900)
    if i.returncode != 0:
        return False, "init rc %d: %s" % (i.returncode, (i.stderr or i.stdout)[-300:].replace("\n", " ")), [], []
    p = tf(root, "plan", "-input=false", "-no-color", "-out=" + pf)
    if p.returncode != 0:
        return False, "plan rc %d: %s" % (p.returncode, (p.stderr or p.stdout)[-300:].replace("\n", " ")), [], []
    line = next((ln.strip() for ln in p.stdout.splitlines() if ln.startswith("Plan:") or "No changes." in ln), "?")
    j = json.loads(tf(root, "show", "-json", pf, timeout=600).stdout)
    rcs = [c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]]
    managed = [c for c in rcs if c.get("mode") != "data"]
    reads = [c for c in rcs if c.get("mode") == "data"]
    return True, line, managed, reads


def changed_attrs(c: dict) -> set:
    b, a = c["change"].get("before") or {}, c["change"].get("after") or {}
    unknown = c["change"].get("after_unknown") or {}
    keys = set(b) | set(a)
    return {k for k in keys if (b.get(k) != a.get(k)) and not unknown.get(k)}


def precheck() -> bool:
    emit("PRE-APPLY -- %s -- every check must hold before any apply" % now())
    ok = True
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    _, wt = git("hash-object", PACKET_REL)
    pk = rc == 0 and head.strip() == PACKET_BLOB == wt.strip()
    ok &= pk
    emit("  packet blob at HEAD %s, worktree %s, signed %s -> %s" % (head.strip(), wt.strip(), PACKET_BLOB,
                                                                     "EQUAL" if pk else "DIFFERS"))
    n = 0
    for who, path in HALVES.items():
        rc, text = git("show", "HEAD:" + path)
        hit = rc == 0 and PACKET_BLOB in text
        n += hit
        emit("  %s half at HEAD (%s): names the blob=%s" % (who, path, hit))
    ok &= n == 2
    emit("  halves: %d of 2" % n)
    s3c = boto3.client("s3", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")
    n_art = 0
    for fn, (sha, ver) in BUILT.items():
        h = s3c.head_object(Bucket=BUCKET, Key="investor-reporting/%s.zip" % fn)
        meta = (h.get("Metadata") or {}).get("content-sha256")
        a_ok = h.get("VersionId") == ver and meta == sha
        n_art += a_ok
        emit("  built artifact %-26s latest %s content-sha256 %s -> %s" % (fn, h.get("VersionId"), meta,
                                                                          "EQUAL" if a_ok else "DIFFERS"))
    for fn, ver in NOT_BUILT.items():
        h = s3c.head_object(Bucket=BUCKET, Key="investor-reporting/%s.zip" % fn)
        nb = h.get("VersionId") == ver
        ok &= nb
        emit("  NOT built %-31s latest %s -> %s" % (fn, h.get("VersionId"), "still the pre-change version" if nb
                                                     else "MOVED -- someone uploaded"))
    ok &= n_art == len(BUILT)
    emit("  built artifacts the latest at their built sha: %d of %d" % (n_art, len(BUILT)))
    n_live = 0
    for fn, pre in PRE.items():
        live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        n_live += live == pre
        emit("  live %-26s CodeSha256 %s -> %s" % (fn, live, "== pre-change" if live == pre else "!= pre-change %s" % pre))
    ok &= n_live == len(PRE)
    emit("  live == packet s4 pre-change: %d of %d" % (n_live, len(PRE)))
    emit("")
    emit("  SUBTRACTION GATE -- plan per root, data-source reads subtracted, what remains graded")
    os.makedirs(PLAN_DIR, exist_ok=True)
    digests = {}
    total_entries = total_subtracted = 0
    for root in list(ROOT_FN) + EMPTY_ROOTS:
        pf = os.path.join(PLAN_DIR, root + ".tfplan")
        good, line, managed, reads = plan(root, pf)
        total_entries += len(managed) + len(reads)
        total_subtracted += len(reads)
        destroys = sum("delete" in c["change"]["actions"] for c in managed)
        verdict = []
        if not good:
            r = False
            verdict.append(line)
        elif root in ROOT_FN:
            fn = ROOT_FN[root]
            sha, ver = BUILT[fn]
            r = len(managed) == 1 and destroys == 0
            if r:
                c = managed[0]
                b, a = c["change"].get("before") or {}, c["change"].get("after") or {}
                attrs = changed_attrs(c)
                r = (c["type"] == "aws_lambda_function" and c["change"]["actions"] == ["update"]
                     and b.get("function_name") == fn and attrs <= ALLOWED_ATTRS
                     and b.get("source_code_hash") == PRE[fn] and a.get("source_code_hash") == sha
                     and a.get("s3_object_version") == ver)
                verdict.append("%s update %s: changed %s, source_code_hash %s -> %s, s3_object_version %s -> %s" % (
                    c["address"], b.get("function_name"), sorted(attrs), b.get("source_code_hash"),
                    a.get("source_code_hash"), b.get("s3_object_version"), a.get("s3_object_version")))
            else:
                verdict.append("managed changes %d: %s" % (len(managed), [(c["address"], c["change"]["actions"])
                                                                           for c in managed]))
        else:
            drift = [c for c in managed if is_known_drift(root, c)]
            other = [c for c in managed if not is_known_drift(root, c)]
            r = not other
            verdict.append("managed changes %d%s" % (len(other), "" if not other else ": %s" % [
                (c["address"], c["change"]["actions"]) for c in other]))
            for c in drift:
                verdict.append("KNOWN PRE-EXISTING DRIFT, NOT APPLIED: %s %s -> %s (instance %s)" % (
                    c["address"], (c["change"].get("before") or {}).get("state"),
                    (c["change"].get("after") or {}).get("state"), (c["change"].get("before") or {}).get("instance_id")))
        digests[root] = managed_digest(managed)
        ok &= r
        emit("  %-11s %s | destroy %d | data reads subtracted %d %s | %s -> %s" % (
            root, line, destroys, len(reads), [c["address"] for c in reads] if reads else "", "; ".join(verdict),
            "EXACT" if r else "OUTSIDE THE SIGNED SET"))
    emit("  gate denominator: %d resource_changes entries across %d roots, %d data-source reads subtracted" % (
        total_entries, len(ROOT_FN) + len(EMPTY_ROOTS), total_subtracted))
    with open(DIGESTS, "w", encoding="utf-8") as fh:
        json.dump(digests, fh, indent=1, sort_keys=True)
    emit("PRE-APPLY: %s" % ("ALL HOLD" if ok else "A CHECK FAILED -- NOTHING MAY BE APPLIED (STOP)"))
    return ok


def reverify_saved() -> bool:
    with open(DIGESTS, encoding="utf-8") as fh:
        want = json.load(fh)
    ok = True
    for root in ROOT_FN:
        pf = os.path.join(PLAN_DIR, root + ".tfplan")
        j = json.loads(tf(root, "show", "-json", pf, timeout=600).stdout)
        managed = [c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]
                   and c.get("mode") != "data"]
        d = managed_digest(managed)
        ok &= d == want.get(root)
        emit("  saved planfile %-11s managed digest %s -> %s" % (root, d[:16], "== gated" if d == want.get(root)
                                                                   else "!= gated %s" % want.get(root, "?")[:16]))
    return ok


def apply_all() -> list:
    emit("")
    emit("APPLY -- %s -- .tools/safe-apply.sh per root, the SAVED planfile" % now())
    if not reverify_saved():
        emit("  a saved planfile does not match the gated digest -- NOTHING APPLIED (STOP)")
        return ["FAILED:reverify"]
    landed = []
    env = dict(tf_env(), OPAL_AGENT_SERIAL=os.environ.get("OPAL_AGENT_SERIAL", ""))
    emit("  %s: 0 managed changes (ycharts-generate not built, row S111) -- not applied" % ", ".join(EMPTY_ROOTS))
    for root in ROOT_FN:
        pf = os.path.join(PLAN_DIR, root + ".tfplan").replace("\\", "/")
        chdir = "infra/aws/terraform/investor-reporting/" + root
        t0 = now()
        p = subprocess.run(bash_argv(".tools/safe-apply.sh", "-chdir=" + chdir, "apply", "-input=false", "-no-color",
                                     pf), cwd=WS, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=env, timeout=1800)
        summary = next((ln.strip() for ln in (p.stdout or "").splitlines() if ln.startswith("Apply complete!")), None)
        emit("  %-11s %s -> %s rc=%d %s" % (root, t0, now(), p.returncode, summary or "NO 'Apply complete!' LINE"))
        if p.returncode != 0 or not summary:
            tail = ((p.stderr or "") + (p.stdout or ""))[-1500:]
            emit("  APPLY FAILED on %s -- STOP. Landed before it: %s. NEVER-2: finish or roll back in-session." % (
                root, landed or "none"))
            for ln in tail.splitlines():
                emit("    | " + ln)
            return landed + ["FAILED:" + root]
        landed.append(root)
    emit("  applied: %d of %d" % (len(landed), len(ROOT_FN)))
    return landed


def post() -> bool:
    emit("")
    emit("POST-APPLY -- %s -- a fresh plan per root must read 'No changes.'; served CodeSha256 read back" % now())
    n = 0
    roots = list(ROOT_FN) + EMPTY_ROOTS
    for root in roots:
        pf = os.path.join(PLAN_DIR, root + ".post.tfplan")
        good, line, managed, reads = plan(root, pf)
        drift = [c for c in managed if is_known_drift(root, c)]
        other = [c for c in managed if not is_known_drift(root, c)]
        zero = good and not other
        n += zero
        emit("  %-11s %s | managed %d (known pre-existing drift %d: %s), data reads %d -> %s" % (
            root, line, len(managed), len(drift), [c["address"] for c in drift], len(reads),
            ("0-DIFF" if not drift else "0-DIFF apart from the known drift, NOT APPLIED") if zero
            else "NOT 0-DIFF: %s" % [c["address"] for c in other]))
    emit("  0-diff: %d of %d" % (n, len(roots)))
    lam = boto3.client("lambda", region_name="us-east-1")
    m = 0
    for fn, (sha, _) in BUILT.items():
        live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        m += live == sha
        emit("  served %-26s CodeSha256 %s -> %s" % (fn, live, "== built" if live == sha else "!= built %s" % sha))
    for fn in NOT_BUILT:
        live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
        u = live == PRE[fn]
        m += u
        emit("  served %-26s CodeSha256 %s -> %s" % (fn, live, "UNCHANGED (not built)" if u else "MOVED"))
    emit("  served as intended: %d of %d" % (m, len(BUILT) + len(NOT_BUILT)))
    return n == len(roots) and m == len(BUILT) + len(NOT_BUILT)


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--plan"
    emit("")
    emit("IB-rth-1 ARM (d) %s -- run at %s as %s -- HEAD %s" % (
        mode, now(), boto3.client("sts").get_caller_identity()["Arn"], git("rev-parse", "HEAD")[1].strip()))
    rc = 1
    if mode == "--plan":
        rc = 0 if precheck() else 1
    elif mode == "--apply":
        landed = apply_all()
        if len(landed) == len(ROOT_FN) and not any(x.startswith("FAILED") for x in landed):
            rc = 0 if post() else 1
        emit("")
        emit("APPLY RESULT: %s" % ("6 of 6 applied, 0-diff 10 of 10, served 7 of 7 as intended" if rc == 0
                                   else "NOT COMPLETE -- see above"))
    with open(OUTPUT_PATH, "a", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
