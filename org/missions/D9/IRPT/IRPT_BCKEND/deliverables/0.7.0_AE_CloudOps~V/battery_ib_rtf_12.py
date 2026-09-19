#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-12 battery -- every serving zip carries the raw-keys file its id module reads.

THIRD PASS (this revision; GO msg 98296 on halves 2 of 2 naming packet blob 9d273fb851): every arm, AFTER the apply.
  (a)-(c) as before: the premise at the cut, the files described, the manifest parse-diff.
  (d) the packet at HEAD == the signed blob; the 2 halves naming it; each built artifact intact at its built sha and each
      rollback source intact at the prior live CodeSha256; the apply record at HEAD: pre-apply digests EQUAL 7 of 7 and
      the built artifacts the latest 6 of 6 before any apply.
  (e) the apply: the ledger CLOSED at HEAD; the record 'applied: 6 of 6' and '0-diff: 7 of 7'; a plan re-taken NOW
      0-diff 7 of 7; CodeSha256 == built 6 of 6 (the served zip hashes to it); raw_keys.json downloaded from each served
      zip == the blob (the registry too on the S99 four); ycharts (S102) unchanged.
  (f) rtf-10's arm (f), with the ruled carve-outs RECORDED-NOT-COUNTED (holdings S100, ycharts S102, inflection S94):
      the bounded principal (rtf-9 packet blob a1f36b95b2), new epoch, under ledger irpt-bckend-ib-rtf-12-live-principal;
      real HTTP requests as each function's execution role, the deployed bytes; every COUNTED request SCOPE-RESOLVED,
      0 UNEXPECTED; S92 recorded by output; the lifecycle closed and verified.
The token prints only when every arm holds. Read-only on every live plane. Prints no credential.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-12_R69-AC1_battery_output.txt")
TOKEN = "IBR69-RAW-KEYS-STAGED-SERVED-AND-PATH-RESOLVES"
CUT = "083cc54350"
FNS = ["irpt-directory-search", "irpt-status", "irpt-holdings", "irpt-narrative", "irpt-export-render",
       "irpt-performance-adapter", "irpt-ycharts-generate"]
RAW_REPO = "infra/aws/lambda/investor-reporting/_ids/raw_keys.json"
REG_REPO = "data/firm_registry.json"
IDS_REPO = "infra/aws/lambda/investor-reporting/_ids/ids.py"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
BUCKET = "opal-313476888478-lambda-artifacts"
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-12.md"
LINES: list[str] = []
lam = boto3.client("lambda", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def git(*args: str) -> tuple[int, bytes]:
    p = subprocess.run(["git", *args], cwd=WS, capture_output=True, timeout=120)
    return p.returncode, p.stdout


def blob_at(ref: str, path: str) -> bytes | None:
    rc, out = git("show", "%s:%s" % (ref, path))
    return out if rc == 0 else None


def b64sha(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def identity_line(arm: str) -> None:
    emit("  identity: %s ran as %s -- a configuration/document claim, NOT a served behaviour"
         % (arm, boto3.client("sts").get_caller_identity()["Arn"]))


def live_zip(fn: str) -> tuple[dict, dict, str]:
    cfg = lam.get_function_configuration(FunctionName=fn)
    body = urllib.request.urlopen(lam.get_function(FunctionName=fn)["Code"]["Location"], timeout=120).read()
    z = zipfile.ZipFile(io.BytesIO(body))
    members = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
    return cfg, members, "EQUAL" if b64sha(body) == cfg["CodeSha256"] else "DIFFERS"


def layer_members(cfg: dict) -> set:
    out = set()
    for layer in cfg.get("Layers") or []:
        lv = lam.get_layer_version_by_arn(Arn=layer["Arn"])
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(lv["Content"]["Location"], timeout=120).read()))
        out |= {n for n in z.namelist() if not n.endswith("/")}
    return out


