#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-10 battery -- the serving roles granted the ownership map and the bucket map.

FIRST PASS (this revision): arms (a)-(d). (e) apply and (f) the live proof run only on the re-hand, after both
never-widen halves are at HEAD naming the packet blob; with a half ABSENT the battery STOPS at (d) and says so.
  (a) CENSUS of the 7 serving functions: role; s3:GetObject on each client firm's ownership map AND on its
      directory pointer (simulate-principal-policy, one resource per call, a positive and a negative control);
      IRPT_DIRECTORY_BUCKET_MAP in the deployed environment; the runtime loader each entry binds; the packet's
      census lines compared with this run.
  (b) THE PACKET: committed (blob at HEAD == worktree), its keys line, and the declared writers W per role.
  (c) THE PLAN per root, re-taken with the vendored terraform: 0 to destroy, every address with its actions, the
      planfile sha256 and the CANONICAL digest (sha256 of the sorted resource changes), each compared with the
      packet's table; every lambda update split into env-only vs code-carrying (source_code_hash / object version).
  (d) THE HALVES at HEAD naming the packet blob, 2 of 2 -- ABSENT is a truthful STOP.
Read-only on every live plane. No apply. Prints no credential.
"""
from __future__ import annotations

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
LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=120)
    return out.returncode, out.stdout


def client_firms() -> list[dict]:
    reg = json.load(open(os.path.join(WS, "data", "firm_registry.json"), encoding="utf-8"))
    return [f for f in reg["firms"] if f.get("kind") == "client" and f.get("enabled")]


def arm_a(packet_text: str) -> bool:
    emit("(a) CENSUS -- the 7 serving functions, measured")
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
    stated = {"CENSUS-OWNERSHIP-GRANTED": "%d of %d" % (om_ok, n), "CENSUS-BUCKET-MAP-PRESENT": "%d of %d" % (maps, len(FUNCS))}
    for k, v in stated.items():
        m = re.search(r"%s: (\d+ of \d+)" % k, packet_text)
        emit("  packet line %s: packet %s, this run %s -> %s" % (k, m.group(1) if m else "ABSENT", v,
                                                                 "EQUAL" if m and m.group(1) == v else "DIFFERS"))
    return pos == "allowed" and neg != "allowed" and len(firms) > 0


def arm_b() -> tuple[bool, str, str]:
    emit("(b) THE PACKET -- committed, its keys, the declared writers")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    ok = bool(head) and head == wt.strip()
    text = git("show", "HEAD:" + PACKET_REL)[1] if head else ""
    emit("  packet %s: blob at HEAD %s, worktree %s -> %s" % (PACKET_REL, head or "ABSENT", wt.strip(),
                                                              "COMMITTED, UNCHANGED" if ok else "NOT COMMITTED OR CHANGED"))
    keys = re.search(r"PACKET-KEYS: (.+)", text)
    emit("  packet keys line: %s" % (keys.group(1) if keys else "ABSENT"))
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
    return ok and bool(keys), head, text


def arm_c(packet_text: str) -> bool:
    emit("(c) THE PLAN per root, re-taken with the vendored terraform -- applied to nothing")
    os.makedirs(PLAN_DIR, exist_ok=True)
    env = dict(os.environ, TF_IN_AUTOMATION="1", AWS_REGION="us-east-1",
               TF_PLUGIN_CACHE_DIR=os.path.join(WS, ".scratch", "tf-plugin-cache"))
    os.makedirs(env["TF_PLUGIN_CACHE_DIR"], exist_ok=True)
    roots = sorted({v[0] for v in FUNCS.values()}, key=lambda r: list(v[0] for v in FUNCS.values()).index(r))
    n_ok = destroy_total = changes_total = code_carrying = 0
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
        destroy_total += destroys
        changes_total += len(rcs)
        in_packet = digest in packet_text
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
                kinds = " [env %s; object version %s; CODE %s]" % ("changes" if envc else "same", "changes" if ver else "same",
                                                                  "CHANGES (%s -> %s)" % (b.get("source_code_hash"), a.get("source_code_hash")) if code else "unchanged")
            emit("     %-8s %s%s" % ("/".join(c["change"]["actions"]), c["address"], kinds))
    emit("  roots planned without destroy: %d of %d; total destroy %d; total changes %d; lambda updates carrying a CODE change %d (row S95)"
         % (n_ok, len(roots), destroy_total, changes_total, code_carrying))
    return n_ok == len(roots) and destroy_total == 0


def arm_d(blob: str) -> bool:
    emit("(d) THE HALVES at HEAD naming the packet blob")
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
    emit("IB-rtf-10 R67-AC1 battery (first pass) -- worktree HEAD %s" % git("rev-parse", "HEAD")[1].strip())
    emit("")
    b_ok, blob, packet_text = arm_b()
    emit("")
    a_ok = arm_a(packet_text)
    emit("")
    c_ok = arm_c(packet_text)
    emit("")
    d_ok = arm_d(blob)
    emit("")
    arms = {"(a) census": a_ok, "(b) packet": b_ok, "(c) plan": c_ok, "(d) halves": d_ok}
    if not d_ok:
        emit("STOP at (d): a half is ABSENT -- nothing is applied; (e) apply and (f) the live proof are NOT RUN")
        arms["(e) apply"] = False
        arms["(f) live proof"] = False
    else:
        emit("(d) holds -- (e)/(f) are the re-hand's arms and are not implemented in this first-pass revision")
        arms["(e) apply"] = False
        arms["(f) live proof"] = False
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else ("NOT RUN" if k.startswith(("(e)", "(f)")) else "FAIL")))
    if all(arms.values()):
        emit("RESULT: R67-AC1 PASS")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R67-AC1 FAIL -- %d of %d arms hold (first pass: STOP at the halves as the face expects)"
             % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
