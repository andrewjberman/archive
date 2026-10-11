"""AMGT_RESAPP round-92 PREP -- AMGT-qq-4: every stored analysis object's re-verified driver is the driver the live /thesis route serves.

  PYTHONPATH=<repo root> python r92_driver_reverified.py [--where deployed|local]

For each stored analysis object (`filings/v1/<key>/<accession>.analysis.json`, listed, not typed): EXPECTED is what the production path
`analyze.reverify_stored_thesis_driver(key, accession, dry_run=True)` computes TODAY on the checkout's code (nothing written); SERVED is
`thesis_driver.points` of the live `/security/<key>/thesis` (the drafting object's driver). The check compares (period, value, span).
    R1 every name whose expected points differ from its stored analysis's points is SERVED with the expected points (the act's effect).
    R2 control: every name whose expected points equal the stored analysis's is served byte-equal to what it served before (it is
       compared to the same expectation, and any difference is a name the act moved without a reason).
    R3 denominators printed: analysis objects, with a served driver, expected-changed, served-equal.
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
    args = ap.parse_args()
    pairs = []
    for page in _S3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-harvest", Prefix="filings/v1/"):
        for o in page.get("Contents", []):
            m = re.match(r"^filings/v1/([^/]+)/([^/]+)\.analysis\.json$", o["Key"])
            if m:
                pairs.append((m.group(1), m.group(2)))
    n = served_n = changed = equal = bad_changed = bad_control = 0
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
        is_changed = expected != stored_pts
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
    for ok, label in ((r1, "R1 every expected-changed name is served with the expected points (at least one such name)"),
                      (r2, "R2 control: every expected-same name is served as expected")):
        print("%s %s" % ("PASS" if ok else "FAIL", label))
    ok = r1 and r2
    print("R92 DRIVER REVERIFIED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
