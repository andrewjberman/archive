#!/usr/bin/env python
"""
B3_AC6_PRIOR_FETCH -- the POSITIVE CONTROL's bytes for POSN_AGGFIX.TO-B3-1 criterion B3-AC6.

B3-AC6 requires that the AGG-absence check it runs on the SERVED control body also be run against
TO-A3-1's PRIOR shared-file version, FETCHED BY VERSIONID, and report AGG PRESENT -- so that a check
which can only ever say ABSENT is distinguished from one that can fail.

This helper does exactly the fetch, and nothing about the verdict: it reads the PRIOR VersionId of
json/positioning/positioning_data.json from TO-A3-1's PROOF INSTANCE (two loci, required to agree --
the same read B3-AC1 made, never this worker's memory and never a key-only read), fetches THAT VERSION
by VersionId, decompresses it if it was stored gzip, writes the decompressed bytes to .scratch, and
prints ONE machine-readable line that b3_served_tier_bodies.mjs parses. The PARSING and the verdict
live in the caller, so the served body and the prior version go through the SAME check.

Read-only toward the cloud: head_object and get_object only; no write to any bucket, no deploy.
"""
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import timezone

BUCKET = "opal-data-portal-v2"
SHARED_KEY = "json/positioning/positioning_data.json"
A3_INSTANCE = ("org/missions/D4/POSN/POSN_AGGFIX/deliverables/0.9.0_WK_POSN_AGGFIX~1/"
               "POSN_AGGFIX.TO-A3-1.deploy-the-producer-and-read-the-served-result.proof_of_spec.json")
OUT_REL = os.path.join(".scratch", "b3_ac6_prior_by_versionid.json")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True,
                      text=True).stdout.strip()


def ids_from_compare_row(ev):
    """A3-AC9's read lines."""
    out = {}
    m = re.search(r"READ\s+json/positioning/positioning_data\.json\s+prior\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_prior"] = m.group(1)
    m = re.search(r"READ\s+json/positioning/positioning_data\.json\s+new\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_new"] = m.group(1)
    return out


def ids_from_head_row(ev):
    """A3-AC8's BEFORE/AFTER head reads -- the second locus."""
    out = {}
    m = re.search(r"BEFORE\s+HEAD\s+json/positioning/positioning_data\.json\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_prior"] = m.group(1)
    m = re.search(r"AFTER\s+HEAD\s+json/positioning/positioning_data\.json\s+VersionId\s+(\S+)", ev)
    if m:
        out["shared_new"] = m.group(1)
    return out


def main():
    inst_path = os.path.join(ROOT, A3_INSTANCE)
    inst_commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", A3_INSTANCE], cwd=ROOT,
                                 capture_output=True, text=True).stdout.strip()
    with open(inst_path, encoding="utf-8") as fh:
        inst = json.load(fh)
    rows = {r.get("criterion_id"): r for r in inst.get("acceptance", [])}

    loci = {}
    if "A3-AC9" in rows:
        loci["A3-AC9"] = ids_from_compare_row(rows["A3-AC9"].get("output_evidence", ""))
    if "A3-AC8" in rows:
        loci["A3-AC8"] = ids_from_head_row(rows["A3-AC8"].get("output_evidence", ""))
    print("PRIOR_FETCH source instance: %s @%s" % (A3_INSTANCE, inst_commit))
    for locus in sorted(loci):
        print("PRIOR_FETCH   from %s: %s" % (locus, json.dumps(loci[locus], sort_keys=True)))

    priors = {locus: v.get("shared_prior") for locus, v in loci.items() if v.get("shared_prior")}
    distinct = sorted(set(priors.values()))
    agree = len(distinct) == 1 and len(priors) >= 2
    print("PRIOR_FETCH loci carrying a prior id: %d; distinct values: %d; agree: %s"
          % (len(priors), len(distinct), agree))
    if not distinct:
        print("PRIOR_FETCH ERROR: no prior VersionId in TO-A3-1's instance")
        return 1
    if len(distinct) != 1:
        print("PRIOR_FETCH ERROR: the loci disagree: %s" % distinct)
        return 1
    prior_id = distinct[0]

    import boto3
    s3 = boto3.client("s3")
    head = s3.head_object(Bucket=BUCKET, Key=SHARED_KEY, VersionId=prior_id)
    body = s3.get_object(Bucket=BUCKET, Key=SHARED_KEY, VersionId=prior_id)["Body"].read()
    enc = head.get("ContentEncoding")
    lm = head["LastModified"].astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if len(body) != head["ContentLength"]:
        print("PRIOR_FETCH ERROR: fetched %d bytes, ContentLength %d" % (len(body), head["ContentLength"]))
        return 1
    raw = gzip.decompress(body) if enc == "gzip" else body

    out_path = os.path.join(ROOT, OUT_REL)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as fh:   # binary: a text-mode write CRLF-ifies on this device
        fh.write(raw)
    back = open(out_path, "rb").read()
    if back != raw:
        print("PRIOR_FETCH ERROR: the file did not read back byte-identical")
        return 1

    payload = {
        "key": SHARED_KEY,
        "bucket": BUCKET,
        "version_id": prior_id,
        "last_modified": lm,
        "content_length": head["ContentLength"],
        "content_encoding": enc,
        "stored_md5": hashlib.md5(body).hexdigest(),
        "decompressed_bytes": len(raw),
        "decompressed_sha256": hashlib.sha256(raw).hexdigest(),
        "path": out_path.replace("\\", "/"),
        "source_instance": A3_INSTANCE,
        "source_instance_commit": inst_commit,
        "loci_agree": agree,
        "loci": loci,
    }
    print("PRIOR_FETCH_JSON " + json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
