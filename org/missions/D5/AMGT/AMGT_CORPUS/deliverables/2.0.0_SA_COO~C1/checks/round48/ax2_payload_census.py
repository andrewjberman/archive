"""AMGT_CORPUS round 48, CRPS-ax-2 -- the Thesis payload census BY KEY (CTO round-47 analysis s.3 item 2). Issuer's file. READ-ONLY.

  PYTHONPATH=. python ax2_payload_census.py <out.json>

For every resolved security, a GET-shaped direct invoke of the live `opal-amgt-scoped-api` (`/api/scoped/amgt/security/<key>/thesis`, firm header `opal`),
and per key the bytes it carries as serialised in that response (`json.dumps` of the value, the separator style that reproduces the whole body's length).
Prints: the function's CodeSha256 and LastModified; the whole response's min / median / max / total bytes; then the top-level keys ranked by total bytes
(min, median, max over the names, share of the summed responses), and the same inside `model`; and, for the three largest keys, the largest names. The
`team_sheet` row reads the served field, so before the /13 redeploy it is the /12 field and after it the /13 field: the census is taken at whichever the
function serves and says so. The output file holds client research content: it stays local; only the printed census is committed.
"""
import concurrent.futures
import json
import statistics
import sys

import boto3

from lib.research.corpus import dossier
from lib.research.harvest import store

FN = "opal-amgt-scoped-api"


def _sep_for(payload, n):
    for sep, ea in (((", ", ": "), True), ((",", ":"), True), ((", ", ": "), False), ((",", ":"), False)):
        if len(json.dumps(payload, separators=sep, ensure_ascii=ea).encode("utf-8")) == n:
            return sep, ea
    return (", ", ": "), True


def _one(lam, key):
    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    body = raw.get("body")
    n = len(body.encode("utf-8")) if isinstance(body, str) else len(json.dumps(body or {}).encode("utf-8"))
    payload = json.loads(body) if isinstance(body, str) else (body or {})
    sep, ea = _sep_for(payload, n)

    def size(v):
        return len(json.dumps(v, separators=sep, ensure_ascii=ea).encode("utf-8"))

    top = {k: size(v) for k, v in payload.items()}
    model = {k: size(v) for k, v in (payload.get("model") or {}).items()} if isinstance(payload.get("model"), dict) else {}
    return key, {"status": raw.get("statusCode"), "bytes": n, "top": top, "model": model}


def _rank(title, per_name, total_bytes, names):
    keys = sorted({k for r in per_name.values() for k in r})
    rows = []
    for k in keys:
        vals = [per_name[n].get(k, 0) for n in names]
        rows.append((sum(vals), k, min(vals), int(statistics.median(vals)), max(vals), max(names, key=lambda n: per_name[n].get(k, 0))))
    rows.sort(reverse=True)
    print("%s (key, total bytes, share of all responses, min / median / max, largest name)" % title)
    for tot, k, mn, md, mx, big in rows[:25]:
        print("  %-34s %10d %5.1f%%  %8d / %8d / %8d  %s" % (k, tot, 100.0 * tot / max(total_bytes, 1), mn, md, mx, big))
    return rows


def main(argv):
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("function %s LastModified %s CodeSha256 %s" % (FN, cfg.get("LastModified"), cfg.get("CodeSha256")))
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    got, failed = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for fut in concurrent.futures.as_completed([pool.submit(_one, lam, k) for k in keys]):
            try:
                k, rec = fut.result()
                got[k] = rec
            except Exception as exc:  # a failed invoke is counted and named, never dropped
                failed.append(str(exc)[:120])
    ok = sorted(k for k, r in got.items() if r["status"] == 200)
    print("census names %d ok %d failed %d" % (len(keys), len(ok), len(failed) + (len(got) - len(ok))))
    if not ok:
        return 1
    sizes = sorted(got[k]["bytes"] for k in ok)
    total = sum(sizes)
    print("response bytes min %d median %d max %d total %d over_1MB %d over_6MB %d" % (
        sizes[0], sizes[len(sizes) // 2], sizes[-1], total, sum(1 for x in sizes if x > 1048576), sum(1 for x in sizes if x > 6291456)))
    _rank("TOP-LEVEL KEYS", {k: got[k]["top"] for k in ok}, total, ok)
    _rank("INSIDE `model`", {k: got[k]["model"] for k in ok}, total, ok)
    if argv:
        json.dump({"function": {"LastModified": cfg.get("LastModified"), "CodeSha256": cfg.get("CodeSha256")}, "keys": got},
                  open(argv[0], "w", encoding="utf-8"), sort_keys=True, ensure_ascii=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