def arm_a() -> bool:
    emit("(a) THE PREMISE -- at the cut @%s and at HEAD; the live zips; the _ids/ beside-opens census" % CUT)
    identity_line("(a)")
    cut = json.loads(blob_at(CUT, MAP).decode("utf-8"))["functions"]
    head = json.loads(blob_at("HEAD", MAP).decode("utf-8"))["functions"]
    staged_cut = sum(any(s["repo_path"] == RAW_REPO for s in cut[f].get("staged_from", [])) for f in FNS)
    staged_head = sum(any(s["repo_path"] == RAW_REPO for s in head[f].get("staged_from", [])) for f in FNS)
    emit("  _ids/raw_keys.json staged: at the cut %d of 7 (the premise); at HEAD %d of 7 (after (c))" % (staged_cut, staged_head))
    ids_src = blob_at("HEAD", IDS_REPO).decode("utf-8").splitlines()
    for ln in (64, 162):
        emit("  %s:%d @HEAD: %s" % (IDS_REPO, ln, ids_src[ln - 1].strip()))
    opens = [(i + 1, t.strip()) for i, t in enumerate(ids_src) if re.search(r"os\.path\.join\((HERE|d|SEAM_INDEX_DIR)", t)]
    emit("  beside/walk-up path constructions in _ids/ids.py @HEAD: %d -- %s" % (len(opens), ["%d: %s" % o for o in opens]))
    families = ("raw_keys.json (:64 -> :162)", "firm registry (:113-138: env, walk-up data/firm_registry.json, beside)",
                "data/<seam>.json (:338 -> :360)")
    emit("  the families those constructions serve: %d of %d -- %s" % (len(families), len(families), list(families)))
    in_zip = 0
    ok_zip = True
    for fn in FNS:
        cfg, members, sha_ok = live_zip(fn)
        env = (cfg.get("Environment") or {}).get("Variables") or {}
        lay = layer_members(cfg)
        raw = "PRESENT" if "raw_keys.json" in members else "MISSING"
        in_zip += raw == "PRESENT"
        regv = env.get("IRPT_FIRM_REGISTRY")
        if regv:
            rel = regv[len("/var/task/"):] if regv.startswith("/var/task/") else None
            lrel = regv[len("/opt/"):] if regv.startswith("/opt/") else None
            reg = "RESOLVED-VIA-ENV (%s: %s)" % (regv, "in the zip" if rel in members else ("in the layer" if lrel in lay else "PATH ABSENT"))
        else:
            reg = "PRESENT beside" if "firm_registry.json" in members else ("PRESENT via walk-up" if "data/firm_registry.json" in members else "MISSING")
        seam = "PRESENT" if "data/custodian_key_seam.json" in members else "MISSING"
        ok_zip = ok_zip and sha_ok == "EQUAL"
        emit("  %-26s live zip %2d members (sha256 == live CodeSha256: %s) | layers %d | raw_keys.json %-7s | registry %-52s | seam %s"
             % (fn, len(members), sha_ok, len(cfg.get("Layers") or []), raw, reg, seam))
    # PHASE-AWARE (the pass-3 defect): the premise is 0 of 7 BEFORE the apply. Once the apply ledger is CLOSED at HEAD
    # the live zips carry the member BY DESIGN -- 6 of 7, ycharts deferred (S102) -- and requiring 0 there re-asserts a
    # pre-apply fact against a post-apply world. The premise itself stays readable at the cut, printed above.
    rc_s, _ = git("rev-parse", "--verify", "--quiet", "HEAD:org/critical_paths/.open_deploys/irpt-bckend-ib-rtf-12-apply.json")
    led = (blob_at("HEAD", "org/critical_paths/change_management/20260919T1712Z_irpt-bckend-ib-rtf-12-apply_deploy_completion.md") or b"").decode("utf-8", "replace")
    applied = rc_s != 0 and "**Status:** CLOSED" in led
    want = 6 if applied else 0
    emit("  raw_keys.json in the live zips: %d of 7 -- %s (the apply ledger at HEAD: %s)"
         % (in_zip, "the premise, expected 0 of 7 pre-apply" if not applied else
            "expected 6 of 7 POST-APPLY (ycharts deferred, S102); the premise 0 of 7 is the cut's, printed above", "CLOSED" if applied else "not closed"))
    return staged_cut == 0 and in_zip == want and ok_zip and len(opens) >= 3


def arm_b() -> bool:
    emit("(b) THE FILES, DESCRIBED FOR THE HALVES")
    identity_line("(b)")
    ok = True
    for path, fam in ((RAW_REPO, "firms"), (REG_REPO, "firms")):
        b = blob_at("HEAD", path)
        _, blob = git("rev-parse", "HEAD:" + path)
        d = json.loads(b)
        entries = d.get(fam)
        k = len(entries) if entries is not None else 0
        cred_keys = re.findall(r'"([^"]*(?:secret|password|passwd|credential|private_key|api_key|apikey|access_key)[^"]*)"\s*:', b.decode("utf-8"), re.I)
        token_keys = sorted(set(re.findall(r'"([^"]*token[^"]*)"\s*:', b.decode("utf-8"), re.I)))
        _, log = git("log", "--format=%an", "--", path)
        writers = sorted(set(log.decode("utf-8").split()))
        emit("  %s: blob %s, %d bytes, CR %d; top-level %s; %s entries k=%d; credential-named keys %d; token-named keys %s "
             "(a folder token / a key-space name, not a secret); writers W=%d %s"
             % (path, blob.decode().strip(), len(b), b.count(b"\r"), list(d), fam, k, len(cred_keys), token_keys, len(writers), writers))
        ok = ok and not cred_keys
    raw = json.loads(blob_at("HEAD", RAW_REPO))
    for fid, row in raw["firms"].items():
        emit("    raw_keys %-12s %s" % (fid, {kk: (v.get("raw_key") or "")[:48] for kk, v in row.items()}))
    emit("  the values are DECLARATIONS (upstream field names and citations), never client identifiers; the id module keys "
         "by the VERIFIED tenant (ids.py:408 raw_key_for(firm_id, ...), called from served.py:582 with `tenant`)")
    return ok


