#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-10 battery -- the serving roles granted the ownership map, the directory and the bucket map.

THIRD PASS (this revision; the S96 ruling (i) @6e027591fc, on the re-hand @2b67d4ff7a + the addendum @77bd04ca41):
arms (a)-(d) against the THIRD-PASS RE-CUT packet. (e) apply and (f) the live proof run only on the next pass, after
both never-widen halves are at HEAD naming this re-cut blob; with a half ABSENT the battery STOPS at (d) and says so.
  (a) CENSUS of the 7 serving functions: role; s3:GetObject on each client firm's ownership map AND on its
      directory object (simulate-principal-policy, one resource per call, a positive and a negative control);
      IRPT_DIRECTORY_BUCKET_MAP in the deployed environment; the runtime loader each entry binds; the packet's
      three CENSUS lines compared with this run.
  (b) THE PACKET: committed (blob at HEAD == worktree), its keys line, REGISTRY-VINTAGE == the HEAD blob of
      data/firm_registry.json, the K-OM / K-DIR ARN lines == the derivation from that registry, the declared
      writers W per role.
  (c) THE PLAN per root, re-taken with the vendored terraform: 0 to destroy, every address with its actions, the
      planfile sha256 and the CANONICAL digest (sha256 of the sorted resource changes), each compared with the
      packet's table; every lambda update split into env / object-version / CODE; EXACTLY ONE code-carrying update
      allowed -- K-CODE's own (module.irpt_directory_search, after-hash == the built sha) -- any other is a FAIL (the
      S95 restore keeps the four drifted functions at their served bytes); the version-only bumps NAMED as noise.
  (c-code) K-CODE: the built irpt-directory-search artifact AT REST -- the latest version is the built version, its
      metadata and re-downloaded bytes equal the built sha, the rollback-source version is still present and equal
      to the prior live CodeSha256, and the function is still UNCHANGED (the build deployed nothing).
  (d) THE HALVES at HEAD naming the packet blob, 2 of 2 -- ABSENT is a truthful STOP.
