#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-12 -- deployed-bytes-vs-build-input diff for inf-etf-ownership-daily.

VERIFY-ONLY, live reads, no writes to any bucket, no update-function-code, no invoke.
Reads the live Lambda configuration + deployed zip (via a presigned GET), builds the
equivalent repo-side zip from infra/aws/lambda/ci/lambda-source-map.json's declared
`files` list for this function, and compares FILE BY FILE (never whole-zip hash, since
zip bytes differ by timestamp even for identical members).

build-zip.sh's own reproducible-build step (`touch -t "202600010000"`) is NOT a valid
date (month 00) and fails with rc=1 on this box -- filed as a surprise row. This script
builds the equivalent deterministic zip directly via zipfile.ZipInfo(date_time=...)
instead, per the TO's own fallback clause ("or an equivalent deterministic zip of the
same files if that script's output dir convention refuses -- say which").
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile

WORKSPACE_ROOT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
).stdout.strip()

FUNCTION_NAME = "inf-etf-ownership-daily"
SOURCE_MAP_PATH = os.path.join(WORKSPACE_ROOT, "infra/aws/lambda/ci/lambda-source-map.json")
SOURCE_DIR = os.path.join(WORKSPACE_ROOT, "infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily")
SCRATCH = os.path.join(WORKSPACE_ROOT, ".scratch")
DEPLOYED_ZIP = os.path.join(SCRATCH, "deployed_inf.zip")
DEPLOYED_EXTRACT = os.path.join(SCRATCH, "deployed_extract")
REPO_ZIP = os.path.join(SCRATCH, "build", "inf-etf-ownership-daily-repo.zip")
REPO_EXTRACT = os.path.join(SCRATCH, "repo_extract")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    # 1. Build input: the source map's declared files for this function.
    with open(SOURCE_MAP_PATH, "r", encoding="utf-8") as fh:
        source_map = json.load(fh)
    entry = source_map["functions"][FUNCTION_NAME]
    files = entry["files"]
    print("SOURCE_MAP: source_dir=%s files=%s artifact_sha256=%s last_deployed_commit=%s last_deployed_at=%s"
          % (entry["source_dir"], ",".join(files), entry.get("artifact_sha256"),
             entry.get("last_deployed_commit"), entry.get("last_deployed_at")))

    # 2. Deployed bytes: extract the already-downloaded zip (fetched by the caller via
    #    `aws lambda get-function --query Code.Location` + curl, a presigned GET -- read only).
    if not os.path.isfile(DEPLOYED_ZIP):
        print("ERROR: %s not found -- run the presigned download first" % DEPLOYED_ZIP)
        return 2
    os.makedirs(DEPLOYED_EXTRACT, exist_ok=True)
    with zipfile.ZipFile(DEPLOYED_ZIP) as z:
        deployed_members = sorted(z.namelist())
        z.extractall(DEPLOYED_EXTRACT)
    print("DEPLOYED_ZIP_MEMBERS: %s" % ",".join(deployed_members))

    # 3. Repo-side equivalent zip, deterministic (sorted, fixed mtimes), built directly
    #    since build-zip.sh's hardcoded touch date is invalid on this box (see docstring).
    os.makedirs(os.path.dirname(REPO_ZIP), exist_ok=True)
    with zipfile.ZipFile(REPO_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):
            p = os.path.join(SOURCE_DIR, f)
            with open(p, "rb") as fh:
                data = fh.read()
            zi = zipfile.ZipInfo(f, date_time=(2026, 1, 1, 0, 0, 0))
            z.writestr(zi, data)
    os.makedirs(REPO_EXTRACT, exist_ok=True)
    with zipfile.ZipFile(REPO_ZIP) as z:
        repo_members = sorted(z.namelist())
        z.extractall(REPO_EXTRACT)
    print("REPO_ZIP_MEMBERS: %s" % ",".join(repo_members))

    # 4. File-by-file sha256 comparison (union of both member sets).
    all_members = sorted(set(deployed_members) | set(repo_members))
    differing = []
    matching = []
    for m in all_members:
        dpath = os.path.join(DEPLOYED_EXTRACT, m)
        rpath = os.path.join(REPO_EXTRACT, m)
        d_hash = sha256_bytes(open(dpath, "rb").read()) if os.path.isfile(dpath) else "ABSENT"
        r_hash = sha256_bytes(open(rpath, "rb").read()) if os.path.isfile(rpath) else "ABSENT"
        status = "MATCH" if d_hash == r_hash else "DIFFERS"
        print("MEMBER %-24s deployed=%-10s repo=%-10s %s" % (
            m, d_hash[:10] if d_hash != "ABSENT" else "ABSENT", r_hash[:10] if r_hash != "ABSENT" else "ABSENT", status))
        if status == "DIFFERS":
            differing.append(m)
        else:
            matching.append(m)

    if differing:
        print("VERDICT: MISMATCH files=%d differing=%s" % (len(all_members), ",".join(differing)))
    else:
        print("VERDICT: MATCH")

    # 5. Which bucket/prefix the DEPLOYED code actually reads vs the REPO source.
    deployed_src = os.path.join(DEPLOYED_EXTRACT, "lambda_function.py")
    repo_src = os.path.join(SOURCE_DIR, "lambda_function.py")

    def extract_bucket_prefix(path: str) -> str:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        import re
        env_assigns = re.findall(r'(\w+)\s*=\s*os\.environ\[["\'](\w+)["\']\]', text)
        return ",".join("%s<-%s" % (var, env_key) for var, env_key in env_assigns)

    print("DEPLOYED_READS: env_bindings=%s" % extract_bucket_prefix(deployed_src))
    print("REPO_READS: env_bindings=%s" % extract_bucket_prefix(repo_src))

    return 0


if __name__ == "__main__":
    sys.exit(main())
