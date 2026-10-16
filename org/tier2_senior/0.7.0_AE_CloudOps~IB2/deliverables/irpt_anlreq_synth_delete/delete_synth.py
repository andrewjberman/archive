"""IRPT_ANLREQ TO-DELETE-SYNTH-INTAKE.fwd1-sets-r33-and-run3-ib2: the 24 named fabric-made synthetic object versions in opal-data-irpt.

  python delete_synth.py check          steps 2 and 3, READ ONLY: parse the four sets, print the count, head-object each by key AND VersionId
  python delete_synth.py delete --go    steps 4 to 6: delete each passing row by VersionId (never key-only, never a prefix), read each back absent, write A_DELETE_SYNTH.txt

The delete stops at once on an AccessDenied from the FIRST delete (nothing else deleted; a positive control is printed). No retry. Keys, VersionIds and counts only.
"""
import re
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

BUCKET = "opal-data-irpt"
A = "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/"
OUT = Path("org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_synth_delete/A_DELETE_SYNTH.txt")
PREFIXES = ("irpt/49financial/state/original_holdings/", "irpt/49financial/state/normalized_portfolios/")
s3 = boto3.client("s3", region_name="us-east-1")


def parse():
    rows = []
    r3 = open(A + "irpt_anlreq_fwd1_r3/OBJECTS_WRITTEN_FWD1_R3.txt", encoding="utf-8").read().splitlines()
    for ln in r3:
        m = re.match(r"^(SET2 |SET3 |RUN |)OBJ (\S+) (\S+) (\S+)$", ln)
        if m:
            rows.append((m.group(2), m.group(3), m.group(4), "r3:" + (m.group(1).strip() or "PROBE1")))
    for ln in open(A + "irpt_anlreq_r33/OBJECTS_WRITTEN_R33.txt", encoding="utf-8").read().splitlines():
        m = re.match(r"^OBJ (\S+) (\S+) (\S+)$", ln)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3), "r33"))
    return rows


def main(argv):
    rows = parse()
    pairs = [(b, k, v) for b, k, v, _ in rows]
    print("LIST rows=%d distinct_keys=%d distinct_pairs=%d buckets=%s sources=%s" % (len(rows), len({k for _, k, _ in pairs}), len(set(pairs)), sorted({b for b, _, _ in pairs}),
                                                                                  sorted({(s, sum(1 for r in rows if r[3] == s)) for s in {r[3] for r in rows}})))
    if len(rows) != 24 or len(set(pairs)) != 24 or {b for b, _, _ in pairs} != {BUCKET}:
        print("STOP: the table is not 24 distinct (key, VersionId) rows in %s" % BUCKET)
        return 3
    passing = []
    for b, k, v, src in rows:
        try:
            h = s3.head_object(Bucket=BUCKET, Key=k, VersionId=v)
        except ClientError as e:
            print("HEAD FAIL %s ... %s: %s" % (src, v, e.response["Error"]["Code"]))
            continue
        marker = bool(h.get("DeleteMarker"))
        ok = (not marker) and k.startswith(PREFIXES)
        print("HEAD %s %s len=%s etag=%s delete_marker=%s prefix_ok=%s" % (src, v, h["ContentLength"], h["ETag"].strip('"')[:12], marker, k.startswith(PREFIXES)))
        if ok:
            passing.append((k, v))
    print("CHECK passed=%d of 24" % len(passing))
    if argv[0] != "delete" or "--go" not in argv:
        return 0 if len(passing) == 24 else 3
    results, first = [], True
    for k, v in passing:
        try:
            s3.delete_object(Bucket=BUCKET, Key=k, VersionId=v)
        except ClientError as e:
            code = e.response["Error"]["Code"]
            print("DELETE %s %s ERROR %s" % (k[-20:], v, code))
            if first and code == "AccessDenied":
                ctl = s3.head_object(Bucket=BUCKET, Key=k, VersionId=v)
                print("STOP: the FIRST delete was AccessDenied; nothing else deleted. Positive control: head by VersionId still reads the version present (len=%s)" % ctl["ContentLength"])
                return 4
            results.append((k, v, "FAIL delete %s" % code))
            first = False
            continue
        first = False
        results.append((k, v, None))
    lines, deleted = [], 0
    for k, v, err in results:
        if err:
            lines.append("DEL %s %s %s" % (k, v, err))
            continue
        gone = False
        try:
            s3.head_object(Bucket=BUCKET, Key=k, VersionId=v)
            why = "head by key and VersionId still answers"
        except ClientError as e:
            code = e.response["Error"]["Code"]
            gone = code in ("404", "NoSuchVersion", "NotFound")
            why = "head answered %s" % code
        pres, markers = False, 0
        for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=k):
            for x in pg.get("Versions", []):
                if x["Key"] == k and x["VersionId"] == v:
                    pres = True
            markers += sum(1 for x in pg.get("DeleteMarkers", []) if x["Key"] == k)
        ok = gone and not pres and markers == 0
        lines.append("DEL %s %s %s" % (k, v, "ABSENT" if ok else "FAIL %s; listed_present=%s delete_markers_for_key=%d" % (why, pres, markers)))
        deleted += ok
    failed = len(rows) - deleted
    lines.append("DEL_TOTAL deleted=%d failed=%d denominator=24" % (deleted, failed))
    OUT.write_text("\n".join(lines) + "\n", encoding="ascii")
    print("WROTE %s deleted=%d failed=%d" % (OUT, deleted, failed))
    return 0 if failed == 0 else 5


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["check"]))
