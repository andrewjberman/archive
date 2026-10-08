"""AMGT_CORPUS round 40, CRPS-ap-10 (d) leg v -- what the DEPLOYED scoped API serves for the dossier fields this round moved.

Read-only: GET-shaped direct invokes of the deployed function `opal-amgt-scoped-api` (the invoke shape of AMGT_RESAPP's
r77_served_shape.py), route /api/scoped/amgt/security/<key>/thesis. Prints, per name and field, whether a value or an absent
reason is served and the last 60 characters of a value (research text appears only as that tail), then the function's
LastModified. NO write.

  python ap10d_live_route.py
"""
import json
import sys

import boto3

FN = "opal-amgt-scoped-api"
ASK = [("TSM_US_Equity", "positives"), ("TSM_US_Equity", "management"), ("8306_JP_Equity", "management"),
       ("8316_JP_Equity", "management"), ("NKE_US_Equity", "special_items"), ("SAP_GY_Equity", "positives"),
       ("SHOP_CN_Equity", "management")]


def find(obj, name):
    if isinstance(obj, dict):
        if name in obj:
            return obj[name]
        for value in obj.values():
            got = find(value, name)
            if got is not None:
                return got
    return None


def main():
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("function %s LastModified %s CodeSha256 %s" % (FN, cfg.get("LastModified"), cfg.get("CodeSha256")))
    seen = {}
    for key, field in ASK:
        if key not in seen:
            event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "requestContext": {"http": {"method": "GET"}},
                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
            raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
            body = raw.get("body")
            seen[key] = (raw.get("statusCode"), json.loads(body) if isinstance(body, str) else body)
        status, payload = seen[key]
        fields = find(payload, "dossier_fields") or {}
        entry = (fields.get("fields") or fields).get(field) if isinstance(fields, dict) else None
        method = find(payload, "method_version")
        if not isinstance(entry, dict):
            print("%-16s %-14s http %s | NOT FOUND in dossier_fields (keys %s)" % (key, field, status, sorted(fields)[:8] if isinstance(fields, dict) else type(fields).__name__))
            continue
        value = entry.get("value")
        tail = str(value)[-60:].encode("ascii", "replace").decode("ascii") if value is not None else None
        print("%-16s %-14s http %s method %s | value_len %s ends %r | absent %r" % (
            key, field, status, str(method).rsplit("/", 1)[-1], len(value) if isinstance(value, str) else None, tail,
            str(entry.get("absent") or entry.get("reason"))[:90]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
