"""Read-only census: which covered names serve the seven header figures as reasoned nulls with the blockless
reason ("We hold no stored company data for this name yet.") on the DEPLOYED opal-amgt-scoped-api.

  python r77_blockless_census.py            # all covered names, GET-shaped direct invokes, no write
  python r77_blockless_census.py --one KEY  # one name, prints its header figures and identity

Asked by 1.0.0_SA_CTO~Z msg 30798 (DSGN_AMGTV1 round-46 grade, FWD-4, MSFT US). Prints its denominator.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
BLOCKLESS = "no stored company data"


def _walk(node, path, out, depth=0):
    """Collect (path, value) for every string value carrying the blockless reason."""
    if depth > 7:
        return
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str) and BLOCKLESS in value:
                out.append((path + "/" + key, value))
            _walk(value, path + "/" + key, out, depth + 1)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            _walk(value, "%s[%d]" % (path, i), out, depth + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--one", default=None)
    ap.add_argument("--dump", default=None, help="write the --one overlay body to this path")
    a = ap.parse_args()
    import boto3

    sys.path.insert(0, ".")
    from lib.research.coverage.covered_universe import covered_security_keys

    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("deployed %s CodeSha256 %s LastModified %s" % (FN, cfg["CodeSha256"], cfg["LastModified"]))

    def overlay(key):
        event = {"rawPath": "%s/security/%s/overlay" % (PREFIX, key), "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
        try:
            return raw.get("statusCode"), json.loads(raw.get("body") or "{}")
        except (ValueError, TypeError):
            return raw.get("statusCode"), {}

    if a.one:
        code, body = overlay(a.one)
        hits = []
        _walk(body, "", hits)
        print("%s status %s top-level keys %d" % (a.one, code, len(body)))
        print("paths carrying the blockless reason: %d" % len(hits))
        for path, _ in hits[:12]:
            print("  ", path)
        if a.dump:
            with open(a.dump, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(body, fh, indent=1, sort_keys=True)
        return 0

    keys = sorted(covered_security_keys())
    blockless, served, bad = [], [], []
    containers = collections.Counter()
    for key in keys:
        code, body = overlay(key)
        if code != 200:
            bad.append((key, code))
            continue
        hits = []
        _walk(body, "", hits)
        if hits:
            blockless.append((key, len(hits)))
            for path, _ in hits:
                containers[path.split("[")[0]] += 1
        else:
            served.append(key)
    print("DENOMINATOR: %d covered names; status 200 on %d; non-200 on %d %s" % (len(keys), len(keys) - len(bad), len(bad), bad[:5]))
    print("BLOCKLESS (the reason appears in the overlay): %d" % len(blockless))
    for key, n in blockless:
        print("   %s  (%d fields)" % (key, n))
    print("NOT blockless: %d   e.g. %s" % (len(served), served[:5]))
    print("containers of the reason: %s" % dict(containers))
    return 0


if __name__ == "__main__":
    sys.exit(main())
