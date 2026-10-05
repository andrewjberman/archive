"""Capture the 15 bodies (9 Lead Panel reads + BA, AMD, ASML_NA /overlay and /peers) via the local handler.
capture15.py <outdir>   (repo root as cwd, PYTHONPATH=<repo root>)"""

import json
import os
import sys
import time

from lib.research.api import scoped_amgt

PREFIX = "/api/scoped/amgt"
READS = [("/lead-panel/timeseries/collected/chatter", {"days": d}) for d in ("30", "90", "365")]
READS += [
    ("/lead-panel/rankings/%s/price" % mv, q)
    for mv in ("trending", "breakout")
    for q in (None, {"days": "90"}, {"days": "365"})
]
for _key in ("BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity"):
    READS += [("/security/%s/overlay" % _key, None), ("/security/%s/peers" % _key, None)]


def name(path, q):
    return path.strip("/").replace("/", "_") + ("_days" + q["days"] if q else "_default") + ".json"


def get(path, q):
    r = scoped_amgt.handler(
        {
            "rawPath": PREFIX + path,
            "requestContext": {"http": {"method": "GET"}},
            "headers": {"x-firm-id": "opal"},
            "queryStringParameters": q,
        }
    )
    return r["statusCode"], json.loads(r["body"])


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for path, q in READS:
        t = time.time()
        st, body = get(path, q)
        with open(os.path.join(out, name(path, q)), "w", encoding="utf-8", newline="\n") as f:
            json.dump(body, f, indent=1, sort_keys=True)
        print(name(path, q), st, round((time.time() - t) * 1000))
