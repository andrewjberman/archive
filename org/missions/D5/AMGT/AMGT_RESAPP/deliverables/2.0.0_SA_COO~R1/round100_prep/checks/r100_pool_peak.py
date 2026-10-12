"""AMGT_RESAPP round-100 PREP -- the PEAK number of simultaneous S3 requests ONE boto3 client carries, per route, over the request path of `opal-amgt-scoped-api`.

  PYTHONPATH=<repo root> python r100_pool_peak.py <out.json>

Why: the function's log carries 'Connection pool is full, discarding connection: opal-data-harvest.s3.amazonaws.com' on 49 of its 53 invocations over 20 s. botocore's HTTP pool is
PER CLIENT (`max_pool_connections`, default 10), so the number that matters is the peak of simultaneous in-flight requests on ONE client, not the process total.
How: `boto3.client` is wrapped for this process; every S3 client made while the handler serves gets `before-send` / `response-received` hooks that count that client's in-flight
requests; a request that raises is counted out by `after-call-error`. Routes are served in-process by the checkout's own `scoped_amgt.handler` on the live pool (GET only, read-only):
the overlay and peers of a set of subjects, the thesis, the timeline, the four ranked lists with their timeseries, and the collected chatter at three windows. Prints, per route
request, the clients created, the maximum in-flight on any one client, the process-wide maximum and the pool size the client was built with (`config.max_pool_connections`), and
`R100 POOL PEAK` with the overall per-client maximum and the number of reads in which ANY client carried more simultaneous requests than its own pool (exit 1 if any). Read-only; writes only <out.json>.
"""
import json
import sys
import threading

import boto3

from lib.research.api import scoped_amgt

PREFIX = "/api/scoped/amgt"
SUBJECTS = ("ASML_NA_Equity", "SAN_FP_Equity", "SAP_GY_Equity", "BA_US_Equity", "AZN_LN_Equity", "ROG_SW_Equity", "TSM_US_Equity")
LOCK = threading.Lock()
STATE = {"clients": []}


class _Meter:
    def __init__(self, pool):
        self.pool = pool
        self.now = 0
        self.peak = 0
        self.calls = 0

    def up(self, **_kw):
        with LOCK:
            self.now += 1
            self.calls += 1
            self.peak = max(self.peak, self.now)

    def down(self, **_kw):
        with LOCK:
            self.now = max(0, self.now - 1)


_real_client = boto3.client


def _wrapped(service, *a, **kw):
    c = _real_client(service, *a, **kw)
    if service == "s3":
        cfg = getattr(c.meta, "config", None)
        meter = _Meter(getattr(cfg, "max_pool_connections", None))
        c.meta.events.register("before-send.s3", meter.up)
        c.meta.events.register("response-received.s3", meter.down)
        c.meta.events.register("after-call-error.s3", meter.down)
        with LOCK:
            STATE["clients"].append(meter)
    return c


def event(path, query=None):
    return {"rawPath": PREFIX + path, "queryStringParameters": query, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def serve(path, query=None):
    r = scoped_amgt.handler(event(path, query))
    return r.get("statusCode")


def main(argv):
    boto3.client = _wrapped
    reads = []
    for s in SUBJECTS:
        for route in ("overlay", "peers", "thesis", "timeline"):
            reads.append(("%s %s" % (route, s), "/security/%s/%s" % (s, route), None))
    for mv in scoped_amgt.MOVEMENTS:
        for sj in scoped_amgt.SUBJECTS:
            reads.append(("rankings %s/%s" % (mv, sj), "/lead-panel/rankings/%s/%s" % (mv, sj), None))
    for days in ("30", "90", "365"):
        reads.append(("collected chatter days=%s" % days, "/lead-panel/timeseries/collected/chatter", {"days": days}))
    out, overall = [], 0
    for label, path, query in reads:
        with LOCK:
            STATE["clients"] = []
        status = serve(path, query)
        with LOCK:
            ms = list(STATE["clients"])
        peak = max([m.peak for m in ms] or [0])
        total = sum(m.calls for m in ms)
        pools = sorted({m.pool for m in ms if m.pool is not None})
        over_here = sum(1 for m in ms if m.pool is not None and m.peak > m.pool)
        overall = max(overall, peak)
        out.append({"read": label, "status": status, "clients": len(ms), "requests": total, "peak_one_client": peak, "pool": pools, "clients_over_pool": over_here})
        print("%-44s status %s clients %3d requests %4d peak_on_one_client %3d pool %s" % (label[:44], status, len(ms), total, peak, pools))
    json.dump({"reads": out, "overall_peak_one_client": overall}, open(argv[0], "w"))
    over = [o for o in out if o["clients_over_pool"]]
    print("R100 POOL PEAK: overall per-client maximum %d over %d reads; reads with a client above its own pool: %d" % (overall, len(out), len(over)))
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
