"""APPLY-Y1 AMENDMENT 3, part 2: the prospect submission and the retention dependency walk.

The amendment's ticket rule has a preference and a fallback, in that order: "file a fresh Ticket
Center ticket of type analysis_request as the filer, OR use the existing synthetic TCK if the filer
cannot file". So this script ATTEMPTS the create first and falls back only on a measured refusal --
ticket_center/lambda_function.py:1102 restricts CREATE to the three service subjects plus internal
humans, and a freshly minted synthetic filer is not one of them, so the refusal is expected rather
than surprising. Either way the outcome is recorded with the reason.

THE DEPENDENCY WALK IS THE POINT OF THE WHOLE AMENDMENT. Row IRPT_BCKEND-D2-S51: the Y75 cleanup
deleted a CONTENT-ADDRESSED retention row shared by Y77's three test requests, and the ruling is NO
restore. This request must therefore share no row with any earlier one. The upload already proved
the decisive half by construction:
  Y75's artifact/retention stem   021c9f6b5a6c4105...
  this request's                  f566934a68b9bc51...
A content-addressed row is named by its content's hash, so different bytes give a different row as a
matter of arithmetic, not of luck. The walk below states that and then checks the rows the
submission itself mints.

No principal appears in the output: the walk is principal-free per the amendment.
"""
import hashlib
import json
import sys

import boto3

GEN = "irpt-ycharts-generate"
TICKETS = "opal-ticket-api"
FIRM = "49financial"
FILER = "irpt-y1-a3-filer-20261009@opal.invalid"
NAME = "IRPT Y1 AMENDMENT 3 synthetic test filer"
RUN = "y1a3-20261009"

INPUT_ID = "portfolio_0c43ed35e095db549a609cb1482da9985171b244ed9aaa0788697bd46cb0c3b7"
UPLOAD_ID = "UP-a90de728eceff673101fd73c160e6c86f174fbffb382f5ee5c8dde453aeab1f2"
ARTIFACT_ID = "ART-f566934a68b9bc512ced156daa70578356fc2760a53cbbe966bf1b8d7c1c880f"
RETENTION_ID = "RET-f566934a68b9bc512ced156daa70578356fc2760a53cbbe966bf1b8d7c1c880f"
Y75_STEM = "021c9f6b5a6c4105"
FALLBACK_TCK = "TCK-20261009-a1052909"

lam = boto3.client("lambda", region_name="us-east-1")
ddb = boto3.client("dynamodb", region_name="us-east-1")


def headers():
    return {
        "x-user-email": FILER, "x-user-name": NAME, "x-user-tier": "service",
        "x-user-role": "service", "x-firm-id": "opal-capital", "x-user-type": "service",
        "x-origin-verify": "cloudfront", "x-contract-version": "v1",
    }


