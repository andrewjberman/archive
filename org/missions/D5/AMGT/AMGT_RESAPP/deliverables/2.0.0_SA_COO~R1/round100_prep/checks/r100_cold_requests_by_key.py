"""AMGT_RESAPP round-100 PREP -- WHAT the ~250 S3 requests of the first overlay request are: operation, key family, count and wall time.

  PYTHONPATH=<repo root> python r100_cold_requests_by_key.py --subject ASML_NA_Equity [--route overlay]

Round 100's second apply (one S3 client per container) left the cold first overlay at 22-28 s on Lambda although it removed 140 client builds and the pool warnings: the time is in the
requests themselves. This runs ONE fresh in-process request (cold: every in-memory cache empty) against the live pool with every S3 request of every client recorded by operation, bucket and
KEY FAMILY (the key with its date, stamp and security-key segments replaced by `*`), and prints, per family, the count, the summed request wall time (requests overlap across threads, so the
sum is thread-seconds, not elapsed) and the first lib frame that asked. Read-only: GET-shaped handler call; writes nothing. Prints the elapsed time, the totals and one line per family sorted by
summed time, then ONE JSON line.
"""
import json
import re
import sys
import threading
import time
import traceback

import boto3

LOCK = threading.Lock()
ROWS = []
SPANS = []
_real = boto3.client
STARTS = {}


def _family(key):
    parts = key.split("/")
    out = []
    for p in parts:
        if re.fullmatch(r"\d{8}T\d{6}Z", p) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", p) or re.fullmatch(r"[A-Za-z0-9]+_[A-Z]{2}_Equity", p) or re.fullmatch(r"[0-9a-f]{8,}", p):
            out.append("*")
        elif "=" in p and re.search(r"=\d", p):
            out.append(p.split("=")[0] + "=*")
        else:
            out.append(p)
    return "/".join(out[:7])


def _caller():
    for fr in reversed(traceback.extract_stack()[:-2]):
        fn = fr.filename.replace("\\", "/")
        if "/lib/" in fn and "r100_cold_requests_by_key" not in fn:
            return "%s:%s" % (fn.split("/lib/")[-1], fr.name)
    return "other"


def _wrapped(service, *a, **kw):
    c = _real(service, *a, **kw)
    if service == "s3":
        def before(model=None, params=None, context=None, **_k):
            who = _caller()  # the lib frame that ISSUED the request (the innermost one), not the one that built the client
            with LOCK:
                STARTS[id(context)] = (time.monotonic(), model.name if model else "?", (params or {}).get("Bucket", ""), (params or {}).get("Key") or (params or {}).get("Prefix") or "", who)

        def after(context=None, **_k):
            with LOCK:
                s = STARTS.pop(id(context), None)
            if s:
                t0, op, bucket, key, w = s
                with LOCK:
                    ROWS.append((op, bucket, _family(key), time.monotonic() - t0, w))
                    SPANS.append((t0, time.monotonic()))

        c.meta.events.register("before-parameter-build.s3", before)
        c.meta.events.register("after-call.s3", after)
    return c


def main(argv):
    def opt(n, d):
        return argv[argv.index(n) + 1] if n in argv else d

    subject, route = opt("--subject", "ASML_NA_Equity"), opt("--route", "overlay")
    boto3.client = _wrapped
    from lib.research.api import scoped_amgt
    ev = {"rawPath": "/api/scoped/amgt/security/%s/%s" % (subject, route), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
          "headers": {"x-firm-id": "opal"}}
    t0 = time.monotonic()
    r = scoped_amgt.handler(ev)
    el = time.monotonic() - t0
    fam = {}
    for op, bucket, family, d, who in ROWS:
        k = (op, bucket, family)
        n, tot, w = fam.get(k, (0, 0.0, {}))
        w[who] = w.get(who, 0) + 1
        fam[k] = (n + 1, tot + d, w)
    print("%s %s: status %s elapsed %.2f s | %d S3 requests, summed request time %.1f thread-seconds" % (route, subject, r.get("statusCode"), el, len(ROWS), sum(x[3] for x in ROWS)))
    union, cur_s, cur_e, peak = 0.0, None, None, 0
    for a, b in sorted(SPANS):
        if cur_e is None or a > cur_e:
            union += (cur_e - cur_s) if cur_e is not None else 0.0
            cur_s, cur_e = a, b
        else:
            cur_e = max(cur_e, b)
    union += (cur_e - cur_s) if cur_e is not None else 0.0
    events = sorted([(a, 1) for a, _ in SPANS] + [(b, -1) for _, b in SPANS])
    now = 0
    for _t, d in events:
        now += d
        peak = max(peak, now)
    print("wall time with at least one S3 request in flight: %.2f s of %.2f s elapsed (%.0f percent); peak simultaneous requests %d" % (union, el, 100 * union / el, peak))
    out = []
    for (op, bucket, family), (n, tot, w) in sorted(fam.items(), key=lambda kv: -kv[1][1])[:25]:
        top = sorted(w.items(), key=lambda kv: -kv[1])[0][0]
        print("  %-14s %-26s %-60s n=%3d sum=%6.2f s avg=%5.0f ms  by %s" % (op, bucket[:26], family[:60], n, tot, 1000 * tot / n, top))
        out.append({"op": op, "bucket": bucket, "family": family, "n": n, "sum_s": round(tot, 2), "caller": top})
    print(json.dumps({"subject": subject, "route": route, "elapsed_s": round(el, 2), "requests": len(ROWS), "families": out}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