Every arm prints the identity it ran as; none of (a)-(d) claims a served behaviour (the identity bar binds (f)).
Read-only on every live plane. No apply. Prints no credential.
"""
from __future__ import annotations

import base64
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-10_R67-AC1_battery_output.txt")
TOKEN = "IBR67-SERVING-ROLES-GRANTED-AND-PATH-RESOLVES"
PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-10.md"
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
KCODE_FN = "irpt-directory-search"
KCODE_PRIOR_LIVE = "aQxATFkcdtEBvs+v/zztQBOPcbR9XH9Lzjm9kUOmhmU="
KCODE_PRIOR_VERSION = "l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4"
KCODE_BUILT = "HOpXPDoHhrVK/ayqsx1uKgzt9mWOjDlK+Ix2CPbCamI="
KCODE_BUILT_VERSION = "hk9OUfwHZxlcwZDqN7cEknbJOXtvB3jd"
KCODE_ADDRESS = "module.irpt_directory_search.aws_lambda_function.this"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
LINES: list[str] = []
IDENTITY: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=120)
    return out.returncode, out.stdout


def identity_line(arm: str) -> None:
    if not IDENTITY:
        IDENTITY.append(boto3.client("sts").get_caller_identity()["Arn"])
    emit("  identity: %s ran as %s -- a configuration/document claim, NOT a served behaviour" % (arm, IDENTITY[0]))


def client_firms() -> list[dict]:
    reg = json.load(open(os.path.join(WS, "data", "firm_registry.json"), encoding="utf-8"))
    return [f for f in reg["firms"] if f.get("kind") == "client" and f.get("enabled")]


def arm_a(packet_text: str) -> bool:
    emit("(a) CENSUS -- the 7 serving functions, measured")
    identity_line("(a)")
    iam = boto3.client("iam")
    lam = boto3.client("lambda", region_name="us-east-1")
    firms = client_firms()

    def sim(src: str, res: str) -> str:
        return iam.simulate_principal_policy(PolicySourceArn=src, ActionNames=["s3:GetObject"],
                                             ResourceArns=[res])["EvaluationResults"][0]["EvalDecision"]
    om_ok = dir_ok = maps = 0
    for fn, (_root, _res, role, entry) in FUNCS.items():
        cfg = lam.get_function_configuration(FunctionName=fn)
        env = (cfg.get("Environment") or {}).get("Variables") or {}
        live_role = cfg["Role"].split("/")[-1]
        src = "arn:aws:iam::%s:role/%s" % (ACCT, live_role)
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
    neg = sim("arn:aws:iam::%s:role/opalinvest-auth-lambda-role" % ACCT, "arn:aws:s3:::%s/platinum/%s/ownership_map.json" % (firms[0]["bucket"], firms[0]["firm_id"]))
    n = len(FUNCS) * len(firms)
    emit("  ownership map readable: %d of %d; directory readable: %d of %d; bucket map present: %d of %d; client firms %d (registry)"
         % (om_ok, n, dir_ok, n, maps, len(FUNCS), len(firms)))
    emit("  controls: positive (user Andrew_Berman) %s; negative (opalinvest-auth-lambda-role) %s" % (pos, neg))
    stated = {"CENSUS-OWNERSHIP-GRANTED": "%d of %d" % (om_ok, n), "CENSUS-DIRECTORY-READ": "%d of %d" % (dir_ok, n),
              "CENSUS-BUCKET-MAP-PRESENT": "%d of %d" % (maps, len(FUNCS))}
    for k, v in stated.items():
        m = re.search(r"%s: (\d+ of \d+)" % k, packet_text)
        emit("  packet line %s: packet %s, this run %s -> %s" % (k, m.group(1) if m else "ABSENT", v,
                                                                 "EQUAL" if m and m.group(1) == v else "DIFFERS"))
    return pos == "allowed" and neg != "allowed" and len(firms) > 0


def arm_b() -> tuple[bool, str, str]:
    emit("(b) THE PACKET -- committed, its keys, the registry vintage and ARN lines, the declared writers")
    identity_line("(b)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    ok = bool(head) and head == wt.strip()
    text = git("show", "HEAD:" + PACKET_REL)[1] if head else ""
    emit("  packet %s: blob at HEAD %s, worktree %s -> %s" % (PACKET_REL, head or "ABSENT", wt.strip(),
                                                              "COMMITTED, UNCHANGED" if ok else "NOT COMMITTED OR CHANGED"))
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
    emit("  W(each function's environment) = 1 declared (its yang-lambda module); console/CLI writes are the unenumerable "
         "qualifier (NEVER-9), covered by the rollback's re-read")
    return ok and bool(keys) and vint_ok and arns_ok, head, text


def arm_c(packet_text: str) -> bool:
    emit("(c) THE PLAN per root, re-taken with the vendored terraform -- applied to nothing")
    identity_line("(c)")
    os.makedirs(PLAN_DIR, exist_ok=True)
    env = dict(os.environ, TF_IN_AUTOMATION="1", AWS_REGION="us-east-1",
               TF_PLUGIN_CACHE_DIR=os.path.join(WS, ".scratch", "tf-plugin-cache"))
    os.makedirs(env["TF_PLUGIN_CACHE_DIR"], exist_ok=True)
    roots = sorted({v[0] for v in FUNCS.values()}, key=lambda r: list(v[0] for v in FUNCS.values()).index(r))
    n_ok = destroy_total = changes_total = code_carrying = 0
    noise: list[str] = []
    digests_ok = planned = 0
    kcode_in_plan = unexpected_code = 0
    for r in roots:
        d = os.path.join(TF_ROOT, r)
        pf = os.path.join(PLAN_DIR, r + ".tfplan")
        i = subprocess.run([TF, "-chdir=" + d, "init", "-input=false", "-no-color"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=900)
        p = subprocess.run([TF, "-chdir=" + d, "plan", "-input=false", "-no-color", "-out=" + pf], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=env, timeout=1200) if i.returncode == 0 else i
        if p.returncode != 0:
            emit("  %-11s init/plan rc %d: %s" % (r, p.returncode, (p.stderr or p.stdout)[-300:].replace("\n", " ")))
            continue
        line = next((ln.strip() for ln in p.stdout.splitlines() if ln.startswith("Plan:") or "No changes." in ln), "?")
        j = json.loads(subprocess.run([TF, "-chdir=" + d, "show", "-json", pf], capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", env=env, timeout=600).stdout)
        rcs = [c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]]
        canon = [{"address": c["address"], "actions": c["change"]["actions"], "before": c["change"].get("before"),
                  "after": c["change"].get("after")} for c in rcs]
        digest = hashlib.sha256(json.dumps(canon, sort_keys=True).encode("utf-8")).hexdigest()
        raw = hashlib.sha256(open(pf, "rb").read()).hexdigest()
        destroys = sum("delete" in c["change"]["actions"] for c in rcs)
        planned += 1
        destroy_total += destroys
        changes_total += len(rcs)
        in_packet = digest in packet_text
        digests_ok += in_packet
        n_ok += destroys == 0
        emit("  %-11s %s destroy %d | planfile sha256 %s | canonical digest %s (%s in the packet)"
             % (r, line, destroys, raw, digest, "EQUAL to the one" if in_packet else "NOT"))
        for c in rcs:
            kinds = ""
            if c["change"]["actions"] == ["update"] and c["type"] == "aws_lambda_function":
                b, a = c["change"]["before"] or {}, c["change"]["after"] or {}
                code = b.get("source_code_hash") != a.get("source_code_hash")
                ver = b.get("s3_object_version") != a.get("s3_object_version")
                envc = b.get("environment") != a.get("environment")
                code_carrying += code
                if code and c["address"] == KCODE_ADDRESS and a.get("source_code_hash") == KCODE_BUILT:
                    kcode_in_plan += 1
                elif code:
                    unexpected_code += 1
                if ver and not code:
                    noise.append(c["address"])
                kinds = " [env %s; object version %s; CODE %s]" % ("changes" if envc else "same", "changes" if ver else "same",
                                                                  "CHANGES (%s -> %s)" % (b.get("source_code_hash"), a.get("source_code_hash")) if code else "unchanged")
            emit("     %-8s %s%s" % ("/".join(c["change"]["actions"]), c["address"], kinds))
    emit("  roots planned without destroy: %d of %d; total destroy %d; total changes %d; lambda updates carrying a CODE change %d "
         "(K-CODE's own, after-hash == built: %d; any other: %d -- 0 allowed)"
         % (n_ok, len(roots), destroy_total, changes_total, code_carrying, kcode_in_plan, unexpected_code))
    emit("  canonical digests equal to the packet's: %d of %d" % (digests_ok, len(roots)))
    emit("  accepted plan noise -- object-version-only bumps, source_code_hash unchanged: %d: %s" % (len(noise), noise))
    for k, v in (("PLAN-ROOTS", "%d of %d planned; destroy %d of %d; changes %d" % (planned, len(roots), planned - n_ok, len(roots), changes_total)),
                 ("PLAN-CODE-CHANGES", "%d of %d" % (code_carrying, len(roots))),
                 ("PLAN-CODE-CHANGE-ADDRESS", "%s %s -> %s" % (KCODE_ADDRESS, KCODE_PRIOR_LIVE, KCODE_BUILT)
                  if kcode_in_plan == 1 else "ABSENT FROM THE PLAN")):
        m = re.search(r"%s: (.+)" % k, packet_text)
        emit("  packet line %s: packet '%s', this run '%s' -> %s" % (k, m.group(1).strip() if m else "ABSENT", v,
                                                                   "EQUAL" if m and m.group(1).strip() == v else "DIFFERS"))
    return (n_ok == len(roots) and destroy_total == 0 and kcode_in_plan == 1 and unexpected_code == 0
            and digests_ok == len(roots))


def arm_c_code() -> bool:
    emit("(c-code) K-CODE -- %s rebuilt from HEAD, AT REST (S96 ruling (i) @6e027591fc)" % KCODE_FN)
    identity_line("(c-code)")
    lam = boto3.client("lambda", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    key = "investor-reporting/%s.zip" % KCODE_FN
    live = lam.get_function_configuration(FunctionName=KCODE_FN)["CodeSha256"]
    head = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=key)
    latest, meta = head.get("VersionId"), (head.get("Metadata") or {}).get("content-sha256")
    body = s3.get_object(Bucket=ARTIFACT_BUCKET, Key=key, VersionId=latest)["Body"].read()
    got = base64.b64encode(hashlib.sha256(body).digest()).decode()
    prior = s3.get_object(Bucket=ARTIFACT_BUCKET, Key=key, VersionId=KCODE_PRIOR_VERSION)["Body"].read()
    prior_sha = base64.b64encode(hashlib.sha256(prior).digest()).decode()
    checks = {
        "latest version == built version": latest == KCODE_BUILT_VERSION,
        "metadata == built sha": meta == KCODE_BUILT,
        "re-downloaded bytes == built sha": got == KCODE_BUILT,
        "rollback source present and == prior live": prior_sha == KCODE_PRIOR_LIVE,
        "function unchanged (== prior live)": live == KCODE_PRIOR_LIVE,
    }
    emit("  build store latest version %s (built %s) content-sha256 %s; re-downloaded sha256(b64) %s; built %s"
         % (latest, KCODE_BUILT_VERSION, meta, got, KCODE_BUILT))
    emit("  rollback source version %s sha256(b64) %s (prior live %s)" % (KCODE_PRIOR_VERSION, prior_sha, KCODE_PRIOR_LIVE))
    emit("  function %s CodeSha256 %s" % (KCODE_FN, live))
    for k, v in checks.items():
        emit("  K-CODE %s: %s" % (k, "OK" if v else "FAIL"))
    emit("  K-CODE at rest: %d of %d checks hold" % (sum(checks.values()), len(checks)))
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


def main() -> int:
    emit("IB-rtf-10 R67-AC1 battery (third pass) -- worktree HEAD %s" % git("rev-parse", "HEAD")[1].strip())
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
    arms = {"(a) census": a_ok, "(b) packet": b_ok, "(c) plan": c_ok, "(c-code) K-CODE built": k_ok, "(d) halves": d_ok}
    if not d_ok:
        emit("STOP at (d): a half is ABSENT -- nothing is applied; (e) apply and (f) the live proof are NOT RUN")
        arms["(e) apply"] = False
        arms["(f) live proof"] = False
    else:
        emit("(d) holds -- (e)/(f) are the next pass's arms and are not implemented in this third-pass revision")
        arms["(e) apply"] = False
        arms["(f) live proof"] = False
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else ("NOT RUN" if k.startswith(("(e)", "(f)")) else "FAIL")))
    if all(arms.values()):
        emit("RESULT: R67-AC1 PASS")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R67-AC1 FAIL -- %d of %d arms hold (third pass: STOP at the halves as the face expects)"
             % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
