#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-10 battery -- the serving roles granted the ownership map, the directory and the bucket map.

FOURTH PASS (this revision; GO msg 98264 on halves 2 of 2 naming packet blob c3a44074d2): every arm, AFTER the apply.
  (a) CENSUS of the 7 serving functions, POST-APPLY: role; s3:GetObject on each client firm's ownership map AND on its
      directory object (simulate-principal-policy, one resource per call, a positive and a negative control);
      IRPT_DIRECTORY_BUCKET_MAP in the deployed environment; the runtime loader each entry binds. Expected after the
      packet's keys: ownership map 18 of 21 (holdings grants nothing, by design), directory 21 of 21, bucket map 7 of 7.
      The packet's own CENSUS lines are the PRE-APPLY record and are printed beside the post-apply read.
  (b) THE PACKET: committed (blob at HEAD == worktree == the signed blob), its keys line, REGISTRY-VINTAGE == the HEAD
      blob of data/firm_registry.json, the K-OM / K-DIR ARN lines == the derivation from that registry, writers W.
  (c) THE PLAN: the apply record at HEAD (IB-rtf-10_apply_output.txt) shows the pre-apply canonical digests EQUAL to the
      packet's 7 of 7, 0 destroy, K-CODE the only code change; and a plan RE-TAKEN NOW reads 0-diff 7 of 7.
  (c-code) K-CODE: the built artifact is the latest version, its bytes == the built sha, the rollback source is still
      present and == the prior live CodeSha256, and the function NOW serves the built sha.
  (d) THE HALVES at HEAD naming the packet blob, 2 of 2.
  (e) THE APPLY: the ledger irpt-bckend-ib-rtf-10-apply CLOSED at HEAD (sentinel gone); the apply record 7 of 7 and
      0-diff 7 of 7; simulate-principal-policy ALLOWED on every K-OM role x firm map (18) and every role x firm
      directory object (21), DENIED on the negative controls (the mockadv map on the shared bucket, another platinum
      object per firm, the holdings role on the maps); the bucket map == the registry-derived value on 7 of 7;
      CodeSha256 UNCHANGED on 6 of 6 non-K-CODE functions and == the built sha on irpt-directory-search.
  (f) THE LIVE PROOF UNDER THE DEPLOYED ROLES: the bounded test principal of packet NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9
      (blob a1f36b95b2, both halves at HEAD), NEW EPOCH, under ledger irpt-bckend-ib-rtf-10-live-principal: K1, K1b,
      one login, real HTTP requests through https://opalinvest.dev/api/scoped/investor-reporting/<route> -- one or more
      per affected function, each printed with the route, the function and the execution role it reached -- then K1b
      and K1 deleted and verified, the refresh REFUSED, 401 after exp, no residue. Every request reads SCOPE-RESOLVED
      (served with data, or a policy refusal carrying a firm_id) and never UNEXPECTED; holdings reads EMPTY_GRANT;
      S92 recorded FIXED or not by output (search WITH a query, resolve WITH a selection); inflection recorded
      UNEXPECTED-BY-ABSENCE (S94) and NOT counted. No POST that enqueues work is sent with a valid body: the analysis
      route is exercised only with a server-owned field present, which the handler refuses BEFORE any enqueue.
