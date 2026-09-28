"""HVST-z-0 AC2: a FAILED LOAD is unreachable to the empty-array encoding, at the ROUTE layer.

Loader failures are injected by replacing the production loader seams on `scoped_amgt` (the
module-level names the handler resolves at call time), then calling `scoped_amgt.handler`
in-process. 3 injections x 2 routes = 6 failure cases, then the honest-empty CONTROLS.
NO S3 access at all: every loader here is an injected fake. NO NETWORK.
"""
import datetime
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.api import scoped_amgt  # noqa: E402
from lib.research.harvest import timeline_api  # noqa: E402

KEY = "992_HK_Equity"
DATA_KEYS = ("series", "events", "articles")
ORIG = {n: getattr(scoped_amgt, n) for n in
        ("_timeline_daily_loader", "_timeline_event_loader", "_timeline_article_loader", "_timeline_snapshot_rows")}
failures = []


def reset():
    for n, f in ORIG.items():
        setattr(scoped_amgt, n, f)


def call(path, query=None):
    event = {"rawPath": path, "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": query}
    resp = scoped_amgt.handler(event)
    return resp["statusCode"], json.loads(resp["body"]), resp["body"]


def caller_predicate(status, body):
    """THE PREDICATE a caller uses: a failed call is `status != 200 and body.error is True`; the
    body-only form (`timeline_api.is_error_body`) is `body.get("error") is True`. Data is read
    ONLY when this returns False."""
    return status != 200 and body.get("error") is True


def boom(*_a, **_k):
    raise RuntimeError("injected loader failure")


def timed_out(*_a, **_k):
    raise timeline_api.UpstreamTimeout("injected loader timeout")


def malformed_daily(_key):
    return [{"security_key": KEY, "mention_score": 1.0}]  # no `day`


RANGE = "/api/scoped/amgt/security/%s/timeline" % KEY
DAY = "/api/scoped/amgt/security/%s/timeline/day/2026-05-22" % KEY
EMPTY_DAY_ROW = [{"security_key": KEY, "day": datetime.date(2026, 5, 22), "articles_total": 0,
                  "mention_score": 0.0, "data_status": "COMPLETE"}]

cases = [
    ("range/raise", RANGE, {"_timeline_daily_loader": boom}),
    ("range/timeout", RANGE, {"_timeline_daily_loader": timed_out}),
    ("range/malformed", RANGE, {"_timeline_daily_loader": malformed_daily}),
    ("day/raise", DAY, {"_timeline_daily_loader": boom}),
    ("day/timeout", DAY, {"_timeline_daily_loader": timed_out}),
    ("day/malformed", DAY, {"_timeline_daily_loader": malformed_daily}),
]

print("FAILURE CASES (each must be HTTP != 200, error:true, non-empty error_code, no series/events/articles key)")
ok_count = 0
for name, path, patches in cases:
    reset()
    for n, f in patches.items():
        setattr(scoped_amgt, n, f)
    status, body, raw = call(path)
    ok = (status != 200 and body.get("error") is True and bool(body.get("error_code"))
          and not any(k in body for k in DATA_KEYS) and caller_predicate(status, body))
    ok_count += ok
    print("%s %-16s HTTP %d error_code=%s data_keys_present=%s\n     body=%s"
          % ("PASS:" if ok else "FAIL:", name, status, body.get("error_code"),
             [k for k in DATA_KEYS if k in body], raw))
    if not ok:
        failures.append(name)
print("failure cases held: %d of %d" % (ok_count, len(cases)))

print("\nBONUS (not one of the 6): a timeout-class exception from the S3 read itself, through the real loader")
reset()


class ReadTimeoutError(Exception):
    pass


def s3_timeout(_table):
    raise ReadTimeoutError("injected S3 read timeout")


import lib.research.harvest.publication_gold as pg  # noqa: E402
_orig_reader = pg._latest_gold_snapshot_rows
pg._latest_gold_snapshot_rows = s3_timeout
try:
    status, body, raw = call(RANGE)
finally:
    pg._latest_gold_snapshot_rows = _orig_reader
print("     HTTP %d body=%s" % (status, raw))
if not (status == 504 and body.get("error_code") == "TIMELINE_TIMEOUT" and not any(k in body for k in DATA_KEYS)):
    failures.append("bonus/s3-timeout")

print("\nCONTRAST: honest empty -- a SUCCESSFUL call with nothing in range (must be HTTP 200, empty array, NO error key)")
reset()
scoped_amgt._timeline_daily_loader = lambda k: []
scoped_amgt._timeline_event_loader = lambda k: []
status, body, raw = call(RANGE, {"from": "2026-03-01", "to": "2026-03-05"})
ok = status == 200 and "error" not in body and body.get("series") == [] and body.get("events") == [] and not caller_predicate(status, body)
print("%s range/honest-empty HTTP %d\n     body=%s" % ("PASS:" if ok else "FAIL:", status, raw))
if not ok:
    failures.append("control/range")

scoped_amgt._timeline_daily_loader = lambda k: list(EMPTY_DAY_ROW)
scoped_amgt._timeline_article_loader = lambda k, d: []
status, body, raw = call(DAY)
ok = status == 200 and "error" not in body and body.get("articles") == [] and not caller_predicate(status, body)
print("%s day/honest-empty (COMPLETE day, 0 articles) HTTP %d\n     body=%s" % ("PASS:" if ok else "FAIL:", status, raw))
if not ok:
    failures.append("control/day")
reset()

print("\nPREDICATE a caller uses to tell them apart:")
print("    failed = (http_status != 200) and (body.get('error') is True)   # == timeline_api.is_error_body(body) on the body")
print("    a failed body carries error:true + error_code and NEVER series/events/articles;")
print("    an honest-empty body is HTTP 200, carries an empty series/events/articles array, and NEVER an `error` key.")

n_ok = ok_count
print("\nRESULT: %s -- %d of %d failure cases + honest-empty controls (%d failing)"
      % ("PASS" if not failures and n_ok == 6 else "FAIL", n_ok, len(cases), len(failures)))
sys.exit(1 if failures or n_ok != 6 else 0)
