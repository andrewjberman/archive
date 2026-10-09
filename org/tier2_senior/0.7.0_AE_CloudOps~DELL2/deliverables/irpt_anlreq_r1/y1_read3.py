"""APPLY-Y1 after-read 3: ONE template-lane request of the test filer, three arms.

THE SIGNED LINK IS NEVER PRINTED, LOGGED OR WRITTEN. Only its sha256, byte length and expiry
leave this script -- the order and the CTO half both require it, so the link is compared in
memory and discarded.

Contracts read from the code at the pin, never assumed:
  upload route   intake/upload_entry.py:21        POST /api/scoped/investor-reporting/analysis/inputs
  submit route   _authz/tests/test_prospect_entry.py:23,32   POST /api/scoped/investor-reporting/analysis
                 -> operation "analysis-requests"
  read route     ops/tests/test_owned_entry.py:18 GET  .../analysis/requests/{requestId}
  original route reports/status_installed.py:60   GET  .../analysis/requests/{requestId}/original
  body schema    docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json --
                 additionalProperties false; allOf[0]: WITH input_id, client_id and snapshot_id
                 MUST be null and account_ids MUST be empty (my first Y77 bodies violated exactly
                 this and were refused INVALID_INPUT; the schema was right)
  principal      _scope/resolve.py:223-242 classify_principal -- branch 5, an x-advisor-id claim
                 makes FIRM_ADVISOR; _scope/prospect.py:34 requires FIRM_ADVISOR or
                 FIRM_OPERATIONS, which is why a `service` identity was refused
                 ProspectOwnershipRefused "verified firm advisor or operations owner required"
  refusals       ops/owned_report.py:223,245 ANALYSIS_ORIGINAL_NOT_APPLICABLE
"""
import hashlib
import json
import time

import boto3

GEN = "irpt-ycharts-generate"
STATUS = "irpt-status"
FIRM = "49financial"
OTHER_FIRM = "cottonwood"          # arm (b): a viewer whose verified firm is NOT the data firm
FILER = "irpt-y1-filer@opalinvest.com"
VIEWER = "irpt-y1-viewer@opalinvest.com"
NAME = "IRPT Y1 synthetic test filer"

CSV = b"Ticker,Dollars\nAAPL,10000\nMSFT,15000\n"
RUN = "y1r3-20261009"

lam = boto3.client("lambda", region_name="us-east-1")
ddb = boto3.client("dynamodb", region_name="us-east-1")


def adv(email):
    return "adv-" + hashlib.sha256(email.lower().encode()).hexdigest()[:12]


def headers(email, firm, name=NAME):
    """FIRM_ADVISOR: the x-advisor-id claim is branch 5 of classify_principal."""
    return {
        "x-user-email": email, "x-user-name": name, "x-user-tier": "advisor",
        "x-user-role": "advisor", "x-firm-id": firm, "x-user-type": "advisor",
        "x-advisor-id": adv(email), "x-advisor-role": "advisor",
        "x-origin-verify": "cloudfront", "x-contract-version": "v1",
    }


def put_user(email, firm, name):
    ddb.put_item(TableName="opal-users-v2", Item={
        "PK": {"S": "USER#" + email}, "SK": {"S": "PROFILE"}, "email": {"S": email},
        "firmId": {"S": firm}, "status": {"S": "active"}, "userType": {"S": "advisor"},
        "name": {"S": name}, "advisorId": {"S": adv(email)},
        "allowedFirmIds": {"L": [{"S": firm}]},
    })


