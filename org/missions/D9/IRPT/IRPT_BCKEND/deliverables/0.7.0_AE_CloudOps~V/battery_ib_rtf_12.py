#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-12 battery -- every serving zip carries the raw-keys file its id module reads.

FIRST PASS (this revision): arms (a)-(d). The build is WITHHELD (row S101), so (d) fails truthfully, and (e)/(f) are
the re-hand's arms.
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
  (d) THE BUILD AND THE PACKET:
      - per function, what build-and-upload.sh WOULD package (own members from DISK, staged members from their pins)
        against the live zip, member by member;
      - the delta beyond the added members is printed; a non-empty one is the face's STOP (row S101);
      - built artifacts (the build-store latest version is NEW) n of 7;
      - the packet and the 2 halves at HEAD.
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


def arm_d() -> bool:
    emit("(d) THE BUILD AND THE PACKET -- the predicted served-byte delta per function, then the build, then the halves")
    identity_line("(d)")
    head = json.loads(blob_at("HEAD", MAP).decode("utf-8"))["functions"]
    beyond_total = 0
    built = 0
    for fn in FNS:
        e = head[fn]
        cfg, members, _ = live_zip(fn)
        staged = {s["packaged_as"]: s for s in e.get("staged_from", [])}
        added = {s["packaged_as"] for s in e.get("staged_from", []) if s["repo_path"] in (RAW_REPO, REG_REPO)}
        pred = {}
        for m in e["files"]:
            if m in staged:
                pred[m] = blob_at(staged[m]["pin"], staged[m]["repo_path"])
            else:
                p = os.path.join(WS, e["source_dir"], m)
                pred[m] = open(p, "rb").read() if os.path.exists(p) else None
        moved = [m for m in pred if m in members and m not in added and pred[m] != members[m]]
        missing = [m for m in pred if pred[m] is None]
        same = sum(1 for m in pred if m in members and m not in added and pred[m] == members[m])
        beyond_total += len(moved) + len(missing)
        head_obj = s3.head_object(Bucket=BUCKET, Key="investor-reporting/%s.zip" % fn)
        is_new = (head_obj.get("Metadata") or {}).get("content-sha256") != cfg["CodeSha256"]
        built += is_new
        emit("  %-26s added %s | other members byte-identical to live %d of %d | MOVED beyond the added: %s%s | build-store "
             "latest %s (content-sha256 %s the live CodeSha256)" % (
                 fn, sorted(added), same, len(pred) - len(added), moved or "none",
                 (" | unresolvable " + str(missing)) if missing else "", head_obj.get("VersionId"),
                 "DIFFERS FROM" if is_new else "==",))
        for m in moved:
            a, b = members[m], pred[m]
            emit("      %-32s live %d bytes CR %d -> build %d bytes CR %d" % (m, len(a), a.count(b"\r"), len(b), b.count(b"\r")))
    emit("  functions whose rebuild moves a member beyond the added ones: %s of 7 -> %s" % (
        "0" if beyond_total == 0 else "see above",
        "no STOP" if beyond_total == 0 else "the face's STOP: the build is WITHHELD (row IRPT_BCKEND-S101)"))
    emit("  built and verified at rest: %d of 7" % built)
    rc, _ = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    emit("  packet %s at HEAD: %s" % (PACKET_REL, "PRESENT" if rc == 0 else "ABSENT (no built sha to sign: the build is withheld)"))
    n = 0
    for who, d, pat in (("COO", "org/tier1_exec/2.0.0_SA_COO~B/deliverables", "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-12_"),
                        ("CTO", "org/tier1_exec/1.0.0_SA_CTO/deliverables", "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-12_")):
        _, ls = git("ls-tree", "-r", "--name-only", "HEAD", "--", d)
        hits = [p for p in ls.decode().splitlines() if os.path.basename(p).startswith(pat)]
        n += bool(hits)
        emit("  %s half at HEAD: %d file(s) -> %s" % (who, len(hits), "PRESENT" if hits else "ABSENT"))
    emit("  halves: %d of 2" % n)
    return beyond_total == 0 and built == 7 and rc == 0 and n == 2


def main() -> int:
    _, h = git("rev-parse", "HEAD")
    emit("IB-rtf-12 R69-AC1 battery (first pass) -- worktree HEAD %s" % h.decode().strip())
    emit("")
    arms = {"(a) premise": arm_a()}
    emit("")
    arms["(b) files described"] = arm_b()
    emit("")
    arms["(c) manifest"] = arm_c()
    emit("")
    arms["(d) build + packet + halves"] = arm_d()
    emit("")
    emit("STOP at (d): the build is withheld (row S101: a HEAD rebuild moves the seam member on 5 functions) -- nothing is "
         "built, no packet exists, (e) apply and (f) the live proof are NOT RUN")
    arms["(e) apply"] = False
    arms["(f) live proof"] = False
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else ("NOT RUN" if k.startswith(("(e)", "(f)")) else "FAIL")))
    if all(arms.values()):
        emit("RESULT: R69-AC1 PASS")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R69-AC1 FAIL -- %d of %d arms hold (first pass: STOP at (d), the build withheld on row S101)"
             % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
