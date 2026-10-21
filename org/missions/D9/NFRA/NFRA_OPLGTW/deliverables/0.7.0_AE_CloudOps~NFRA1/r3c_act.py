#!/usr/bin/env python
"""OG-rl-19 Phase B, supervised steps (run from the repository root; each prints its verdict and exits non-zero on a STOP). Counts, statement ids, hashes and times only; no account number or role ARN is written.
  python r3c_act.py pre             gates before anything: the three halves SIGNED at HEAD on release 2923d1ee99 and ask 5f25fa44f2cb, the R3a confirmation files read, batch16's ledger CLOSED at HEAD, the clock inside 07:00Z-11:30Z,
                                    the host marker equal to base_sha (the re-read), the .tf blob equal to trunk's
  python r3c_act.py iam before|after   the two roles' policies as IAM serves them: statement ids and counts (get-role-policy), plus comp-iam's own lines for each role
  python r3c_act.py plan            the saved plan of the two targeted policies: exactly add 0, change 2, destroy 0 on the two addresses
  python r3c_act.py apply           ONE safe-apply of that saved plan
  python r3c_act.py rollback_iam    revert schwab_reader_iam.tf to the base's bytes in the working tree (uncommitted), plan the same two targets, safe-apply, restore the file"""
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

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "r3c_pb/"
SCR = "C:/tmp/ap50_scratch/rl17/"
REL, BASE, TRUNK = "2923d1ee99a014dab841b181af08ca67c643705e", "8e3eddf95916e430e4e9bbf615ca4fd91f9e852f", "a4c6ecfd30ca47a56c317d10ea5dfdcacc8741a4"
ASK16 = "5f25fa44f2cb"
TF_DIR, TF = "infra/aws/terraform/opal-gateway", "infra/aws/terraform/opal-gateway/schwab_reader_iam.tf"
TARGETS = ["aws_iam_role_policy.schwab_catalog_read_policy", "aws_iam_role_policy.schwab_data_read_policy"]
ROLES = {"data": ("gateway-schwab-read-role", "schwab_data_read_policy"), "catalog": ("gateway-schwab-catalog-read-role", "schwab_catalog_read_policy")}
step = sys.argv[1]
os.makedirs(R, exist_ok=True)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True)


def stop(msg):
    print("STOP: " + msg)
    sys.exit(3)


def market_root():
    sys.path.insert(0, os.getcwd())
    from lib.opal_naming import address
    return address("sharepoint", "transcripts", "bronze", "market_update", "date=X")[:-len("date=X")]


def tf(*args, out=None):
    r = subprocess.run(["terraform", "-chdir=" + TF_DIR] + list(args), capture_output=True, text=True)
    if out:
        io.open(out, "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


def host_marker():
    ssm = boto3.client("ssm", region_name="us-east-1")
    cid = ssm.send_command(InstanceIds=["i-07dccb1615503ac99"], DocumentName="AWS-RunShellScript", Parameters={"commands": ["cat /opt/opal-gateway/.deployed_commit"]}, TimeoutSeconds=60)["Command"]["CommandId"]
    for _ in range(30):
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId="i-07dccb1615503ac99")
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return inv["StandardOutputContent"].strip()
    return None