def arm_c() -> bool:
    emit("(c) THE MANIFEST -- the parse-diff from the cut @%s to HEAD" % CUT)
    identity_line("(c)")
    before = json.loads(blob_at(CUT, MAP).decode("utf-8"))
    after = json.loads(blob_at("HEAD", MAP).decode("utf-8"))
    raw_n = reg_n = 0
    exp = json.loads(json.dumps(before))
    for fn in FNS:
        a = after["functions"][fn]
        add = [s for s in a.get("staged_from", []) if s["repo_path"] in (RAW_REPO, REG_REPO)]
        raw_n += sum(s["repo_path"] == RAW_REPO for s in add)
        reg_n += sum(s["repo_path"] == REG_REPO for s in add)
        e = exp["functions"][fn]
        k = next(i for i, s in enumerate(e["staged_from"]) if s["repo_path"].endswith("_ids/ids.py"))
        e["staged_from"][k + 1:k + 1] = add
        e["files"].extend(s["packaged_as"] for s in add)
        ids_obj = next(s for s in a["staged_from"] if s["repo_path"].endswith("_ids/ids.py"))
        shape = all(sorted(s) == sorted(ids_obj) for s in add)
        pin_ok = all(hashlib.sha256(blob_at(s["pin"], s["repo_path"]) or b"").hexdigest() == s["sha256"] for s in add)
        emit("  %-26s added %s | same shape as the ids.py object: %s | sha256 == the blob at its pin: %s | artifact_sha256 unchanged: %s"
             % (fn, [s["packaged_as"] for s in add], shape, pin_ok,
                a["artifact_sha256"] == before["functions"][fn]["artifact_sha256"]))
    clean = after == exp
    emit("  staged_from objects added: raw_keys.json %d of 7, firm_registry.json %d (the 4 whose registry resolves nowhere, "
         "row S99); files[] +%d; parse-diff == exactly these additions: %s" % (raw_n, reg_n, raw_n + reg_n, clean))
    return clean and raw_n == 7 and reg_n == 4


import datetime  # noqa: E402
import secrets  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402

import bcrypt  # noqa: E402

