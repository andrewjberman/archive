"""AMGT_RESAPP round 118, AMGT-by-3: the C-S189 census across every covered name.

  python r118_cs189_census.py [outfile.json]

Read-only (S3 listing of the model-block pool, and Lambda invokes of GET /thesis and GET /print?format=pdf on opal-amgt-scoped-api).
Denominator: every security key that has a folder under `derived/model_block/` in the pool bucket. For each key it reads the served
`dossier_fields.last_stated_position` (status and value text) and the LIVE printed pack's Summary section, and classifies:
  PRINTED          the position is SERVED and its text appears in the Summary of the printed pack
  NOT-PRINTED      the position is SERVED and its text is NOT in the Summary: a DEFECT (listed with the Summary's first lines)
  ABSENT:<why>     the position is not served (status and reason, plain): the Summary reads the no-recommendation sentence or a drafted one
  ERROR            a request did not return 200 (the status and a reason)
Prints the counts with the denominator and every name that is not PRINTED or ABSENT with its cause. It grades nothing by itself.
"""
import base64
import concurrent.futures as cf
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
LAM = boto3.client("lambda", region_name="us-east-1")


def keys():
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
    return sorted(out)


def _call(key, route, query=None):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/%s" % (key, route), "queryStringParameters": query,
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    return json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())


def summary_of(text):
    lines = [ln.rstrip() for ln in text.splitlines()]
    try:
        i = lines.index("Summary")
    except ValueError:
        return None
    j = i + 1
    while j < len(lines) and lines[j] not in ("Thesis pillars", "Risks and considerations"):
        j += 1
    return "\n".join(lines[i + 1:j])


def _norm(s):
    return re.sub(chr(92) + "s+", " ", s).strip().lower()


def one(key):
    try:
        t = _call(key, "thesis")
        if t.get("statusCode") != 200:
            return key, "ERROR", "thesis status %s" % t.get("statusCode")
        body = json.loads(t["body"])
        lsp = (body.get("dossier_fields") or {}).get("last_stated_position") or {}
        status = lsp.get("status")
        text = ((lsp.get("value") or {}).get("text") or "").strip()
        p = _call(key, "print", {"format": "pdf"})
        if p.get("statusCode") != 200:
            return key, "ERROR", "print status %s" % p.get("statusCode")
        raw = base64.b64decode(p["body"])
        pack = "\n".join(pg.get_text() for pg in fitz.open(stream=raw, filetype="pdf"))
        summ = summary_of(pack) or ""
        if status == "SERVED" and text:
            if _norm(text) in _norm(summ):
                return key, "PRINTED", text
            return key, "NOT-PRINTED", "served %r; Summary begins %r" % (text, _norm(summ)[:140])
        why = (lsp.get("reason") or "")[:100] if isinstance(lsp.get("reason"), str) else ""
        return key, "ABSENT", "status=%s %s | Summary begins %r" % (status, why, _norm(summ)[:90])
    except Exception as err:  # noqa: BLE001
        return key, "ERROR", "%s: %s" % (type(err).__name__, str(err)[:100])


def main(argv):
    ks = keys()
    print("DENOMINATOR: %d security keys under s3://%s/%s" % (len(ks), BUCKET, PREFIX))
    res = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(one, ks):
            res.append(r)
    counts = {}
    for _, c, _ in res:
        counts[c] = counts.get(c, 0) + 1
    print("COUNTS: " + ", ".join("%s=%d" % kv for kv in sorted(counts.items())) + " (of %d)" % len(res))
    for k, c, d in res:
        if c in ("NOT-PRINTED", "ERROR"):
            print("  %-12s %-22s %s" % (c, k, d))
    absent = [(k, d) for k, c, d in res if c == "ABSENT"]
    print("ABSENT (%d): the position is not served; sample causes:" % len(absent))
    causes = {}
    for k, d in absent:
        causes.setdefault(d.split("|")[0].strip(), []).append(k)
    for cause, ks2 in sorted(causes.items(), key=lambda kv: -len(kv[1])):
        print("  %3d x %s  e.g. %s" % (len(ks2), cause[:110], ", ".join(ks2[:3])))
    if len(argv) > 1:
        with open(argv[1], "w", encoding="utf-8") as f:
            json.dump([{"key": k, "class": c, "detail": d} for k, c, d in res], f, indent=1)
    ok = counts.get("NOT-PRINTED", 0) == 0 and counts.get("ERROR", 0) == 0
    print("C-S189 CENSUS: %s (%d PRINTED, %d ABSENT, %d NOT-PRINTED, %d ERROR of %d)" % ("YES" if ok else "NO", counts.get("PRINTED", 0), counts.get("ABSENT", 0), counts.get("NOT-PRINTED", 0), counts.get("ERROR", 0), len(res)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
