#!/usr/bin/env python3
"""THE DISCRIMINATOR FOR W1-AC4's SATELLITES-BLOCK ARM (row POSN_ASTTAX-Z-W24-S1).

POSN_ASTTAX.TO-W1-1, cell AT6-s-1, `0.9.0_WK_POSN_ASTTAX~24`.

W1-AC4 asks whether the local dry run's `satellites` block is parse-identical to the SERVED
artifact's WHEN THE INPUTS TRIPLE IS UNCHANGED. It measured: triple unchanged, blocks NOT
identical (one leaf, Opal Satellite 30 beta). There are exactly two explanations and they
must not be confused:

    (a) THE CODE moved a field it was not allowed to move  -> the never-widen half's Branch B
    (b) THE INPUT BYTES moved under an UNCHANGED as_of      -> the triple is not an identity

This runs the WORKING module over the INPUT VERSIONS THAT WERE LIVE when the served artifact
was written (read by VersionId, read-only) and compares the resulting `satellites` block to
the served one. DEEP-EQUAL on those vintages is the discriminator: same code, older bytes,
same answer -- (b), and nothing to roll back. It is the SERVED-plane companion to W1-AC3,
which already proved the code identical over one shared set of objects in memory.

NOTHING IS WRITTEN. ASCII only.
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import sys

import boto3

sys.path.insert(0, ".")
HOLDINGS = ("opal-data-cot", "platinum/satellites/holdings.json")
POSITIONING = ("opal-data-portal-v2", "json/positioning/positioning_data.json")
SERVED = ("opal-data-cot", "platinum/satellites/characteristics.json")
BBG_BUCKET = "opal-data-etfs"


def read_json(s3, bucket, key, version=None):
    kw = {"Bucket": bucket, "Key": key}
    if version:
        kw["VersionId"] = version
    raw = s3.get_object(**kw)["Body"].read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def deep_equal(a, b, path="$"):
    if type(a) is not type(b):
        return "%s: type %s != %s" % (path, type(a).__name__, type(b).__name__)
    if isinstance(a, dict):
        for k in a:
            if k not in b:
                return "%s.%s only in first" % (path, k)
        for k in b:
            if k not in a:
                return "%s.%s only in second" % (path, k)
        for k in a:
            d = deep_equal(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return "%s: len %d != %d" % (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = deep_equal(x, y, "%s[%d]" % (path, i))
            if d:
                return d
        return None
    return None if a == b else "%s: %r != %r" % (path, a, b)


def all_differences(a, b, path="$", out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(list(a) + list(b)):
            if k in a and k in b:
                all_differences(a[k], b[k], "%s.%s" % (path, k), out)
            else:
                out.append("%s.%s: only in %s" % (path, k, "first" if k in a else "second"))
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            all_differences(x, y, "%s[%d]" % (path, i), out)
    elif a != b:
        out.append("%s: %r != %r" % (path, a, b))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="input-vintage discriminator")
    ap.add_argument("--holdings-version", required=True)
    ap.add_argument("--positioning-version", required=True)
    ap.add_argument("--bbg-as-of", required=True)
    ap.add_argument("--served-version", required=True)
    a = ap.parse_args()

    import pandas as pd
    from data.assets.scripts.gold import build_satellites_characteristics as work

    s3 = boto3.client("s3")
    holdings = read_json(s3, HOLDINGS[0], HOLDINGS[1], a.holdings_version)
    positioning = read_json(s3, POSITIONING[0], POSITIONING[1], a.positioning_version)
    pq = "bbg/%s/characteristics.parquet" % a.bbg_as_of
    frame = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BBG_BUCKET, Key=pq)["Body"].read()))
    manifest = read_json(s3, BBG_BUCKET, "bbg/%s/run_manifest.json" % a.bbg_as_of)
    served = read_json(s3, SERVED[0], SERVED[1], a.served_version)

    print("INPUT VINTAGES (by VersionId, read-only):")
    print("  holdings.json        %s  as_of=%s" % (a.holdings_version, holdings.get("as_of")))
    print("  positioning_data.json %s data_as_of=%s" % (a.positioning_version, positioning.get("data_as_of")))
    print("  bbg partition        %s" % pq)
    print("  served artifact      %s  as_of=%s" % (a.served_version, served.get("as_of")))

    rows, coll, extra = work.bbg_index(frame)
    doc = work.build(holdings, positioning, rows, manifest, served.get("as_of"), a.bbg_as_of,
                     bbg_collisions=coll, bbg_extra=extra, history_loader=None)
    d = deep_equal(served.get("satellites"), doc.get("satellites"))
    print("")
    print("WORKING CODE over the SERVED artifact's OWN input vintages:")
    print("  satellites block DEEP-EQUAL to the served block: %s" % (d is None))
    if d:
        diffs = all_differences(served.get("satellites"), doc.get("satellites"))
        print("  differences: %d" % len(diffs))
        for line in diffs[:40]:
            print("    %s" % line)

    live_h = read_json(s3, *HOLDINGS)
    live_p = read_json(s3, *POSITIONING)
    print("")
    print("WHY THE LIVE RUN DIFFERS -- the same as_of on DIFFERENT BYTES:")
    print("  holdings.json  as_of %s -> %s | bytes differ: %s"
          % (holdings.get("as_of"), live_h.get("as_of"),
             json.dumps(holdings, sort_keys=True) != json.dumps(live_h, sort_keys=True)))
    print("  positioning    data_as_of %s -> %s | bytes differ: %s"
          % (positioning.get("data_as_of"), live_p.get("data_as_of"),
             json.dumps(positioning, sort_keys=True) != json.dumps(live_p, sort_keys=True)))
    return 0 if d is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
