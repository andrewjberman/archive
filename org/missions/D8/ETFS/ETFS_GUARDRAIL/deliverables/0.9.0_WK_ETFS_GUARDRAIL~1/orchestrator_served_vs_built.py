#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-8 -- served CodeSha256 vs the zip Terraform built.

READ-ONLY: one live get-function-configuration call (CodeSha256) plus a local
sha256/base64 hash of the archive_file-built zip. No update-function-code, no
apply, no invoke.
"""
from __future__ import annotations

import base64
import hashlib
import os
import subprocess
import sys

sys.path.insert(0, ".tools")
from git_bash_resolver import git_bash  # noqa: E402 -- a python-spawned bash needs the absolute exe

ZIP_PATH = "infra/aws/terraform/etfs-reports/.build/etfs-reports-orchestrator.zip"
FUNCTION_NAME = "etfs-reports-orchestrator"


def main() -> int:
    with open(ZIP_PATH, "rb") as fh:
        zip_bytes = fh.read()
    built_b64sha256 = base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode("ascii")

    bash = git_bash()
    if not bash:
        print("ERROR: no Git Bash found -- cannot invoke .tools/aws from Python on this box")
        return 2
    result = subprocess.run(
        [bash, ".tools/aws", "lambda", "get-function-configuration",
         "--function-name", FUNCTION_NAME, "--query", "CodeSha256", "--output", "text"],
        capture_output=True, text=True, check=True, cwd=os.getcwd(),
    )
    served_sha256 = result.stdout.strip()

    print("SERVED_CODE_SHA256: %s" % served_sha256)
    print("BUILT_ZIP_SHA256_B64: %s" % built_b64sha256)
    if served_sha256 == built_b64sha256:
        print("VERDICT: MATCH")
    else:
        print("VERDICT: MISMATCH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
