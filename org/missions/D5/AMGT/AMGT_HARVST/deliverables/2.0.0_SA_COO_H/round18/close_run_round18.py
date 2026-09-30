"""AMGT_HARVST round 18 -- the COO's ONE REAL RUN at close, on the DEPLOYED plane (read-only).

Round 18 served one outcome: the alias rule (HVST-g-1) rebuilt into the three served gold tables (HVST-g-2).
This invokes the DEPLOYED scoped API Lambda directly (the gateway's event shape) for:
  ASML_NA_Equity -- whole-brand alias ASML; its coverage days move DENIED -> PARTIAL (row Z-W45-S2)
  DELL_US_Equity -- whole-brand alias Dell, the largest mover (40 added spans)
  BA_US_Equity   -- exact-case ticker BA; its served event is KEPT
  FDX_US_Equity  -- control: +1 mention span but 0 daily cells in the pair
and compares every series day and every event a user now receives to the newest landed chatter_daily /
chatter_event rows read directly. INVOKE + S3 GET only.
"""
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402

FUNCTION = "opal-amgt-scoped-api"
KEYS = ("ASML_NA_Equity", "DELL_US_Equity", "BA_US_Equity", "FDX_US_Equity")
FIELDS = ("mention_score", "articles_total", "tier_a", "tier_b", "tier_c", "tier_d", "mention_count_total",
          "publishers_distinct", "cumulative_ytd", "data_status")

lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FUNCTION)
print("deployed CodeSha256=%s LastModified=%s" % (cfg["CodeSha256"], cfg["LastModified"]))

landed_events = pg._latest_gold_snapshot_rows("chatter_event")
landed_daily = {}
for r in pg._latest_gold_snapshot_rows("chatter_daily"):
    if r["security_key"] in KEYS:
        landed_daily[(r["security_key"], str(r["day"])[:10])] = r

ok = True
for key in KEYS:
    path = "/api/scoped/amgt/security/%s/timeline" % key
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    payload = json.loads(lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))["Payload"].read())
    body = json.loads(payload.get("body") or "{}")
    events = body.get("events") or []
    series = body.get("series") or []
    print("GET %s (deployed) -> HTTP %s, %d events, %d series days" % (path, payload.get("statusCode"), len(events),
                                                                      len(series)))
    if payload.get("statusCode") != 200:
        ok = False
        continue
    served_ev = sorted((str(e["first_day"]), str(e["last_day"]), e.get("lead_headline")) for e in events)
    want_ev = sorted((str(r["first_day"])[:10], str(r["last_day"])[:10], r.get("lead_headline")) for r in landed_events
                     if r["security_key"] == key)
    for s in served_ev:
        print("   event %s..%s  lead=%r" % (s[0], s[1], (s[2] or "").encode("ascii", "replace").decode("ascii")))
    ev_eq = [(a, b) for a, b, _ in served_ev] == [(a, b) for a, b, _ in want_ev]
    print("   events served == newest landed (span): %s" % ev_eq)
    ok = ok and ev_eq
    mism = 0
    compared = 0
    status_counts = {}
    for day in series:
        d = str(day.get("date"))[:10]
        row = landed_daily.get((key, d))
        if row is None:
            continue
        compared += 1
        status_counts[day.get("data_status")] = status_counts.get(day.get("data_status"), 0) + 1
        for f in FIELDS:
            if f in day and f in row:
                a, b = day[f], row[f]
                if isinstance(a, float) or isinstance(b, float):
                    same = a is not None and b is not None and abs(float(a) - float(b)) < 1e-9
                else:
                    same = a == b
                if not same:
                    mism += 1
                    if mism <= 5:
                        print("   MISMATCH %s %s %s served=%r landed=%r" % (key, d, f, a, b))
    print("   series days compared to landed daily: %d; field mismatches: %d; served data_status counts: %s"
          % (compared, mism, status_counts))
    ok = ok and mism == 0 and compared > 0
    if key == "ASML_NA_Equity":
        sample = [s for s in series if "2026-07-15" <= str(s.get("date"))[:10] <= "2026-09-26"][:3]
        for s in sample:
            print("   ASML coverage day %s data_status=%s publishers_covered=%s" % (
                s.get("date"), s.get("data_status"), s.get("publishers_covered")))
print("CLOSE RUN: %s" % ("OK" if ok else "FAIL"))
