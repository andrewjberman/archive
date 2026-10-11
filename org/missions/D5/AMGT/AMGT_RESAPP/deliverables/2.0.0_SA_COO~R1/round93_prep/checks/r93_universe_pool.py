"""AMGT_RESAPP round-93 PREP -- rr-5: the candidate universe's pool home carries the scanner's vintage as its own NEW dated key.

  PYTHONPATH=<repo root> python r93_universe_pool.py --prior-version-id <VersionId of date=2026-08-06 before the act> [--vintage 2026-10-02]

After `python -m lib.research.peers.universe --refresh` (AMGT-qq-2's writer: a refresh dates the key by the document's own vintage and never
overwrites), the pool holds the scanner's vintage as its own object and the old one is untouched. Read-only (S3 list, head, get).

    U1 `date=<vintage>/candidate_universe.json` exists under the prefix the builder (`universe.candidate_universe_address`) names.
    U2 its document's `vintage` equals the scanner's, it carries rows (the database denominator printed), and its `document-sha256`
       metadata equals the SHA-256 of its bytes.
    U3 control: the `date=2026-08-06` object is untouched: its current VersionId equals the prior one and its version count is unchanged
       (no second version since the prior id was recorded).
    U4 the loader (`universe.load_candidate_universe()`, no path, no override) returns the new vintage.
Verdict: R93 UNIVERSE POOL: YES|NO (exit 0|1). At the base (2026-10-11) U1, U2 and U4 FAIL (no dated key; the loader reads 2026-08-06 and REFUSES it against the scanner at 2026-10-02), U3 PASSes.
"""
import argparse
import hashlib
import json
import os
import sys

import boto3

from lib.research.peers import universe

OLD = "2026-08-06"


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def split(address):
    return address[len("s3://"):].split("/", 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior-version-id", required=True)
    ap.add_argument("--vintage", default="2026-10-02")
    args = ap.parse_args()
    os.environ.pop(universe.ENV_CACHE, None)
    s3 = boto3.client("s3", region_name="us-east-1")
    new_bucket, new_key = split(universe.candidate_universe_address(args.vintage))
    old_bucket, old_key = split(universe.candidate_universe_address(OLD))
    results = []
    body = None
    try:
        head = s3.head_object(Bucket=new_bucket, Key=new_key)
        body = s3.get_object(Bucket=new_bucket, Key=new_key)["Body"].read()
        results.append(say(True, "U1 the dated key for the scanner's vintage exists", "%s %d bytes" % (new_key, len(body))))
    except Exception as exc:  # noqa: BLE001 -- a missing key is the verdict
        head = None
        results.append(say(False, "U1 the dated key for the scanner's vintage exists", "%s: %s" % (new_key, type(exc).__name__)))
    if body is not None:
        doc = json.loads(body.decode("utf-8"))
        digest = hashlib.sha256(body).hexdigest()
        stored = (head.get("Metadata") or {}).get("document-sha256")
        rows = len(doc.get("rows") or [])
        results.append(say(doc.get("vintage") == args.vintage and rows > 0 and stored == digest,
                           "U2 vintage equals the scanner's, rows present, document-sha256 equals the bytes",
                           "vintage %s, rows %d, sha %s" % (doc.get("vintage"), rows, "equal" if stored == digest else "DIFFERENT")))
    else:
        results.append(say(False, "U2 vintage equals the scanner's, rows present, document-sha256 equals the bytes", "no object"))
    versions = s3.list_object_versions(Bucket=old_bucket, Prefix=old_key).get("Versions") or []
    versions = [v for v in versions if v["Key"] == old_key]
    latest = next((v for v in versions if v.get("IsLatest")), None)
    results.append(say(latest is not None and latest["VersionId"] == args.prior_version_id,
                       "U3 control: date=%s is untouched (current VersionId equals the prior one)" % OLD,
                       "current %s, versions %d" % (latest["VersionId"] if latest else None, len(versions))))
    try:
        loaded = universe.load_candidate_universe()
        results.append(say(loaded.get("vintage") == args.vintage, "U4 the loader returns the new vintage",
                           "loader vintage %s" % loaded.get("vintage")))
    except ValueError as exc:  # the loader REFUSES an old document against a newer scanner: that is the verdict, not a crash
        results.append(say(False, "U4 the loader returns the new vintage", "the loader raised: %s" % str(exc)[:120]))
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R93 UNIVERSE POOL: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
