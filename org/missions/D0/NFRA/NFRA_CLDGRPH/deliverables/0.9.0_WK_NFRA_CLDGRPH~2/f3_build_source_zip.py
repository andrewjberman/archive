#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-F-3 (CG-s-23) -- build the stitch source zip LOCALLY.

The SECOND route. The FIRST route is .github/workflows/stitch-source-push.yml,
which fires only on a push to CLOUD (0.0.0_AB_MSTR's act) and whose portal
checkout needs secrets.PORTAL_REPO_PAT. This script reproduces that workflow's
own recipe byte-for-byte in intent, from a local worktree:

    zip -r -q /tmp/stitch-source.zip \
      portal/src org/modules infra/aws .tools stitch_source_sha.txt \
      -x '*/node_modules/*' '*/.terraform/*' '*/__pycache__/*' '*.pyc'
    find data -path '*/scripts/*' -name '*.py' -print | zip -q ... -@

portal/ is a bare gitlink in this repo (mode 160000, no .gitmodules), so
portal/src is taken from a SEPARATE portal checkout named on the command line
and its HEAD is recorded.  stitch_source_sha.txt = the superproject HEAD.

Usage:
  python f3_build_source_zip.py --repo <worktree> --portal <portal checkout> --out <zip>
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile

EXCLUDE_DIR_PARTS = ("node_modules", ".terraform", "__pycache__", ".git")
BASE_TREES = ("org/modules", "infra/aws", ".tools")


def _skip(rel: str) -> bool:
    parts = rel.replace("\\", "/").split("/")
    if any(p in EXCLUDE_DIR_PARTS for p in parts):
        return True
    return rel.endswith(".pyc")


def _walk(root: str, sub: str):
    base = os.path.join(root, sub)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIR_PARTS]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if _skip(rel):
                continue
            yield full, rel


def _data_scripts(root: str):
    """find data -path '*/scripts/*' -name '*.py'"""
    base = os.path.join(root, "data")
    if not os.path.isdir(base):
        return
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIR_PARTS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if "/scripts/" not in rel:
                continue
            if _skip(rel):
                continue
            yield full, rel


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--portal", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", default="")
    a = ap.parse_args()

    repo = os.path.abspath(a.repo)
    portal = os.path.abspath(a.portal)

    head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    portal_head = subprocess.run(["git", "-C", portal, "rev-parse", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.strip()
    portal_files = subprocess.run(["git", "-C", portal, "ls-files", "src"],
                                  capture_output=True, text=True, check=True).stdout
    portal_rel = [ln.strip() for ln in portal_files.splitlines() if ln.strip()]

    counts = {}
    if os.path.exists(a.out):
        os.remove(a.out)
    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        n = 0
        for rel in portal_rel:
            full = os.path.join(portal, rel.replace("/", os.sep))
            if not os.path.isfile(full) or _skip(rel):
                continue
            z.write(full, "portal/" + rel)
            n += 1
        counts["portal/src"] = n
        for sub in BASE_TREES:
            n = 0
            for full, rel in _walk(repo, sub):
                z.write(full, rel)
                n += 1
            counts[sub] = n
        z.writestr("stitch_source_sha.txt", head + "\n")
        counts["stitch_source_sha.txt"] = 1
        n = 0
        for full, rel in _data_scripts(repo):
            z.write(full, rel)
            n += 1
        counts["data/*/scripts/**/*.py"] = n

    size = os.path.getsize(a.out)
    sha = hashlib.sha256(open(a.out, "rb").read()).hexdigest()
    with zipfile.ZipFile(a.out) as z:
        names = z.namelist()
    rep = {
        "zip": os.path.abspath(a.out),
        "bytes": size,
        "sha256": sha,
        "entries": len(names),
        "counts": counts,
        "repo_head": head,
        "portal_checkout": portal,
        "portal_head": portal_head,
        "portal_src_files": counts["portal/src"],
    }
    print(json.dumps(rep, indent=2))
    if a.report:
        with open(a.report, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
