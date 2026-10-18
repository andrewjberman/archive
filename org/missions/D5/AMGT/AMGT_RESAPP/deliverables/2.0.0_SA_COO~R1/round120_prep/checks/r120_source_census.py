"""AMGT_RESAPP round 120 (ca-2, ca-4): the census of every SOURCE line in the printed pack and the rich export of EVERY covered name.

  python r120_source_census.py [live|local] [outfile.json]      (default live)

Read-only. Names: every folder under s3://opal-data-harvest/derived/model_block/ (`BP` is addressed as `BP-SLASH-_LN_Equity`).
For each name it fetches the PDF pack (`format=pdf`) and the rich export (`format=rich`) and reads:
  PDF   every line after the heading `Appendix: model figures` that looks like `<label>: <value> - <source>[ - <date text>]`; the source is the
        segment after the first ` - ` that follows the colon (the date segment, when present, is the last); a line whose source segment is exactly `?`
        or empty is a QUESTION-MARK SOURCE; a line whose source segment reads `source not stated` is a STATED ABSENCE.
  RICH  every table cell and every ` - ` segment equal to exactly `?`.
Prints the denominator, the totals, the distinct source words with counts, every question-mark source (name, line) and every stated absence.
It grades nothing by itself: the grade (no `?` source anywhere, each absent source stated) is the reader's.
"""
import base64
import collections
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
_LOCAL = []
DATE_TAIL = re.compile(r"(?i)(date not stored|as of|period|\b(19|20)\d\d\b)")


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
    if MODE == "local":
        r = _handler()(ev, None)
    else:
        r = json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())
    if r.get("statusCode") != 200:
        return None
    body = base64.b64decode(r["body"]) if r.get("isBase64Encoded") else r["body"].encode("utf-8")
    if fmt == "pdf":
        return "\n".join(p.get_text() for p in fitz.open(stream=body, filetype="pdf"))
    return body.decode("utf-8")


def source_of(line):
    """The source segment of an appendix figure line, or None when the line is not a figure line."""
    if ": " not in line:
        return None
    rest = line.split(": ", 1)[1]
    segs = rest.split(" - ")
    if len(segs) < 2:
        return None
    tail = segs[1:]
    if len(tail) >= 2 and DATE_TAIL.search(tail[-1]):
        return tail[0].strip()
    return tail[-1].strip()


def scan(key):
    try:
        pdf, rich = fetch(key, "pdf"), fetch(key, "rich")
    except Exception as err:  # noqa: BLE001
        return key, {"error": "%s: %s" % (type(err).__name__, str(err)[:90])}
    if pdf is None or rich is None:
        return key, {"error": "status not 200 (pdf %s, rich %s)" % (pdf is not None, rich is not None)}
    lines = [ln.strip() for ln in pdf.splitlines() if ln.strip()]
    try:
        app = lines.index("Appendix: model figures")
    except ValueError:
        app = len(lines)
    words, qmark, stated = collections.Counter(), [], []
    for ln in lines[app + 1:]:
        s = source_of(ln)
        if s is None:
            continue
        if s in ("", "?"):
            qmark.append(ln[:140])
        elif s == "source not stated":
            stated.append(ln[:140])
        words[s if len(s) <= 40 else s[:40] + "..."] += 1
    rich_q = [ln.strip()[:140] for ln in rich.splitlines()
              if re.search(r"\|\s*\?\s*(\||$)", ln) or re.search(r" - \?\s*$", ln.strip())]
    return key, {"words": dict(words), "qmark": qmark, "stated": stated, "rich_qmark": rich_q}


def main():
    ks = names()
    print("DENOMINATOR: %d distinct names (%s)" % (len(ks), MODE))
    with cf.ThreadPoolExecutor(max_workers=1 if MODE == "local" else 6) as ex:
        res = list(ex.map(scan, ks))
    ok = [(k, r) for k, r in res if "error" not in r]
    err = [(k, r) for k, r in res if "error" in r]
    allwords = collections.Counter()
    for _, r in ok:
        allwords.update(r["words"])
    q = [(k, ln) for k, r in ok for ln in r["qmark"]]
    st = [(k, ln) for k, r in ok for ln in r["stated"]]
    rq = [(k, ln) for k, r in ok for ln in r["rich_qmark"]]
    print("NAMES READ: %d of %d (%d error)" % (len(ok), len(ks), len(err)))
    for k, r in err:
        print("  ERROR %-24s %s" % (k, r["error"]))
    print("SOURCE WORDS (appendix, distinct, count): " + "; ".join("%s=%d" % (w, c) for w, c in allwords.most_common(25)))
    print("QUESTION-MARK SOURCES in the PDF appendix: %d line(s) on %d name(s)" % (len(q), len({k for k, _ in q})))
    for k, ln in q[:60]:
        print("  QMARK %-24s %s" % (k, ln))
    print("STATED ABSENCES (`source not stated`) in the PDF appendix: %d line(s) on %d name(s)" % (len(st), len({k for k, _ in st})))
    for k, ln in st[:30]:
        print("  STATED %-24s %s" % (k, ln))
    print("QUESTION-MARK SOURCES in the rich exports: %d line(s) on %d name(s)" % (len(rq), len({k for k, _ in rq})))
    for k, ln in rq[:30]:
        print("  RICHQ %-24s %s" % (k, ln))
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            json.dump([{"key": k, **r} for k, r in res], f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
