"""Mint the Y1 synthetic test filer and run after-read 2b.

WHY A SEPARATE IDENTITY FROM Y75'S. Y75's filer is deliberately OPAL-GLOBAL-homed (firmId
opal-capital, allowedFirmIds [49financial]) because X-1 was an ON-BEHALF test. Y1's reads need the
OWNER of a template-lane request inside one firm, and an Opal-global home without a roster
entitlement is refused FIRM_BINDING at the owned-record read -- measured, not assumed: the live
call returned {"ok": false, "public_reason_code": "FIRM_BINDING"} for operation
analysis-request-history, which _scope/tests/test_global.py pins to
census["binding_tenant_matches_effective_firm"] is False.

Rostering the Y75 subject for global reach would WIDEN access to clear a test, which is not an
applier's act. A synthetic identity homed in the test firm is the narrow move: it reads only its
own firm's data and owns only what this test creates.
"""
import json
import sys

import boto3

USERS = "opal-users-v2"
FIRM = "49financial"
FILER = "irpt-y1-filer@opalinvest.com"   # synthetic; no login identity, service userType
NAME = "IRPT Y1 synthetic test filer"

ddb = boto3.client("dynamodb", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def put_filer():
    item = {
        "PK": {"S": "USER#" + FILER},
        "SK": {"S": "PROFILE"},
        "email": {"S": FILER},
        "firmId": {"S": FIRM},
        "status": {"S": "active"},
        "userType": {"S": "service"},
        "name": {"S": NAME},
        "allowedFirmIds": {"L": [{"S": FIRM}]},
    }
    ddb.put_item(TableName=USERS, Item=item)
    back = ddb.get_item(TableName=USERS, Key={"PK": item["PK"], "SK": item["SK"]},
                        ConsistentRead=True).get("Item")
    # the ATTRIBUTE TYPE is printed, because an earlier reader of allowedFirmIds asked for .L on a
    # scalar S and got [] BY CONSTRUCTION -- an empty list that was the reader's bug, not the data's
    got = back.get("allowedFirmIds") if back else None
    print("  filer written: %s" % (back is not None))
    print("  firmId        %r" % (back or {}).get("firmId"))
    print("  allowedFirmIds type=%s value=%r" % (list(got)[0] if got else None, got))
    return back is not None


def headers(email, name, firm):
    return {
        "x-user-email": email, "x-user-name": name, "x-user-tier": "service",
        "x-user-role": "service", "x-firm-id": firm, "x-user-type": "service",
        "x-origin-verify": "cloudfront", "x-contract-version": "v1",
    }


def call(route, path, hdrs, qs=None, method="GET"):
    ev = {"version": "2.0", "routeKey": route, "rawPath": path, "headers": hdrs,
          "queryStringParameters": qs or {},
          "requestContext": {"http": {"method": method, "path": path}}, "isBase64Encoded": False}
    r = lam.invoke(FunctionName="irpt-status", Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        return json.loads(raw)
    except ValueError:
        return {"_raw": raw[:400]}


def main():
    print("== mint the Y1 synthetic test filer, homed in the test firm ==")
    put_filer()
    print()
    print("== READ 2b: GET .../analysis/requests for the test filer, expect 200/ok ==")
    out = call("GET /api/scoped/investor-reporting/analysis/requests",
               "/api/scoped/investor-reporting/analysis/requests",
               headers(FILER, NAME, FIRM), {"selected_tenant": FIRM})
    print("  ok              %r" % out.get("ok"))
    print("  operation       %r" % out.get("operation"))
    st = out.get("status") or {}
    print("  state           %r" % st.get("state"))
    print("  public_reason   %r" % st.get("public_reason_code"))
    items = out.get("requests") or out.get("items") or (out.get("data") or {}).get("requests") or []
    print("  requests        %d  (denominator for the read 3/4/5 candidate picks)" % len(items))
    for it in items[:20]:
        if isinstance(it, dict):
            print("    %s" % json.dumps({k: it.get(k) for k in
                  ("request_id", "requestId", "status", "variant", "ticket_id", "input_id")}))
    print("  top-level keys  %s" % sorted(out))
    if len(sys.argv) > 1 and sys.argv[1] == "--dump":
        print(json.dumps(out)[:1500])


if __name__ == "__main__":
    main()
