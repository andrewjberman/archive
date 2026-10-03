"""P-2 window rollback, data half (packet @855fdad77c section "Rollback, per key"; CTO batch 222 addition 2).

For every key recorded by p2_prewindow_versions.py whose current VersionId moved, copy the RECORDED version back over the key
as a new version (never a delete). Keys that are NEW since the record are only LISTED: rolling them back is a delete marker
per key, an S3 delete that needs a human's confirmation at that moment (Agent Autonomy), so this script never deletes.

Usage:
  python p2_rollback_restore.py <prewindow.json> --plan      # print what would be restored and what is new; writes nothing
  python p2_rollback_restore.py <prewindow.json> --restore   # copy each moved key's recorded version back, then re-read it
"""
import json
import sys

import boto3

s3 = boto3.client("s3")


def current(bucket, prefixes):
    out = {}
    for p in prefixes:
        for page in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=p):
            for v in page.get("Versions", []):
                if v["IsLatest"]:
                    out[v["Key"]] = v["VersionId"]
            for d in page.get("DeleteMarkers", []):
                if d["IsLatest"]:
                    out[d["Key"]] = "DELETE_MARKER:" + d["VersionId"]
    return out


def main():
    rec = json.load(open(sys.argv[1], encoding="utf-8"))
    bucket, keys = rec["bucket"], rec["keys"]
    now = current(bucket, rec["prefixes"])
    moved = sorted(k for k, v in keys.items() if "version_id" in v and now.get(k) != v["version_id"])
    new = sorted(set(now) - set(keys))
    print("DENOMINATOR: %d recorded keys; %d moved since %s; %d NEW (not restorable without a delete)"
          % (len(keys), len(moved), rec["read_at"], len(new)))
    if "--plan" in sys.argv:
        for k in moved[:20]:
            print("  RESTORE", k, "->", keys[k]["version_id"])
        for k in new[:20]:
            print("  NEW (delete marker on a human's confirmation)", k)
        return
    if "--restore" not in sys.argv:
        sys.exit("say --plan or --restore")
    bad = []
    for k in moved:
        vid = keys[k]["version_id"]
        s3.copy_object(Bucket=bucket, Key=k, CopySource={"Bucket": bucket, "Key": k, "VersionId": vid},
                       MetadataDirective="COPY")
        etag = s3.head_object(Bucket=bucket, Key=k)["ETag"].strip('"')
        if etag != keys[k]["etag"]:
            bad.append("%s etag %s != recorded %s" % (k, etag, keys[k]["etag"]))
    print("RESTORED %d keys; %d etag mismatches" % (len(moved) - len(bad), len(bad)))
    for b in bad[:20]:
        print("  FAIL", b)
    print("NEW keys left in place: %d (each needs a human-confirmed delete marker)" % len(new))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
