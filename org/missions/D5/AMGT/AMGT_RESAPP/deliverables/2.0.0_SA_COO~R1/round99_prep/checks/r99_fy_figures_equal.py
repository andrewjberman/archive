"""AMGT_RESAPP round-99 PREP -- is the Thesis payload's top-level `fiscal_year_figures` EQUAL to `model.fiscal_year_figures`, name by name?

  PYTHONPATH=<repo root> python r99_fy_figures_equal.py [--where local|live] [--limit N]

CTO round-98 analysis section 2: the portal repoint (every reader of the TOP-LEVEL `fiscal_year_figures` reads `model.fiscal_year_figures` instead) renders byte-equal only where the two
copies are equal in the served payload. This reads the `/thesis` response of every resolved name (`dossier._resolved_security_keys`; `--where local` the checkout's own handler on the live
pool, `--where live` one invoke per name of the live function) and compares, per name, the two keys by canonical JSON (sorted keys, ASCII).
Classes, one per name: EQUAL (both present, equal), BOTH_EMPTY (both absent or both empty lists), DIFFER (both present, unequal), TOP_ONLY (only the top-level key is present and non-empty),
MODEL_ONLY (only the model copy is present and non-empty), NOREAD (the route did not serve 200). Prints one line per DIFFER, TOP_ONLY, MODEL_ONLY and NOREAD name (its path of first
difference), the counts, and `R99 FY FIGURES EQUAL: YES|NO` (YES = every name EQUAL or BOTH_EMPTY, and no NOREAD). Read-only; writes nothing.
"""
import concurrent.futures
import json
import sys

from lib.research.corpus import dossier
from lib.research.harvest import store

FN = "opal-amgt-scoped-api"


def _event(key):
    return {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
            "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}


def _canon(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=True)


def _first_diff(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return "%s.%s (%s)" % (path, k, "only in model" if k in b else "only in top")
            d = _first_diff(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return "%s.<length> %d vs %d" % (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = _first_diff(x, y, "%s[%d]" % (path, i))
            if d:
                return d
        return None
    return None if a == b else "%s %r vs %r" % (path, str(a)[:30], str(b)[:30])


def main(argv):
    where = argv[argv.index("--where") + 1] if "--where" in argv else "local"
    limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else None
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    if limit:
        keys = keys[:limit]
    if where == "live":
        import boto3
        lam = boto3.client("lambda", region_name="us-east-1")

        def read(key):
            r = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(_event(key)).encode())["Payload"].read())
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
    else:
        from lib.research.api import scoped_amgt

        def read(key):
            r = scoped_amgt.handler(_event(key))
            return r.get("statusCode"), json.loads(r.get("body") or "{}")

    def one(key):
        status, body = read(key)
        if status != 200:
            return key, "NOREAD", "status %s" % status
        top = body.get("fiscal_year_figures")
        mod = (body.get("model") or {}).get("fiscal_year_figures")
        t_has, m_has = bool(top), bool(mod)
        if not t_has and not m_has:
            return key, "BOTH_EMPTY", ""
        if t_has and not m_has:
            return key, "TOP_ONLY", "top %d figures, model %s" % (len(top), "absent" if mod is None else "empty")
        if m_has and not t_has:
            return key, "MODEL_ONLY", "model %d figures, top %s" % (len(mod), "absent" if top is None else "empty")
        if _canon(top) == _canon(mod):
            return key, "EQUAL", ""
        return key, "DIFFER", _first_diff(top, mod) or "unequal"

    rows, failed = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for fut in concurrent.futures.as_completed([pool.submit(one, k) for k in keys]):
            try:
                rows.append(fut.result())
            except Exception as exc:  # a failed read is counted and named, never dropped
                failed.append("%s: %s" % (type(exc).__name__, str(exc)[:100]))
    counts = {}
    for _k, cls, _d in rows:
        counts[cls] = counts.get(cls, 0) + 1
    for k, cls, d in sorted(rows):
        if cls not in ("EQUAL", "BOTH_EMPTY"):
            print("%-10s %-22s %s" % (cls, k, d))
    for f in failed[:5]:
        print("FAILED %s" % f)
    print("names %d | read %d | failed %d | %s" % (len(keys), len(rows), len(failed), json.dumps(counts, sort_keys=True)))
    ok = not failed and len(rows) == len(keys) and all(cls in ("EQUAL", "BOTH_EMPTY") for _k, cls, _d in rows)
    print("R99 FY FIGURES EQUAL: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
