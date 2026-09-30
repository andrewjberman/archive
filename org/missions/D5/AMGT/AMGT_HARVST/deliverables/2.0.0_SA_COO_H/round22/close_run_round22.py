"""AMGT_HARVST round 22 -- the COO's ONE REAL RUN at close, on the DEPLOYED plane (read-only).
Invokes the deployed opal-amgt-scoped-api /timeline for the 3 CHANGED securities (992_HK, AMZN, HD) and 3 KEPT
controls (NVDA, BA, COST), and compares each served event span and lead to the newest LANDED chatter_event rows.
INVOKE + S3 GET only."""
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402
ev = pg._latest_gold_snapshot_rows("chatter_event")
print("newest event rows", len(ev))
for r in sorted(ev, key=lambda r: (r["security_key"], str(r["first_day"]))):
    print(" ", r["security_key"], r["first_day"], r["last_day"], r["articles_total"], r["event_id"][:12],
          (r["lead_headline"] or "").encode("ascii", "replace").decode("ascii")[:60])
lam = boto3.client("lambda", region_name="us-east-1")
c = lam.get_function_configuration(FunctionName="opal-amgt-scoped-api")
print("reader", c["CodeSha256"], c["LastModified"])
ok = True
for key in ("992_HK_Equity", "AMZN_US_Equity", "HD_US_Equity", "NVDA_US_Equity", "BA_US_Equity", "COST_US_Equity"):
    path = "/api/scoped/amgt/security/%s/timeline" % key
    e = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
         "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    p = json.loads(lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(e).encode())["Payload"].read())
    b = json.loads(p.get("body") or "{}")
    served = sorted((x["first_day"], x["last_day"], x.get("lead_headline")) for x in b.get("events") or [])
    want = sorted((str(r["first_day"])[:10], str(r["last_day"])[:10], r["lead_headline"]) for r in ev if r["security_key"] == key)
    eq = served == want
    ok &= eq and p.get("statusCode") == 200
    print("GET /timeline", key, p.get("statusCode"), "events", len(served), "served==landed (span+lead)", eq,
          [(a, b_) for a, b_, _ in served])
print("CLOSE RUN:", "OK" if ok else "FAIL")
