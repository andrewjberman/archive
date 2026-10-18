"""AMGT_RESAPP round 118: scan the printed pack of EVERY covered name for a storage path, an order id or a vendor error in reader-facing text.

  python r118_leak_scan.py [live|local] [outfile.json]      (default live)

Read-only. `live` invokes GET /print?format=pdf on opal-amgt-scoped-api per name; `local` runs this checkout's own Lambda handler over the live pool
(with the `ai_fill` reader on its S3 default, as the live function runs it). Names: every folder under s3://opal-data-harvest/derived/model_block/
(a slash-encoded folder `BP` is addressed as `BP-SLASH-_LN_Equity`). A line is a LEAK when it matches s3://, an `AMGT-<letters>` id, NoSuchKey, a
`.json` or `.docx` file name, or an UPPER_SNAKE token outside the lines of the figure appendix that legitimately name a mnemonic. Prints the
denominator, the count of names with at least one leak, and every leaking line (name, line, 140 characters). It grades nothing by itself.
"""
import base64
import concurrent.futures as cf
import importlib.util
import json
import os
import re
import sys

import boto3

os.environ.pop("AMGT_AIFILL_ROOT", None)
sys.path.insert(0, ".")
import fitz  # noqa: E402

FN = "opal-amgt-scoped-api"
BUCKET = "opal-data-harvest"
PREFIX = "derived/model_block/"
MODE = (sys.argv[1] if len(sys.argv) > 1 else "live")
LAM = boto3.client("lambda", region_name="us-east-1")
LEAK = re.compile(r"s3://|\bAMGT-[A-Za-z]|NoSuchKey|\.json\b|\.docx\b|Traceback|botocore")
SNAKE = re.compile(r"\b[A-Z]{2,}(?:_[A-Z0-9]+)+\b")
_LOCAL = []


def _handler():
    if not _LOCAL:
        spec = importlib.util.spec_from_file_location("lam", "infra/aws/lambda/research/scoped_amgt_api/lambda_function.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        os.environ.pop("AMGT_AIFILL_ROOT", None)
        _LOCAL.append(mod.lambda_handler)
    return _LOCAL[0]


def names():
    s3 = boto3.client("s3", region_name="us-east-1")
    out, tok = [], None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [p["Prefix"][len(PREFIX):-1] for p in r.get("CommonPrefixes", [])]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    fix = {"BP": "BP-SLASH-_LN_Equity"}
    return sorted({fix.get(k, k) for k in out})


def pack_text(key):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": "pdf"},
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if MODE == "local":
        r = _handler()(ev, None)
    else:
        r = json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    if r.get("statusCode") != 200:
        return None, r.get("statusCode")
    raw = base64.b64decode(r["body"])
    return "\n".join(p.get_text() for p in fitz.open(stream=raw, filetype="pdf")), 200


def scan(key):
    try:
        t, st = pack_text(key)
    except Exception as err:  # noqa: BLE001
        return key, "ERROR", ["%s: %s" % (type(err).__name__, str(err)[:90])]
    if t is None:
        return key, "ERROR", ["status %s" % st]
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    try:
        app = lines.index("Appendix: model figures")
    except ValueError:
        app = len(lines)
    hits = []
    for i, ln in enumerate(lines):
        if LEAK.search(ln) or (i < app and SNAKE.search(ln)):
            hits.append(ln[:140])
    return key, ("LEAK" if hits else "CLEAN"), hits


def main():
    ks = names()
    print("DENOMINATOR: %d distinct names (%s)" % (len(ks), MODE))
    with cf.ThreadPoolExecutor(max_workers=1 if MODE == "local" else 6) as ex:
        res = list(ex.map(scan, ks))
    leak = [r for r in res if r[1] == "LEAK"]
    err = [r for r in res if r[1] == "ERROR"]
    for k, _, h in leak:
        for ln in h[:3]:
            print("  LEAK %-24s %s" % (k, ln))
    for k, _, h in err:
        print("  ERROR %-24s %s" % (k, h[0]))
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            json.dump([{"key": k, "class": c, "lines": h} for k, c, h in res], f, indent=1)
    print("LEAK SCAN: %s (%d leaking, %d error, %d clean of %d)" % ("NO LEAK" if not leak and not err else "LEAKS", len(leak), len(err), len(res) - len(leak) - len(err), len(res)))
    return 0 if not leak and not err else 1


if __name__ == "__main__":
    sys.exit(main())
