"""C2 of the pool re-mint's CTO half (@7dfe0c3f57): one served read through the live route, plus resolve() on five
universe-sourced keys. Read-only: GET-shaped direct invokes of opal-amgt-scoped-api and pool reads. Prints one JSON document.

  python r77_pool_remint_c2_read.py [SECURITY_KEY]

With no argument it walks the covered names in sorted order and stops at the first whose served peers block names a
universe-sourced pool key. With a key it reads that name (the AFTER read names the BEFORE read's key).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sys

FN = "opal-amgt-scoped-api"
FIVE = ["2602335D_US_Equity", "MSFT_US_Equity", "PLTR_US_Equity", "BE_US_Equity", "GEV_US_Equity"]
CONTROLS = ["AMD_US_Equity", "CSCO_US_Equity"]
FIELDS = ("security_key", "resolution", "matched_as", "raw_identifier")


def _identities(node, out):
    if isinstance(node, dict):
        if isinstance(node.get("identity"), dict):
            out.append(node["identity"])
        for value in node.values():
            _identities(value, out)
    elif isinstance(node, list):
        for value in node:
            _identities(value, out)


def main():
    sys.path.insert(0, ".")
    import boto3

    from lib.research.coverage.covered_universe import covered_security_keys
    from lib.research.identity import crosswalk

    lam = boto3.client("lambda", region_name="us-east-1")

    def overlay(key):
        event = {"rawPath": "/api/scoped/amgt/security/%s/overlay" % key, "requestContext": {"http": {"method": "GET"}},
                 "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
        return raw.get("statusCode"), json.loads(raw.get("body") or "{}")

    doc, src = crosswalk._read_pool_latest()
    uni = {r["security_key"] for r in doc["records"]
           if "universe/v1" in json.dumps(r.get("provenance", {}).get("source_row", ""))}
    out = {"at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "pool": src,
           "pool_records": len(doc["records"]), "universe_sourced": len(uni)}
    want = sys.argv[1] if len(sys.argv) > 1 else None
    for key in ([want] if want else sorted(covered_security_keys())):
        code, body = overlay(key)
        peers = body.get("peers")
        hits = sorted(k for k in uni if k in json.dumps(peers))
        if want or hits:
            ids = []
            _identities(peers, ids)
            out.update({
                "name": key, "status": code, "peers_type": type(peers).__name__,
                "universe_sourced_keys_in_peers_block": hits,
                "peer_identities": [{f: i.get(f) for f in FIELDS} for i in ids],
                "peers_block_sha256": hashlib.sha256(json.dumps(peers, sort_keys=True).encode()).hexdigest(),
            })
            break
    out["resolve"] = {k: {f: crosswalk.resolve(k).get(f) for f in FIELDS} for k in FIVE + CONTROLS}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
