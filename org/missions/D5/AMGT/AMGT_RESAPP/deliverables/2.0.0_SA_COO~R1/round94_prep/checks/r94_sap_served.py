"""AMGT_RESAPP round-94 PREP -- AMGT-ff-5's served outcome: what the live /thesis route serves for the three names the stored-driver writes touched.

  PYTHONPATH=<repo root> python r94_sap_served.py [--where deployed|local]

Replaces `r92_driver_reverified.py --write-set SAP_GY_Equity` as ff-5's AC1: that check takes its EXPECTED points from a production re-verification of the stored object,
and a re-verification of an object whose points already carry rescaled values reads `value` (13.745) where the excerpt prints 13,745, so it keeps 1 of 3 (row D1-S24:
`reverify_stored_thesis_driver` is not idempotent over a rescaled object). The expectation here is the PAIR's table, not a recomputation.
    V1 SAP_GY_Equity serves exactly three points: 2023 = 13.745, 2024 = 18.078, 2025 = 21.05 (rounded to 6 decimals), each carrying `stated_scale` (million for 2023
       and 2024, billion for 2025), `stated_value` and `rescaled_to` `billion`.
    V2 control: ASML_NA_Equity serves no points (round 93's write).
    V3 control: BABA_US_Equity serves FY2025 = 118028 and FY2026 = 158132 (round 92's write).
Verdict: R94 SAP SERVED: YES|NO (exit 0|1). Before the act V1 FAILs (SAP serves none).
"""
import argparse
import json
import sys

import boto3

from lib.research.api import scoped_amgt

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
_LAM = boto3.client("lambda", region_name="us-east-1")


def points(where, key):
    event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, key), "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if where == "deployed":
        r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        r = scoped_amgt.handler(event)
    body = json.loads(r.get("body") or "{}")
    return (body.get("thesis_driver") or {}).get("points") or []


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", default="deployed", choices=["deployed", "local"])
    args = ap.parse_args()
    results = []
    sap = {p.get("period"): p for p in points(args.where, "SAP_GY_Equity")}
    shown = {k: round(float(v.get("value")), 6) for k, v in sap.items()}
    want = {"2023": 13.745, "2024": 18.078, "2025": 21.05}
    scales = {k: v.get("stated_scale") for k, v in sap.items()}
    fields = (scales == {"2023": "million", "2024": "million", "2025": "billion"}
              and all(v.get("rescaled_to") == "billion" and v.get("stated_value") is not None for v in sap.values()))
    results.append(say(shown == want and fields, "V1 SAP serves its three points on the billion scale with their stated scale and value",
                       "values %s, stated scales %s" % (shown, scales)))
    asml = points(args.where, "ASML_NA_Equity")
    results.append(say(not asml, "V2 control: ASML serves no points", "%d point(s)" % len(asml)))
    baba = {p.get("period"): p.get("value") for p in points(args.where, "BABA_US_Equity")}
    results.append(say(baba == {"FY2025": 118028, "FY2026": 158132}, "V3 control: BABA serves FY2025 = 118028 and FY2026 = 158132", str(baba)))
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R94 SAP SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
