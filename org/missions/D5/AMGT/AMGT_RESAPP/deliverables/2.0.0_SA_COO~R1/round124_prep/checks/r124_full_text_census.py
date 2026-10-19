"""AMGT_RESAPP round 124 (cf-2, cf-3): the before/after census of EVERY printed line of every covered name, PDF pack and rich export.

  python r124_full_text_census.py capture <live|local> <out.json>   read every name's pack and export, write {name: {pdf, rich}} (full text)
  python r124_full_text_census.py compare <before.json> <after.json>  the moved lines, classified

Read-only. Names: every folder under s3://opal-data-harvest/derived/model_block/ (`BP` is addressed as `BP-SLASH-_LN_Equity`). `live` invokes
GET /print?format=pdf and format=rich on opal-amgt-scoped-api; `local` runs this checkout's own Lambda handler over the live pool (the `ai_fill`
reader on its S3 default, as the live function runs it).

compare, RICH (line-structured): a line only in BEFORE is REMOVED, a line only in AFTER is ADDED. A REMOVED/ADDED pair is EXPECTED when it is
  PEERS-COLUMN  `<column>: ABSENT -- <reason>`  ->  `<column>: Not available -- <reason>`   (a line INSIDE the `## Peers` section; the same column, the same reason), or
  CHART         `The chart: ABSENT[ -- tail]`   ->  `The chart: Not available[ -- tail]`.
Every other moved line is OTHER: a row, and it stops the redeploy (the CTO's round-123 section 2). Names are listed with their counts.
compare, PDF (wrapped text): the whitespace-collapsed AFTER, with `Not available` read back as `ABSENT`, must equal the whitespace-collapsed
BEFORE with `Not available` read back as `ABSENT` (so the only difference is the word); the count of `ABSENT` removed equals the rich count.
Prints the denominator and counts; grades nothing by itself.
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
MODE = "live"
LAM = boto3.client("lambda", region_name="us-east-1")
_LOCAL = []
OLD, NEW = "ABSENT", "Not available"


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


def one(key):
    try:
        pdf, rich = fetch(key, "pdf"), fetch(key, "rich")
    except Exception as err:  # noqa: BLE001
        return key, {"error": "%s: %s" % (type(err).__name__, str(err)[:90])}
    if pdf is None or rich is None:
        return key, {"error": "status not 200 (pdf %s, rich %s)" % (pdf is not None, rich is not None)}
    return key, {"pdf": pdf, "rich": rich}


def capture(mode, out):
    global MODE
    MODE = mode
    ks = names()
    print("DENOMINATOR: %d distinct names (%s)" % (len(ks), mode))
    with cf.ThreadPoolExecutor(max_workers=1 if mode == "local" else 6) as ex:
        res = dict(ex.map(one, ks))
    ok = {k: v for k, v in res.items() if "error" not in v}
    err = {k: v for k, v in res.items() if "error" in v}
    print("NAMES READ: %d of %d (%d error)" % (len(ok), len(ks), len(err)))
    for k, v in err.items():
        print("  ERROR %-24s %s" % (k, v["error"]))
    print("LINES WITH THE LITERAL %s (rich, all names): %d; WITH %r: %d" % (
        OLD, sum(1 for v in ok.values() for ln in v["rich"].splitlines() if re.search(r"\bABSENT\b", ln)),
        NEW, sum(1 for v in ok.values() for ln in v["rich"].splitlines() if NEW in ln)))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f)
    return 0


def _collapse(text):
    return re.sub(r"\s+", " ", text.replace(NEW, OLD)).strip()


def _peers_lines(lines):
    """The lines of the `## Peers` section (from its heading to the next `## ` heading)."""
    out, inside = set(), False
    for ln in lines:
        if ln.startswith("## "):
            inside = ln.strip() == "## Peers"
            continue
        if inside:
            out.add(ln)
    return out


def _expected_pair(old, new, peers):
    m = re.match(r"^(.+?): ABSENT -- (.*)$", old)
    if m and old in peers and new == "%s: %s -- %s" % (m.group(1), NEW, m.group(2)):
        return "PEERS-COLUMN"
    m = re.match(r"^The chart: ABSENT( -- .*)?$", old)
    if m and new == "The chart: %s%s" % (NEW, m.group(1) or ""):
        return "CHART"
    return None


def compare(a, b):
    ja, jb = json.load(open(a, encoding="utf-8")), json.load(open(b, encoding="utf-8"))
    both = sorted(set(ja) & set(jb))
    skipped = [k for k in both if "error" in ja[k] or "error" in jb[k]]
    kinds, other, moved_names, pdf_bad = collections.Counter(), [], collections.Counter(), []
    pdf_removed = rich_removed = 0
    for k in both:
        if k in skipped:
            continue
        ra, rb = ja[k]["rich"].splitlines(), jb[k]["rich"].splitlines()
        only_a, only_b = [x for x in ra if x not in set(rb)], [x for x in rb if x not in set(ra)]
        peers = _peers_lines(ra)
        used = set()
        for old in only_a:
            cand = [n for n in only_b if n not in used and _expected_pair(old, n, peers)]
            if cand:
                used.add(cand[0])
                kinds[_expected_pair(old, cand[0], peers)] += 1
                moved_names[k] += 1
                rich_removed += 1
            else:
                other.append((k, "rich", "REMOVED", old))
        for new in only_b:
            if new not in used:
                other.append((k, "rich", "ADDED", new))
        if _collapse(ja[k]["pdf"]) != _collapse(jb[k]["pdf"]):
            pdf_bad.append(k)
        pdf_removed += len(re.findall(r"\bABSENT\b", ja[k]["pdf"])) - len(re.findall(r"\bABSENT\b", jb[k]["pdf"]))
    print("COMPARE: %d names in both captures, %d skipped (an error in a capture)" % (len(both), len(skipped)))
    for k in skipped:
        print("  SKIPPED %s" % k)
    print("RICH MOVED LINES (expected pairs): " + "; ".join("%s=%d" % kv for kv in sorted(kinds.items())) + "; names moved: %d" % len(moved_names))
    for k, n in sorted(moved_names.items()):
        print("  %-26s %d line(s)" % (k, n))
    print("RICH OTHER MOVED LINES (a row, stops the redeploy): %d" % len(other))
    for k, fmt, how, line in other[:60]:
        print("  OTHER %-24s %s %s: %s" % (k, fmt, how, line[:160]))
    print("PDF: %d name(s) differ beyond the word swap%s; ABSENT occurrences removed in PDF text: %d (rich pairs: %d)" % (
        len(pdf_bad), (": " + ", ".join(pdf_bad[:12])) if pdf_bad else "", pdf_removed, rich_removed))
    clean = not other and not pdf_bad and not skipped
    print("CENSUS: %s" % ("only the expected lines moved (PEERS-COLUMN and CHART)" if clean else "NOT CLEAN: read the OTHER / PDF lines above"))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "capture" and sys.argv[2] in ("live", "local"):
        sys.exit(capture(sys.argv[2], sys.argv[3]))
    if len(sys.argv) == 4 and sys.argv[1] == "compare":
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    print(__doc__)
    sys.exit(2)
