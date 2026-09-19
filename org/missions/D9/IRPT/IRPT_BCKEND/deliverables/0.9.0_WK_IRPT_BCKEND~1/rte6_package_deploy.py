#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rte-6 arm (c) -- package, upload and verify the 7 functions this cell
changed. SHARED_ROOTS resolution adapted from the sibling ~2 slot's
`rt6_package.py` (source_dir first, then lib/, _authz/, _scope/, _keys/, _ids/ --
including `_ids/data/` for a subdirectory-declared member), because
`build-and-upload.sh`'s generic packer cannot resolve a file that is not physically
present in the function's own `source_dir` (rows IRPT_BCKEND-W1-S19/S20; the untracked
production-source-file class).

Builds a deterministic zip per function, uploads it to
s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip with the
`content-sha256` metadata `yang-lambda` reads, and verifies the served `CodeSha256`
against the built artifact AFTER a `terraform apply` (run separately, by hand, under
`.tools/safe-apply.sh`, per root -- this script does not apply).

Usage:
  py -3.12 rte6_package_deploy.py build            # build + print resolved members
  py -3.12 rte6_package_deploy.py upload           # build + upload every changed function
  py -3.12 rte6_package_deploy.py verify           # read served CodeSha256, compare to built

NO AWS CALL under `build`. `upload` and `verify` are the only network-touching verbs.
ASCII only.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
OUT = os.path.join(REPO, ".scratch", "rte6-zips")
IRPT_ROOT = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")

SHARED_ROOTS = [
    os.path.join(REPO, "lib"),
    os.path.join(IRPT_ROOT, "_authz"),
    os.path.join(IRPT_ROOT, "_scope"),
    os.path.join(IRPT_ROOT, "_keys"),
    os.path.join(IRPT_ROOT, "_ids"),
    os.path.join(IRPT_ROOT, "_ids", "data"),
    # FALLBACK ONLY, LOWEST PRIORITY: `irpt-status`'s declared `files[]` names `handler.py` and
    # `checkpoint.py`, neither of which exists in `source_dir` or any shared root -- the SAME
    # untracked-production-source-file class IB-rtd-8 named for `irpt-holdings`'s
    # `served.py`/`loaders.py` (row IRPT_BCKEND-W1-S20). Extracted UNCHANGED from the
    # currently-deployed zip (`.tools/aws lambda get-function`, this cell), materialized here for
    # the build only, never committed. See the surprise row this cell files for `irpt-status`.
    os.path.join(REPO, ".scratch", "ops_extracted"),
    # SAME CLASS, `irpt-ycharts-generate`: `gate.py`, `firm_destination_policy.json`,
    # `firm_registry.json`, `settings.json` -- none present in `source_dir` or a shared root.
    # Extracted UNCHANGED from the currently-deployed zip, this cell, never committed.
    os.path.join(REPO, ".scratch", "ycharts_extracted"),
]

ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ZIP_DATE = (2026, 9, 18, 0, 0, 0)

# THE 7 FUNCTIONS THIS CELL WIRED. `ids.py` and the bundled seam data file
# are added to whichever function's declared `files[]` does not already carry them --
# every one of these 7 now imports `_ids` (row IRPT_BCKEND-W1-S22's fix).
FUNCTIONS = ("irpt-directory-search", "irpt-export-render", "irpt-holdings",
             "irpt-narrative", "irpt-status", "irpt-performance-adapter",
             "irpt-ycharts-generate")

EXTRA_MEMBERS = ("ids.py", "data/custodian_key_seam.json")


def source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
        return json.load(fh)


def declared_files(fn):
    files = list(source_map()["functions"][fn].get("files") or [])
    for extra in EXTRA_MEMBERS:
        if extra not in files:
            files.append(extra)
    return files


def resolve(source_dir, name):
    p = os.path.join(source_dir, name.replace("/", os.sep))
    if os.path.isfile(p):
        return p, "source_dir"
    for root in SHARED_ROOTS:
        q = os.path.join(root, os.path.basename(name))
        if os.path.isfile(q):
            return q, os.path.relpath(root, REPO).replace(os.sep, "/")
    return None, None


