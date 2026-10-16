"""IRPT_ANLREQ TO-RUN-FWD1 window 3 (0.7.0_AE_CloudOps~AQ2): list the intake store (bucket opal-data-irpt, prefix irpt/49financial/) with versions and delete markers (READ ONLY).

  python intake_snapshot_run3.py snap <out.json>         writes the (key, VersionId, size) set and prints the denominator
  python intake_snapshot_run3.py diff <before.json>      lists every (key, VersionId) now present that the snapshot did not hold, as OBJ lines, and OBJ_COUNT
"""
from __future__ import annotations

import json
import sys

BUCKET, PREFIX = "opal-data-irpt", "irpt/49financial/"


def listing():
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    items, markers = {}, 0
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for v in pg.get("Versions", []) or []:
            items["%s\t%s" % (v["Key"], v["VersionId"])] = v["Size"]
        markers += len(pg.get("DeleteMarkers", []) or [])
    return items, markers


def main(argv):
    if argv[0] == "snap":
        items, markers = listing()
        json.dump({"items": items, "delete_markers": markers}, open(argv[1], "w"))
        print("SNAP %s/%s versions %d delete markers %d" % (BUCKET, PREFIX, len(items), markers))
        return 0
    before = json.load(open(argv[1]))
    items, markers = listing()
    new = sorted(k for k in items if k not in before["items"])
    print("DIFF versions BEFORE %d AFTER %d; delete markers %d and %d" % (len(before["items"]), len(items), before["delete_markers"], markers))
    for k in new:
        key, ver = k.split("\t")
        print("OBJ %s %s %s" % (BUCKET, key, ver))
    print("OBJ_COUNT %d" % len(new))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
