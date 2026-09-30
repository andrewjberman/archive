"""HVST-n-6 shared instruments: an S3 metering proxy, a phase timer, and the fresh-process runner
that times one /timeline/day path (OLD or NEW) cold (rep 1) and warm (reps 2..N).

READ-ONLY: S3 LIST/GET and read-only Lambda Invoke. No PUT, no env change, no vendor call.
"""
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", "..", ".."))
FUNCTION = "opal-amgt-scoped-api"

# the three days the order names (AC1) plus ONE extra 992_HK day that really has articles
# (the named 992_HK 2026-09-23 has none in the newest mention snapshot -- surprise row W60-S1)
NAMED_DAYS = [
    ("992_HK_Equity", "2026-09-23"),
    ("AMZN_US_Equity", "2026-09-07"),
    ("HD_US_Equity", "2026-08-18"),
]
EXTRA_DAYS = [("992_HK_Equity", "2026-08-13")]
ALL_DAYS = NAMED_DAYS + EXTRA_DAYS


class Meter:
    """Counts S3 list pages / get calls / bytes / seconds, by phase. Thread-safe."""

    def __init__(self):
        self.lock = threading.Lock()
        self.phase = "other"
        self.data = {}
        self.decode_s = 0.0
        self.client = None

    def _slot(self):
        return self.data.setdefault(self.phase, {"list_ops": 0, "list_pages": 0, "list_s": 0.0,
                                                 "gets": 0, "get_bytes": 0, "get_s": 0.0})

    def reset(self):
        with self.lock:
            self.data = {}
            self.decode_s = 0.0

    def totals(self):
        t = {"list_ops": 0, "list_pages": 0, "list_s": 0.0, "gets": 0, "get_bytes": 0, "get_s": 0.0}
        for v in self.data.values():
            for k in t:
                t[k] += v[k]
        t["decode_s"] = self.decode_s
        return t


METER = Meter()


class _Body:
    def __init__(self, raw):
        self._b = raw

    def read(self):
        return self._b


class _Pager:
    def __init__(self, inner):
        self._inner = inner

    def paginate(self, **kw):
        with METER.lock:
            METER._slot()["list_ops"] += 1
        it = iter(self._inner.paginate(**kw))
        while True:
            t = time.perf_counter()
            try:
                page = next(it)
            except StopIteration:
                dt = time.perf_counter() - t
                with METER.lock:
                    METER._slot()["list_s"] += dt
                return
            dt = time.perf_counter() - t
            with METER.lock:
                s = METER._slot()
                s["list_pages"] += 1
                s["list_s"] += dt
            yield page


class MeteredClient:
    """A read-only proxy: only get_paginator (list_objects_v2) and get_object are exposed."""

    def __init__(self, inner):
        self._inner = inner

    def get_paginator(self, name):
        if name != "list_objects_v2":
            raise RuntimeError("n6 meter: only list_objects_v2 is allowed, got %r" % name)
        return _Pager(self._inner.get_paginator(name))

    def get_object(self, **kw):
        t = time.perf_counter()
        resp = self._inner.get_object(**kw)
        raw = resp["Body"].read()
        dt = time.perf_counter() - t
        with METER.lock:
            s = METER._slot()
            s["gets"] += 1
            s["get_bytes"] += len(raw)
            s["get_s"] += dt
        out = dict(resp)
        out["Body"] = _Body(raw)
        return out


def install_meter():
    """Route store._default_client() through the metering proxy; time pq.read_table (decode).
    The boto client is built lazily on the first call so a COLD rep pays for it."""
    import boto3
    import pyarrow.parquet as pq
    from lib.research.harvest import store

    def _client():
        if METER.client is None:
            METER.client = MeteredClient(boto3.client("s3", region_name="us-east-1"))
        return METER.client

    store._default_client = _client
    real = pq.read_table

    def timed(*a, **k):
        t = time.perf_counter()
        try:
            return real(*a, **k)
        finally:
            dt = time.perf_counter() - t
            with METER.lock:
                METER.decode_s += dt

    pq.read_table = timed
    return _client


def phase_wrap(module, name, label_fn):
    """Wrap module.<name> so its wall time is booked under a phase label."""
    inner = getattr(module, name)
    book = PHASE_WALL

    def wrapped(*a, **k):
        label = label_fn(*a, **k)
        prev = METER.phase
        METER.phase = label
        t = time.perf_counter()
        try:
            return inner(*a, **k)
        finally:
            book[label] = book.get(label, 0.0) + (time.perf_counter() - t)
            METER.phase = prev

    setattr(module, name, wrapped)


