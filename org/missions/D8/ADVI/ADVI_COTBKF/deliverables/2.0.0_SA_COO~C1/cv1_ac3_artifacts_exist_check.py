"""ADVI_COTBKF TO-CB-cv-1 AC3 (issuer's check): does every artifact the completion report cites exist at the cited version or commit?

Reads the report (repo-relative path below; run from the repo root). For each row's artifact:
  s3_key_version : ref = "s3://bucket/key", version_or_commit = the VersionId -> head-object on that version must answer;
  commit         : ref = a note or path, version_or_commit = a commit hash -> `git cat-file -e <hash>^{commit}` must succeed;
  file_at_commit : ref = a repo-relative path, version_or_commit = a commit hash -> `git cat-file -e <hash>:<path>` must succeed.
Prints one line:
  ARTIFACTS exist=<k> of <n>
Expected: k equals n (and n is 9). Read-only: object METADATA and git object existence only; no object body is read. Needs AWS read credentials.
"""
import json
import sys
import subprocess

import boto3

P = sys.argv[1] if len(sys.argv) > 1 else "org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~189/COMPLETION_REPORT.json"
rows = json.load(open(P, encoding="utf-8")).get("rows") or []
s3 = boto3.client("s3", region_name="us-east-1")


def exists(a):
    kind, ref, v = a.get("kind"), str(a.get("ref", "")).strip(), str(a.get("version_or_commit", "")).strip()
    try:
        if kind == "s3_key_version":
            b, _, k = ref[len("s3://"):].partition("/")
            s3.head_object(Bucket=b, Key=k, VersionId=v)
            return True
        if kind == "commit":
            return subprocess.run(["git", "cat-file", "-e", v + "^{commit}"], capture_output=True).returncode == 0
        if kind == "file_at_commit":
            return subprocess.run(["git", "cat-file", "-e", v + ":" + ref], capture_output=True).returncode == 0
    except Exception:
        return False
    return False


k = sum(1 for r in rows if exists(r.get("artifact") or {}))
print("ARTIFACTS exist=%d of %d" % (k, len(rows)))
