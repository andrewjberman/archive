"""AMGT_HARVST round 19, cell HVST-i-4, AC1 -- issuer-written, dry-run at the base before the cut.

A PARTIAL DAY NAMES ITS PUBLISHER ON THE DEPLOYED PLANE, on both timeline routes.
The DEPLOYED Lambda is invoked directly with the gateway's event shape (x-firm-id header):
  (1) /timeline for ASML_NA_Equity answers HTTP 200, and EVERY series entry carries `publishers_covered` (int) and
      `publishers_covered_codes` (list);
  (2) every PARTIAL entry names >= 1 code and len(codes) == publishers_covered; every DENIED entry names 0 codes;
      at least one PARTIAL entry names `sa`;
  (3) the served codes equal the newest LANDED chatter_daily row's `publishers_covered_codes` on EVERY day
      compared (denominator printed);
  (4) /timeline/day/2026-07-15 (an ASML PARTIAL day) answers 200 with `publishers_covered_codes` naming `sa`;
  (5) control: /timeline for FDX_US_Equity answers 200, every entry DENIED with 0 codes.
READ-ONLY: INVOKE of a read API + S3 GET. Exit 0 only if every line reads PASS.
"""
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.harvest import publication_gold as pg  # noqa: E402

FUNCTION = "opal-amgt-scoped-api"
KEY = "ASML_NA_Equity"
DAY = "2026-07-15"
CONTROL = "FDX_US_Equity"
failures = []


def check(label, ok, detail=""):
    print("%s: %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        failures.append(label)


lam = boto3.client("lambda", region_name="us-east-1")


def invoke(path):
    event = {"version": "2.0", "rawPath": path, "requestContext": {"http": {"method": "GET", "path": path}},
             "headers": {"x-firm-id": "bd"}, "queryStringParameters": None}
    resp = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode("utf-8"))
    payload = json.loads(resp["Payload"].read())
    body = json.loads(payload.get("body") or "{}")
    return payload.get("statusCode"), body


cfg = lam.get_function_configuration(FunctionName=FUNCTION)
print("deployed CodeSha256=%s LastModified=%s" % (cfg["CodeSha256"], cfg["LastModified"]))

landed = {str(r["day"])[:10]: r for r in pg._latest_gold_snapshot_rows("chatter_daily") if r["security_key"] == KEY}

status, body = invoke("/api/scoped/amgt/security/%s/timeline" % KEY)
series = body.get("series") or []
print("GET /timeline %s -> HTTP %s, %d series days" % (KEY, status, len(series)))
check("(1) /timeline answers 200 with a series", status == 200 and len(series) > 0)
missing = [s.get("date") for s in series if "publishers_covered" not in s or "publishers_covered_codes" not in s]
check("(1) every series entry carries publishers_covered + publishers_covered_codes", not missing and bool(series),
      "missing on %d of %d" % (len(missing), len(series)))

partial = [s for s in series if s.get("data_status") == "PARTIAL"]
denied = [s for s in series if s.get("data_status") == "DENIED"]
bad_partial = [s.get("date") for s in partial
               if not s.get("publishers_covered_codes")
               or len(s.get("publishers_covered_codes") or []) != s.get("publishers_covered")]
bad_denied = [s.get("date") for s in denied if s.get("publishers_covered_codes")]
print("series classes: PARTIAL=%d DENIED=%d other=%d" % (len(partial), len(denied),
                                                          len(series) - len(partial) - len(denied)))
check("(2) every PARTIAL entry names >= 1 code, len == publishers_covered", bool(partial) and not bad_partial,
      "bad %d of %d" % (len(bad_partial), len(partial)))
check("(2) every DENIED entry names 0 codes", not bad_denied, "bad %d of %d" % (len(bad_denied), len(denied)))
check("(2) at least one PARTIAL entry names sa", any("sa" in (s.get("publishers_covered_codes") or []) for s in partial))

compared = 0
unequal = []
for s in series:
    row = landed.get(str(s.get("date"))[:10])
    if row is None:
        continue
    compared += 1
    want = list(row.get("publishers_covered_codes") or []) if "publishers_covered_codes" in row else None
    if want is None or list(s.get("publishers_covered_codes") or []) != want:
        unequal.append(s.get("date"))
check("(3) served codes == newest landed chatter_daily codes on every day", compared > 0 and not unequal,
      "%d unequal of %d compared (landed days %d)" % (len(unequal), compared, len(landed)))

status, body = invoke("/api/scoped/amgt/security/%s/timeline/day/%s" % (KEY, DAY))
print("GET /timeline/day/%s %s -> HTTP %s, keys %s" % (DAY, KEY, status, sorted(body)))
check("(4) timeline_day answers 200 and names sa", status == 200
      and "sa" in (body.get("publishers_covered_codes") or []), "codes=%r" % body.get("publishers_covered_codes"))

status, body = invoke("/api/scoped/amgt/security/%s/timeline" % CONTROL)
cseries = body.get("series") or []
cbad = [s.get("date") for s in cseries if s.get("data_status") != "DENIED" or s.get("publishers_covered_codes")]
check("(5) control %s answers 200, every day DENIED with 0 codes" % CONTROL,
      status == 200 and bool(cseries) and not cbad and all("publishers_covered_codes" in s for s in cseries),
      "%d of %d off" % (len(cbad), len(cseries)))

print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
sys.exit(0 if not failures else 1)
