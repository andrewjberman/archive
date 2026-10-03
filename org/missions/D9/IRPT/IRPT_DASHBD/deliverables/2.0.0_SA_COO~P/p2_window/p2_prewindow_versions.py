"""P-2 window, leg A2 precondition (packet @855fdad77c, rollback per key): record the current VersionId of every key the
window may overwrite, so the rollback copies each prior version back as a new version, never a delete.

Read-only. Usage: python p2_prewindow_versions.py <out.json> [--compare <earlier.json>]
Scope (opal-data-49financial, versioned): gold/account_return_daily/**, gold/dim_return_method/**, platinum/reporting/**.
Prints the denominator per prefix. --compare prints every key whose VersionId moved, appeared or vanished since <earlier>.
"""
import json
import sys
from datetime import datetime, timezone

import boto3

BUCKET = "opal-data-49financial"
PREFIXES = ("irpt/49financial/gold/account_return_daily/", "irpt/49financial/gold/dim_return_method/",
            "irpt/49financial/platinum/reporting/")


def census(s3):
    out = {}
    for p in PREFIXES:
        n = 0
        for page in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=p):
            for v in page.get("Versions", []):
                if v["IsLatest"]:
                    out[v["Key"]] = {"version_id": v["VersionId"], "etag": v["ETag"].strip('"'), "size": v["Size"],
                                     "last_modified": v["LastModified"].isoformat()}
                    n += 1
            for d in page.get("DeleteMarkers", []):
                if d["IsLatest"]:
                    out[d["Key"]] = {"delete_marker": d["VersionId"]}
        print("  %s: %d current keys" % (p, n))
    return out


def main():
    s3 = boto3.client("s3")
    keys = census(s3)
    doc = {"bucket": BUCKET, "read_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "prefixes": list(PREFIXES), "keys": keys, "count": len(keys)}
    json.dump(doc, open(sys.argv[1], "w", encoding="utf-8"), indent=0, sort_keys=True)
    print("OK: %d keys recorded to %s" % (len(keys), sys.argv[1]))
    if "--compare" in sys.argv:
        old = json.load(open(sys.argv[sys.argv.index("--compare") + 1], encoding="utf-8"))["keys"]
        moved = sorted(k for k in keys if k in old and keys[k] != old[k])
        new = sorted(set(keys) - set(old))
        gone = sorted(set(old) - set(keys))
        print("COMPARE: moved %d, new %d, vanished %d" % (len(moved), len(new), len(gone)))
        for k in (moved + new + gone)[:40]:
            print("   ", k)


if __name__ == "__main__":
    main()
