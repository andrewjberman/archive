"""AMGT_RESAPP round 80 -- AMGT-dd-4's deployed arm for AMGT-dd-2: no served citation names a letterless heading.

  python r80_dd4_served.py [--where deployed|local]

For every name with a stored drafting document (s3://opal-data-harvest/drafting/v1/, listed read only), GET
/security/<name>/thesis and walk the WHOLE body: every string under a key named `location` is a served citation location.
D1 the names were read and every answer was 200 (N of N);
D2 locations were served (denominator printed);
D3 0 of them carries a middle segment with no letter (the first segment is the item, the last 'paragraph N').
Verdict: R80 DD4 SERVED: YES|NO (exit 0|1). Against the live function before dd-4 it reads NO (4 letterless at the cut).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BUCKET = "opal-data-harvest"
DRAFTING = "drafting/v1/"


def letterless_middle(location):
    parts = [p.strip() for p in str(location).split(" / ")]
    return [p for p in parts[1:-1] if not any(ch.isalpha() for ch in p)]


def walk(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "location" and isinstance(v, str):
                out.append(v)
            else:
                walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("deployed", "local"), default="deployed")
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if root not in sys.path:
        sys.path.insert(0, root)
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    names = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=DRAFTING):
        names += [o["Key"][len(DRAFTING):-5] for o in page.get("Contents", []) if o["Key"].endswith(".json")]
    names.sort()
    if a.where == "deployed":
        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        def raw(event):
            return scoped_amgt.handler(event)

    ok200, locs, bad = 0, [], []
    for name in names:
        event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, name), "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        try:
            r = raw(event)
            code, body = r.get("statusCode"), json.loads(r.get("body") or "{}")
        except Exception as err:  # noqa: BLE001 -- a failed read is a FAIL line, never a crash
            code, body = "%s: %s" % (type(err).__name__, str(err)[:100]), {}
        ok200 += code == 200
        mine = []
        walk(body, mine)
        locs += mine
        bad += [(name, loc) for loc in mine if letterless_middle(loc)]
        print("   %-18s %s locations=%d letterless=%d" % (name, code, len(mine), sum(1 for loc in mine if letterless_middle(loc))))
    d1 = bool(names) and ok200 == len(names)
    d2 = len(locs) > 0
    d3 = not bad
    print("%s D1 the names were read and answered 200: %d of %d" % ("PASS" if d1 else "FAIL", ok200, len(names)))
    print("%s D2 served locations: %d" % ("PASS" if d2 else "FAIL", len(locs)))
    print("%s D3 served locations with a letterless heading: %d of %d %s" % ("PASS" if d3 else "FAIL", len(bad), len(locs), bad[:4]))
    ok = d1 and d2 and d3
    print("R80 DD4 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
