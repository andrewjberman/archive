"""AMGT_HARVST round 19, cell HVST-i-4, AC2 -- issuer-written, dry-run at the base before the cut.

THE DEPLOY MOVED THE CODE, SUCCEEDED, AND LEFT ITS ROLLBACK TARGET STANDING.
  (1) opal-amgt-scoped-api's CodeSha256 differs from the round-19 base
      lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s= (AMGT_RESAPP ww-1, 19:18:58Z) and LastUpdateStatus is Successful;
  (2) the PRIOR artifact version -- the one the never-widen halves name as the rollback target, re-read at signing;
      61Fb7L90ggUdpjcXaX4T8CcMgquyzn0U at the cut -- still exists under
      s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip, and a NEWER version is latest;
  (3) the RESAPP control routes still answer 200: /thesis, /overlay, /peers for 992_HK_Equity, invoked directly.
READ-ONLY. Exit 0 only if every line reads PASS. If the halves name a different rollback VersionId (a later RESAPP
deploy), the issuer amends PRIOR_VERSION before the seat runs; it is never edited by the seat.
"""
import json
import sys

import boto3

FUNCTION = "opal-amgt-scoped-api"
BASE_SHA = "lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s="
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "research/opal-amgt-scoped-api.zip"
PRIOR_VERSION = "61Fb7L90ggUdpjcXaX4T8CcMgquyzn0U"
SECURITY = "992_HK_Equity"
failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


lam = boto3.client("lambda", region_name="us-east-1")
cfg = lam.get_function_configuration(FunctionName=FUNCTION)
print("deployed CodeSha256=%s LastModified=%s LastUpdateStatus=%s"
      % (cfg["CodeSha256"], cfg["LastModified"], cfg.get("LastUpdateStatus")))
check("(1) code moved off the round-19 base", cfg["CodeSha256"] != BASE_SHA, "base=%s" % BASE_SHA)
check("(1) update Successful", cfg.get("LastUpdateStatus") == "Successful")

s3 = boto3.client("s3", region_name="us-east-1")
versions, marker = [], {}
while True:
    resp = s3.list_object_versions(Bucket=BUCKET, Prefix=KEY, **marker)
    versions.extend(v for v in resp.get("Versions", []) if v["Key"] == KEY)
    if not resp.get("IsTruncated"):
        break
    marker = {"KeyMarker": resp["NextKeyMarker"], "VersionIdMarker": resp["NextVersionIdMarker"]}
latest = [v for v in versions if v.get("IsLatest")]
print("artifact versions under %s: %d; latest=%s" % (KEY, len(versions), latest[0]["VersionId"] if latest else "NONE"))
check("(2) prior artifact version still exists (rollback target)",
      any(v["VersionId"] == PRIOR_VERSION for v in versions), PRIOR_VERSION)
check("(2) a NEW artifact version is latest", bool(latest) and latest[0]["VersionId"] != PRIOR_VERSION)

for route in ("thesis", "overlay", "peers"):
    path = "/api/scoped/amgt/security/%s/%s" % (SECURITY, route)
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    resp = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))
    payload = json.loads(resp["Payload"].read())
    check("(3) RESAPP control route answers 200", payload.get("statusCode") == 200 and not resp.get("FunctionError"),
          "%s -> %s" % (path, payload.get("statusCode")))

print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
sys.exit(0 if not failures else 1)