PHASE_WALL = {}


def body_text(body, serialise):
    return serialise(body)


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def run_worker(path_name, key, day, reps):
    """Runs INSIDE a fresh interpreter (one per path/day) so rep 1 is genuinely cold.
    key == "SEQ": `day` is `key:day,key:day,...`, each visited ONCE in the same process (reps ignored),
    i.e. the first hit on a not-yet-seen day in a WARM process."""
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    install_meter()
    from lib.research.api import scoped_amgt
    from lib.research.harvest import timeline_api

    if path_name == "old":
        sys.path.insert(0, HERE)
        import n6_old_path as mod
        phase_wrap(mod, "_timeline_snapshot_rows", lambda table: "gold:" + table)
        phase_wrap(mod, "_timeline_silver_articles", lambda keys: "silver")

        def call():
            return timeline_api.get_timeline_day(key, day, mod._timeline_daily_loader, mod._timeline_article_loader)
    else:
        mod = scoped_amgt
        phase_wrap(mod, "_timeline_snapshot_rows", lambda table: "gold:" + table)
        phase_wrap(mod, "_timeline_silver_articles", lambda keys: "silver")

        def call():
            return timeline_api.get_timeline_day(key, day, mod._timeline_daily_loader, mod._timeline_article_loader)

    if key == "SEQ":
        plan = [tuple(p.split(":", 1)) for p in day.split(",")]
    else:
        plan = [(key, day)] * reps
    out = []
    for rep, (key, day) in enumerate(plan, 1):
        METER.reset()
        PHASE_WALL.clear()
        t0 = time.perf_counter()
        body = call()
        total = time.perf_counter() - t0
        text = scoped_amgt._timeline_response(body)["body"]
        tot = METER.totals()
        rec = {
            "rep": rep, "cold": rep == 1, "key": key, "day": day, "total_s": round(total, 4),
            "phase_wall_s": {k: round(v, 4) for k, v in sorted(PHASE_WALL.items())},
            "phase_s3": {k: {"list_ops": v["list_ops"], "list_pages": v["list_pages"], "gets": v["gets"],
                             "get_bytes": v["get_bytes"], "list_s": round(v["list_s"], 4), "get_s": round(v["get_s"], 4)}
                         for k, v in sorted(METER.data.items())},
            "list_ops": tot["list_ops"], "list_pages": tot["list_pages"], "gets": tot["gets"],
            "get_bytes": tot["get_bytes"], "list_s": round(tot["list_s"], 4), "get_s_sum": round(tot["get_s"], 4),
            "decode_s_sum": round(tot["decode_s"], 4),
            "articles": len(body.get("articles") or []), "error": bool(body.get("error")),
            "body_sha256": sha256_text(text), "body_len": len(text),
        }
        out.append(rec)
    return out, text


def spawn(path_name, key, day, reps):
    """Fresh-process run of one path/day; returns (list of rep records, body text)."""
    p = subprocess.run(
        [sys.executable, os.path.join(HERE, "n6_worker.py"), path_name, key, day, str(reps)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=600,
    )
    if p.returncode != 0:
        raise RuntimeError("worker %s %s %s rc=%s\n%s" % (path_name, key, day, p.returncode, p.stderr[-2000:]))
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("N6JSON ")][-1]
    obj = json.loads(line[len("N6JSON "):])
    return obj["reps"], obj["body"]


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0


def invoke_deployed(key, day):
    """One read-only Invoke of the deployed route; returns (wall_s, report dict, status, body text)."""
    import boto3

    lam = boto3.client("lambda", region_name="us-east-1")
    path = "/api/scoped/amgt/security/%s/timeline/day/%s" % (key, day)
    ev = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
          "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    t = time.perf_counter()
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev).encode(), LogType="Tail")
    payload = json.loads(r["Payload"].read())
    wall = time.perf_counter() - t
    log = base64.b64decode(r["LogResult"]).decode("utf-8", "replace")
    rep = {}
    m = re.search(r"Duration: ([\d.]+) ms", log)
    if m:
        rep["duration_ms"] = float(m.group(1))
    m = re.search(r"Init Duration: ([\d.]+) ms", log)
    if m:
        rep["init_ms"] = float(m.group(1))
    m = re.search(r"Max Memory Used: (\d+) MB", log)
    if m:
        rep["max_mem_mb"] = int(m.group(1))
    return wall, rep, payload.get("statusCode"), payload.get("body") or ""
