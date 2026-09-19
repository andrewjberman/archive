#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-10 third pass -- verify the K-CODE build of irpt-directory-search AT REST (row S96 ruling (i)).

Reads, never writes. For the build-store key investor-reporting/irpt-directory-search.zip:
  - the latest version is NEW (not the prior live version l4JK6aUn...), its content-sha256 metadata == the built sha256
    the builder printed, and the re-downloaded bytes hash to it;
  - every zip member equals a COMMITTED blob: the function's own files at the build HEAD, and each staged_from member
    at its declared pin (sha256 == the manifest's declared sha256) -- so the served seam member is the LF blob, never
    the CRLF hand copy the prior build carried;
  - the member set == the manifest's files[] for this function (10 of 10);
  - the prior version is still in the versioned bucket and still hashes to the prior live CodeSha256 (the rollback
    source);
  - the function's CodeSha256 is UNCHANGED (the build deploys nothing).
Prints no URL and no credential.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import io
import json
import os
import subprocess
import sys
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-10_k_code_build_verify_output.txt")
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "investor-reporting/irpt-directory-search.zip"
FN = "irpt-directory-search"
BUILT = sys.argv[1]  # the sha256(b64) build-and-upload.sh printed
BUILD_HEAD = sys.argv[2]  # the worktree HEAD the build ran from
PRIOR_LIVE = "aQxATFkcdtEBvs+v/zztQBOPcbR9XH9Lzjm9kUOmhmU="
PRIOR_VERSION = "l4JK6aUnUgtrg.TFrxiKU8.XBM_6APl4"
LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def b64sha(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def git_blob(ref: str, path: str) -> bytes:
    out = subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=WS, capture_output=True)
    if out.returncode != 0:
        raise SystemExit("ERROR: git show %s:%s rc=%d" % (ref, path, out.returncode))
    return out.stdout


def main() -> int:
    s3 = boto3.client("s3", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")
    emit("IB-rtf-10 K-CODE build verification -- run at %s as %s; build HEAD %s" % (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        boto3.client("sts").get_caller_identity()["Arn"], BUILD_HEAD))
    checks: dict[str, bool] = {}
    head = s3.head_object(Bucket=BUCKET, Key=KEY)
    latest, meta = head["VersionId"], (head.get("Metadata") or {}).get("content-sha256")
    body = s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=latest)["Body"].read()
    got = b64sha(body)
    checks["new version latest"] = latest != PRIOR_VERSION
    checks["metadata == built"] = meta == BUILT
    checks["bytes == built"] = got == BUILT
    emit("latest version %s (uploaded %s, %d bytes); content-sha256 %s; re-downloaded sha256(b64) %s; built %s" % (
        latest, head["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), len(body), meta, got, BUILT))

    sm = json.loads(git_blob(BUILD_HEAD, "infra/aws/lambda/ci/lambda-source-map.json").decode("utf-8"))
    ent = sm["functions"][FN]
    staged = {s["packaged_as"]: s for s in ent.get("staged_from", [])}
    z = zipfile.ZipFile(io.BytesIO(body))
    names = sorted(i.filename for i in z.infolist())
    checks["members == files[]"] = names == sorted(ent["files"])
    emit("zip members %d; manifest files[] %d -> %s" % (len(names), len(ent["files"]),
                                                          "EQUAL" if checks["members == files[]"] else "DIFFER"))
    ok_m = 0
    for n in names:
        data = z.read(n)
        if n in staged:
            s = staged[n]
            ref = git_blob(s["pin"], s["repo_path"])
            src = "staged %s@%s (declared sha256 %s...)" % (s["repo_path"], s["pin"][:10], s["sha256"][:12])
            good = data == ref and hashlib.sha256(data).hexdigest() == s["sha256"]
        else:
            ref = git_blob(BUILD_HEAD, ent["source_dir"] + "/" + n)
            src = "%s/%s@%s" % (ent["source_dir"], n, BUILD_HEAD[:10])
            good = data == ref
        ok_m += good
        emit("  %-30s %7d bytes CR %-5d sha256 %s... == %s -> %s" % (n, len(data), data.count(b"\r"),
                                                                   hashlib.sha256(data).hexdigest()[:16], src,
                                                                   "EQUAL" if good else "DIFFERS"))
    checks["members == committed blobs"] = ok_m == len(names)
    emit("members equal to their committed blob: %d of %d" % (ok_m, len(names)))

    prior = s3.get_object(Bucket=BUCKET, Key=KEY, VersionId=PRIOR_VERSION)["Body"].read()
    checks["rollback source kept"] = b64sha(prior) == PRIOR_LIVE
    emit("rollback source: version %s still present, sha256(b64) %s -> %s" % (
        PRIOR_VERSION, b64sha(prior), "== the prior live CodeSha256" if checks["rollback source kept"] else "DIFFERS"))
    live = lam.get_function_configuration(FunctionName=FN)["CodeSha256"]
    checks["function unchanged"] = live == PRIOR_LIVE
    emit("function %s CodeSha256 %s -> %s" % (FN, live, "UNCHANGED (the build deployed nothing)"
                                             if checks["function unchanged"] else "CHANGED"))
    for k, v in checks.items():
        emit("CHECK %s: %s" % (k, "OK" if v else "FAIL"))
    emit("RESULT: %d of %d checks hold" % (sum(checks.values()), len(checks)))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