def build(fn):
    sm = source_map()["functions"][fn]
    source_dir = os.path.join(REPO, sm["source_dir"].replace("/", os.sep))
    files = declared_files(fn)
    members, where, unresolved = {}, {}, []
    for name in files:
        path, origin = resolve(source_dir, name)
        if path is None:
            unresolved.append(name)
            continue
        members[name] = path
        where[name] = origin
    os.makedirs(OUT, exist_ok=True)
    zip_path = os.path.join(OUT, "%s.zip" % fn)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arc in sorted(members):
            info = zipfile.ZipInfo(arc, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.create_system = 0
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(members[arc], "rb") as fh:
                zf.writestr(info, fh.read())
    with open(zip_path, "rb") as fh:
        raw = fh.read()
    sha_b64 = base64.b64encode(hashlib.sha256(raw).digest()).decode("ascii")
    return {"function": fn, "zip_path": zip_path, "sha256_b64": sha_b64,
            "size": len(raw), "members": sorted(members), "where": where,
            "unresolved": unresolved, "declared_count": len(files)}


def cmd_build():
    out = []
    for fn in FUNCTIONS:
        rec = build(fn)
        print("=== %s ===" % fn)
        print("  declared: %d  resolved: %d  unresolved: %s"
              % (rec["declared_count"], len(rec["members"]), rec["unresolved"]))
        print("  sha256(b64)=%s size=%d" % (rec["sha256_b64"], rec["size"]))
        for m in rec["members"]:
            print("    %-40s <- %s" % (m, rec["where"][m]))
        out.append(rec)
        if rec["unresolved"]:
            print("BLOCKED: %s has UNRESOLVED members" % fn)
            return 1, out
    return 0, out


def cmd_upload():
    rc, recs = cmd_build()
    if rc != 0:
        return rc
    aws = os.path.join(REPO, ".tools", "aws.cmd")
    for rec in recs:
        fn = rec["function"]
        key = "investor-reporting/%s.zip" % fn
        # Verified existence BEFORE upload (the pre-fix bytes, for the negative control).
        pre = subprocess.run([aws, "lambda", "get-function-configuration",
                             "--function-name", fn, "--query", "CodeSha256",
                             "--output", "text"], capture_output=True, text=True, timeout=60)
        print("%s PRE-UPLOAD served CodeSha256: %s" % (fn, (pre.stdout or "").strip()))
        cp = subprocess.run(
            [aws, "s3", "cp", rec["zip_path"], "s3://%s/%s" % (ARTIFACT_BUCKET, key),
             "--metadata", "content-sha256=%s" % rec["sha256_b64"], "--region", "us-east-1"],
            capture_output=True, text=True, timeout=120)
        print("%s UPLOAD rc=%s %s" % (fn, cp.returncode, (cp.stderr or cp.stdout or "").strip()[:200]))
        if cp.returncode != 0:
            return 1
        head = subprocess.run(
            [aws, "s3api", "head-object", "--bucket", ARTIFACT_BUCKET, "--key", key],
            capture_output=True, text=True, timeout=60)
        try:
            meta = json.loads(head.stdout)
        except Exception:
            meta = {}
        served_meta = (meta.get("Metadata") or {}).get("content-sha256")
        ok = (meta.get("ContentLength") == rec["size"] and served_meta == rec["sha256_b64"])
        print("%s VERIFY-UPLOAD size=%s/%s meta=%s ok=%s"
              % (fn, meta.get("ContentLength"), rec["size"], served_meta, ok))
        if not ok:
            print("BLOCKED: %s upload did not verify" % fn)
            return 1
    return 0


def cmd_verify():
    aws = os.path.join(REPO, ".tools", "aws.cmd")
    _rc, recs = cmd_build()
    by_fn = {r["function"]: r for r in recs}
    all_ok = True
    for fn in FUNCTIONS:
        cfg = subprocess.run([aws, "lambda", "get-function-configuration",
                             "--function-name", fn], capture_output=True, text=True, timeout=60)
        try:
            data = json.loads(cfg.stdout)
        except Exception:
            data = {}
        served = data.get("CodeSha256")
        built_b64 = by_fn[fn]["sha256_b64"] if fn in by_fn else None
        ok = served == built_b64
        all_ok = all_ok and ok
        print("%s served=%s built=%s MATCH=%s" % (fn, served, built_b64, ok))
    return 0 if all_ok else 1


def main():
    verb = sys.argv[1] if len(sys.argv) > 1 else "build"
    if verb == "build":
        rc, _ = cmd_build()
        return rc
    if verb == "upload":
        return cmd_upload()
    if verb == "verify":
        return cmd_verify()
    print("unknown verb: %s" % verb)
    return 2


if __name__ == "__main__":
    sys.exit(main())
