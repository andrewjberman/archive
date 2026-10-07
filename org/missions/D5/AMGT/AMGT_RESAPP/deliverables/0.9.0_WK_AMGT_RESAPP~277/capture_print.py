"""Capture the PDF route's body for three names into a directory; print per-name wall time."""
import base64
import pathlib
import sys
import time

from lib.research.api import scoped_amgt

NAMES = ["BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity"]


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    for k in NAMES:
        ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % k, "requestContext": {"http": {"method": "GET"}},
              "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        started = time.time()
        r = scoped_amgt.handler(ev)
        print(k, r.get("statusCode"), "%.2fs" % (time.time() - started), len(r.get("body") or ""))
        if r.get("statusCode") == 200:
            (out / (k + ".pdf")).write_bytes(base64.b64decode(r["body"]))
        else:
            (out / (k + ".err")).write_text(r.get("body") or "")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
