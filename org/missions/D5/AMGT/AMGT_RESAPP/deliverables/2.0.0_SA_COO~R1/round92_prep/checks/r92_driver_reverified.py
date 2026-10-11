"""AMGT_RESAPP round-92 PREP -- AMGT-qq-4: every stored analysis object's re-verified driver is the driver the live /thesis route serves.

  PYTHONPATH=<repo root> python r92_driver_reverified.py [--where deployed|local] [--hold KEY[,KEY...]] [--write-set KEY[,KEY...]]

For each stored analysis object (`filings/v1/<key>/<accession>.analysis.json`, listed, not typed): EXPECTED is what the production path
`analyze.reverify_stored_thesis_driver(key, accession, dry_run=True)` computes TODAY on the checkout's code (nothing written); SERVED is
`thesis_driver.points` of the live `/security/<key>/thesis` (the drafting object's driver). The check compares (period, value, span).
    R1 every name whose expected points differ from its stored analysis's points is SERVED with the expected points (the act's effect).
    R2 control: every name whose expected points equal the stored analysis's is served byte-equal to what it served before (it is
       compared to the same expectation, and any difference is a name the act moved without a reason).
    R3 denominators printed: analysis objects, with a served driver, expected-changed, served-equal.
    --write-set KEY,...  the names the act WRITES. A name in it is graded as expected-changed whatever the stored object now holds, so
       the check reads the same verdict before the write (NO: served != expected) and after it (YES: served == expected); without it the
       class is computed from stored != expected, which is empty once the write has landed (RA1's finding, msg 3717).
    --hold KEY,...  names the issuer HOLDS out of the write (round 92: `SAP_GY_Equity`, whose expected points mix a EUR-millions
       rendering (2023, 2024) with a EUR-billions one (2025)): a held name must still serve its STORED points (it is not written),
       its would-be expected points are printed, and a held name that is not expected-changed fails R4 (a stale hold).
Verdict: R92 DRIVER REVERIFIED: YES|NO (exit 0|1). Before the act the expected-changed names read NO.
"""
import argparse
import json
import re
import sys

import boto3

from lib.research.api import scoped_amgt
from lib.research.filings import analyze

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
_LAM = boto3.client("lambda", region_name="us-east-1")
_S3 = boto3.client("s3", region_name="us-east-1")


def thesis(where, key):
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if where == "deployed":
        r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        r = scoped_amgt.handler(event)
    return json.loads(r.get("body") or "{}")


def triples(points):
    return sorted((str(p.get("period")), str(p.get("value")), json.dumps(p.get("span"))) for p in points or [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    ap.add_argument("--hold", default="")
    ap.add_argument("--write-set", default="")
    args = ap.parse_args()
    pairs = []
    for page in _S3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-harvest", Prefix="filings/v1/"):
        for o in page.get("Contents", []):
            m = re.match(r"^filings/v1/([^/]+)/([^/]+)\.analysis\.json$", o["Key"])
            if m:
                pairs.append((m.group(1), m.group(2)))
    hold = {k for k in args.hold.split(",") if k}
    write_set = {k for k in args.write_set.split(",") if k}
    seen_write = set()
    n = served_n = changed = equal = bad_changed = bad_control = 0
    held_changed = set()
    lines = []
    for key, acc in sorted(pairs):
        n += 1
        stored = json.loads(_S3.get_object(Bucket="opal-data-harvest", Key="filings/v1/%s/%s.analysis.json" % (key, acc))["Body"].read())
        doc, _k, _r = analyze.reverify_stored_thesis_driver(key, acc, client=_S3, dry_run=True)
        expected = triples((doc.get("thesis_driver") or {}).get("points"))
        stored_pts = triples((stored.get("thesis_driver") or {}).get("points"))
        body = thesis(args.where, key)
        td = body.get("thesis_driver")
        if not isinstance(td, dict):
            lines.append("   %-16s no served driver (no drafting object or no driver)" % key)
            continue
        served_n += 1
        served = triples(td.get("points"))
        is_changed = expected != stored_pts or key in write_set
        if key in write_set:
            seen_write.add(key)
        if key in hold:
            if is_changed:
                held_changed.add(key)
            ok = served == stored_pts
            bad_control += (not ok)
            equal += 1
            lines.append("   %-16s HELD    | would-be expected %d point(s) %s | stored %d | served %d | %s" % (
                key, len(expected), expected, len(stored_pts), len(served), "OK (stored points still served)" if ok else "SERVED != STORED"))
            continue
        ok = served == expected
        if is_changed:
            changed += 1
            bad_changed += (not ok)
        else:
            equal += 1
            bad_control += (not ok)
        lines.append("   %-16s %s | expected %d point(s) | stored %d | served %d | %s" % (
            key, "CHANGED" if is_changed else "same   ", len(expected), len(stored_pts), len(served), "OK" if ok else "SERVED != EXPECTED"))
    print("\n".join(lines))
    print("   where=%s analysis objects %d | with a served driver %d | expected-changed %d | expected-same %d" % (
        args.where, n, served_n, changed, equal))
    r1 = bad_changed == 0 and changed >= 1
    r2 = bad_control == 0
    r4 = hold <= held_changed
    r5 = write_set <= seen_write and not (write_set & hold)
    for ok, label in ((r1, "R1 every expected-changed name is served with the expected points (at least one such name)"),
                      (r2, "R2 control: every expected-same name (and every held name) is served as expected")) + (
            ((r4, "R4 every held name is expected-changed (no stale hold): %s" % ",".join(sorted(hold))),) if hold else ()) + (
            ((r5, "R5 every write-set name is a listed analysis object and none is held: %s" % ",".join(sorted(write_set))),) if write_set else ()):
        print("%s %s" % ("PASS" if ok else "FAIL", label))
    ok = r1 and r2 and r4 and r5
    print("R92 DRIVER REVERIFIED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