if step == "pre":
    ok = True
    for who, pat in (("CTO", "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/1.0.0_SA_CTO~Z/NEVER_WIDEN_HALF_CTO_OG-rl-19_*.md"), ("COO", "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-19_*.md"),
                     ("CVO", "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/3.0.0_SA_CVO~Z/NEVER_WIDEN_HALF_CVO_OG-rl-19_*.md")):
        files = sorted(glob.glob(pat))
        if not files:
            print("%s half: ABSENT (%s)" % (who, pat))
            ok = False
            continue
        t = io.open(files[-1], encoding="utf-8").read()
        signed = bool(re.search(r"(?i)\bSIGNED\b", t)) and (ASK16 in t or REL[:10] in t)
        print("%s half: %s SIGNED at the ask or release: %s" % (who, os.path.basename(files[-1]), signed))
        ok = ok and signed
    r3a = sorted(glob.glob("org/mcp/inbox/2.0.0_SA_COO/~O/read/*R3a*") + glob.glob("org/mcp/inbox/2.0.0_SA_COO/~O/*R3a*") + glob.glob("org/mcp/inbox/0.7.0_AE_CloudOps/~NFRA1/read/*R3a*"))
    print("R3a confirmation files found: %d %s" % (len(r3a), [os.path.basename(x)[:70] for x in r3a[:4]]))
    ok = ok and len(r3a) >= 1
    ent = [p for p in git("ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/change_management/").stdout.decode().split() if p.endswith("_nfra-oplgtw-gateway-release-batch16_deploy_completion.md")]
    closed = bool(ent) and bool(re.search(r"(?m)^\*\*Status:\*\* CLOSED", git("show", "HEAD:" + ent[-1]).stdout.decode()))
    sent = git("ls-tree", "--name-only", "HEAD", "org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-batch16.json").stdout.decode().strip()
    print("batch16 ledger CLOSED at HEAD: %s; sentinel at HEAD: %s" % (closed, bool(sent)))
    ok = ok and closed and not sent
    t_now = now()
    inwin = "2026-10-21T07:00:00Z" <= t_now <= "2026-10-21T11:30:00Z"
    print("now %s inside 2026-10-21T07:00Z..11:30Z: %s" % (t_now, inwin))
    ok = ok and inwin
    mk = host_marker()
    print("host marker %s base_sha %s: %s" % ((mk or "NONE")[:10], BASE[:10], "equal" if mk == BASE else "DIFFERS"))
    ok = ok and mk == BASE
    blob_equal = git("rev-parse", "HEAD:" + TF).stdout.decode().strip() == git("rev-parse", TRUNK + ":" + TF).stdout.decode().strip() and not git("status", "--short", TF).stdout.decode().strip()
    print(".tf blob equals trunk's and the working tree is clean: %s" % blob_equal)
    ok = ok and blob_equal
    rel_ok = git("rev-parse", "rel-nfra-oplgtw-r3c").stdout.decode().strip() == REL
    print("release branch head equals release_sha: %s" % rel_ok)
    ok = ok and rel_ok
    json.dump({"checked_at": now(), "all_hold": ok, "host_marker_equals_base_sha": mk == BASE, "r3a_files": [os.path.basename(x) for x in r3a]}, io.open(R + "pre.json", "w", encoding="utf-8", newline="\n"), indent=1)
    print("PRE: %s" % ("ALL HOLD" if ok else "NOT READY"))
    sys.exit(0 if ok else 3)

if step == "iam":
    which = sys.argv[2]
    iam = boto3.client("iam")
    rec = {"read_at": now(), "when": which, "roles": {}}
    for kind, (role, _res) in ROLES.items():
        names = iam.list_role_policies(RoleName=role)["PolicyNames"]
        info = {"inline_policies": len(names), "policies": {}}
        for n in names:
            doc = iam.get_role_policy(RoleName=role, PolicyName=n)["PolicyDocument"]
            st = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
            sids = [s.get("Sid") for s in st]
            res_forms = [r for s in st for r in ([s.get("Resource")] if isinstance(s.get("Resource"), str) else (s.get("Resource") or []))]
            info["policies"][n] = {"statements": len(st), "sids": sids, "allow": sum(1 for s in st if s["Effect"] == "Allow"), "deny": sum(1 for s in st if s["Effect"] == "Deny"),
                                   "mentions_49financial": sum(1 for r in res_forms if isinstance(r, str) and "49financial" in r), "sha256_16": hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]}
        c = subprocess.run(["bash", "-c", "comp-iam role " + role], capture_output=True, text=True, timeout=120)
        lines = [ln for ln in (c.stdout + c.stderr).splitlines() if "FOUND-LIVE" in ln or "No role matching" in ln or "granted" in ln.lower()]
        info["comp_iam_lines"] = [re.sub(r"\d{12}", "<acct>", ln)[:160] for ln in lines]
        rec["roles"][kind] = info
    io.open(R + "iam_%s.json" % which, "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: {p: (v["statements"], v["mentions_49financial"]) for p, v in r["policies"].items()} for k, r in rec["roles"].items()}))

if step == "plan":
    rc, out = tf("plan", "-lock=false", "-no-color", "-input=false", "-out=" + SCR + "r3c_act.tfplan", "-target=" + TARGETS[1], "-target=" + TARGETS[0], "-var", "market_update_s3_root=" + market_root(), out=SCR + "r3c_act_plan.txt")
    m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out)
    changed = sorted(re.findall(r"# (\S+) will be (?:updated in-place|created|destroyed|replaced)", out))
    print("plan rc=%s: %s; resources %s" % (rc, m.group(0) if m else "NO PLAN LINE", changed))
    if rc != 0 or not m or m.groups() != ("0", "2", "0") or changed != TARGETS:
        stop("the plan is not exactly the two in-place policy updates")
    print("PLAN OK")