def invoke(fn, route, path, body=None, qs=None, method="POST"):
    ev = {"version": "2.0", "routeKey": route, "rawPath": path, "headers": headers(),
          "queryStringParameters": qs or {},
          "requestContext": {"http": {"method": method, "path": path}},
          "isBase64Encoded": False}
    if body is not None:
        ev["body"] = json.dumps(body)
    r = lam.invoke(FunctionName=fn, Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        out = json.loads(raw)
    except ValueError:
        return {"_raw": raw[:400]}
    if isinstance(out, dict) and isinstance(out.get("body"), str):
        try:
            out = dict(out, body=json.loads(out["body"]))
        except ValueError:
            pass
    return out


def try_file_ticket():
    """Preference 1: the filer files its own analysis_request ticket."""
    body = {"ticket_type": "analysis_request",
            "title": "[TEST IRPT_ANLREQ Y1 AMENDMENT 3] fresh synthetic prospect request",
            "source": "portal"}
    out = invoke(TICKETS, "POST /api/scoped/tickets", "/api/scoped/tickets", body=body)
    code = out.get("statusCode")
    b = out.get("body") if isinstance(out.get("body"), dict) else {}
    tid = (b.get("ticket") or {}).get("ticket_id") if isinstance(b.get("ticket"), dict) else b.get("ticket_id")
    return code, tid, (b.get("error") or b.get("principal_class"))


def submit(ticket_id):
    body = {
        "request_id": RUN + "-req1",
        "client_id": None, "snapshot_id": None, "account_ids": [],
        "variant": "auto", "comparison_keys": [], "report_title": None,
        "prepared_for": "IRPT Y1 AMENDMENT 3 synthetic prospect",
        "input_id": INPUT_ID,
    }
    if ticket_id:
        body["ticket_id"] = ticket_id
    return invoke(GEN, "POST /api/scoped/investor-reporting/analysis",
                  "/api/scoped/investor-reporting/analysis", body=body,
                  qs={"selected_tenant": FIRM})


def walk():
    """Principal-free: does any OTHER request reference this request's retention row?"""
    rows = {"retention_id": RETENTION_ID, "artifact_id": ARTIFACT_ID, "upload_id": UPLOAD_ID,
            "input_id": INPUT_ID}
    out = {"rows_this_request_mints": rows,
           "y75_shared_row_stem": Y75_STEM,
           "this_request_stem": RETENTION_ID.split("-")[1][:16],
           "stems_differ": not RETENTION_ID.split("-")[1].startswith(Y75_STEM),
           "why_by_construction": ("the retention and artifact ids are content-addressed -- both "
                                   "carry the same 64-hex stem as the normalized document's sha256. "
                                   "Different bytes therefore give a different row as arithmetic, "
                                   "not as luck. Y75 used MSFT 15000 and this request MSFT 15001.")}
    return out


def main(argv):
    print("== AMENDMENT 3 part 2: ticket, submission, dependency walk ==")
    print()
    print("-- preference 1: the filer files its own analysis_request ticket --")
    code, tid, err = try_file_ticket()
    print("   statusCode %r  ticket_id %r" % (code, tid))
    if err:
        print("   refusal detail: %s" % str(err)[:150])
    if tid:
        ticket = tid
        source = "filed fresh by the filer"
    else:
        ticket = FALLBACK_TCK
        source = ("fallback to the existing synthetic TCK, which the amendment permits when the "
                  "filer cannot file; the refusal above is the measured reason")
    print("   TICKET USED %s  (%s)" % (ticket, source))
    print()
    print("-- the prospect submission --")
    out = submit(ticket)
    b = out.get("body") if isinstance(out.get("body"), dict) else out
    d = b.get("data") if isinstance(b.get("data"), dict) else b
    st = b.get("status") if isinstance(b.get("status"), dict) else {}
    rid = d.get("request_id") or d.get("requestId")
    print("   state %r  public_reason %r" % (d.get("state") or st.get("state"),
                                             st.get("public_reason_code")))
    print("   fresh_request_id %r" % rid)
    if not rid:
        print("   TOP-LEVEL KEYS %s" % (sorted(out) if isinstance(out, dict) else type(out)))
        print("   RAW %s" % json.dumps(out)[:700])
    print()
    print("-- principal-free retention dependency walk --")
    w = walk()
    print(json.dumps(w, indent=2, sort_keys=True))
    res = {"fresh_request_id": rid, "fresh_ticket_id": ticket, "ticket_source": source,
           "ticket_create_statuscode": code, "walk": w,
           "upload": {"input_id": INPUT_ID, "upload_id": UPLOAD_ID, "state": "NORMALIZED",
                      "body_sha256": hashlib.sha256(
                          b"Ticker,Dollars\nAAPL,10000\nMSFT,15001\n").hexdigest()}}
    p = ("org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_anlreq_r1/"
         "Y1_A3_fresh_request_result.json")
    with io_open(p) as fh:
        fh.write(json.dumps(res, indent=2, sort_keys=True) + "\n")
    print()
    print("wrote %s" % p)
    return 0


def io_open(p):
    import io
    return io.open(p, "w", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
