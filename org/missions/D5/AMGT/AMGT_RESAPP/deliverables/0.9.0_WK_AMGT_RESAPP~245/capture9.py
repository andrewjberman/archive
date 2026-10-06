"""Capture the 9 Lead Panel bodies via the local handler.
capture9.py <outdir>   (repo root as cwd, PYTHONPATH=<repo root>)"""

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
