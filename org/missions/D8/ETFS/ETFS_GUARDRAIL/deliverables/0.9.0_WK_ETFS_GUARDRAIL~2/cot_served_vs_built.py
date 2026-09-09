"""cot_served_vs_built.py -- EG-s-1 S1-AC7: served CodeSha256 vs the source map's
artifact_sha256 (and the local zip's, if kept). Prints the values and ONE verdict line.

READ-ONLY: one lambda get-function-configuration call (via boto3 directly -- Python
spawning the .tools/aws bash shim as a subprocess is a known trap on this box, CLAUDE.md
Rule 16, since it is not a native Windows executable) + a source-map JSON read.
"""
from __future__ import annotations

import json
import subprocess
import sys

import boto3

HERE_REPO_ROOT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
).stdout.strip()

SOURCE_MAP_PATH = HERE_REPO_ROOT + "/infra/aws/lambda/ci/lambda-source-map.json"
FUNCTION_NAME = "cot-etf-ownership-daily"


def _served_code_sha256() -> str:
    lam = boto3.client("lambda")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION_NAME)
    return cfg["CodeSha256"]


def _built_artifact_sha256() -> str:
    with open(SOURCE_MAP_PATH, encoding="utf-8") as fh:
        sm = json.load(fh)
    entry = sm["functions"][FUNCTION_NAME]
    return entry["artifact_sha256"]


def main() -> int:
    served = _served_code_sha256()
    built = _built_artifact_sha256()
    print("SERVED CodeSha256 (live get-function-configuration): %s" % served)
    print("BUILT  artifact_sha256 (lambda-source-map.json, written by build-and-upload.sh): %s" % built)
    match = served == built
    print("VERDICT: %s" % ("MATCH" if match else "MISMATCH"))
    return 0 if match else 1


if __name__ == "__main__":
    sys.exit(main())