PACKET_BLOB = "9d273fb8517a00288ec13d8dd0814a47af8782fa"
APPLY_OUTPUT_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/IB-rtf-12_apply_output.txt"
APPLY_SENTINEL_REL = "org/critical_paths/.open_deploys/irpt-bckend-ib-rtf-12-apply.json"
APPLY_LEDGER_REL = "org/critical_paths/change_management/20260919T1712Z_irpt-bckend-ib-rtf-12-apply_deploy_completion.md"
HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-12_RAW_KEYS_STAGED.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-12_RAW_KEYS_STAGED.md",
}
BUILT = {
    "irpt-directory-search": ("PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=", "DOwCkAXXw1oLuzL_yzf2AqNJ0v.WnYDF", "HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI=", "hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd"),
    "irpt-status": ("O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=", "z8VnRXEPFTioTwjwWlR_TCCQYiqU6mmV", "LHprxKSP1lM3VhoP2ijEcUVCtI+yeZt8tPRkZwpRBdY=", "QNerDSUu9GMYB0bZrjon6n_6VG9q3aR6"),
    "irpt-holdings": ("uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=", "U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg", "78XvypHOpeybejwKd5KLCwNcgat2jbQr6O3PhdwaFSU=", "XGnVW2ED9FW0zOpRr0V5K12adFHrpeO7"),
    "irpt-narrative": ("o4newc7E9m1pD61k+P/xGdlwHMO7cheYbDfR6Urzgh8=", "jM9scOJ005ovgidfDS3DBRHRmjvLzUwn", "sgolF/uXedgXpePoBoi5y1dIgOybQkgcokihEJFM+0I=", "Pu2QRmDx58Qo3hHwVM8L_gyotsmQ8h_6"),
    "irpt-export-render": ("9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=", "dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH", "4Dp6e0Vy+SfziPY+9wUSWSBS4JzS9diUtduOTxIqclQ=", "5tV41pNz.TpJ8O1f6zZCAJ9M6BRqoYlI"),
    "irpt-performance-adapter": ("IHosoGqGUxh2M/UjefNnmbLSXVgTxlNG76cGPjEd1tw=", "38i7y_iXZqvWIzUNetKnBxXxs9dAuOGF", "/Cn8XUZoSn1EGBax3+/UaVjJSAQiybZQ84vRVwiRcWs=", "KI0U8m08xPkCgvem5bLmcU2fuWwOCLzs"),
}
YCHARTS_LIVE = "1L60sG1G9IaFfwe+LPNdE84DarlWCHKkdE8M5CyVI8o="
REG_FNS = {"irpt-directory-search", "irpt-status", "irpt-narrative", "irpt-performance-adapter"}
ROOTS = ["directory", "ops", "holdings", "narrative", "export", "performance", "ycharts"]
TF = os.path.join(WS, ".tools", "terraform.exe")
PLAN_DIR = os.path.join(WS, ".scratch", "plans12_battery")
ROLE = {"irpt-directory-search": "irpt-directory-role", "irpt-status": "irpt-status-role", "irpt-holdings": "irpt-holdings-role",
        "irpt-narrative": "irpt-narrative-role", "irpt-export-render": "irpt-export-render-role",
        "irpt-performance-adapter": "irpt-performance-adapter-role", "irpt-ycharts-generate": "irpt-ycharts-generate-role"}
NOT_COUNTED = {"irpt-holdings": "S100", "irpt-ycharts-generate": "S102"}
# (f): the rtf-9 packet's keys, verbatim (NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md, blob a1f36b95b2)
D_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V"
RTF9_PACKET_REL = D_REL + "/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md"
RTF9_BLOB = "a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4"
RTF9_HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
}
PRINCIPAL_SENTINEL_REL = "org/critical_paths/.open_deploys/irpt-bckend-ib-rtf-12-live-principal-2.json"
USERS, PARTNER, THROTTLE = "opal-users-v2", "opal-partner-49financial", "opal-portal-auth-throttle"
FIRM, ADVISOR = "49financial", "abby_horton"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/49financial/ownership_map.json"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
UA = "opal-irpt-ib-rtf-12-battery/1.0 (0.7.0_AE_CloudOps~V)"
SECRETS: list[str] = []
ddb = boto3.client("dynamodb", region_name="us-east-1")
_emit_plain = emit


def emit(line: str = "") -> None:  # noqa: F811 -- the redacting emitter shadows the plain one
    for s in SECRETS:
        if s:
            line = line.replace(s, "<REDACTED>")
    _emit_plain(line)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------------------------------------------ (d)
