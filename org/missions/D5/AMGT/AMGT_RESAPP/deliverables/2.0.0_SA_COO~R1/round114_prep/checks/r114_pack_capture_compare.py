"""AMGT_RESAPP round 114, AMGT-bu-7 instrument: capture the LIVE printed pack text for a fixed set of names, and compare two captures.

  python r114_pack_capture_compare.py capture <outdir>            # GET /print?format=pdf on opal-amgt-scoped-api for each name, PDF text to <outdir>/<key>.txt
  python r114_pack_capture_compare.py capture-rich <outdir>        # round 115: the rich (markdown) export, <outdir>/<key>.md
  python r114_pack_capture_compare.py compare-rich <before> <after>
  python r114_pack_capture_compare.py config                       # the live function's CodeSha256, LastModified, RevisionId, memory, timeout, environment keys
  python r114_pack_capture_compare.py compare <before> <after>    # after = before with each long-form date mapped back to ISO (a hand-written inverse), whitespace collapsed, and the page-1 'Printed <run date>' day masked (it is the capture day)

Read-only (Lambda invoke of a GET). The compare grades the EXPECTED OUTCOME of the redeploy: the only difference between the
live pack before and after is dates (long form instead of ISO), and no ISO day remains after. Prints one verdict line.
"""
import base64
import json
import re
import sys

import boto3

NAMES = ["RIO_LN_Equity", "ICT_PM_Equity", "GOOGL_US_Equity", "ICICIBC_IN_Equity", "HD_US_Equity", "BA_US_Equity", "KMB_US_Equity", "TSM_US_Equity"]
FN = "opal-amgt-scoped-api"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
LONG = re.compile(r"\b(%s) (\d{1,2})(?:st|nd|rd|th), (\d{4})\b" % "|".join(MONTHS))
ISO = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
ISO_ANY = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")  # also a day followed by T..Z (a timestamp), which ISO above does not see
TS = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?Z?")


