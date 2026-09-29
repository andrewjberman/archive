"""AMGT_HARVST round 15 -- the COO's ONE REAL RUN at close, on the DEPLOYED plane (read-only).

Round 15 served one outcome: the common-name aliases (HVST-d-1) rebuilt into the three served gold tables
(HVST-d-2). This invokes the DEPLOYED Lambda directly (the gateway's event shape) for AMZN_US_Equity -- the
security the alias change moved, and whose first event is new -- plus BA_US_Equity and 992_HK_Equity as kept
controls, and compares what a user now receives to the newest landed chatter_event rows read directly. For
AMZN it also prints every daily figure the response carries for 2026-09-07 beside the landed chatter_daily row.
INVOKE + S3 GET only.
"""
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402

FUNCTION = "opal-amgt-scoped-api"
lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FUNCTION)
print("deployed CodeSha256=%s LastModified=%s" % (cfg["CodeSha256"], cfg["LastModified"]))

landed = pg._latest_gold_snapshot_rows("chatter_event")
daily = {(r["security_key"], str(r["day"])): r for r in pg._latest_gold_snapshot_rows("chatter_daily")
         if r["security_key"] == "AMZN_US_Equity"}
ok = True
for key in ("AMZN_US_Equity", "BA_US_Equity", "992_HK_Equity"):
    path = "/api/scoped/amgt/security/%s/timeline" % key
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    payload = json.loads(lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))["Payload"].read())
    body = json.loads(payload.get("body") or "{}")
    events = body.get("events") or []
    print("GET %s (deployed) -> HTTP %s, %d events, response keys %s" % (
        path, payload.get("statusCode"), len(events), sorted(body)))
    served = sorted((str(e["first_day"]), str(e["last_day"]), e.get("lead_headline")) for e in events)
    want = sorted((str(r["first_day"]), str(r["last_day"]), r.get("lead_headline")) for r in landed
                  if r["security_key"] == key)
    for s in served:
        print("   %s..%s  lead=%r" % (s[0], s[1], (s[2] or "").encode("ascii", "replace").decode("ascii")))
    match = served == want
    print("   served == newest landed rows (span AND lead): %s" % match)
    ok = ok and payload.get("statusCode") == 200 and match and len(events) > 0
    if key == "AMZN_US_Equity":
        for e in events:
            print("   AMZN event fields: %s" % {k: e[k] for k in sorted(e) if k not in ("lead_headline",)})
        for name in sorted(body):
            val = body[name]
            if isinstance(val, list) and val and isinstance(val[0], dict) and ("day" in val[0] or "date" in val[0]):
                hit = [d for d in val if str(d.get("day") or d.get("date")) == "2026-09-07"]
                print("   response series %r: %d days; 2026-09-07 -> %s" % (name, len(val), hit[:1]))
        row = daily.get(("AMZN_US_Equity", "2026-09-07"))
        print("   landed chatter_daily AMZN 2026-09-07: articles_total=%s tier_a=%s tier_b=%s mention_count_total=%s" % (
            row and row["articles_total"], row and row["tier_a"], row and row["tier_b"], row and row["mention_count_total"]))

print("CLOSE RUN: %s" % ("OK" if ok else "NOT OK"))
sys.exit(0 if ok else 1)