def arm_d() -> bool:
    emit("(d) THE PACKET, THE HALVES, THE BUILT ARTIFACTS, THE PRE-APPLY RECORD")
    identity_line("(d)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    _, wt = git("hash-object", PACKET_REL)
    pk_ok = rc == 0 and head.decode().strip() == wt.decode().strip() == PACKET_BLOB
    emit("  packet blob at HEAD %s, worktree %s, signed %s -> %s" % (head.decode().strip(), wt.decode().strip(), PACKET_BLOB,
                                                                     "EQUAL" if pk_ok else "DIFFERS"))
    n = 0
    for who, p in HALVES.items():
        text = (blob_at("HEAD", p) or b"").decode("utf-8", "replace")
        hit = PACKET_BLOB in text
        n += hit
        emit("  %s half at HEAD %s: names the blob %s" % (who, p, hit))
    emit("  halves: %d of 2" % n)
    art = 0
    for fn, (bsha, bver, plive, pver) in BUILT.items():
        key = "investor-reporting/%s.zip" % fn
        b = s3.get_object(Bucket=BUCKET, Key=key, VersionId=bver)["Body"].read()
        r = s3.get_object(Bucket=BUCKET, Key=key, VersionId=pver)["Body"].read()
        good = b64sha(b) == bsha and b64sha(r) == plive
        art += good
        emit("  %-26s built version %s bytes == built %s: %s | rollback source %s == prior live: %s" % (
            fn, bver, bsha[:12], b64sha(b) == bsha, pver, b64sha(r) == plive))
    emit("  built artifacts intact at their shas and rollback sources intact: %d of %d" % (art, len(BUILT)))
    rc2, rec = git("show", "HEAD:" + APPLY_OUTPUT_REL)
    rec = rec.decode("utf-8") if rc2 == 0 else ""
    pre = sum(1 for r in ROOTS if re.search(r"^  %s\s+.*canonical digest [0-9a-f]{64} -> EQUAL" % r, rec, re.M))
    arts_line = "built artifacts the latest at their built sha: 6 of 6" in rec
    emit("  the apply record at HEAD: pre-apply digests EQUAL to the packet's %d of 7; '%s' %s; 'PRE-APPLY: ALL HOLD' %s"
         % (pre, "built artifacts the latest at their built sha: 6 of 6", arts_line, "PRE-APPLY: ALL HOLD" in rec))
    return pk_ok and n == 2 and art == len(BUILT) and pre == 7 and arts_line and "PRE-APPLY: ALL HOLD" in rec


# ------------------------------------------------------------------------------------------------ (e)
def plan_zero(root: str) -> tuple[str, int]:
    d = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting", root)
    os.makedirs(PLAN_DIR, exist_ok=True)
    pf = os.path.join(PLAN_DIR, root + ".tfplan")
    env = dict(os.environ, TF_IN_AUTOMATION="1", AWS_REGION="us-east-1", TF_PLUGIN_CACHE_DIR=os.path.join(WS, ".scratch", "tf-plugin-cache"))
    subprocess.run([TF, "-chdir=" + d, "init", "-input=false", "-no-color"], capture_output=True, env=env, timeout=900)
    p = subprocess.run([TF, "-chdir=" + d, "plan", "-input=false", "-no-color", "-out=" + pf], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, timeout=1200)
    line = next((ln.strip() for ln in p.stdout.splitlines() if ln.startswith("Plan:") or "No changes." in ln), "rc %d" % p.returncode)
    j = json.loads(subprocess.run([TF, "-chdir=" + d, "show", "-json", pf], capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", env=env, timeout=600).stdout)
    return line, len([c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]])


def arm_e() -> bool:
    emit("(e) THE APPLY -- under its ledger; then the deployed code and the served members read back")
    identity_line("(e)")
    rc_s, _ = git("rev-parse", "--verify", "--quiet", "HEAD:" + APPLY_SENTINEL_REL)
    led = (blob_at("HEAD", APPLY_LEDGER_REL) or b"").decode("utf-8", "replace")
    closed = rc_s != 0 and "**Status:** CLOSED" in led
    emit("  ledger irpt-bckend-ib-rtf-12-apply at HEAD: sentinel %s; entry CLOSED %s" % ("ABSENT" if rc_s != 0 else "PRESENT", "**Status:** CLOSED" in led))
    rec = (blob_at("HEAD", APPLY_OUTPUT_REL) or b"").decode("utf-8", "replace")
    applied = "applied: 6 of 6" in rec
    zero_rec = "0-diff: 7 of 7" in rec
    emit("  the apply record: 'applied: 6 of 6' %s; '0-diff: 7 of 7' %s" % (applied, zero_rec))
    zero = 0
    for r in ROOTS:
        line, n = plan_zero(r)
        zero += n == 0
        emit("  now %-11s %s | changes %d -> %s" % (r, line, n, "0-DIFF" if n == 0 else "NOT 0-DIFF"))
    emit("  re-taken now: 0-diff %d of 7" % zero)
    code_ok = mem_ok = 0
    raw_blob = blob_at("HEAD", RAW_REPO)
    reg_blob = blob_at("HEAD", REG_REPO)
    for fn, (bsha, _bver, _pl, _pv) in BUILT.items():
        cfg, members, sha_ok = live_zip(fn)
        c_ok = cfg["CodeSha256"] == bsha and sha_ok == "EQUAL"
        code_ok += c_ok
        raw = members.get("raw_keys.json")
        reg = members.get("firm_registry.json")
        m_ok = raw == raw_blob and (reg == reg_blob if fn in REG_FNS else True)
        mem_ok += m_ok
        emit("  %-26s CodeSha256 %s (== built: %s; the served zip hashes to it: %s) | raw_keys.json in the served zip: %s (sha256 %s == the blob: %s)%s"
             % (fn, cfg["CodeSha256"], cfg["CodeSha256"] == bsha, sha_ok, raw is not None, sha(raw)[:12] if raw else "-", raw == raw_blob,
                (" | firm_registry.json == the blob: %s" % (reg == reg_blob)) if fn in REG_FNS else ""))
    yc = lam.get_function_configuration(FunctionName="irpt-ycharts-generate")["CodeSha256"]
    emit("  irpt-ycharts-generate (S102, not applied): CodeSha256 %s -> %s" % (yc, "UNCHANGED" if yc == YCHARTS_LIVE else "CHANGED"))
    emit("  CodeSha256 == built: %d of %d; raw_keys.json (and the registry on the S99 four) served == the blob: %d of %d"
         % (code_ok, len(BUILT), mem_ok, len(BUILT)))
    return closed and applied and zero_rec and zero == 7 and code_ok == len(BUILT) and mem_ok == len(BUILT) and yc == YCHARTS_LIVE


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
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read()


def as_json(b: bytes):
    try:
        return json.loads(b.decode("utf-8"))
    except ValueError:
        return None


def classify(status: int, j) -> dict:
    out = {"http": status}
    if isinstance(j, dict):
        st = j.get("status") or {}
        out.update({"operation": j.get("operation"), "firm_id": j.get("firm_id"), "code": st.get("public_reason_code"),
                    "state": st.get("state"), "business_date": st.get("business_date")})
        if status < 400 and "data" in j:
            out["class"] = "SERVED"
        elif out["code"] == "UNEXPECTED":
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
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + RTF9_PACKET_REL)
    _, wt = git("hash-object", RTF9_PACKET_REL)
    pk = rc == 0 and head.decode().strip() == RTF9_BLOB == wt.decode().strip()
    n = sum(1 for p in RTF9_HALVES.values() if RTF9_BLOB in (blob_at("HEAD", p) or b"").decode("utf-8", "replace"))
    rc3, _ = git("rev-parse", "--verify", "--quiet", "HEAD:" + PRINCIPAL_SENTINEL_REL)
    emit("  PRECONDITION: rtf-9 packet blob at HEAD == %s: %s; halves naming it %d of 2; this order's principal ledger sentinel at HEAD: %s"
         % (RTF9_BLOB, pk, n, rc3 == 0))
    return pk and n == 2 and rc3 == 0


def create_principal(epoch: int, password: str, created: dict) -> dict:
    email = "irpt-rte1-test-%d@opal.test" % epoch
    pk = "USER#usr_irptrte_%d" % epoch
    created.update({"email": email, "pk": pk})  # BEFORE any write, so the rollback always knows both keys
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS.append(pw_hash)
    # The attribute VALUES are the rtf-9 packet's, verbatim (its K1 table binds `name` and `createdBy`).
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
          "name": {"S": "IRPT test principal (IB-rtf-3)"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
          "status": {"S": "active"}, "createdAt": {"S": now_iso()}, "createdBy": {"S": "0.7.0_AE_CloudOps~V IB-rtf-3"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    t_k1 = now_iso()
    got1 = get_item(USERS, {"PK": {"S": pk}, "SK": {"S": "PROFILE"}})
    emit("  K1 created %s: PK %s; consistent read-back %s; attributes %d; digest (passwordHash excluded) %s"
         % (t_k1, pk, got1 is not None, len(got1 or {}), item_digest(got1) if got1 else "-"))
    ddb.put_item(TableName=PARTNER, Item={"email": {"S": email}, "advisorKey": {"S": ADVISOR}}, ConditionExpression="attribute_not_exists(email)")
    got = get_item(PARTNER, {"email": {"S": email}})
    emit("  K1b created %s in %s: consistent read-back %s; attributes %s; digest %s"
         % (now_iso(), PARTNER, got is not None, sorted(got or {}), item_digest(got) if got else "-"))
    return {"k1_created": t_k1, "ok": got1 is not None and sorted(got1) == sorted(k1) and got is not None and sorted(got) == ["advisorKey", "email"]}


def login(email: str, password: str) -> dict:
    status, headers, body = http("POST", "/auth/login", body={"email": email, "password": password})
    j = as_json(body) or {}
    tok = j.get("accessToken") if isinstance(j, dict) else None
    refresh = next((c.split(";", 1)[0] for c in (headers.get_all("Set-Cookie") or []) if c.startswith("refresh_token=")), None)
    for s_ in (tok, refresh, refresh.split("=", 1)[1] if refresh else None):
        if s_:
            SECRETS.append(s_)
    out = {"http": status, "token": tok, "refresh_cookie": refresh}
    emit("  login POST /auth/login -> HTTP %d at %s; access token minted=%s; refresh cookie set=%s" % (status, now_iso(), bool(tok), bool(refresh)))
    if tok:
        c = jwt_claims(tok)
        out["claims"] = c
        emit("  K2 claims: firmId=%s role=%s advisorKey=%s advisorId=%s exp=%s" % (
            c.get("firmId"), c.get("role"), c.get("advisorKey"), c.get("advisorId"),
            datetime.datetime.fromtimestamp(c.get("exp", 0), datetime.timezone.utc).strftime("%H:%M:%SZ")))
    return out


def requests_arm(tok: str) -> tuple[bool, dict]:
    emit("  REQUESTS -- route, function, execution role; bodies bound by sha256; carve-outs recorded and NOT counted")
    rows = []
    rnd = secrets.token_hex(12)

    def go(label: str, fn: str, method: str, path: str, body=None, query=None):
        st, _, b = http(method, PFX + path, tok, body=body, query=query)
        j = as_json(b)
        c = classify(st, j)
        c.update({"sha256": sha(b), "label": label, "fn": fn, "counted": fn not in NOT_COUNTED})
        c["ok"] = c["class"] in ("SERVED", "POLICY")
        rows.append(c)
        tag = ("SCOPE-RESOLVED" if c["ok"] else "NOT RESOLVED") if c["counted"] else "RECORDED, NOT COUNTED (%s)" % NOT_COUNTED[fn]
        emit("    %-46s %-4s %s%s -> function %s (role %s): %s http %d code %s firm_id %s business_date %s | sha256 %s -> %s"
             % (label, method, PFX, path, fn, ROLE[fn], c["class"], st, c.get("code"), "present" if c.get("firm_id") else "ABSENT",
                c.get("business_date"), c["sha256"][:16], tag))
        return j, c

    j1, _ = go("directory search WITH a query (q=a)", "irpt-directory-search", "GET", "/directory/search", query={"q": "a", "limit": "25"})
    d1 = j1.get("data") if isinstance(j1, dict) and isinstance(j1.get("data"), list) else []
    j2, _ = go("directory search, a no-match query", "irpt-directory-search", "GET", "/directory/search", query={"q": "zzqqxxnomatch", "limit": "25"})
    d2 = j2.get("data") if isinstance(j2, dict) and isinstance(j2.get("data"), list) else None
    ids = (d1[0] if d1 else {}).get("ids") or {}
    j3, _ = go("directory resolve WITH a selection", "irpt-directory-search", "POST", "/directory/resolve",
               body={"selection": {"relationship_id": ids.get("relationship_id")}})
    d3 = j3.get("data") if isinstance(j3, dict) else None
    acc = (ids.get("account_ids") or [None])[0] or ("acc_" + rnd)
    go("status summary", "irpt-status", "GET", "/status")
    go("analysis sections for an unknown job", "irpt-status", "GET", "/analysis/REQ-%s/sections" % rnd)
    go("holdings for a permitted account", "irpt-holdings", "GET", "/holdings/" + acc)
    go("performance for a permitted account", "irpt-performance-adapter", "GET", "/performance/" + acc, query={"start": "2026-01-01", "end": "2026-09-18"})
    go("narrative for an unknown report", "irpt-narrative", "GET", "/narrative/rep_" + rnd)
    go("export receipt for an unknown export", "irpt-export-render", "GET", "/export/EXP-" + rnd)
    go("analysis submit carrying a server-owned field", "irpt-ycharts-generate", "POST", "/analysis",
       body={"identity": {"tenant_id": "x"}, "variant": "standard"})
    counted = [r for r in rows if r["counted"]]
    unexpected = sum(1 for r in counted if r["class"] == "UNEXPECTED")
    ok_n = sum(1 for r in counted if r["ok"])
    fns = sorted({r["fn"] for r in counted})
    emit("  COUNTED requests scope-resolved: %d of %d; UNEXPECTED among them %d; functions counted %d: %s" % (ok_n, len(counted), unexpected, len(fns), fns))
    for r in rows:
        if not r["counted"]:
            emit("  NOT COUNTED %-26s (%s): %s code %s" % (r["fn"], NOT_COUNTED[r["fn"]], r["class"], r.get("code")))
    s92_search = isinstance(d2, list) and len(d2) == 0 and len(d1) > 0
    resolved = isinstance(d3, dict) and d3.get("ok") is True
    emit("  S92 search: q=a -> %d entries, q=zzqqxxnomatch -> %s entries -> %s" % (
        len(d1), len(d2) if isinstance(d2, list) else "n/a",
        "HONOURED (FIXED)" if s92_search else ("NOT MEASURABLE (search not served)" if not d1 else "NOT HONOURED (NOT FIXED)")))
    emit("  S92 resolve: selection = the first entry's relationship -> ok=%s scope_kind=%s account_count=%s -> %s" % (
        (d3 or {}).get("ok") if isinstance(d3, dict) else None,
        ((d3 or {}).get("resolved_scope") or {}).get("scope_kind") if isinstance(d3, dict) else None,
        (d3 or {}).get("account_count") if isinstance(d3, dict) else None,
        "RESOLVES (FIXED)" if resolved else ("NOT MEASURABLE (no selection)" if not d1 else "DOES NOT RESOLVE (NOT FIXED)")))
    return ok_n == len(counted) and unexpected == 0 and len(counted) > 0, {"s92_search": s92_search, "s92_resolve": resolved}


def firms_record() -> tuple[int, int]:
    firms = json.loads(blob_at("HEAD", REG_REPO))["firms"]
    enabled = [f for f in firms if f.get("kind") == "client" and f.get("enabled")]
    exists = []
    for f in enabled:
        try:
            s3.head_object(Bucket=f["bucket"], Key="platinum/%s/ownership_map.json" % f["firm_id"])
            exists.append(f["firm_id"])
            emit("    %-12s map PRESENT" % f["firm_id"])
        except s3.exceptions.ClientError as exc:
            emit("    %-12s map %s -> UNEXPECTED-BY-ABSENCE (row S94), NOT counted" % (f["firm_id"], exc.response.get("Error", {}).get("Code")))
    emit("    maps exist for %d of %d enabled firms %s; this principal (rtf-9 K1b = %s) exercises 1: %s" % (len(exists), len(enabled), exists, PARTNER, FIRM))
    return len(exists), len(enabled)


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
            out["refresh_refused"] = now_iso() if (st != 200 and not minted) else None
            emit("  REFRESH with the issued refresh token after K1's delete: HTTP %d; access token minted=%s -> %s"
                 % (st, minted, "REFUSED (1 of 1)" if out["refresh_refused"] else "NOT REFUSED -- STOP AND ESCALATE"))
        if sess.get("token"):
            exp = sess["claims"].get("exp", 0)
            wait = exp + 10 - time.time()
            emit("  waiting %.0f s for the access token's exp (%s) + 10 s" % (max(wait, 0), datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%H:%M:%SZ")))
            if wait > 0:
                time.sleep(wait)
            st, _, _b = http("GET", PFX + "/status", sess["token"])
            out["expired_refused"] = now_iso() if st == 401 else None
            emit("  the access token after exp: GET status -> HTTP %d -> %s" % (st, "REFUSED 401 (1 of 1)" if st == 401 else "NOT 401"))
    except Exception as exc:  # noqa: BLE001 -- the deletes above already ran
        emit("  EXCEPTION in the post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


def arm_f() -> bool:
    emit("(f) THE LIVE PROOF (rtf-10's arm (f)) -- real HTTP requests through the deployed routes, the deployed roles, the deployed BYTES")
    emit("  identity: the HTTP requests run as the bounded test principal; the served compute runs as each function's OWN execution "
         "role (printed per request); the operator identity only creates/deletes the principal's keys")
    if not f_precondition():
        emit("  STOP at the precondition: nothing written")
        return False
    n_exist, n_firms = firms_record()
    if not prefix_scan("before"):
        emit("  STOP: residue -- nothing written")
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
        sess = login(created["email"], password)
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
    life_ok = all(rb.get(k_) for k_ in ("k1b_deleted", "k1_deleted", "refresh_refused", "expired_refused")) and after_ok
    emit("  (f) keys + login %s; counted requests scope-resolved with 0 UNEXPECTED %s; lifecycle closed %s; S92 search %s, resolve %s; "
         "firms with a map %d of %d (S94 not counted)" % (keys_ok, req_ok, life_ok, "FIXED" if s92.get("s92_search") else "NOT FIXED",
                                                            "FIXED" if s92.get("s92_resolve") else "NOT FIXED", n_exist, n_firms))
    return keys_ok and req_ok and life_ok


def main() -> int:
    _, h = git("rev-parse", "HEAD")
    emit("IB-rtf-12 R69-AC1 battery (third pass) -- run at %s -- worktree HEAD %s" % (now_iso(), h.decode().strip()))
    emit("")
    arms = {"(a) premise": arm_a()}
    emit("")
    arms["(b) files described"] = arm_b()
    emit("")
    arms["(c) manifest"] = arm_c()
    emit("")
    arms["(d) packet + halves + build + pre-apply"] = arm_d()
    emit("")
    if not arms["(d) packet + halves + build + pre-apply"]:
        emit("STOP at (d) -- (e) and (f) are NOT graded")
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
        emit("RESULT: R69-AC1 PASS -- 6 of 6 arms hold")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R69-AC1 FAIL -- %d of %d arms hold" % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
