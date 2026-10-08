"""DSGN_AMGTV1 round 53 -- capture the served bodies the round-53 cells draw (read only).

  python capture_served.py

GET-shaped direct invokes of opal-amgt-scoped-api (the AMGT_RESAPP round-79 deployed function), the same event shape
AMGT_RESAPP's r79_cc6.py --where deployed sends. Writes one JSON per read into ./served/ beside this file and prints one
line per read: path, http code, and the field the round draws. No store write, no vendor, web or model call.
"""
from __future__ import annotations

import json
import os

import boto3

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "served")
THESIS_NAMES = ("AMD_US_Equity", "ASML_NA_Equity", "NU_US_Equity", "8766_JP_Equity", "HD_US_Equity")


def main():
    os.makedirs(OUT, exist_ok=True)
    lam = boto3.client("lambda", region_name="us-east-1")

    def get(path, query=None):
        event = {"rawPath": PREFIX + path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
                 "queryStringParameters": query}
        r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
        return r.get("statusCode"), json.loads(r.get("body") or "{}")

    for name in THESIS_NAMES:
        code, body = get("/security/%s/thesis" % name)
        with open(os.path.join(OUT, "thesis_%s.json" % name), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(body, fh, indent=1, sort_keys=True)
        st = body.get("segment_table") or {}
        ds = body.get("dossier_sections") or []
        print("thesis %s http %s; segment_table status %r rows %d; dossier_sections %s" % (
            name, code, st.get("status"), len(st.get("rows") or []),
            [(e.get("field"), e.get("status")) for e in ds if isinstance(e, dict)]))

    code, page = get("/freshness", {"view": "page"})
    with open(os.path.join(OUT, "freshness_page.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(page, fh, indent=1, sort_keys=True)
    states = {}
    for row in page.get("rows") or []:
        s = (row.get("seeking_alpha") or {}).get("state")
        states[s] = states.get(s, 0) + 1
    print("freshness?view=page http %s; rows %d; seeking_alpha states %s; snapshot %s" % (
        code, len(page.get("rows") or []), json.dumps(states, sort_keys=True, default=str),
        json.dumps(page.get("snapshot"), default=str)[:160]))


if __name__ == "__main__":
    main()
