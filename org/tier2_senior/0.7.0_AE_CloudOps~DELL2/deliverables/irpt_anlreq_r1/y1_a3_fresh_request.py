"""APPLY-Y1 AMENDMENT 3: ONE fresh template-lane on-behalf request with NEW bytes and a new ticket.

WHY NEW BYTES ARE THE WHOLE POINT. Row IRPT_BCKEND-D2-S51: reads 3a, 4_route and 5 refused upstream
on a CONTENT-ADDRESSED retention row that the Y75 cleanup deleted, and that row is shared by Y77's
three test requests. The ruling is NO restore. So this request must not land on the same row, and
the only way to guarantee that is different bytes: a content-addressed row is named by the content's
own hash, so one changed holding gives a different row by construction rather than by hope.

Y75's body sha256 was 12ac4fb85e1691df...; this file changes one holding so the hash must differ,
and the script PRINTS both so the difference is measured rather than asserted.

Identities, per the amendment and the bounds:
  the SAME verified 49financial advisor as Y75 read 4, passed as an OPAQUE id (adv-04b85b8aefda)
  and resolved in memory -- a real address as an argv would land in the transcript, and the bounds
  say opaque ids only for real people. Y75's record names it in its "advisor" field; its
  "unlisted_advisor" adv-27637b75127c is a DIFFERENT principal, the other-firm negative arm, and is
  deliberately not used here.
  a FRESH synthetic test filer on the non-routable @opal.invalid domain, because Y75's was deleted
  at its cleanup ("ConsistentRead get-item reads NOT FOUND").

Contracts read from code rather than assumed:
  upload route   intake/upload_entry.py:21  POST /api/scoped/investor-reporting/analysis/inputs
  submit route   POST /api/scoped/investor-reporting/analysis -> operation analysis-requests
  body           intake/uploads.py:102 required {upload_token, filename, file_base64, file_type}
  token          TOKEN = [A-Za-z0-9_-]{8,128}
  headers        _scope/resolve.py:104 TRUSTED_HEADERS plus x-contract-version, which
                 _authz/authz_dispatch.py:55-56,138 checks FIRST, before any scope work
  schema         AnalysisSubmissionRequest: additionalProperties false; allOf[0] -- WITH input_id,
                 client_id and snapshot_id MUST be null and account_ids empty
  ticket_id      submission.py:78-80 -- a ticket_id with a malformed or absent input_id raises
                 TICKET_REFERENCE; the public classifier reports INVALID_INPUT, so the typed cause
                 is only visible in CloudWatch
"""
import base64
import hashlib
import json
import sys
import time

import boto3

GEN = "irpt-ycharts-generate"
USERS = "opal-users-v2"
FIRM = "49financial"
FILER = "irpt-y1-a3-filer-20261009@opal.invalid"
NAME = "IRPT Y1 AMENDMENT 3 synthetic test filer"
RUN = "y1a3-20261009"

# NEW BYTES: Y75 used MSFT,15000. One holding changed, so the content hash differs by construction.
CSV = b"Ticker,Dollars\nAAPL,10000\nMSFT,15001\n"
BODY_SHA256 = hashlib.sha256(CSV).hexdigest()
Y75_BODY_SHA256 = "12ac4fb85e1691df"

UPLOAD_ROUTE = "POST /api/scoped/investor-reporting/analysis/inputs"
UPLOAD_PATH = "/api/scoped/investor-reporting/analysis/inputs"
SUBMIT_ROUTE = "POST /api/scoped/investor-reporting/analysis"
SUBMIT_PATH = "/api/scoped/investor-reporting/analysis"

ddb = boto3.client("dynamodb", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def adv(email):
    return "adv-" + hashlib.sha256(email.lower().encode()).hexdigest()[:12]


def resolve_by_opaque(opaque, firm=None):
    """Return the address whose adv- label is `opaque`. Never printed, only used in memory."""
    pg = ddb.get_paginator("scan")
    for page in pg.paginate(TableName=USERS):
        for it in page.get("Items", []):
            em = (it.get("email") or {}).get("S")
            if em and adv(em) == opaque and (firm is None
                                             or (it.get("firmId") or {}).get("S") == firm):
                return em
    return None


def put_filer():
    item = {
        "PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"},
        "email": {"S": FILER}, "firmId": {"S": "opal-capital"},
        "status": {"S": "active"}, "userType": {"S": "service"},
        "name": {"S": NAME}, "allowedFirmIds": {"L": [{"S": FIRM}]},
    }
    ddb.put_item(TableName=USERS, Item=item)
    back = ddb.get_item(TableName=USERS, Key={"PK": item["PK"], "SK": item["SK"]},
                        ConsistentRead=True).get("Item")
    got = (back or {}).get("allowedFirmIds")
    # the TYPE TAG is printed because an earlier reader of this attribute asked for .L on a scalar
    # and got [] BY CONSTRUCTION
    return back is not None, (list(got)[0] if got else None)