def call(fn, route, path, hdrs, body=None, qs=None, method="GET", path_params=None):
    ev = {"version": "2.0", "routeKey": route, "rawPath": path, "headers": hdrs,
          "queryStringParameters": qs or {},
          "requestContext": {"http": {"method": method, "path": path}},
          "isBase64Encoded": False}
    if path_params:
        ev["pathParameters"] = path_params
    if body is not None:
        ev["body"] = json.dumps(body)
    r = lam.invoke(FunctionName=fn, Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        out = json.loads(raw)
    except ValueError:
        return {"_raw": raw[:500], "_fn_error": r.get("FunctionError")}
    if isinstance(out, dict) and isinstance(out.get("body"), str):
        try:
            out = dict(out, body=json.loads(out["body"]))
        except ValueError:
            pass
    out["_fn_error"] = r.get("FunctionError")
    return out


def reason(out):
    """The PUBLIC code, which masks the internal typed one; the internal name is in CloudWatch."""
    st = out.get("status") or (out.get("body") or {}).get("status") or {}
    if isinstance(st, dict) and st.get("public_reason_code"):
        return st.get("public_reason_code")
    return out.get("code") or (out.get("body") or {}).get("code")


def upload_template():
    token = RUN + "-" + hashlib.sha256(CSV).hexdigest()[:16]   # TOKEN regex [A-Za-z0-9_-]{8,128}
    import base64
    body = {"upload_token": token, "filename": "y1_r3_template.csv",
            "file_base64": base64.b64encode(CSV).decode(), "file_type": "csv"}
    out = call(GEN, "POST /api/scoped/investor-reporting/analysis/inputs",
               "/api/scoped/investor-reporting/analysis/inputs",
               headers(FILER, FIRM), body=body, qs={"selected_tenant": FIRM}, method="POST")
    return token, out


def submit(input_id):
    body = {
        "request_id": RUN + "-req1",
        "client_id": None, "snapshot_id": None, "account_ids": [],
        "variant": "auto", "comparison_keys": [], "report_title": None,
        "prepared_for": "IRPT Y1 synthetic prospect",
        "input_id": input_id,
    }
    return call(GEN, "POST /api/scoped/investor-reporting/analysis",
                "/api/scoped/investor-reporting/analysis",
                headers(FILER, FIRM), body=body, qs={"selected_tenant": FIRM}, method="POST")


def original(request_id, email, firm):
    path = "/api/scoped/investor-reporting/analysis/requests/%s/original" % request_id
    return call(STATUS, "GET /api/scoped/investor-reporting/analysis/requests/{requestId}/original",
                path, headers(email, firm), qs={"selected_tenant": firm},
                path_params={"requestId": request_id})


def link_facts(out):
    """sha256 + length + expiry ONLY. The url is read, hashed and dropped -- never returned."""
    body = out.get("body") if isinstance(out.get("body"), dict) else out
    d = body.get("data") if isinstance(body.get("data"), dict) else body
    url = None
    for k in ("url", "link", "signed_url", "download_url"):
        if isinstance(d.get(k), str):
            url = d.get(k)
            break
    facts = {"url_present": url is not None,
             "url_sha256": hashlib.sha256(url.encode()).hexdigest() if url else None,
             "artifact_sha256": d.get("sha256") or d.get("content_sha256"),
             "byte_length": d.get("byte_length") or d.get("length"),
             "expires_at": d.get("expires_at") or d.get("expiry")}
    del url
    return facts


def main():
    print("== identities (synthetic; advisor ids are derived, no real person) ==")
    put_user(FILER, FIRM, NAME)
    put_user(VIEWER, OTHER_FIRM, "IRPT Y1 synthetic other-firm viewer")
    print("  filer  %s @ %s  advisor %s" % (FILER, FIRM, adv(FILER)))
    print("  viewer %s @ %s  advisor %s" % (VIEWER, OTHER_FIRM, adv(VIEWER)))

    print("\n== step 1: template upload (the Y75 read-4 shape) ==")
    token, up = upload_template()
    print("  token          %s" % token)
    print("  fn_error       %r" % up.get("_fn_error"))
    print("  reason         %r" % reason(up))
    b = up.get("body") if isinstance(up.get("body"), dict) else up
    d = b.get("data") if isinstance(b.get("data"), dict) else b
    input_id = d.get("input_id") or d.get("inputId")
    state = (b.get("status") or {}).get("state") if isinstance(b.get("status"), dict) else None
    print("  state          %r" % state)
    print("  input_id       %r" % input_id)
    if not input_id:
        print("  body keys      %s" % sorted(b))
        print("  RAW            %s" % json.dumps(up)[:700])
        return

    # the upload normalizes asynchronously; re-POST the SAME token until it is NORMALIZED
    for i in range(12):
        time.sleep(5)
        _, again = upload_template()
        bb = again.get("body") if isinstance(again.get("body"), dict) else again
        dd = bb.get("data") if isinstance(bb.get("data"), dict) else bb
        st = (bb.get("status") or {}).get("state") if isinstance(bb.get("status"), dict) else None
        print("  poll %2d: state=%r input_id=%r" % (i + 1, st, dd.get("input_id")))
        if st in ("NORMALIZED", "READY", "AVAILABLE"):
            input_id = dd.get("input_id") or input_id
            break

    print("\n== step 2: submit the template-lane request ==")
    sub = submit(input_id)
    print("  fn_error       %r" % sub.get("_fn_error"))
    print("  reason         %r" % reason(sub))
    sb = sub.get("body") if isinstance(sub.get("body"), dict) else sub
    sd = sb.get("data") if isinstance(sb.get("data"), dict) else sb
    request_id = sd.get("request_id") or sd.get("requestId")
    print("  request_id     %r" % request_id)
    if not request_id:
        print("  RAW            %s" % json.dumps(sub)[:800])
        return

    print("\n== step 3 arm (a): the OWNER reads /original ==")
    for i in range(10):
        a = original(request_id, FILER, FIRM)
        r = reason(a)
        print("  attempt %2d: reason=%r" % (i + 1, r))
        if r is None:
            print("  LINK FACTS (the url itself is never printed): %s" % json.dumps(link_facts(a)))
            break
        if r not in ("NOT_READY", "PENDING", "UNAVAILABLE"):
            print("  RAW %s" % json.dumps(a)[:600])
            break
        time.sleep(6)

    print("\n== step 3 arm (b): a viewer at ANOTHER firm reads /original -- must be REFUSED ==")
    bout = original(request_id, VIEWER, OTHER_FIRM)
    print("  reason         %r" % reason(bout))
    print("  RAW            %s" % json.dumps(bout)[:400])

    print("\n== ids for the after-reads file ==")
    print(json.dumps({"input_id": input_id, "request_id": request_id, "token": token}))


if __name__ == "__main__":
    main()
