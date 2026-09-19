#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-12 battery -- every serving zip carries the raw-keys file its id module reads.

SECOND PASS (this revision; rulings msg 98279: S101 accepted, S102 ycharts deferred -> K-CODE x 6, S100 recorded-not-
counted): arms (a)-(d); (d) STOPS at the halves (the expected outcome); (e)/(f) are the third pass's arms.
  (a) THE PREMISE AT THE CUT (@083cc54350) AND AT HEAD:
      - _ids/raw_keys.json staged per function;
      - a raw_keys.json member in each LIVE zip (downloaded; sha256 == the live CodeSha256; member count printed);
      - ids.py:64 and :162 cited with the bytes at those lines;
      - the census of every file _ids/ids.py opens relative to its own location, n of n, each classed per function as
        PRESENT / RESOLVED-VIA-ENV / MISSING on the deployed layout (the zip at /var/task, the layer at /opt/python,
        the env).
  (b) THE FILES, DESCRIBED FOR THE HALVES: blob, bytes, top-level shape, k entries, credential scan, writers W.
  (c) THE MANIFEST: the parse-diff from the cut to HEAD. Exactly 7 raw_keys.json + 4 firm_registry.json objects added
      (row S99 INCLUDES the second member), files[] +11, artifact_sha256 untouched 7 of 7, nothing else moved.
  (d) THE BUILD, THE PLANS, THE PACKET, THE HALVES (K-CODE x 6):
      - per function: the build-store latest version == the packet's BUILT version, and metadata == bytes == the built
        sha; the rollback source (the packet's prior version) hashes to the prior live CodeSha256; the function is
        still unchanged; members == files[]; the delta vs the LIVE zip == exactly the added member(s) + the seam line
        endings (S101); the own CRLF members byte-identical to live;
      - plans per root re-taken: 0 destroy; code changes exactly the 6, each after-hash == its built sha with the env
        unchanged; ycharts "No changes"; every canonical digest EQUAL to the packet's;
      - the packet committed; the 2 halves at HEAD naming its blob.
Read-only on every live plane. Prints no credential.
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
    emit("  raw_keys.json in the live zips: %d of 7 (the premise)" % in_zip)
    return staged_cut == 0 and in_zip == 0 and ok_zip and len(opens) >= 3


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


DEFERRED = "irpt-ycharts-generate"  # S102
PACKET_BLOB_CHECK = True
SEAM = "data/custodian_key_seam.json"
ROOT_OF = {"irpt-directory-search": "directory", "irpt-status": "ops", "irpt-holdings": "holdings", "irpt-narrative": "narrative",
           "irpt-export-render": "export", "irpt-performance-adapter": "performance"}
ADDR_OF = {"irpt-directory-search": "module.irpt_directory_search.aws_lambda_function.this",
           "irpt-status": "module.irpt_status.aws_lambda_function.this",
           "irpt-holdings": "module.irpt_holdings.aws_lambda_function.this",
           "irpt-narrative": "module.irpt_narrative.aws_lambda_function.this",
           "irpt-export-render": "module.irpt_export_render.aws_lambda_function.this",
           "irpt-performance-adapter": "module.irpt_performance_adapter.aws_lambda_function.this"}
TF = os.path.join(WS, ".tools", "terraform.exe")
PLAN_DIR = os.path.join(WS, ".scratch", "plans12_battery")


def packet_facts() -> tuple[str, str, dict, dict]:
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head_blob = head.decode().strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    text = (blob_at("HEAD", PACKET_REL) or b"").decode("utf-8")
    built = {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(r"^BUILT: (\S+) (\S+) (\S+)$", text, re.M)}
    prior = {}
    for m in re.finditer(r"^\| `(irpt-[a-z-]+)` \| `([A-Za-z0-9+/=]{44})` \(`([^`]+)`\)", text, re.M):
        prior[m.group(1)] = (m.group(2), m.group(3))
    return head_blob, wt.decode().strip(), built, prior


def plan_root(root: str) -> tuple[str, list, str]:
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
    rcs = [c for c in j.get("resource_changes") or [] if c["change"]["actions"] != ["no-op"]]
    canon = [{"address": c["address"], "actions": c["change"]["actions"], "before": c["change"].get("before"),
              "after": c["change"].get("after")} for c in rcs]
    return line, rcs, hashlib.sha256(json.dumps(canon, sort_keys=True).encode("utf-8")).hexdigest()


def arm_d() -> bool:
    emit("(d) THE BUILD, THE PLANS, THE PACKET, THE HALVES -- K-CODE x 6 (%s deferred, S102)" % DEFERRED)
    identity_line("(d)")
    head_blob, wt_blob, built, prior = packet_facts()
    pk_ok = bool(head_blob) and head_blob == wt_blob
    emit("  packet %s: blob at HEAD %s, worktree %s -> %s; BUILT lines %d; prior-live rows %d"
         % (PACKET_REL, head_blob or "ABSENT", wt_blob, "COMMITTED, UNCHANGED" if pk_ok else "NOT COMMITTED OR CHANGED", len(built), len(prior)))
    head = json.loads(blob_at("HEAD", MAP).decode("utf-8"))["functions"]
    ok_fns = crlf_same = crlf_total = 0
    for fn in ROOT_OF:
        e = head[fn]
        want_sha, want_ver = built.get(fn, ("?", "?"))
        prior_live, prior_ver = prior.get(fn, ("?", "?"))
        key = "investor-reporting/%s.zip" % fn
        h = s3.head_object(Bucket=BUCKET, Key=key)
        body = s3.get_object(Bucket=BUCKET, Key=key, VersionId=h["VersionId"])["Body"].read()
        rb = s3.get_object(Bucket=BUCKET, Key=key, VersionId=prior_ver)["Body"].read() if prior_ver != "?" else b""
        cfg, live_m, _ = live_zip(fn)
        z = zipfile.ZipFile(io.BytesIO(body))
        new_m = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
        added_expected = {s["packaged_as"] for s in e.get("staged_from", []) if s["repo_path"] in (RAW_REPO, REG_REPO)}
        added = set(new_m) - set(live_m)
        changed = [m for m in new_m if m in live_m and new_m[m] != live_m[m]]
        seam_only = all(m == SEAM and live_m[m].replace(b"\r\n", b"\n") == new_m[m] and new_m[m].count(b"\r") == 0 for m in changed)
        same = sum(1 for m in new_m if m in live_m and new_m[m] == live_m[m])
        staged = {s["packaged_as"] for s in e.get("staged_from", [])}
        own_crlf = [m for m in new_m if m not in staged and new_m[m].count(b"\r")]
        crlf_total += len(own_crlf)
        crlf_same += sum(1 for m in own_crlf if live_m.get(m) == new_m[m])
        checks = [h["VersionId"] == want_ver, (h.get("Metadata") or {}).get("content-sha256") == want_sha, b64sha(body) == want_sha,
                  b64sha(rb) == prior_live, cfg["CodeSha256"] == prior_live, sorted(new_m) == sorted(e["files"]),
                  added == added_expected, not (set(live_m) - set(new_m)), seam_only]
        good = all(checks)
        ok_fns += good
        emit("  %-26s built %s (version %s latest: %s; metadata == bytes == built: %s) | rollback source %s == prior live: %s | "
             "function unchanged: %s | delta: added %s, changed %s (seam line endings only: %s), other members byte-identical %d | -> %s"
             % (fn, want_sha, want_ver, h["VersionId"] == want_ver, checks[1] and checks[2], prior_ver, checks[3], checks[4],
                sorted(added), changed or "none", seam_only, same, "VERIFIED" if good else "NOT VERIFIED"))
    emit("  built and verified at rest: %d of %d; own CRLF members byte-identical to live: %d of %d" % (ok_fns, len(ROOT_OF), crlf_same, crlf_total))
    text = (blob_at("HEAD", PACKET_REL) or b"").decode("utf-8")
    dig_ok = code_ok = destroy = changes = 0
    roots = list(ROOT_OF.values()) + ["ycharts"]
    for r in roots:
        line, rcs, digest = plan_root(r)
        destroy += sum("delete" in c["change"]["actions"] for c in rcs)
        changes += len(rcs)
        in_packet = digest in text
        dig_ok += in_packet
        codes = []
        for c in rcs:
            if c["type"] == "aws_lambda_function":
                b, a = c["change"]["before"] or {}, c["change"]["after"] or {}
                if b.get("source_code_hash") != a.get("source_code_hash"):
                    fn = next((f for f, ad in ADDR_OF.items() if ad == c["address"]), None)
                    good = fn is not None and built.get(fn, ("",))[0] == a.get("source_code_hash") and b.get("environment") == a.get("environment")
                    code_ok += good
                    codes.append("%s -> %s%s" % (c["address"], a.get("source_code_hash"), " == built" if good else " NOT AS SIGNED"))
        emit("  plan %-11s %s | changes %d | canonical digest %s (%s the packet's) | %s" % (
            r, line, len(rcs), digest, "EQUAL to" if in_packet else "NOT", codes or "no code change"))
    emit("  plans: roots %d; destroy %d; changes %d; code changes == built %d of %d; digests EQUAL to the packet %d of %d"
         % (len(roots), destroy, changes, code_ok, len(ROOT_OF), dig_ok, len(roots)))
    n = 0
    for who, dd, pat in (("COO", "org/tier1_exec/2.0.0_SA_COO~B/deliverables", "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-12_"),
                         ("CTO", "org/tier1_exec/1.0.0_SA_CTO/deliverables", "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-12_")):
        _, ls = git("ls-tree", "-r", "--name-only", "HEAD", "--", dd)
        hits = [p for p in ls.decode().splitlines() if os.path.basename(p).startswith(pat)]
        naming = [p for p in hits if head_blob and head_blob in (blob_at("HEAD", p) or b"").decode("utf-8", "replace")]
        n += bool(naming)
        emit("  %s half at HEAD: %d file(s), %d naming blob %s -> %s" % (who, len(hits), len(naming), head_blob or "?", "PRESENT" if naming else "ABSENT"))
    emit("  halves: %d of 2" % n)
    return (pk_ok and ok_fns == len(ROOT_OF) and crlf_same == crlf_total and destroy == 0 and code_ok == len(ROOT_OF)
            and changes == len(ROOT_OF) and dig_ok == len(roots) and n == 2)


def main() -> int:
    _, h = git("rev-parse", "HEAD")
    emit("IB-rtf-12 R69-AC1 battery (second pass) -- worktree HEAD %s" % h.decode().strip())
    emit("")
    arms = {"(a) premise": arm_a()}
    emit("")
    arms["(b) files described"] = arm_b()
    emit("")
    arms["(c) manifest"] = arm_c()
    emit("")
    arms["(d) build + plans + packet + halves"] = arm_d()
    emit("")
    if not arms["(d) build + plans + packet + halves"]:
        emit("STOP at (d): a half is ABSENT (or a build/plan check failed above) -- nothing is applied; (e) apply and (f) the live "
             "proof are NOT RUN")
    else:
        emit("(d) holds -- (e)/(f) are the next pass's arms and are not implemented in this second-pass revision")
    arms["(e) apply"] = False
    arms["(f) live proof"] = False
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else ("NOT RUN" if k.startswith(("(e)", "(f)")) else "FAIL")))
    if all(arms.values()):
        emit("RESULT: R69-AC1 PASS")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R69-AC1 FAIL -- %d of %d arms hold (second pass: STOP at the halves as the face expects)"
             % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
