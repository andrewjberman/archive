"""AMGT-ba-11 AC2: the print route's PDF body, rebuilt now, equals the one captured before the edit.

Comparison: page count AND the extracted text of every page (pypdf, layout mode). Raw bytes are NOT compared: a PDF
carries its creation time, so two renders of the same content can differ in bytes. Prints `EQUAL n of 3`; exit 0 only
on 3. The `before/` PDFs were captured from the base (text step on) by capture_print.py.
"""
import base64
import pathlib
import sys
import time

import pypdf

from lib.research.api import scoped_amgt

HERE = pathlib.Path(__file__).resolve().parent
NAMES = ["BA_US_Equity", "AMD_US_Equity", "ASML_NA_Equity"]


def pages_text(path):
    reader = pypdf.PdfReader(str(path))
    return [(pg.extract_text(extraction_mode="layout") or "") for pg in reader.pages]


def main():
    equal = 0
    for k in NAMES:
        ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % k, "requestContext": {"http": {"method": "GET"}},
              "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
        started = time.time()
        r = scoped_amgt.handler(ev)
        seconds = time.time() - started
        before = HERE / "before" / (k + ".pdf")
        if r.get("statusCode") != 200 or not before.exists():
            print("%s: status %s, before present %s -> NOT EQUAL" % (k, r.get("statusCode"), before.exists()))
            continue
        after = HERE / "after" / (k + ".pdf")
        after.parent.mkdir(exist_ok=True)
        after.write_bytes(base64.b64decode(r["body"]))
        text_before, text_after = pages_text(before), pages_text(after)
        same = len(text_before) == len(text_after) and text_before == text_after
        print("%s: pages before %d after %d; text %s; %.2fs; bytes %d vs %d" % (
            k, len(text_before), len(text_after), "IDENTICAL" if same else "DIFFERS", seconds,
            before.stat().st_size, after.stat().st_size))
        equal += same
    print("EQUAL %d of 3" % equal)
    return 0 if equal == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
