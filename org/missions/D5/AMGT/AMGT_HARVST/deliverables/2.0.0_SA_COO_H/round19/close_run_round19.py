"""AMGT_HARVST round 19 -- the COO's ONE REAL RUN at close, on the DEPLOYED plane (read-only).

Round 19 served one outcome: a PARTIAL day names its publisher (HVST-i-2 rule, HVST-i-3 served daily part, HVST-i-4
deploy). This invokes the DEPLOYED scoped API Lambda directly (the gateway's event shape) for:
  ASML_NA_Equity -- 74 PARTIAL days naming sa
  992_HK_Equity  -- the one PARTIAL day naming wsj, plus its served events (a kept control)
  BA_US_Equity   -- all DENIED, one served event (a kept control)
  FDX_US_Equity  -- all DENIED, no event
and compares EVERY series field a user receives -- the ones served before this round and the two new ones -- with the
newest LANDED chatter_daily row, day by day, and every event with the newest landed chatter_event rows. It also reads
the timeline_day body for one PARTIAL day of each PARTIAL security. INVOKE + S3 GET only.
"""
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import timeline_api as ta  # noqa: E402

FUNCTION = "opal-amgt-scoped-api"
KEYS = ("ASML_NA_Equity", "992_HK_Equity", "BA_US_Equity", "FDX_US_Equity")
STORED = tuple(f for f in ta.SERIES_STORED_FIELDS if f != "date")

lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FUNCTION)
print("deployed CodeSha256=%s LastModified=%s" % (cfg["CodeSha256"], cfg["LastModified"]))
print("series stored fields compared (%d): %s" % (len(STORED), ", ".join(STORED)))


def invoke(path):
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    payload = json.loads(lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))["Payload"].read())
    return payload.get("statusCode"), json.loads(payload.get("body") or "{}")


def same(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return a is not None and b is not None and abs(float(a) - float(b)) < 1e-9
    if isinstance(b, (list, tuple)) or hasattr(b, "tolist"):
        b = list(b.tolist() if hasattr(b, "tolist") else b)
    return a == b


landed_events = pg._latest_gold_snapshot_rows("chatter_event")
landed_daily = {}
for r in pg._latest_gold_snapshot_rows("chatter_daily"):
    if r["security_key"] in KEYS:
        landed_daily[(r["security_key"], str(r["day"])[:10])] = r

ok = True
for key in KEYS:
    status, body = invoke("/api/scoped/amgt/security/%s/timeline" % key)
    series = body.get("series") or []
    events = body.get("events") or []
    print("GET /timeline %s -> HTTP %s, %d series days, %d events" % (key, status, len(series), len(events)))
    if status != 200:
        ok = False
        continue
    compared = mism = 0
    partial = []
    for day in series:
        d = str(day.get("date"))[:10]
        row = landed_daily.get((key, d))
        if row is None:
            continue
        compared += 1
        if day.get("data_status") == "PARTIAL":
            partial.append((d, day.get("publishers_covered_codes")))
        for f in STORED:
            if f not in day or f not in row or not same(day[f], row[f]):
                mism += 1
                if mism <= 5:
                    print("   MISMATCH %s %s %s served=%r landed=%r" % (key, d, f, day.get(f), row.get(f)))
    print("   series days compared %d of %d landed; field mismatches %d (over %d fields each)"
          % (compared, sum(1 for k in landed_daily if k[0] == key), mism, len(STORED)))
    codes = sorted({tuple(c or []) for _, c in partial})
    print("   PARTIAL days %d, distinct code lists %s" % (len(partial), codes))
    served_ev = sorted((str(e["first_day"]), str(e["last_day"])) for e in events)
    want_ev = sorted((str(r["first_day"])[:10], str(r["last_day"])[:10]) for r in landed_events
                     if r["security_key"] == key)
    print("   events served == newest landed (span): %s (%d)" % (served_ev == want_ev, len(served_ev)))
    ok = ok and compared > 0 and mism == 0 and served_ev == want_ev
    if partial:
        d0 = partial[0][0]
        s2, b2 = invoke("/api/scoped/amgt/security/%s/timeline/day/%s" % (key, d0))
        print("   GET /timeline/day/%s -> HTTP %s, data_status=%s publishers_covered=%s codes=%s"
              % (d0, s2, b2.get("data_status"), b2.get("publishers_covered"), b2.get("publishers_covered_codes")))
        ok = ok and s2 == 200 and b2.get("publishers_covered_codes") == list(partial[0][1] or [])
print("CLOSE RUN: %s" % ("OK" if ok else "FAIL"))
