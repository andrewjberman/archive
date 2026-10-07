"""Issuer act (ADVI_COTBKF round 3, ledger advi-cotbkf-r3-imaging-and-silver-20261007): land the three imaging archives to bronze.

Key, from the naming builder (rule 30): address('commonwealth', <scope>, 'bronze', 'imaging', 'date=<data-date>',
object='plan_id=<ID>/<member>') -- the plan_id sub-path the CTO named (msg 105909); the builder's partition takes one segment, its
object takes the rest. Each archive is streamed out of the outer Box zip untouched (never written to local disk) through a multipart
upload; its SHA-256 and the expected multipart ETag are computed on the same bytes, so the read-back proves the object byte for byte
without downloading it again. A key already holding a different object is refused; the same object is skipped. The manifest gains
each file through commonwealth_landing.merge_manifest (never drops one).

    python land_imaging_plan_id.py --source <outer zip> --data-date 2026-06-23 --received-date 2026-10-06 [--apply] HKE.zip ...
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import zipfile

import boto3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 7))
sys.path.insert(0, os.path.join(ROOT, "lib"))
from opal_naming import address, lookup  # noqa: E402

PART = 64 * 1024 * 1024
SCOPE = lookup("cottonwood")["long"]


def landing_module():
    spec = importlib.util.spec_from_file_location(
        "commonwealth_landing", os.path.join(ROOT, "data", "assets", "scripts", "bronze", "commonwealth_landing.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def split(uri):
    bucket, _, key = uri[len("s3://"):].partition("/")
    return bucket, key


def members_of(outer, member):
    with zipfile.ZipFile(outer.open(member)) as inner:
        return [{"path": i.filename, "bytes": i.file_size} for i in inner.infolist() if not i.is_dir()]


def land(s3, outer, member, data_date, apply):
    plan_id = member.rsplit(".", 1)[0]
    uri = address("commonwealth", SCOPE, "bronze", "imaging", "date=" + data_date, object="plan_id=%s/%s" % (plan_id, member))
    bucket, key = split(uri)
    size = outer.getinfo(member).file_size
    print("PLAN %s -> %s bytes=%d" % (member, uri, size))
    if not apply:
        return {"name_as_shipped": member, "bytes": size, "bronze_key": uri, "sha256": None, "members": None}
    try:
        head = s3.head_object(Bucket=bucket, Key=key)
    except s3.exceptions.ClientError as exc:
        if exc.response["Error"]["Code"] not in ("404", "NoSuchKey", "NotFound"):
            raise
        head = None
    if head is not None and head["ContentLength"] != size:
        raise SystemExit("REFUSED %s: key holds a different object (%d bytes)" % (uri, head["ContentLength"]))
    sha, md5s, parts = hashlib.sha256(), [], []
    upload = None if head else s3.create_multipart_upload(Bucket=bucket, Key=key)
    try:
        with outer.open(member) as src:
            n = 0
            while True:
                chunk = src.read(PART)
                if not chunk:
                    break
                n += 1
                sha.update(chunk)
                md5s.append(hashlib.md5(chunk).digest())
                if upload:
                    r = s3.upload_part(Bucket=bucket, Key=key, PartNumber=n, UploadId=upload["UploadId"], Body=chunk)
                    parts.append({"PartNumber": n, "ETag": r["ETag"]})
        if upload:
            s3.complete_multipart_upload(Bucket=bucket, Key=key, UploadId=upload["UploadId"], MultipartUpload={"Parts": parts})
    except BaseException:
        if upload:
            s3.abort_multipart_upload(Bucket=bucket, Key=key, UploadId=upload["UploadId"])
        raise
    expect_etag = '"%s-%d"' % (hashlib.md5(b"".join(md5s)).hexdigest(), len(md5s))
    back = s3.head_object(Bucket=bucket, Key=key)
    ok = back["ContentLength"] == size and back["ETag"] == expect_etag
    print("%s %s bytes=%d sha256=%s etag=%s readback_bytes=%d readback_etag=%s verified=%s"
          % ("SKIP-SAME" if head else "PUT", member, size, sha.hexdigest(), expect_etag, back["ContentLength"], back["ETag"], ok))
    if not ok:
        raise SystemExit("REFUSED %s: read-back does not match the streamed bytes" % uri)
    return {"name_as_shipped": member, "bytes": size, "sha256": sha.hexdigest(), "bronze_key": uri,
            "members": members_of(outer, member)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--data-date", required=True)
    ap.add_argument("--received-date", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("members", nargs="+")
    a = ap.parse_args()
    s3 = boto3.client("s3")
    lm = landing_module()
    manifest_uri = address("commonwealth", SCOPE, "bronze", "manifest", "date=" + a.data_date) + "/manifest.json"
    mb, mk = split(manifest_uri)
    with zipfile.ZipFile(a.source) as outer:
        entries = [land(s3, outer, m, a.data_date, a.apply) for m in a.members]
    if not a.apply:
        print("LANDING-IMAGING files=%d apply=False" % len(entries))
        return 0
    manifest = json.loads(s3.get_object(Bucket=mb, Key=mk)["Body"].read())
    for e in entries:
        new = {"files": [e], "builder": manifest.get("builder", {})}
        manifest = lm.merge_manifest(manifest, new)
    body = json.dumps(manifest, indent=1).encode("utf-8")
    s3.put_object(Bucket=mb, Key=mk, Body=body, ChecksumAlgorithm="SHA256")
    back = json.loads(s3.get_object(Bucket=mb, Key=mk)["Body"].read())
    names = sorted(f["name_as_shipped"] for f in back["files"])
    print("LANDING-IMAGING files=%d apply=True manifest_files=%d %s" % (len(entries), len(names), names))
    return 0


if __name__ == "__main__":
    sys.exit(main())
