"""AMGT_RESAPP round-100 PREP -- ONE cold request, in a FRESH process, against the live pool: what the first request after a quiet period costs, and where.

  PYTHONPATH=<repo root> python r100_cold_request.py --subject ASML_NA_Equity [--route overlay] [--pool N] [--reuse]

The function's slow tail (53 of 32,528 invocations over 20 s in a day, 49 with a 'Connection pool is full' warning) was read in round 99. This measures one fresh in-process request
twice (the first is COLD: every module-level and in-memory cache empty; the second is WARM), with `boto3.client` wrapped so that every S3 client creation and every S3 request is counted
and ATTRIBUTED to the lib frame that built the client (`clients_by_caller`) and to the next distinct lib frame above it (`clients_by_upstream`).
  --pool N   (N > 0) builds every S3 client that the code builds without its own `Config` with `Config(max_pool_connections=N)`; omitted, the code is untouched (botocore's pool of 10).
  --reuse    hands every caller the SAME S3 client (the first built, per service and arguments): a throwaway measuring arm for what a process-level client would cost; no file changes.
Read-only: GET-shaped handler calls on the live pool; writes nothing. Prints ONE line of JSON:
  {"subject", "route", "pool", "reuse", "cold": {"elapsed_s", "status", "clients", "client_creation_s", "requests", "peak_one_client"}, "warm": {same},
   "clients_by_caller": {"<file>:<function>": n}, "clients_by_upstream": {"<file>:<function>": n}, "requests_by_caller": {"<file>:<function>": n}}
Each run is a new process: the caller loops subjects x pools x repeats in the shell.
"""
import json
import sys
import threading
import time
import traceback

import boto3

LOCK = threading.Lock()
S = {"create_s": 0.0, "clients": 0, "reqs": 0, "caller_clients": {}, "caller_reqs": {}, "upstream_clients": {}, "meters": []}
_real = boto3.client
POOL = 0
REUSE = False
_CACHE = {}


def _caller():
    """(the first lib frame, the next distinct lib frame above it) of the call stack that reached `boto3.client`."""
    found = []
    for fr in reversed(traceback.extract_stack()[:-2]):
        fn = fr.filename.replace("\\", "/")
        if "/lib/" not in fn or "r100_cold_request" in fn:
            continue
        name = "%s:%s" % (fn.split("/lib/")[-1], fr.name)
        if not found or name != found[-1]:
            found.append(name)
        if len(found) == 2:
            break
    return (found[0] if found else "other", found[1] if len(found) > 1 else "other")


class _Meter:
    def __init__(self, who):
        self.who, self.now, self.peak = who, 0, 0

    def up(self, **_kw):
        with LOCK:
            self.now += 1
            self.peak = max(self.peak, self.now)
            S["reqs"] += 1
            S["caller_reqs"][self.who] = S["caller_reqs"].get(self.who, 0) + 1

    def down(self, **_kw):
        with LOCK:
            self.now = max(0, self.now - 1)


def _tally(who, up):
    S["caller_clients"][who] = S["caller_clients"].get(who, 0) + 1
    S["upstream_clients"][up] = S["upstream_clients"].get(up, 0) + 1


def _wrapped(service, *a, **kw):
    if POOL and service == "s3" and "config" not in kw:
        from botocore.config import Config
        kw["config"] = Config(max_pool_connections=POOL)
    who, up = _caller()
    ck = (service, a, tuple(sorted((k, ("cfg", getattr(v, "max_pool_connections", None)) if k == "config" else str(v)) for k, v in kw.items())))
    if REUSE and service == "s3":
        with LOCK:
            hit = _CACHE.get(ck)
            if hit is not None:
                _tally(who, up)
                return hit
    t = time.monotonic()
    c = _real(service, *a, **kw)
    d = time.monotonic() - t
    if service == "s3":
        m = _Meter(who)
        c.meta.events.register("before-send.s3", m.up)
        c.meta.events.register("response-received.s3", m.down)
        c.meta.events.register("after-call-error.s3", m.down)
        with LOCK:
            S["create_s"] += d
            S["clients"] += 1
            _tally(who, up)
            S["meters"].append(m)
            if REUSE:
                _CACHE[ck] = c
    return c


def main(argv):
    global POOL, REUSE

    def opt(name, default):
        return argv[argv.index(name) + 1] if name in argv else default

    subject, route, POOL = opt("--subject", "ASML_NA_Equity"), opt("--route", "overlay"), int(opt("--pool", "0"))
    REUSE = "--reuse" in argv
    boto3.client = _wrapped
    from lib.research.api import scoped_amgt
    ev = {"rawPath": "/api/scoped/amgt/security/%s/%s" % (subject, route), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
          "headers": {"x-firm-id": "opal"}}
    out = {"subject": subject, "route": route, "pool": POOL or "default(10)", "reuse": REUSE}
    for label in ("cold", "warm"):
        with LOCK:
            S.update({"create_s": 0.0, "clients": 0, "reqs": 0, "meters": []})
            if label == "cold":
                S["caller_clients"], S["caller_reqs"], S["upstream_clients"] = {}, {}, {}
        t0 = time.monotonic()
        r = scoped_amgt.handler(ev)
        el = time.monotonic() - t0
        with LOCK:
            out[label] = {"elapsed_s": round(el, 2), "status": r.get("statusCode"), "clients": S["clients"], "client_creation_s": round(S["create_s"], 2),
                          "requests": S["reqs"], "peak_one_client": max([m.peak for m in S["meters"]] or [0])}
    out["clients_by_caller"] = dict(sorted(S["caller_clients"].items(), key=lambda kv: -kv[1])[:12])
    out["clients_by_upstream"] = dict(sorted(S["upstream_clients"].items(), key=lambda kv: -kv[1])[:12])
    out["requests_by_caller"] = dict(sorted(S["caller_reqs"].items(), key=lambda kv: -kv[1])[:12])
    print(json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