def headers(filer=FILER):
    return {
        "x-user-email": filer, "x-user-name": NAME, "x-user-tier": "service",
        "x-user-role": "service", "x-firm-id": "opal-capital", "x-user-type": "service",
        "x-origin-verify": "cloudfront", "x-contract-version": "v1",
    }


def call(route, path, body, qs):
    ev = {"version": "2.0", "routeKey": route, "rawPath": path, "headers": headers(),
          "queryStringParameters": qs,
          "requestContext": {"http": {"method": "POST", "path": path}},
          "body": json.dumps(body), "isBase64Encoded": False}
    r = lam.invoke(FunctionName=GEN, Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        out = json.loads(raw)
    except ValueError:
        return {"_raw": raw[:400], "_fn_error": r.get("FunctionError")}
    if isinstance(out, dict) and isinstance(out.get("body"), str):
        try:
            out = dict(out, body=json.loads(out["body"]))
        except ValueError:
            pass
    out["_fn_error"] = r.get("FunctionError")
    return out


def inner(out):
    b = out.get("body") if isinstance(out.get("body"), dict) else out
    return b.get("data") if isinstance(b.get("data"), dict) else b


def reason(out):
    b = out.get("body") if isinstance(out.get("body"), dict) else out
    st = b.get("status") if isinstance(b.get("status"), dict) else {}
    return st.get("public_reason_code") or b.get("code")


def upload(advisor, token):
    body = {"upload_token": token, "filename": "y1_a3_template.csv",
            "file_base64": base64.b64encode(CSV).decode(), "file_type": "csv"}
    return call(UPLOAD_ROUTE, UPLOAD_PATH, body,
                {"selected_tenant": FIRM, "advisor_email": advisor})


def main(argv):
    opaque = argv[1] if len(argv) > 1 else "adv-04b85b8aefda"
    print("== AMENDMENT 3: one fresh template-lane on-behalf request, NEW bytes ==")
    print("  advisor opaque      %s" % opaque)
    advisor = resolve_by_opaque(opaque, FIRM)
    if advisor is None:
        print("  REFUSED: no active user in %s carries that opaque id" % FIRM)
        return 1
    print("  advisor resolved    yes (address held in memory, never printed)")
    print("  advisor opaque echo %s  <- equals the input, so the right principal resolved" % adv(advisor))
    print("  NEW body sha256     %s" % BODY_SHA256)
    print("  Y75 body sha256     %s...  <- MUST differ, and does: %s"
          % (Y75_BODY_SHA256, not BODY_SHA256.startswith(Y75_BODY_SHA256)))
    ok, tag = put_filer()
    print("  fresh filer written %s   allowedFirmIds type tag %s" % (ok, tag))
    print()

    token = RUN + "-" + BODY_SHA256[:16]
    print("== upload, re-POSTing the SAME token until NORMALIZED ==")
    input_id = None
    for i in range(14):
        out = upload(advisor, token)
        d = inner(out)
        b = out.get("body") if isinstance(out.get("body"), dict) else out
        st = (b.get("status") or {}).get("state") if isinstance(b.get("status"), dict) else None
        input_id = d.get("input_id") or input_id
        print("  poll %2d  state=%-12r reason=%-18r input_id=%r"
              % (i + 1, st, reason(out), d.get("input_id")))
        if st in ("NORMALIZED", "READY", "AVAILABLE"):
            break
        if reason(out) not in (None, "NOT_READY", "RESOLVING", "PENDING"):
            print("  RAW %s" % json.dumps(out)[:500])
            break
        time.sleep(5)
    print()
    print("  input_id            %r" % input_id)
    print("  token               %s" % token)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
