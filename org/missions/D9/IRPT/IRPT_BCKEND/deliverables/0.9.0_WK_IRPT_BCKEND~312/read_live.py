"""IB-pr-456 live reads (AWS READS ONLY, through .tools/aws; ASCII). From the worktree root:
    python <this file> <scratch_dir> <out_json> <fn> [<fn> ...]
Per function: lambda get-function-configuration (live CodeSha256 + read time); lambda get-function -> the package link is used ONCE,
in memory, to download the live zip to <scratch>/live/<fn>.zip (the link is never printed or written); the S3 version of the
function's own artifact key (bucket and key read from its real map entry; the bucket name is NOT written to the output) whose
content sha256 equals the live digest = rollback_version_id: the version's content-sha256 metadata (head-object) first; a version with
no metadata is hashed by get-object to scratch. Nothing is written to AWS."""
import base64
import datetime
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True).stdout.decode().strip())
scratch, out = Path(sys.argv[1]), Path(sys.argv[2])
FNS = sys.argv[3:]
DEFAULT_BUCKET_NOTE = "default artifact bucket (build-and-upload.sh ARTIFACT_BUCKET) when the entry names none"
smap = json.loads(subprocess.run(["git", "show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json"], cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8"))["functions"]
DEFAULT_BUCKET = None
for line in (ROOT / "infra/aws/lambda/ci/build-and-upload.sh").read_text(encoding="utf-8").splitlines():
    if line.startswith("ARTIFACT_BUCKET="):
        DEFAULT_BUCKET = line.split("=", 1)[1].strip('"')


def aws(*a, raw=False):
    r = subprocess.run(["bash", ".tools/aws"] + list(a) + ["--output", "json"], cwd=str(ROOT), capture_output=True, timeout=120)
    if r.returncode:
        raise SystemExit("aws failed (%s): %s" % (a[:2], r.stderr.decode("utf-8", "replace")[-200:]))
    return json.loads(r.stdout.decode("utf-8")) if not raw else r.stdout


def b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode()


res = []
(scratch / "live").mkdir(parents=True, exist_ok=True)
(scratch / "vers").mkdir(parents=True, exist_ok=True)
for fn in FNS:
    e = smap[fn]
    bucket, key = e.get("artifact_s3_bucket") or DEFAULT_BUCKET, e["artifact_s3_key"]
    read_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cfg = aws("lambda", "get-function-configuration", "--function-name", fn)
    live = cfg["CodeSha256"]
    gf = aws("lambda", "get-function", "--function-name", fn)
    loc = gf["Code"]["Location"]
    data = urllib.request.urlopen(loc, timeout=120).read()
    del loc, gf
    (scratch / "live" / (fn + ".zip")).write_bytes(data)
    vers = aws("s3api", "list-object-versions", "--bucket", bucket, "--prefix", key)
    cand = sorted([v for v in vers.get("Versions", []) if v["Key"] == key], key=lambda v: v["LastModified"], reverse=True)
    rows, rollback = [], None
    for v in cand:
        if v["Size"] != cfg["CodeSize"]:
            # a version of a different byte length cannot be the live package; recorded, not read further
            rows.append({"version_id": v["VersionId"], "is_latest": v.get("IsLatest"), "last_modified": v["LastModified"], "size": v["Size"], "sha256_b64": None, "sha_basis": "skipped: size differs from the live CodeSize"})
            continue
        h = aws("s3api", "head-object", "--bucket", bucket, "--key", key, "--version-id", v["VersionId"])
        meta = (h.get("Metadata") or {}).get("content-sha256")
        how, sha = "metadata", meta
        if rollback is None and meta != live:
            # the metadata is the uploader's claim; hash the version's bytes when the claim is absent
            if not meta:
                p = scratch / "vers" / "v.bin"
                aws("s3api", "get-object", "--bucket", bucket, "--key", key, "--version-id", v["VersionId"], str(p))
                sha, how = b64(p.read_bytes()), "get-object-hash"
                p.unlink()
        rows.append({"version_id": v["VersionId"], "is_latest": v.get("IsLatest"), "last_modified": v["LastModified"], "size": v["Size"], "sha256_b64": sha, "sha_basis": how})
        if rollback is None and sha == live:
            # confirm by bytes: the version's own content hash
            p = scratch / "vers" / "v.bin"
            aws("s3api", "get-object", "--bucket", bucket, "--key", key, "--version-id", v["VersionId"], str(p))
            ok = b64(p.read_bytes()) == live
            p.unlink()
            rows[-1]["bytes_hash_equals_live"] = ok
            if ok:
                rollback = v["VersionId"]
    r = {"function": fn, "live_code_sha256": live, "live_read_at_utc": read_at, "live_last_modified": cfg["LastModified"], "live_code_size": cfg["CodeSize"],
         "downloaded_zip_sha256_b64": b64(data), "downloaded_zip_equals_live_code_sha256": b64(data) == live, "downloaded_bytes": len(data),
         "artifact_key": key, "bucket_source": "entry" if e.get("artifact_s3_bucket") else DEFAULT_BUCKET_NOTE,
         "versions_of_key": len(rows), "versions": rows, "rollback_version_id": rollback}
    if rollback is None:
        r["rollback_version_absent_reason"] = "none of the %d S3 versions of the artifact key has content sha256 equal to the live CodeSha256" % len(rows)
    res.append(r)
    print(fn, live, "dl_ok=%s" % r["downloaded_zip_equals_live_code_sha256"], "versions=%d" % len(rows), "rollback=%s" % rollback)
for r in res:
    r["versions_of_key_same_size_as_live"] = sum(1 for x in r["versions"] if x["sha_basis"] != "skipped: size differs from the live CodeSize")
out.write_text(json.dumps({"live_reads": res}, indent=1) + "\n", encoding="utf-8")
