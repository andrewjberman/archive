"""Capture /lead-panel/timeseries/collected/chatter at days 30/90/365 through the local handler into a folder.
usage: capture.py <outdir>"""
import os
import sys

from lib.research.api import scoped_amgt


def main(out):
    os.makedirs(out, exist_ok=True)
    for days in (30, 90, 365):
        ev = {"rawPath": "/api/scoped/amgt/lead-panel/timeseries/collected/chatter",
              "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
              "queryStringParameters": {"days": str(days)}}
        r = scoped_amgt.handler(ev)
        body = r.get("body") or ""
        with open(os.path.join(out, "days%d.json" % days), "w", encoding="utf-8", newline="") as fh:
            fh.write("%s\n%s" % (r.get("statusCode"), body))
        print("days", days, "status", r.get("statusCode"), "bytes", len(body))


if __name__ == "__main__":
    main(sys.argv[1])