if step == "apply":
    t0 = now()
    t_start = time.monotonic()
    env = dict(os.environ, HALT_ACK="1", AGENT_NAME="0.7.0_AE_CloudOps~NFRA1")
    r = subprocess.run(["bash", ".tools/safe-apply.sh", "-chdir=" + TF_DIR, "apply", "-input=false", "-no-color", SCR + "r3c_act.tfplan"], capture_output=True, text=True, env=env)
    io.open(SCR + "r3c_act_apply.txt", "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
    m = re.search(r"Apply complete! Resources: (\d+) added, (\d+) changed, (\d+) destroyed", r.stdout)
    rec = {"apply_started_utc": t0, "apply_finished_utc": now(), "apply_seconds": round(time.monotonic() - t_start, 1), "rc": r.returncode, "via": "safe-apply", "apply_result": m.group(0) if m else "NO APPLY LINE",
           "add": int(m.group(1)) if m else None, "change": int(m.group(2)) if m else None, "destroy": int(m.group(3)) if m else None, "resources": TARGETS}
    io.open(R + "apply.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
    print(json.dumps(rec))
    sys.exit(0 if (r.returncode == 0 and m and m.groups() == ("0", "2", "0")) else 3)

if step == "rollback_iam":
    t_start = time.monotonic()
    cur = git("show", "HEAD:" + TF).stdout
    old = git("show", BASE + ":" + TF).stdout
    try:
        open(TF, "wb").write(old)
        rc, out = tf("plan", "-lock=false", "-no-color", "-input=false", "-out=" + SCR + "r3c_rb.tfplan", "-target=" + TARGETS[1], "-target=" + TARGETS[0], "-var", "market_update_s3_root=" + market_root(), out=SCR + "r3c_rb_plan.txt")
        m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out)
        print("rollback plan rc=%s: %s" % (rc, m.group(0) if m else "NO PLAN LINE"))
        if rc != 0 or not m or m.groups() != ("0", "2", "0"):
            stop("the rollback plan is not the two in-place updates")
        env = dict(os.environ, HALT_ACK="1", AGENT_NAME="0.7.0_AE_CloudOps~NFRA1")
        r = subprocess.run(["bash", ".tools/safe-apply.sh", "-chdir=" + TF_DIR, "apply", "-input=false", "-no-color", SCR + "r3c_rb.tfplan"], capture_output=True, text=True, env=env)
        io.open(SCR + "r3c_rb_apply.txt", "w", encoding="utf-8", newline="\n").write(r.stdout + r.stderr)
        print("rollback apply rc=%s: %s" % (r.returncode, (re.search(r"Apply complete! Resources: .*", r.stdout) or [""])[0]))
    finally:
        open(TF, "wb").write(cur)
    print("rollback seconds (plan + apply): %.1f; working tree .tf restored: %s" % (time.monotonic() - t_start, git("diff", "--quiet", "HEAD", "--", TF).returncode == 0))
