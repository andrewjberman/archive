"""AMGT_HARVST round 12 -- the COO's ONE REAL RUN at close, on the DEPLOYED plane (read-only).

Round 12 served two outcomes along one path: the timeline routes now mounted and packaged on the deployed scoped API
(HVST-a-1/a-2), serving the chatter_event part rebuilt with the plurality lead (HVST-a-3/a-4). This invokes the DEPLOYED
Lambda directly (the gateway's event shape) for BA_US_Equity -- the security whose 2026-09-08 lead the rebuild moved --
and compares what a user now receives to the newest landed chatter_event rows read directly. It also re-invokes the
validation security (992_HK_Equity) so the close run covers the round-11 thread. INVOKE + S3 GET only.
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
ok = True
for key in ("BA_US_Equity", "992_HK_Equity"):
    path = "/api/scoped/amgt/security/%s/timeline" % key
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    payload = json.loads(lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))["Payload"].read())
    body = json.loads(payload.get("body") or "{}")
    events = body.get("events") or []
    print("GET %s (deployed) -> HTTP %s, %d events" % (path, payload.get("statusCode"), len(events)))
    served = sorted((str(e["first_day"]), str(e["last_day"]), e.get("lead_headline")) for e in events)
    want = sorted((str(r["first_day"]), str(r["last_day"]), r.get("lead_headline")) for r in landed
                  if r["security_key"] == key)
    for s in served:
        print("   %s..%s  lead=%r" % s)
    match = served == want
    print("   served == newest landed rows (span AND lead): %s" % match)
    ok = ok and payload.get("statusCode") == 200 and match and len(events) > 0

ba = [e for e in landed if e["security_key"] == "BA_US_Equity" and str(e["first_day"]) == "2026-09-08"]
print("BA 2026-09-08 landed lead: %r" % (ba[0]["lead_headline"] if ba else None))
print("CLOSE RUN: %s" % ("OK" if ok else "NOT OK"))
sys.exit(0 if ok else 1)
