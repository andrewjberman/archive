"""AMGT_RESAPP round-110 PREP -- the served DELTA of `AMGT-bp-3` (the label of an unresolved segment column, merged @1514402a12): the blast radius of its redeploy (`AMGT-bp-6`).

  PYTHONPATH=<repo root> python r110_bp3_served_delta.py <out.json> [--workers 4] [--limit N]

For every resolved security key this reads the LIVE function's `/thesis` body (the base) and this checkout's own handler on the same pool (the candidate) and compares ONLY the
`segment_table` block (the checkout carries other merged rounds the live function has not deployed, so nothing else is compared). Read-only: GET Lambda invokes and S3 reads; writes nothing but <out.json>.
Per name it classes the difference:
  EQUAL       the two `segment_table` blocks are equal;
  LABEL_NOTE  the blocks differ ONLY in a period `label` (an unresolved column that carries a figure) and/or in `period_note` / a period `note` sentence (the three reworded constants);
  OTHER       any other key differs (a rows value, a currency, the units, a status) -- must be ZERO for the redeploy to be a label change and nothing else;
  ERROR       either side did not answer 200.
Prints `names N | EQUAL a | LABEL_NOTE b | OTHER c | ERROR d | columns relabelled r (names with one: s)` and each OTHER and ERROR name. It grades nothing; the issuer reads the lines.
Controls: a name whose columns are all tied or empty must read EQUAL; a name with an untied figure-bearing column (RIO LN) must read LABEL_NOTE with `Period 5` -> `Year not stated (column 5)`.
"""
import concurrent.futures
import contextlib
import io
import json
import os
import sys

import boto3

os.environ.setdefault("AMGT_AIFILL_ROOT", "/var/empty/aifill-hold")
sys.path.insert(0, ".")
from lib.research.api import scoped_amgt as m  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_LAM = boto3.client("lambda", region_name="us-east-1")


def event(key):
    return {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key):
    r = json.loads(_LAM.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event(key)).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def local(key):
    with contextlib.redirect_stdout(io.StringIO()):
        r = m.handler(event(key))
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def classify(base, cand):
    """Return (class, relabelled columns [(period, old, new)]) for two segment_table blocks."""
    if base == cand:
        return "EQUAL", []
    if not isinstance(base, dict) or not isinstance(cand, dict):
        return "OTHER", []
    other = [k for k in set(base) | set(cand) if k not in ("periods", "period_note") and base.get(k) != cand.get(k)]
    if other:
        return "OTHER", []
    relabelled, ok = [], True
    bp, cp = base.get("periods") or [], cand.get("periods") or []
    if len(bp) != len(cp):
        return "OTHER", []
    for b, c in zip(bp, cp):
        extra = [k for k in set(b) | set(c) if k not in ("label", "note") and b.get(k) != c.get(k)]
        if extra:
            ok = False
        if b.get("label") != c.get("label"):
            relabelled.append((b.get("period"), b.get("label"), c.get("label")))
    return ("LABEL_NOTE" if ok else "OTHER"), relabelled


def one(key):
    try:
        bs, bb = live(key)
        cs, cb = local(key)
    except Exception as exc:  # noqa: BLE001 - a failed read is a counted ERROR, never silently dropped
        return {"key": key, "class": "ERROR", "detail": repr(exc)[:200]}
    if bs != 200 or cs != 200:
        return {"key": key, "class": "ERROR", "detail": "live %s local %s" % (bs, cs)}
    cls, rel = classify(bb.get("segment_table"), cb.get("segment_table"))
    return {"key": key, "class": cls, "relabelled": rel}


def main():
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    if "--limit" in sys.argv:
        keys = keys[: int(sys.argv[sys.argv.index("--limit") + 1])]
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for r in pool.map(one, keys):
            res.append(r)
    json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), default=str)
    count = {c: sum(1 for r in res if r["class"] == c) for c in ("EQUAL", "LABEL_NOTE", "OTHER", "ERROR")}
    cols = sum(len(r.get("relabelled", [])) for r in res)
    names_with = sum(1 for r in res if r.get("relabelled"))
    print("names %d | EQUAL %d | LABEL_NOTE %d | OTHER %d | ERROR %d | columns relabelled %d (names with one: %d)" % (
        len(res), count["EQUAL"], count["LABEL_NOTE"], count["OTHER"], count["ERROR"], cols, names_with))
    for r in res:
        if r["class"] in ("OTHER", "ERROR"):
            print("  %-6s %-24s %s" % (r["class"], r["key"], r.get("detail", "")))
    for r in res:
        if r.get("relabelled"):
            print("  RELABEL %-24s %s" % (r["key"], r["relabelled"]))


if __name__ == "__main__":
    main()
