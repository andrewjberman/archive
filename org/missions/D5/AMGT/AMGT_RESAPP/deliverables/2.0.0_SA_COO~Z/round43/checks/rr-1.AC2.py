"""AMGT_RESAPP round 43, AMGT-rr-1 AC2 -- the SERVED page of each of the five names now carries figures: the deployed function's
thesis route returns fiscal-year figures for each (the page's Model tab reads them). A read (lambda invoke of Opal's own function).
usage (repo root): python <this>"""
import json
import sys

import boto3

KEYS = ["AMD_US_Equity", "GOOGL_US_Equity", "LLY_US_Equity", "PWR_US_Equity", "UNH_US_Equity"]
client = boto3.client("lambda", region_name="us-east-1")
served = 0
for key in KEYS:
    path = "/api/scoped/amgt/security/%s/thesis" % key
    event = {"rawPath": path, "headers": {"x-firm-id": "opal"},
             "requestContext": {"http": {"method": "GET", "path": path}}, "queryStringParameters": None}
    resp = json.loads(client.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event).encode())["Payload"].read())
    body = json.loads(resp.get("body") or "{}")
    n = len(body.get("fiscal_year_figures") or [])
    served += resp.get("statusCode") == 200 and n > 0
    print("%s status=%s fiscal_year_figures=%d" % (key, resp.get("statusCode"), n))
print("served pages with figures: %d of %d" % (served, len(KEYS)))
sys.exit(0 if served == len(KEYS) else 1)