def _pdf_text(raw):
    import fitz  # PyMuPDF

    doc = fitz.open(stream=raw, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def _fetch(key):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": "pdf"},
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(boto3.client("lambda", region_name="us-east-1").invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    if r.get("statusCode") != 200:
        return None, r.get("statusCode")
    body = r.get("body") or ""
    raw = base64.b64decode(body) if r.get("isBase64Encoded") else body.encode("latin-1")
    return _pdf_text(raw), 200


def _norm(text):
    # the printed page wraps at a fixed width, so a longer date moves the wrap: compare with all whitespace collapsed
    return re.sub(r"\s+", " ", text).strip()


def _inverse(text):
    return LONG.sub(lambda m: "%s-%02d-%02d" % (m.group(3), MONTHS.index(m.group(1)) + 1, int(m.group(2))), text)


def _run_date_masked(text):
    # page 1 prints "Printed <the day the pack was built>": it differs between two captures made on different UTC days, by design
    text = re.sub(r"Printed \d{4}-\d{2}-\d{2}", "Printed <RUN DATE>", text)
    return re.sub(r"Printed (?:%s) \d{1,2}(?:st|nd|rd|th), \d{4}" % "|".join(MONTHS), "Printed <RUN DATE>", text)


def main(argv):
    if len(argv) >= 3 and argv[1] == "capture":
        out = argv[2]
        import os

        os.makedirs(out, exist_ok=True)
        got = bad = 0
        for key in NAMES:
            text, status = _fetch(key)
            if text is None:
                print("%s status %s" % (key, status))
                bad += 1
                continue
            open("%s/%s.txt" % (out, key), "w", encoding="utf-8", newline="\n").write(text)
            got += 1
            print("%s: %d chars, %d ISO days, %d long-form days" % (key, len(text), len(ISO.findall(text)), len(LONG.findall(text))))
        print("PACK CAPTURE: %d of %d names captured (%d not 200)" % (got, len(NAMES), bad))
        return 0 if bad == 0 else 1
    if len(argv) >= 4 and argv[1] == "compare":
        before, after = argv[2], argv[3]
        ok = 0
        for key in NAMES:
            b = _norm(open("%s/%s.txt" % (before, key), encoding="utf-8").read())
            a = _norm(open("%s/%s.txt" % (after, key), encoding="utf-8").read())
            iso_left = len(ISO.findall(a))
            same = _run_date_masked(_norm(_inverse(a))) == _run_date_masked(b)
            print("%s: iso_after=%d long_after=%d equal_after_inverse=%s" % (key, iso_left, len(LONG.findall(a)), same))
            ok += 1 if (same and iso_left == 0) else 0
        print("PACK COMPARE: %s (%d of %d names: no ISO day after and equal to before once the long forms map back)" % ("YES" if ok == len(NAMES) else "NO", ok, len(NAMES)))
        return 0 if ok == len(NAMES) else 1
    if len(argv) >= 3 and argv[1] == "capture-rich":
        # round 115 (AMGT-bv-5): the rich (markdown) export of the same eight names, as served text
        import os

        os.makedirs(argv[2], exist_ok=True)
        got = bad = 0
        for key in NAMES:
            ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": "rich"},
                  "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
            r = json.loads(boto3.client("lambda", region_name="us-east-1").invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
            if r.get("statusCode") != 200:
                print("%s status %s" % (key, r.get("statusCode")))
                bad += 1
                continue
            body = r.get("body") or ""
            if r.get("isBase64Encoded"):
                body = base64.b64decode(body).decode("utf-8")
            open("%s/%s.md" % (argv[2], key), "w", encoding="utf-8", newline="\n").write(body)
            got += 1
            print("%s: %d chars, %d ISO days, %d long-form days" % (key, len(body), len(ISO_ANY.findall(body)), len(LONG.findall(body))))
        print("RICH CAPTURE: %d of %d names captured (%d not 200)" % (got, len(NAMES), bad))
        return 0 if bad == 0 else 1
    if len(argv) >= 4 and argv[1] == "compare-rich":
        # the after export equals the before export once each long-form date maps back to ISO, and carries FEWER ISO days than before
        # (a source's own words, the exempt lines, keep theirs: they are equal in both)
        ok = 0
        for key in NAMES:
            b = TS.sub(r"\1", _norm(open("%s/%s.md" % (argv[2], key), encoding="utf-8").read()))
            a = TS.sub(r"\1", _norm(open("%s/%s.md" % (argv[3], key), encoding="utf-8").read()))
            same = _run_date_masked(_norm(_inverse(a))) == _run_date_masked(b)
            ib, ia = len(ISO_ANY.findall(b)), len(ISO_ANY.findall(a))
            print("%s: iso_before=%d iso_after=%d long_after=%d equal_after_inverse=%s" % (key, ib, ia, len(LONG.findall(a)), same))
            ok += 1 if (same and ia < ib or (same and ib == 0)) else 0
        print("RICH COMPARE: %s (%d of %d names: equal to before once the long forms map back, and fewer ISO days after)" % ("YES" if ok == len(NAMES) else "NO", ok, len(NAMES)))
        return 0 if ok == len(NAMES) else 1
    if len(argv) >= 4 and argv[1] == "same":
        # round 115 (AMGT-bv-5): the PDF-text packs are UNCHANGED by the act (the pack path prints no ISO day to exempt on these names):
        # the after pack equals the before pack once whitespace is collapsed and the page-1 'Printed' day is masked
        ok = 0
        for key in NAMES:
            b = _run_date_masked(_norm(open("%s/%s.txt" % (argv[2], key), encoding="utf-8").read()))
            a = _run_date_masked(_norm(open("%s/%s.txt" % (argv[3], key), encoding="utf-8").read()))
            same = a == b
            print("%s: equal=%s iso_after=%d" % (key, same, len(ISO_ANY.findall(a))))
            ok += 1 if same else 0
        print("PACK SAME: %s (%d of %d names: the pack text equals the before set)" % ("YES" if ok == len(NAMES) else "NO", ok, len(NAMES)))
        return 0 if ok == len(NAMES) else 1
    if len(argv) >= 2 and argv[1] == "config":
        c = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName=FN)
        env = sorted((c.get("Environment") or {}).get("Variables", {}).keys())
        print("CONFIG sha=%s modified=%s rev=%s mem=%s timeout=%s state=%s update=%s" % (c["CodeSha256"], c["LastModified"], c["RevisionId"], c["MemorySize"], c["Timeout"], c.get("State"), c.get("LastUpdateStatus")))
        print("ENV keys=%s" % env)
        print("AMGT_AIFILL_ROOT in env: %s" % ("AMGT_AIFILL_ROOT" in env))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