NEVER PRINTED OR WRITTEN: the password, the access or refresh token, the Authorization header, any secret value; response
bodies are bound by sha256 and summarised by counts and codes only. The token prints only when every arm holds.
"""
from __future__ import annotations

import base64
import datetime
import glob
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request

import bcrypt
import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-10_R67-AC1_battery_output.txt")
TOKEN = "IBR67-SERVING-ROLES-GRANTED-AND-PATH-RESOLVES"
D_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V"
PACKET_REL = D_REL + "/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md"
PACKET_BLOB = "c3a44074d2dabe4292bfc648d855be4b99fe48db"
APPLY_OUTPUT_REL = D_REL + "/IB-rtf-10_apply_output.txt"
APPLY_SENTINEL_REL = "org/critical_paths/.open_deploys/irpt-bckend-ib-rtf-10-apply.json"
APPLY_LEDGER_REL = "org/critical_paths/change_management/20260919T1420Z_irpt-bckend-ib-rtf-10-apply_deploy_completion.md"
TF = os.path.join(WS, ".tools", "terraform.exe")
TF_ROOT = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting")
PLAN_DIR = os.path.join(WS, ".scratch", "plans_battery")
ACCT = "313476888478"
# function -> (terraform root, role resource name in that root, role name, entry file)
FUNCS = {
    "irpt-directory-search": ("directory", "irpt_directory", "irpt-directory-role", "directory/entry.py"),
    "irpt-status": ("ops", "irpt_status", "irpt-status-role", "ops/entry.py"),
    "irpt-holdings": ("holdings", "holdings", "irpt-holdings-role", "holdings/entry.py"),
    "irpt-narrative": ("narrative", "narrative", "irpt-narrative-role", "narrative/entry.py"),
    "irpt-export-render": ("export", "export_render", "irpt-export-render-role", "export/entry.py"),
    "irpt-performance-adapter": ("performance", "performance_adapter", "irpt-performance-adapter-role", "performance/entry.py"),
    "irpt-ycharts-generate": ("ycharts", "generate", "irpt-ycharts-generate-role", "ycharts/generate/entry.py"),
}
ROOT_ORDER = ["directory", "ops", "holdings", "narrative", "export", "performance", "ycharts"]
KCODE_FN = "irpt-directory-search"
KCODE_PRIOR_LIVE = "aQxATFkcdtEBvs+v/zztQBOPcbR9XH9Lzjm9kUOmhmU="
KCODE_PRIOR_VERSION = "l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4"
KCODE_BUILT = "HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI="
KCODE_BUILT_VERSION = "hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
# The pre-apply CodeSha256 of the 6 non-K-CODE functions (the third-pass census @94bbf091ee, output @9752ba2a85).
PRE_APPLY_CODE = {
    "irpt-status": "LHprxKSP1lM3VhoP2ijEcUVCtI+yeZt8tPRkZwpRBdY=",
    "irpt-holdings": "78XvypHOpeybejwKd5KLCwNcgat2jbQr6O3PhdwaFSU=",
    "irpt-narrative": "sgolF/uXedgXpePoBoi5y1dIgOybQkgcokihEJFM+0I=",
    "irpt-export-render": "4Dp6e0Vy+SfziPY+9wUSWSBS4JzS9diUtduOTxIqclQ=",
    "irpt-performance-adapter": "/Cn8XUZoSn1EGBax3+/UaVjJSAQiybZQ84vRVwiRcWs=",
    "irpt-ycharts-generate": "1L60sG1G9IaFfwe+LPNdE84DarlWCHKkdE8M5CyVI8o=",
}
EXPECTED_POST = {"ownership": 18, "directory": 21, "bucket_map": 7}
# (f): the rtf-9 packet's keys, verbatim (NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md, blob a1f36b95b2)
RTF9_PACKET_REL = D_REL + "/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md"
RTF9_BLOB = "a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4"
RTF9_HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
}
PRINCIPAL_SENTINEL_REL = "org/critical_paths/.open_deploys/irpt-bckend-ib-rtf-10-live-principal.json"
USERS, PARTNER, THROTTLE = "opal-users-v2", "opal-partner-49financial", "opal-portal-auth-throttle"
FIRM, ADVISOR = "49financial", "abby_horton"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/49financial/ownership_map.json"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
UA = "opal-irpt-ib-rtf-10-battery/1.0 (0.7.0_AE_CloudOps~V)"

LINES: list[str] = []
SECRETS: list[str] = []
IDENTITY: list[str] = []
ddb = boto3.client("dynamodb", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")
iam = boto3.client("iam")


def emit(line: str = "") -> None:
    for s in SECRETS:
        if s:
            line = line.replace(s, "<REDACTED>")
    LINES.append(line)
    print(line, flush=True)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=120)
    return out.returncode, out.stdout


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def b64sha(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def identity_line(arm: str, served: bool = False) -> None:
    if not IDENTITY:
        IDENTITY.append(boto3.client("sts").get_caller_identity()["Arn"])
    if served:
        emit("  identity: %s -- the HTTP requests run as the bounded test principal; the served compute runs as each "
             "function's OWN execution role (printed per request); the operator identity %s only creates/deletes the "
             "principal's keys and reads configuration" % (arm, IDENTITY[0]))
    else:
        emit("  identity: %s ran as %s -- a configuration/document claim, NOT a served behaviour" % (arm, IDENTITY[0]))


def client_firms() -> list[dict]:
    reg = json.load(open(os.path.join(WS, "data", "firm_registry.json"), encoding="utf-8"))
    return [f for f in reg["firms"] if f.get("kind") == "client" and f.get("enabled")]


def sim(src: str, res: str) -> str:
    return iam.simulate_principal_policy(PolicySourceArn=src, ActionNames=["s3:GetObject"],
                                         ResourceArns=[res])["EvaluationResults"][0]["EvalDecision"]


def role_arn(role: str) -> str:
    return "arn:aws:iam::%s:role/%s" % (ACCT, role)


# ------------------------------------------------------------------------------------------------ (a)-(d)
def arm_a(packet_text: str) -> bool:
    emit("(a) CENSUS -- the 7 serving functions, measured POST-APPLY")
    identity_line("(a)")
    firms = client_firms()
    om_ok = dir_ok = maps = 0
    for fn, (_root, _res, role, entry) in FUNCS.items():
        cfg = lam.get_function_configuration(FunctionName=fn)
        env = (cfg.get("Environment") or {}).get("Variables") or {}
        live_role = cfg["Role"].split("/")[-1]
        src = role_arn(live_role)
        om = [sim(src, "arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (f["bucket"], f["firm_id"])) for f in firms]
        dr = [sim(src, "arn:aws:s3:::%s/investor-reporting/directory/latest.json" % f["bucket"]) for f in firms]
        _, etext = git("show", "HEAD:infra/aws/lambda/investor-reporting/" + entry)
        shared = "deps=_loaders.deps" in etext
        om_ok += sum(d == "allowed" for d in om)
        dir_ok += sum(d == "allowed" for d in dr)
        maps += "IRPT_DIRECTORY_BUCKET_MAP" in env
        emit("  %-25s role %-30s (declared %s) loader %-18s ownership map %d of %d | directory %d of %d | bucket map %s | CodeSha256 %s"
             % (fn, live_role, "OK" if live_role == role else "DIFFERS", "shared _loaders" if shared else "own (_no_grant)",
                sum(d == "allowed" for d in om), len(om), sum(d == "allowed" for d in dr), len(dr),
                "present" if "IRPT_DIRECTORY_BUCKET_MAP" in env else "ABSENT", cfg["CodeSha256"]))
    pos = sim("arn:aws:iam::%s:user/Andrew_Berman" % ACCT, "arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (firms[0]["bucket"], firms[0]["firm_id"]))
    neg = sim(role_arn("opalinvest-auth-lambda-role"), "arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (firms[0]["bucket"], firms[0]["firm_id"]))
    n = len(FUNCS) * len(firms)
    emit("  ownership map readable: %d of %d; directory readable: %d of %d; bucket map present: %d of %d; client firms %d (registry)"
         % (om_ok, n, dir_ok, n, maps, len(FUNCS), len(firms)))
    emit("  controls: positive (user Andrew_Berman) %s; negative (opalinvest-auth-lambda-role) %s" % (pos, neg))
    post = {"ownership": om_ok, "directory": dir_ok, "bucket_map": maps}
    for k, want in EXPECTED_POST.items():
        emit("  POST-APPLY %s: %d, expected after the packet's keys %d -> %s" % (k, post[k], want, "EQUAL" if post[k] == want else "DIFFERS"))
    for k in ("CENSUS-OWNERSHIP-GRANTED", "CENSUS-DIRECTORY-READ", "CENSUS-BUCKET-MAP-PRESENT"):
        m = re.search(r"%s: (\d+ of \d+)" % k, packet_text)
        emit("  PRE-APPLY record, packet line %s: %s" % (k, m.group(1) if m else "ABSENT"))
    return pos == "allowed" and neg != "allowed" and len(firms) == 3 and post == EXPECTED_POST


def arm_b() -> tuple[bool, str, str]:
    emit("(b) THE PACKET -- committed, its keys, the registry vintage and ARN lines, the declared writers")
    identity_line("(b)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    ok = bool(head) and head == wt.strip() == PACKET_BLOB
    text = git("show", "HEAD:" + PACKET_REL)[1] if head else ""
    emit("  packet %s: blob at HEAD %s, worktree %s, signed %s -> %s" % (PACKET_REL, head or "ABSENT", wt.strip(), PACKET_BLOB,
                                                                         "COMMITTED, UNCHANGED" if ok else "NOT THE SIGNED BLOB"))
    keys = re.search(r"PACKET-KEYS: (.+)", text)
    emit("  packet keys line: %s" % (keys.group(1) if keys else "ABSENT"))
    rc, reg_blob = git("rev-parse", "--verify", "--quiet", "HEAD:data/firm_registry.json")
    reg_blob = reg_blob.strip() if rc == 0 else ""
    vint = re.search(r"REGISTRY-VINTAGE: blob ([0-9a-f]{40})", text)
    vint_ok = bool(vint) and vint.group(1) == reg_blob
    emit("  REGISTRY-VINTAGE: packet %s, HEAD data/firm_registry.json blob %s -> %s" % (
        vint.group(1) if vint else "ABSENT", reg_blob or "ABSENT", "EQUAL" if vint_ok else "DIFFERS (a STOP: the ARN list moved)"))
    firms = client_firms()
    derived = {
        "K-OM-ARNS": ["arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (f["bucket"], f["firm_id"]) for f in firms],
        "K-DIR-ARNS": sorted({"arn:aws:s3:::%s/investor-reporting/directory/*" % f["bucket"] for f in firms}),
    }
    arns_ok = True
    for k, want in derived.items():
        m = re.search(r"%s: (.+)" % k, text)
        got = sorted(x.strip() for x in m.group(1).split("|")) if m else []
        eq = got == sorted(want)
        arns_ok = arns_ok and eq
        emit("  %s: packet %d ARN(s), derived from the registry %d -> %s" % (k, len(got), len(want), "EQUAL" if eq else "DIFFERS"))
        for a in sorted(want):
            emit("     %s" % a)
    for fn, (root, res, role, _entry) in FUNCS.items():
        names = []
        for f in sorted(glob.glob(os.path.join(TF_ROOT, root, "*.tf"))):
            t = open(f, encoding="utf-8").read()
            for m in re.finditer(r'resource "aws_iam_role_policy(?:_attachment)?" "([^"]+)" \{(.*?)\n\}', t, re.S):
                if re.search(r'role\s*=\s*aws_iam_role\.%s\.(id|name)' % re.escape(res), m.group(2)):
                    names.append(m.group(1))
        emit("  W(%s policies) = %d declared: %s" % (role, len(names), names))
    return ok and bool(keys) and vint_ok and arns_ok, head, text


def tf_env() -> dict:
    env = dict(os.environ, TF_IN_AUTOMATION="1", AWS_REGION="us-east-1",
               TF_PLUGIN_CACHE_DIR=os.path.join(WS, ".scratch", "tf-plugin-cache"))
    os.makedirs(env["TF_PLUGIN_CACHE_DIR"], exist_ok=True)
    return env


def arm_c(packet_text: str) -> bool:
    emit("(c) THE PLAN -- the pre-apply record at HEAD, and a plan re-taken NOW")
    identity_line("(c)")
    rc, rec = git("show", "HEAD:" + APPLY_OUTPUT_REL)
    rec = rec if rc == 0 else ""
    pre_equal = 0
    for r in ROOT_ORDER:
        m = re.search(r"^  %s\s+(Plan: .*?) \| destroy (\d+) \| code changes (.*?) \| canonical digest ([0-9a-f]{64}) -> (\w+)" % r, rec, re.M)
        good = bool(m) and m.group(5) == "EQUAL" and m.group(2) == "0" and m.group(4) in packet_text
        pre_equal += good
        emit("  pre-apply %-11s %s" % (r, ("%s | destroy %s | code %s | digest %s -> %s" % m.groups()) if m else "ABSENT FROM THE RECORD"))
    applied = "applied: 7 of 7" in rec
    zero_rec = "0-diff: 7 of 7" in rec
    emit("  apply record %s @HEAD: pre-apply digests EQUAL to the packet's %d of 7; 'applied: 7 of 7' %s; '0-diff: 7 of 7' %s"
         % (APPLY_OUTPUT_REL, pre_equal, applied, zero_rec))
    os.makedirs(PLAN_DIR, exist_ok=True)
    zero_now = 0
    for r in ROOT_ORDER:
        d = os.path.join(TF_ROOT, r)
        pf = os.path.join(PLAN_DIR, r + ".tfplan")
        i = subprocess.run([TF, "-chdir=" + d, "init", "-input=false", "-no-color"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=tf_env(), timeout=900)
        p = subprocess.run([TF, "-chdir=" + d, "plan", "-input=false", "-no-color", "-out=" + pf], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=tf_env(), timeout=1200) if i.returncode == 0 else i
        if p.returncode != 0:
            emit("  now %-11s init/plan rc %d: %s" % (r, p.returncode, (p.stderr or p.stdout)[-300:].replace("\n", " ")))
            continue
        line = next((ln.strip() for ln in p.stdout.splitlines() if ln.startswith("Plan:") or "No changes." in ln), "?")
        j = json.loads(subprocess.run([TF, "-chdir=" + d, "show", "-json", pf], capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", env=tf_env(), timeout=600).stdout)
        rcs = [c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]]
        zero_now += not rcs
        emit("  now %-11s %s | changes %d | planfile sha256 %s -> %s" % (r, line, len(rcs), sha(open(pf, "rb").read()),
                                                                         "0-DIFF" if not rcs else [c["address"] for c in rcs]))
    emit("  re-taken now: 0-diff %d of 7" % zero_now)
    return pre_equal == 7 and applied and zero_rec and zero_now == 7


def arm_c_code() -> bool:
    emit("(c-code) K-CODE -- %s: the built artifact, the rollback source, and what the function NOW serves" % KCODE_FN)
    identity_line("(c-code)")
    key = "investor-reporting/%s.zip" % KCODE_FN
    live = lam.get_function_configuration(FunctionName=KCODE_FN)["CodeSha256"]
    head = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=key)
    latest, meta = head.get("VersionId"), (head.get("Metadata") or {}).get("content-sha256")
    got = b64sha(s3.get_object(Bucket=ARTIFACT_BUCKET, Key=key, VersionId=latest)["Body"].read())
    prior_sha = b64sha(s3.get_object(Bucket=ARTIFACT_BUCKET, Key=key, VersionId=KCODE_PRIOR_VERSION)["Body"].read())
    checks = {
        "latest version == built version": latest == KCODE_BUILT_VERSION,
        "metadata == built sha": meta == KCODE_BUILT,
        "re-downloaded bytes == built sha": got == KCODE_BUILT,
        "rollback source present and == prior live": prior_sha == KCODE_PRIOR_LIVE,
        "function serves the built sha": live == KCODE_BUILT,
    }
    emit("  build store latest version %s content-sha256 %s; re-downloaded sha256(b64) %s; built %s" % (latest, meta, got, KCODE_BUILT))
    emit("  rollback source version %s sha256(b64) %s (prior live %s)" % (KCODE_PRIOR_VERSION, prior_sha, KCODE_PRIOR_LIVE))
    emit("  function %s CodeSha256 NOW %s" % (KCODE_FN, live))
    for k, v in checks.items():
        emit("  K-CODE %s: %s" % (k, "OK" if v else "FAIL"))
    emit("  K-CODE: %d of %d checks hold" % (sum(checks.values()), len(checks)))
    return all(checks.values())


def arm_d(blob: str) -> bool:
    emit("(d) THE HALVES at HEAD naming the packet blob")
    identity_line("(d)")
    n = 0
    for who, pattern in (("COO", "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-10_*.md"),
                         ("CTO", "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-10_*.md")):
        _, listing = git("ls-tree", "-r", "--name-only", "HEAD", "--", os.path.dirname(pattern))
        hits = [p for p in listing.splitlines() if re.fullmatch(pattern.replace(".", r"\.").replace("*", ".*"), p)]
        naming = [p for p in hits if blob and blob in git("show", "HEAD:" + p)[1]]
        n += bool(naming)
        emit("  %s half: %d file(s) matching at HEAD, %d naming blob %s -> %s" % (who, len(hits), len(naming), blob or "?",
                                                                               "PRESENT" if naming else "ABSENT"))
    emit("  halves: %d of 2" % n)
    return n == 2


# ------------------------------------------------------------------------------------------------ (e)
def arm_e() -> bool:
    emit("(e) THE APPLY -- under its ledger, then the deployed grants, environment and code read back")
    identity_line("(e)")
    firms = client_firms()
    rc_s, _ = git("rev-parse", "--verify", "--quiet", "HEAD:" + APPLY_SENTINEL_REL)
    rc_l, ledger = git("show", "HEAD:" + APPLY_LEDGER_REL)
    closed = rc_s != 0 and rc_l == 0 and "**Status:** CLOSED" in ledger
    emit("  ledger irpt-bckend-ib-rtf-10-apply at HEAD: sentinel %s; entry status %s -> %s" % (
        "ABSENT" if rc_s != 0 else "PRESENT (still open)",
        (re.search(r"\*\*Status:\*\* (.+)", ledger).group(1) if rc_l == 0 and re.search(r"\*\*Status:\*\* (.+)", ledger) else "ABSENT"),
        "CLOSED" if closed else "NOT CLOSED"))
    om_roles = [v[2] for k, v in FUNCS.items() if k != "irpt-holdings"]
    om = [(r, f["firm_id"], sim(role_arn(r), "arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (f["bucket"], f["firm_id"])))
          for r in om_roles for f in firms]
    om_ok = sum(d == "allowed" for *_, d in om)
    emit("  K-OM: ownership map allowed %d of %d (6 roles x %d firms)" % (om_ok, len(om), len(firms)))
    dr = [(v[2], f["firm_id"], sim(role_arn(v[2]), "arn:aws:s3:::%s/investor-reporting/directory/latest.json" % f["bucket"]))
          for v in FUNCS.values() for f in firms]
    dr_ok = sum(d == "allowed" for *_, d in dr)
    emit("  K-DIR + the existing directory reads: directory object allowed %d of %d (7 roles x %d firms)" % (dr_ok, len(dr), len(firms)))
    negs = []
    for r in om_roles:
        negs.append(("%s on opal-data-bd/platinum/mockadv/ownership_map.json" % r,
                     sim(role_arn(r), "arn:aws:s3:::opal-data-bd/platinum/mockadv/ownership_map.json")))
        for f in firms:
            negs.append(("%s on %s/platinum/%s/positions.parquet" % (r, f["bucket"], f["firm_id"]),
                         sim(role_arn(r), "arn:aws:s3:::%s/platinum/%s/positions.parquet" % (f["bucket"], f["firm_id"]))))
    for f in firms:
        negs.append(("irpt-holdings-role on %s/platinum/%s/ownership_map.json (no grant by design)" % (f["bucket"], f["firm_id"]),
                     sim(role_arn("irpt-holdings-role"), "arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (f["bucket"], f["firm_id"]))))
    neg_ok = sum(d != "allowed" for _, d in negs)
    for name, d in negs:
        if d == "allowed":
            emit("  NEGATIVE CONTROL ALLOWED (a widening): %s" % name)
    emit("  negative controls denied: %d of %d (mockadv map x6 roles, another platinum object x6 roles x%d firms, holdings on the maps x%d)"
         % (neg_ok, len(negs), len(firms), len(firms)))
    pos = sim("arn:aws:iam::%s:user/Andrew_Berman" % ACCT, "arn:aws:s3:::opal-data-bd/platinum/mockadv/ownership_map.json")
    emit("  instrument positive control: user Andrew_Berman on the mockadv map -> %s (the resource grain resolves)" % pos)
    want_map = {f["firm_id"]: f["bucket"] for f in firms}
    env_ok = 0
    code_ok = 0
    for fn in FUNCS:
        cfg = lam.get_function_configuration(FunctionName=fn)
        env = (cfg.get("Environment") or {}).get("Variables") or {}
        raw = env.get("IRPT_DIRECTORY_BUCKET_MAP")
        try:
            val = json.loads(raw) if raw else None
        except ValueError:
            val = None
        e_ok = val == want_map
        env_ok += e_ok
        want_code = KCODE_BUILT if fn == KCODE_FN else PRE_APPLY_CODE[fn]
        c_ok = cfg["CodeSha256"] == want_code
        code_ok += c_ok
        emit("  %-25s bucket map %s (== registry: %s) | CodeSha256 %s -> %s (%s)" % (
            fn, "present" if raw else "ABSENT", e_ok, cfg["CodeSha256"], "EQUAL" if c_ok else "DIFFERS",
            "== the K-CODE built sha" if fn == KCODE_FN else "UNCHANGED from pre-apply"))
    emit("  bucket map == registry-derived value: %d of %d; CodeSha256 as the packet signs (6 unchanged + K-CODE built): %d of %d"
         % (env_ok, len(FUNCS), code_ok, len(FUNCS)))
    return (closed and om_ok == len(om) and dr_ok == len(dr) and neg_ok == len(negs) and pos == "allowed"
            and env_ok == len(FUNCS) and code_ok == len(FUNCS))


# ------------------------------------------------------------------------------------------------ (f)
def http(method: str, path: str, token: str | None = None, body: dict | None = None,
         query: dict | None = None, cookie: str | None = None):
    url = BASE + path
    if query:
        url += "?" + "&".join("%s=%s" % (k, urllib.request.quote(str(v))) for k, v in query.items())
    headers = {"User-Agent": UA, "X-Contract-Version": "v1", "Origin": BASE}
    if token:
        headers["Authorization"] = "Bearer " + token
    if cookie:
        headers["Cookie"] = cookie
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def as_json(b: bytes):
    try:
        return json.loads(b.decode("utf-8"))
    except ValueError:
        return None


def classify(status: int, j) -> dict:
    """SERVED (2xx with data) | POLICY (a refusal carrying a firm_id and a code that is not UNEXPECTED) |
    UNEXPECTED (the S90 shape) | UNRESOLVED (any other refusal: no firm_id -- the scope was never read)."""
    out = {"http": status}
    if isinstance(j, dict):
        st = j.get("status") or {}
        out.update({"operation": j.get("operation"), "firm_id": j.get("firm_id"), "code": st.get("public_reason_code"),
                    "state": st.get("state"), "business_date": st.get("business_date")})
        if status < 400 and "data" in j:
            out["class"] = "SERVED"
            return out
        if out["code"] == "UNEXPECTED":
            out["class"] = "UNEXPECTED"
        elif out.get("firm_id"):
            out["class"] = "POLICY"
        else:
            out["class"] = "UNRESOLVED"
        return out
    out["class"] = "UNEXPECTED" if status >= 500 else "UNRESOLVED"
    return out


def get_item(table: str, key: dict) -> dict | None:
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def item_digest(item: dict) -> str:
    return sha(json.dumps({k: v for k, v in item.items() if k != "passwordHash"}, sort_keys=True).encode("utf-8"))


def jwt_claims(tok: str) -> dict:
    seg = tok.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()).decode("utf-8"))


def prefix_scan(label: str) -> bool:
    ok = True
    for table, attr, prefix in ((USERS, "PK", "USER#usr_irptrte_"), (USERS, "email", "irpt-rte1-test-"), (PARTNER, "email", "irpt-rte1-test-")):
        d = ddb.scan(TableName=table, Select="COUNT", FilterExpression="begins_with(#a, :p)",
                     ExpressionAttributeNames={"#a": attr}, ExpressionAttributeValues={":p": {"S": prefix}})
        ok = ok and d["Count"] == 0
        emit("  %s: %s %s begins_with '%s': %d of %d scanned" % (label, table, attr, prefix, d["Count"], d["ScannedCount"]))
    return ok


def f_precondition() -> bool:
    emit("  PRECONDITION: the rtf-9 packet's 2 of 2 halves at HEAD; this order's principal ledger committed OPEN")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + RTF9_PACKET_REL)
    _, wt = git("hash-object", RTF9_PACKET_REL)
    pk = rc == 0 and head.strip() == RTF9_BLOB == wt.strip()
    n = 0
    for who, path in RTF9_HALVES.items():
        rc2, text = git("show", "HEAD:" + path)
        n += rc2 == 0 and RTF9_BLOB in text
    rc3, _ = git("rev-parse", "--verify", "--quiet", "HEAD:" + PRINCIPAL_SENTINEL_REL)
    emit("  rtf-9 packet blob at HEAD %s (== %s: %s); halves naming it %d of 2; principal ledger sentinel at HEAD: %s"
         % (head.strip(), RTF9_BLOB, pk, n, rc3 == 0))
    return pk and n == 2 and rc3 == 0


def create_principal(epoch: int, password: str, created: dict) -> dict:
    email = "irpt-rte1-test-%d@opal.test" % epoch
    pk = "USER#usr_irptrte_%d" % epoch
    created.update({"email": email, "pk": pk})  # BEFORE any write, so the rollback always knows both keys
    created_at = now_iso()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS.append(pw_hash)
    # The attribute VALUES are the rtf-9 packet's, verbatim (its K1 table binds `name` and `createdBy`).
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
          "name": {"S": "IRPT test principal (IB-rtf-3)"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
          "status": {"S": "active"}, "createdAt": {"S": created_at}, "createdBy": {"S": "0.7.0_AE_CloudOps~V IB-rtf-3"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    t_k1 = now_iso()
    got1 = get_item(USERS, {"PK": {"S": pk}, "SK": {"S": "PROFILE"}})
    emit("  K1 created %s: PK %s; consistent read-back %s; attributes %d; digest (passwordHash excluded) %s"
         % (t_k1, pk, got1 is not None, len(got1 or {}), item_digest(got1) if got1 else "-"))
    k1b = {"email": {"S": email}, "advisorKey": {"S": ADVISOR}}
    ddb.put_item(TableName=PARTNER, Item=k1b, ConditionExpression="attribute_not_exists(email)")
    t_k1b = now_iso()
    got = get_item(PARTNER, {"email": {"S": email}})
    emit("  K1b created %s in %s: consistent read-back %s; attributes %s; digest %s"
         % (t_k1b, PARTNER, got is not None, sorted(got or {}), item_digest(got) if got else "-"))
    return {"email": email, "pk": pk, "k1_created": t_k1,
            "ok": got1 is not None and sorted(got1) == sorted(k1) and got is not None and sorted(got) == ["advisorKey", "email"]}


def login(email: str, password: str) -> dict:
    status, headers, body = http("POST", "/auth/login", body={"email": email, "password": password})
    j = as_json(body) or {}
    tok = j.get("accessToken") if isinstance(j, dict) else None
    cookies = headers.get_all("Set-Cookie") or []
    refresh = next((c.split(";", 1)[0] for c in cookies if c.startswith("refresh_token=")), None)
    for s in (tok, refresh, refresh.split("=", 1)[1] if refresh else None):
        if s:
            SECRETS.append(s)
    out = {"http": status, "token": tok, "refresh_cookie": refresh, "at": now_iso()}
    emit("  login POST /auth/login -> HTTP %d at %s; access token minted=%s; refresh cookie set=%s" % (status, out["at"], bool(tok), bool(refresh)))
    if tok:
        c = jwt_claims(tok)
        out["claims"] = c
        emit("  K2 claims: firmId=%s role=%s advisorKey=%s advisorId=%s exp=%s" % (
            c.get("firmId"), c.get("role"), c.get("advisorKey"), c.get("advisorId"),
            datetime.datetime.fromtimestamp(c.get("exp", 0), datetime.timezone.utc).strftime("%H:%M:%SZ")))
    return out


def route_role(fn: str) -> str:
    return FUNCS[fn][2]


def requests_arm(tok: str) -> tuple[bool, dict]:
    emit("  REQUESTS -- each route, the function it reaches, that function's execution role; bodies bound by sha256")
    rows = []
    rnd = secrets.token_hex(12)

    def go(label: str, fn: str, method: str, path: str, body=None, query=None, want: str = "SCOPE"):
        st, _, b = http(method, PFX + path, tok, body=body, query=query)
        j = as_json(b)
        c = classify(st, j)
        c["sha256"] = sha(b)
        c["label"] = label
        c["fn"] = fn
        ok = c["class"] in ("SERVED", "POLICY") and (want == "SCOPE" or c.get("code") == want or c["class"] == want)
        c["ok"] = ok
        rows.append(c)
        emit("    %-44s %-6s %s%s -> function %s (role %s): %s http %d code %s firm_id %s business_date %s | sha256 %s -> %s"
             % (label, method, PFX, path, fn, route_role(fn), c["class"], st, c.get("code"), "present" if c.get("firm_id") else "ABSENT",
                c.get("business_date"), c["sha256"][:16], "SCOPE-RESOLVED" if ok else "NOT AS REQUIRED"))
        return j, c

    j1, c1 = go("directory search WITH a query (q=a)", "irpt-directory-search", "GET", "/directory/search", query={"q": "a", "limit": "25"}, want="SERVED")
    d1 = j1.get("data") if isinstance(j1, dict) and isinstance(j1.get("data"), list) else []
    j2, c2 = go("directory search, a no-match query", "irpt-directory-search", "GET", "/directory/search", query={"q": "zzqqxxnomatch", "limit": "25"})
    d2 = j2.get("data") if isinstance(j2, dict) and isinstance(j2.get("data"), list) else None
    first = d1[0] if d1 else {}
    ids = first.get("ids") or {}
    j3, c3 = go("directory resolve WITH a selection", "irpt-directory-search", "POST", "/directory/resolve",
                body={"selection": {"relationship_id": ids.get("relationship_id")}})
    d3 = j3.get("data") if isinstance(j3, dict) else None
    resolved = isinstance(d3, dict) and d3.get("ok") is True
    acc = (ids.get("account_ids") or [None])[0] or ("acc_" + rnd)
    go("status summary", "irpt-status", "GET", "/status")
    go("analysis sections for an unknown job", "irpt-status", "GET", "/analysis/REQ-%s/sections" % rnd)
    _, ch = go("holdings for a permitted account", "irpt-holdings", "GET", "/holdings/" + acc, want="EMPTY_GRANT")
    go("performance for a permitted account", "irpt-performance-adapter", "GET", "/performance/" + acc,
       query={"start": "2026-01-01", "end": "2026-09-18"})
    go("narrative for an unknown report", "irpt-narrative", "GET", "/narrative/rep_" + rnd)
    go("export receipt for an unknown export", "irpt-export-render", "GET", "/export/EXP-" + rnd)
    go("analysis submit carrying a server-owned field", "irpt-ycharts-generate", "POST", "/analysis",
       body={"identity": {"tenant_id": "x"}, "variant": "standard"}, want="INVALID_INPUT")
    unexpected = sum(1 for r in rows if r["class"] == "UNEXPECTED")
    ok_n = sum(1 for r in rows if r["ok"])
    fns = sorted({r["fn"] for r in rows})
    emit("  requests scope-resolved as required: %d of %d; UNEXPECTED %d; functions reached %d of %d: %s"
         % (ok_n, len(rows), unexpected, len(fns), len(FUNCS), fns))
    s92_search = isinstance(d2, list) and len(d2) == 0 and len(d1) > 0
    emit("  S92 search: q=a -> %d entries, q=zzqqxxnomatch -> %s entries -> the query is %s" % (
        len(d1), len(d2) if isinstance(d2, list) else "n/a", "HONOURED (FIXED)" if s92_search else "NOT HONOURED (NOT FIXED)"))
    emit("  S92 resolve: selection = the first entry's relationship -> ok=%s scope_kind=%s account_count=%s -> %s" % (
        (d3 or {}).get("ok") if isinstance(d3, dict) else None,
        ((d3 or {}).get("resolved_scope") or {}).get("scope_kind") if isinstance(d3, dict) else None,
        (d3 or {}).get("account_count") if isinstance(d3, dict) else None, "RESOLVES (FIXED)" if resolved else "DOES NOT RESOLVE (NOT FIXED)"))
    emit("  holdings: %s code %s -> %s" % (ch["class"], ch.get("code"), "its designed EMPTY_GRANT" if ch.get("code") == "EMPTY_GRANT" else "NOT the designed EMPTY_GRANT"))
    return ok_n == len(rows) and unexpected == 0, {"s92_search": s92_search, "s92_resolve": resolved}


def s94_record(firms: list) -> tuple[int, int]:
    emit("  FIRMS -- the token's 0 UNEXPECTED reads over the registry-enabled firms whose ownership map EXISTS")
    exists = []
    for f in firms:
        try:
            s3.head_object(Bucket=f["bucket"], Key="platinum/%s/ownership_map.json" % f["firm_id"])
            exists.append(f["firm_id"])
            emit("    %-12s map PRESENT at s3://%s/platinum/%s/ownership_map.json" % (f["firm_id"], f["bucket"], f["firm_id"]))
        except s3.exceptions.ClientError as exc:
            emit("    %-12s map %s at s3://%s/platinum/%s/ownership_map.json -> UNEXPECTED-BY-ABSENCE (row S94), NOT counted"
                 % (f["firm_id"], exc.response.get("Error", {}).get("Code"), f["bucket"], f["firm_id"]))
    emit("    maps exist for %d of %d enabled firms: %s; this principal (the rtf-9 packet's K1b is opal-partner-49financial) "
         "exercises 1 of %d: %s" % (len(exists), len(firms), exists, len(exists), FIRM))
    return len(exists), len(firms)


def rollback(created: dict, sess: dict) -> dict:
    emit("  ROLLBACK -- K1b FIRST, then K1; each verified by a failing consistent base-table read")
    out = {"k1b_deleted": None, "k1_deleted": None, "refresh_refused": None, "expired_refused": None}
    if created.get("email"):
        ddb.delete_item(TableName=PARTNER, Key={"email": {"S": created["email"]}})
        gone = get_item(PARTNER, {"email": {"S": created["email"]}}) is None
        out["k1b_deleted"] = now_iso() if gone else None
        emit("  K1b DeleteItem -> consistent GetItem returns no Item: %s at %s" % (gone, now_iso()))
    if created.get("pk"):
        ddb.delete_item(TableName=USERS, Key={"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}})
        gone = get_item(USERS, {"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}}) is None
        out["k1_deleted"] = now_iso() if gone else None
        emit("  K1  DeleteItem -> consistent GetItem returns no Item: %s at %s" % (gone, now_iso()))
    emit("  deletions verified: %d of 2" % sum(1 for k in ("k1b_deleted", "k1_deleted") if out[k]))
    try:
        if sess.get("refresh_cookie"):
            st, _, b = http("POST", "/auth/refresh", cookie=sess["refresh_cookie"])
            j = as_json(b) or {}
            minted = isinstance(j, dict) and bool(j.get("accessToken"))
            refused = st != 200 and not minted
            out["refresh_refused"] = now_iso() if refused else None
            emit("  REFRESH with the issued refresh token after K1's delete: HTTP %d; access token minted=%s -> %s"
                 % (st, minted, "REFUSED (1 of 1)" if refused else "NOT REFUSED -- STOP AND ESCALATE"))
        if sess.get("token"):
            exp = sess["claims"].get("exp", 0)
            wait = exp + 10 - time.time()
            emit("  waiting %.0f s for the access token's exp (%s) + 10 s" % (
                max(wait, 0), datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%H:%M:%SZ")))
            if wait > 0:
                time.sleep(wait)
            st, _, _b = http("GET", PFX + "/status", sess["token"])
            out["expired_refused"] = now_iso() if st == 401 else None
            emit("  the access token after exp: GET status -> HTTP %d -> %s" % (st, "REFUSED 401 (1 of 1)" if st == 401 else "NOT 401"))
    except Exception as exc:  # noqa: BLE001 -- the deletes above already ran
        emit("  EXCEPTION in the post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


def arm_f() -> bool:
    emit("(f) THE LIVE PROOF -- real HTTP requests through the deployed routes, under the deployed roles")
    identity_line("(f)", served=True)
    if not f_precondition():
        emit("  STOP at the precondition: nothing written")
        return False
    firms = client_firms()
    n_exist, n_firms = s94_record(firms)
    if not prefix_scan("before"):
        emit("  STOP: a principal key already exists (residue) -- nothing written")
        return False
    om = json.loads(s3.get_object(Bucket=OM_BUCKET, Key=OM_KEY)["Body"].read().decode("utf-8"))
    present = ADVISOR in (om.get("advisors") or {})
    emit("  GUARD: %s PRESENT in s3://%s/%s: %s" % (ADVISOR, OM_BUCKET, OM_KEY, present))
    if not present:
        emit("  STOP at the guard: nothing written")
        return False
    password = secrets.token_urlsafe(24)
    SECRETS.append(password)
    created: dict = {}
    sess: dict = {}
    req_ok = keys_ok = False
    s92: dict = {}
    try:
        k = create_principal(int(time.time()), password, created)
        created["k1_created"] = k["k1_created"]
        sess = login(k["email"], password)
        c = sess.get("claims") or {}
        keys_ok = k["ok"] and sess.get("http") == 200 and c.get("firmId") == FIRM and c.get("advisorKey") == ADVISOR
        emit("  keys read back 2 of 2 and the session as the rtf-9 packet declares: %s" % keys_ok)
        if keys_ok:
            req_ok, s92 = requests_arm(sess["token"])
    except Exception as exc:  # noqa: BLE001 -- recorded, then the rollback runs
        emit("  EXCEPTION during the act: %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))
    finally:
        rb = rollback(created, sess)
    after_ok = prefix_scan("after")
    thr = get_item(THROTTLE, {"pk": {"S": "login#acct#" + sha((created.get("email") or "").strip().lower().encode())}}) if created.get("email") else None
    emit("  failed-login throttle counter for the test e-mail: %s" % ("PRESENT (named here, TTL'd)" if thr else "none"))
    ends = [x for x in (rb.get("k1_deleted"), rb.get("k1b_deleted"), rb.get("refresh_refused")) if x]
    exp = (sess.get("claims") or {}).get("exp")
    if exp:
        ends.append(datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    emit("  INTERVAL: [%s, %s]" % (created.get("k1_created"), max(ends) if ends else "-"))
    life_ok = bool(rb.get("k1b_deleted")) and bool(rb.get("k1_deleted")) and bool(rb.get("refresh_refused")) and bool(rb.get("expired_refused")) and after_ok
    emit("  (f) keys + login %s; requests scope-resolved with 0 UNEXPECTED %s; lifecycle closed (2 of 2 deleted, refresh refused, "
         "401 after exp, no residue) %s; S92 search %s, resolve %s (recorded); firms with a map %d of %d (S94 not counted)"
         % (keys_ok, req_ok, life_ok, "FIXED" if s92.get("s92_search") else "NOT FIXED",
            "FIXED" if s92.get("s92_resolve") else "NOT FIXED", n_exist, n_firms))
    return keys_ok and req_ok and life_ok


def main() -> int:
    emit("IB-rtf-10 R67-AC1 battery (fourth pass) -- run at %s -- worktree HEAD %s" % (now_iso(), git("rev-parse", "HEAD")[1].strip()))
    emit("")
    b_ok, blob, packet_text = arm_b()
    emit("")
    a_ok = arm_a(packet_text)
    emit("")
    c_ok = arm_c(packet_text)
    emit("")
    k_ok = arm_c_code()
    emit("")
    d_ok = arm_d(blob)
    emit("")
    arms = {"(a) census": a_ok, "(b) packet": b_ok, "(c) plan": c_ok, "(c-code) K-CODE": k_ok, "(d) halves": d_ok}
    if not d_ok:
        emit("STOP at (d): a half is ABSENT -- (e) and (f) are NOT graded")
        arms["(e) apply"] = False
        arms["(f) live proof"] = False
    else:
        arms["(e) apply"] = arm_e()
        emit("")
        arms["(f) live proof"] = arm_f()
    emit("")
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else "FAIL"))
    if all(arms.values()):
        emit("RESULT: R67-AC1 PASS -- 7 of 7 arms hold")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R67-AC1 FAIL -- %d of %d arms hold" % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
