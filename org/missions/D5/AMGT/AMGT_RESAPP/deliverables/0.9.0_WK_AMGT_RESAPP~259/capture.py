"""Capture /lead-panel/timeseries/collected/chatter at days 30/90/365 (local handler) into a directory.
usage: python capture.py <outdir>"""
import json
import os
import sys
from lib.research.api import scoped_amgt

PATH = "/api/scoped/amgt/lead-panel/timeseries/collected/chatter"


def body(days):
    ev = {"rawPath": PATH, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
          "queryStringParameters": {"days": str(days)}}
    r = scoped_amgt.handler(ev)
    assert r.get("statusCode") == 200, r.get("statusCode")
    return json.loads(r["body"])


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for d in (30, 90, 365):
        with open(os.path.join(out, "chatter_{0}.json".format(d)), "w", encoding="utf-8", newline="\n") as f:
            json.dump(body(d), f, sort_keys=True)
    print("captured 3 to", out)
