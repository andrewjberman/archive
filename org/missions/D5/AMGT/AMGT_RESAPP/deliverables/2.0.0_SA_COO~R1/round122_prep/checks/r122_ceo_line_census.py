"""AMGT_RESAPP round 122 (cc-1, cc-2): the census of the printed CEO-profile LINE of every covered name, in the PDF pack and the rich export.

  python r122_ceo_line_census.py capture <live|local> <out.json>     read every name's pack and export, write {name: {pdf, rich}}
  python r122_ceo_line_census.py compare <a.json> <b.json>           the names whose printed line differs between two captures

Read-only. Names: every folder under s3://opal-data-harvest/derived/model_block/ (`BP` is addressed as `BP-SLASH-_LN_Equity`). `live` invokes
GET /print?format=pdf and format=rich on opal-amgt-scoped-api; `local` runs this checkout's own Lambda handler over the live pool (the `ai_fill` reader
on its S3 default, as the live function runs it). The line is `CEO public profile...` from the first such line to the end of its wrapped continuation
(the following lines that start with whitespace in the PDF text), joined by single spaces; in the export, the one line that starts with `CEO public
profile`. A name with no such line (a cleared management passage printed instead) reads `(none)`. The CTO's round-121 grade: if every printed line is
byte-identical between the live function and the candidate, the change is DELTA=0 and needs no never-widen pair; if any line moves, the moved names are
listed. Prints the denominator and counts; grades nothing by itself.
"""
import base64
import collections
import concurrent.futures as cf
import importlib.util
import json
import os
import sys

import boto3

os.environ.pop("AMGT_AIFILL_ROOT", None)
sys.path.insert(0, ".")
import fitz  # noqa: E402

FN = "opal-amgt-scoped-api"
BUCKET = "opal-data-harvest"
PREFIX = "derived/model_block/"
MODE = "live"
LAM = boto3.client("lambda", region_name="us-east-1")
_LOCAL = []
LABEL = "CEO public profile"


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


def fetch(key, fmt):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/print" % key, "queryStringParameters": {"format": fmt},
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = _handler()(ev, None) if MODE == "local" else json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    if r.get("statusCode") != 200:
        return None
    body = base64.b64decode(r["body"]) if r.get("isBase64Encoded") else r["body"].encode("utf-8")
    if fmt == "pdf":
        return "\n".join(p.get_text() for p in fitz.open(stream=body, filetype="pdf"))
    return body.decode("utf-8")


def pdf_line(text):
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith(LABEL):
            parts = [ln.strip()]
            for nxt in lines[i + 1:]:
                if nxt[:1] in (" ", "\t") and nxt.strip():
                    parts.append(nxt.strip())
                else:
                    break
            return " ".join(parts)
    return "(none)"


def rich_line(text):
    for ln in text.splitlines():
        if ln.strip().startswith(LABEL):
            return ln.strip()
    return "(none)"


def one(key):
    try:
        pdf, rich = fetch(key, "pdf"), fetch(key, "rich")
    except Exception as err:  # noqa: BLE001
        return key, {"error": "%s: %s" % (type(err).__name__, str(err)[:90])}
    if pdf is None or rich is None:
        return key, {"error": "status not 200 (pdf %s, rich %s)" % (pdf is not None, rich is not None)}
    return key, {"pdf": pdf_line(pdf), "rich": rich_line(rich)}


def capture(mode, out):
    global MODE
    MODE = mode
    ks = names()
    print("DENOMINATOR: %d distinct names (%s)" % (len(ks), mode))
    with cf.ThreadPoolExecutor(max_workers=1 if mode == "local" else 6) as ex:
        res = dict(ex.map(one, ks))
    ok = {k: v for k, v in res.items() if "error" not in v}
    err = {k: v for k, v in res.items() if "error" in v}
    kinds = collections.Counter()
    for v in ok.values():
        kinds[v["pdf"][:60] if v["pdf"] != "(none)" else "(none)"] += 1
    print("NAMES READ: %d of %d (%d error)" % (len(ok), len(ks), len(err)))
    for k, v in err.items():
        print("  ERROR %-24s %s" % (k, v["error"]))
    print("PDF LINE KINDS (first 60 chars, count): " + "; ".join("%s=%d" % kv for kv in kinds.most_common(12)))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    return 0


def compare(a, b):
    ja, jb = json.load(open(a, encoding="utf-8")), json.load(open(b, encoding="utf-8"))
    both = sorted(set(ja) & set(jb))
    moved, same, skipped = [], 0, []
    for k in both:
        if "error" in ja[k] or "error" in jb[k]:
            skipped.append(k)
            continue
        if ja[k] == jb[k]:
            same += 1
        else:
            moved.append(k)
    print("COMPARE: %d names in both captures, %d byte-identical (pdf and rich), %d MOVED, %d skipped (an error in a capture)" % (len(both), same, len(moved), len(skipped)))
    for k in skipped:
        print("  SKIPPED %s" % k)
    for k in moved:
        for fmt in ("pdf", "rich"):
            if ja[k][fmt] != jb[k][fmt]:
                print("  MOVED %-24s %s\n      before: %s\n      after : %s" % (k, fmt, ja[k][fmt][:200], jb[k][fmt][:200]))
    print("DELTA: %s" % ("0 (every printed CEO line is byte-identical)" if not moved else "%d name(s) moved: a never-widen pair is owed" % len(moved)))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "capture" and sys.argv[2] in ("live", "local"):
        sys.exit(capture(sys.argv[2], sys.argv[3]))
    if len(sys.argv) == 4 and sys.argv[1] == "compare":
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(2)
