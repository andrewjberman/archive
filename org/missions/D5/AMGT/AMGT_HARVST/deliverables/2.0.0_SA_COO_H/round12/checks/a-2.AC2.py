"""AMGT_HARVST round 12, cell HVST-a-2, AC2 -- issuer-written, dry-run at the base before the cut.

THE DEPLOY MOVED THE CODE, SUCCEEDED, AND LEFT ITS ROLLBACK TARGET STANDING.
  (1) opal-amgt-scoped-api's CodeSha256 differs from the round-12 base vBSCqd71wGn1GNOpaWGKr+KdI6t+zo3QVovzEd9Mrew=
      and LastUpdateStatus is Successful;
  (2) the PRIOR artifact version (VersionId 0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS, the rollback target named on the
      never-widen halves) still exists under s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip;
  (3) the RESAPP control routes still answer: /thesis, /overlay, /peers for 992_HK_Equity, invoked directly.
READ-ONLY. Exit 0 only if every line reads PASS.
"""
import json
import sys

import boto3

FUNCTION = "opal-amgt-scoped-api"
BASE_SHA = "vBSCqd71wGn1GNOpaWGKr+KdI6t+zo3QVovzEd9Mrew="
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "research/opal-amgt-scoped-api.zip"
PRIOR_VERSION = "0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS"
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
check("code moved off the round-12 base", cfg["CodeSha256"] != BASE_SHA, "base=%s" % BASE_SHA)
check("update Successful", cfg.get("LastUpdateStatus") == "Successful")

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
check("prior artifact version still exists (rollback target)",
      any(v["VersionId"] == PRIOR_VERSION for v in versions), PRIOR_VERSION)
check("a NEW artifact version is latest", bool(latest) and latest[0]["VersionId"] != PRIOR_VERSION)

for route in ("thesis", "overlay", "peers"):
    path = "/api/scoped/amgt/security/%s/%s" % (SECURITY, route)
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    resp = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))
    payload = json.loads(resp["Payload"].read())
    check("RESAPP control route answers 200", payload.get("statusCode") == 200 and not resp.get("FunctionError"),
          "%s -> %s" % (path, payload.get("statusCode")))

print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
sys.exit(0 if not failures else 1)
