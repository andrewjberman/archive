"""APPLY-Y1 after-reads 2b and the candidate discovery for reads 3, 4 and 5.

Contracts read from the code at the pin rather than assumed:
  routes        reports/status_installed.py:54-60 HISTORY_ROUTES -- the owned original reader is
                "GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original"
                -> operation "analysis-request-original", class OWNED_RECORD, id param "requestId"
                (ops/entry.py:228-240)
  refusals      ops/owned_report.py:195 -- ANALYSIS_ORIGINAL_NOT_APPLICABLE is the CUSTODY lane
                (no input_id in the frozen composition's browser half, :223) and also a lane that
                is neither CSV_UPLOAD nor a v2 TEMPLATE_UPLOAD (:245)
  headers       _scope/resolve.py:104 TRUSTED_HEADERS, plus x-contract-version, which
                _authz/authz_dispatch.py:55-56,138 checks FIRST, before any scope work

THE LINK IS NEVER PRINTED, LOGGED OR WRITTEN. Only its sha256, its byte length and its expiry
leave this script, per the order and the CTO half.
"""
import json
import sys

import boto3

FUNCTION = "irpt-status"
LIST_ROUTE = "GET /api/scoped/investor-reporting/analysis/requests"
LIST_PATH = "/api/scoped/investor-reporting/analysis/requests"

lam = boto3.client("lambda", region_name="us-east-1")


def headers(email, name, firm="opal-capital", tier="service", role="service"):
    return {
        "x-user-email": email,
        "x-user-name": name,
        "x-user-tier": tier,
        "x-user-role": role,
        "x-firm-id": firm,
        "x-user-type": "service",
        "x-origin-verify": "cloudfront",
        "x-contract-version": "v1",
    }


def call(route, path, hdrs, qs=None, method="GET"):
    ev = {
        "version": "2.0", "routeKey": route, "rawPath": path,
        "headers": hdrs, "queryStringParameters": qs or {},
        "requestContext": {"http": {"method": method, "path": path}},
        "isBase64Encoded": False,
    }
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        out = json.loads(raw)
    except ValueError:
        return {"lambda_status": r.get("StatusCode"), "function_error": r.get("FunctionError"),
                "raw": raw[:400]}
    inner = out.get("body") if isinstance(out, dict) else None
    if isinstance(inner, str):
        try:
            inner = json.loads(inner)
        except ValueError:
            pass
    return {"lambda_status": r.get("StatusCode"), "function_error": r.get("FunctionError"),
            "http_status": out.get("statusCode") if isinstance(out, dict) else None,
            "body": inner}


def main():
    email, name = sys.argv[1], "IRPT Y1 test filer"
    tenant = sys.argv[2] if len(sys.argv) > 2 else "49financial"

    print("== READ 2b: GET .../analysis/requests for the test filer, expect 200 ==")
    res = call(LIST_ROUTE, LIST_PATH, headers(email, name), {"selected_tenant": tenant})
    print("  lambda_status  %s  function_error %s" % (res.get("lambda_status"), res.get("function_error")))
    print("  HTTP STATUS    %s" % res.get("http_status"))
    body = res.get("body")
    if isinstance(body, dict):
        items = body.get("requests") or body.get("items") or []
        print("  requests returned: %d  (the denominator for the candidate picks below)" % len(items))
        for it in items[:25]:
            if not isinstance(it, dict):
                continue
            print("    id=%s status=%s lane=%s ticket=%s has_input=%s" % (
                it.get("request_id") or it.get("requestId"), it.get("status"),
                (it.get("source") or {}).get("lane") if isinstance(it.get("source"), dict) else it.get("lane"),
                bool(it.get("ticket_id")), bool(it.get("input_id"))))
        print("  body keys: %s" % sorted(body))
    else:
        print("  body: %s" % json.dumps(body)[:500])


if __name__ == "__main__":
    main()
