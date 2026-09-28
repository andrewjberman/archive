"""AMGT_HARVST round 12, cell HVST-a-2, AC1 -- issuer-written, dry-run at the base before the cut.

THE TWO TIMELINE ROUTES ANSWER ON THE DEPLOYED PLANE, both halves of the path, with in-region timing.
  (1) MOUNTED: the gateway's APPLIED route set (apigatewayv2 get-routes, every page, counted client-side)
      carries both timeline route_keys; the /thesis route is the positive control.
  (2) SERVED: the DEPLOYED Lambda, invoked directly with the gateway's event shape (x-firm-id header),
      answers both timeline routes HTTP 200 with data for 992_HK_Equity; /thesis is the control.
  (3) TIMED: the Lambda's own REPORT Duration for each call, against the 29 s integration ceiling
      (scoped-amgt-api.tf timeout = 29).
READ-ONLY: GET-ROUTES + INVOKE of a read API. No write of any kind. Exit 0 only if all three hold.
"""
import base64
import json
import re
import sys

import boto3

API_ID = "7k3ed8px20"
FUNCTION = "opal-amgt-scoped-api"
KEY = "992_HK_Equity"
DAY = "2026-05-22"
CEILING_S = 29.0
WANT = [
    "GET /api/scoped/amgt/security/{security_key}/timeline",
    "GET /api/scoped/amgt/security/{security_key}/timeline/day/{date}",
]
CONTROL = "GET /api/scoped/amgt/security/{security_key}/thesis"

failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


def all_route_keys(client, api_id):
    """Every route_key on the API, over EVERY page (a length() on one page is the page count, not the total)."""
    found, n_pages, next_token = [], 0, None
    while True:
        params = {"ApiId": api_id}
        if next_token:
            params["NextToken"] = next_token
        page = client.get_routes(**params)
        n_pages += 1
        found.extend(r["RouteKey"] for r in page.get("Items", []))
        next_token = page.get("NextToken")
        if not next_token:
            return found, n_pages


gw = boto3.client("apigatewayv2", region_name="us-east-1")
keys, pages = all_route_keys(gw, API_ID)
amgt = sorted(k for k in keys if "/api/scoped/amgt/" in k)
print("get-routes %s: %d route(s) over %d page(s); %d under /api/scoped/amgt/" % (API_ID, len(keys), pages, len(amgt)))
check("control route mounted", CONTROL in keys, CONTROL)
for want in WANT:
    check("timeline route mounted", want in keys, want)

lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FUNCTION)
print("deployed %s CodeSha256=%s LastModified=%s" % (FUNCTION, cfg["CodeSha256"], cfg["LastModified"]))


def invoke(path, route_key):
    event = {"version": "2.0", "routeKey": route_key, "rawPath": path,
             "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    resp = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"), LogType="Tail")
    payload = json.loads(resp["Payload"].read())
    tail = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    m = re.search(r"\tDuration: ([0-9.]+) ms", tail)
    secs = float(m.group(1)) / 1000.0 if m else None
    status = payload.get("statusCode")
    try:
        body = json.loads(payload.get("body") or "{}")
    except ValueError:
        body = {}
    return status, body, secs, resp.get("FunctionError")


base = "/api/scoped/amgt/security/%s" % KEY
calls = [
    ("control /thesis", base + "/thesis", CONTROL, None),
    ("timeline range", base + "/timeline", WANT[0], "events"),
    ("timeline day", base + "/timeline/day/" + DAY, WANT[1], "articles"),
]
for label, path, route_key, data_key in calls:
    status, body, secs, ferr = invoke(path, route_key)
    n = len(body.get(data_key) or []) if data_key else None
    print("INVOKE %s -> HTTP %s FunctionError=%s duration=%s s %s" % (
        path, status, ferr, "%.2f" % secs if secs is not None else "UNREAD",
        ("%s=%s" % (data_key, n)) if data_key else ""))
    if data_key is None:
        check(label + " answers 200", status == 200)
        continue
    check(label + " answers 200 with data", status == 200 and not body.get("error") and (n or 0) > 0,
          "status=%s error=%s %s=%s" % (status, body.get("error"), data_key, n))
    # timed only on a 200 -- a 404 from the catch-all answers in a millisecond and would pass vacuously
    check(label + " answers 200 inside the %.0f s ceiling" % CEILING_S,
          status == 200 and secs is not None and secs < CEILING_S, "status=%s duration=%s" % (status, secs))

print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
sys.exit(0 if not failures else 1)
