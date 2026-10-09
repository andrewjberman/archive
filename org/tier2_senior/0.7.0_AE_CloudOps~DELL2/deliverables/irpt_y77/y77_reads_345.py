"""Y77 release 6b, after-reads 3, 4 and 5: the custody path, the prospect path and the live ticket binding.

ONE direct IAM invoke per arm against the deployed irpt-ycharts-generate, on the submit route the
function's own ROUTES table serves (entry.py:147 "POST /api/scoped/investor-reporting/analysis").

Every contract is taken from code or from the order, not from memory:
  body shape   the order names "the test_generate_installed_custody.py shape, synthetic statement,
               no real-person data" -- reports/tests/test_generate_installed_custody.py:69-70
               CUSTODY_BODY. Nothing here is a real person or a real account.
  fields       docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json:
               required request_id, client_id, account_ids, snapshot_id, variant, comparison_keys,
               report_title, prepared_for; optional input_id ^portfolio_[0-9a-f]{64}$ and
               ticket_id ^TCK-[0-9]{8}-[0-9a-f]{8}$; additionalProperties False.
  headers      _scope/resolve.py:104 TRUSTED_HEADERS, plus X-Contract-Version, whose absence
               refused all four X-1 arms identically on Y75 and is checked before any scope work
               (_authz/authz_dispatch.py:138).

Read 3 PASSES when the answer shows no CUSTODY_FACTORY_REQUIRED and no ImportError, and the outcome
is EITHER an accepted custody entry OR a typed refusal from the factory's own validation -- the
order says so explicitly, so a typed refusal is not a failure.
"""
import io
import json
import sys

import boto3

FUNCTION = "irpt-ycharts-generate"
ROUTE = "POST /api/scoped/investor-reporting/analysis"
RAW_PATH = "/api/scoped/investor-reporting/analysis"
PRINCIPAL = "andrew@opalinvest.com"   # on the resident allow list; OPAL_GLOBAL home
RUN = "y77r6b-20261009"

# test_generate_installed_custody.py:69-70, verbatim shape, synthetic throughout
CUSTODY_BODY = {"request_id": RUN + "-custody", "client_id": "client-1", "account_ids": ["acct-1"],
                "snapshot_id": "cst_" + "b" * 64, "variant": "auto", "comparison_keys": [],
                "report_title": None, "prepared_for": "Client"}

# release 3's prospect shape: a real-shaped input_id (the one Y75's X-1 normalised), schema pattern
# ^portfolio_[0-9a-f]{64}$
INPUT_ID = "portfolio_3bd61083df29ad69915b0002ccb292f4ef48c718ebad93614ed4ae195d9e40d7"

# AnalysisSubmissionRequest.schema.json allOf[0]: IF input_id is present THEN client_id and
# snapshot_id must be null and account_ids empty; ELSE they must be populated. My first pass sent
# the custody fields alongside input_id and the schema correctly refused INVALID_INPUT, so the
# prospect body nulls them rather than inheriting CUSTODY_BODY wholesale.
PROSPECT_BASE = dict(CUSTODY_BODY, client_id=None, snapshot_id=None, account_ids=[])

lam = boto3.client("lambda", region_name="us-east-1")


def event(tenant, body):
    headers = {
        "x-user-email": PRINCIPAL,
        "x-user-name": "Andrew Berman",
        "x-user-tier": "partner",
        "x-user-role": "user",
        "x-firm-id": "opal-capital",
        "x-user-type": "Advisor",
        "x-origin-verify": "cloudfront",
        "x-contract-version": "v1",
    }
    return {"version": "2.0", "routeKey": ROUTE, "rawPath": RAW_PATH, "headers": headers,
            "queryStringParameters": {"selected_tenant": tenant},
            "requestContext": {"http": {"method": "POST", "path": RAW_PATH}},
            "body": json.dumps(body), "isBase64Encoded": False}


def invoke(ev):
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        out = json.loads(raw)
    except ValueError:
        return {"lambda_status": r.get("StatusCode"), "function_error": r.get("FunctionError"),
                "raw": raw[:500]}
    inner = out
    if isinstance(out, dict) and isinstance(out.get("body"), str):
        try:
            inner = json.loads(out["body"])
        except ValueError:
            inner = out["body"]
    return {"lambda_status": r.get("StatusCode"), "function_error": r.get("FunctionError"),
            "answer": inner}


def verdict(res):
    """The order's own PASS rule for read 3, applied to the answer text."""
    t = json.dumps(res)
    return {"has_custody_factory_required": "CUSTODY_FACTORY_REQUIRED" in t,
            "has_import_error": "ImportError" in t or "ModuleNotFound" in t,
            "has_access_denied": "AccessDenied" in t}


def main():
    out = {"run": RUN, "route": ROUTE, "principal_is_allow_listed": True, "arms": {}}

    # read 3 -- the custody path, cottonwood, NO input_id
    r3 = {"skipped": "read 3 already ran and PASSED; the order allows ONE invoke, so it is not re-fired"} if "--skip3" in sys.argv else invoke(event("cottonwood", CUSTODY_BODY))
    out["arms"]["3_custody_cottonwood"] = {**r3, "checks": verdict(r3)}
    print("(3) CUSTODY    lambda=%s err=%s" % (r3.get("lambda_status"), r3.get("function_error")))
    print("    checks:", json.dumps(verdict(r3)))
    print("    answer:", json.dumps(r3.get("answer"))[:360])

    # read 4 -- the prospect path, an input_id body
    b4 = dict(PROSPECT_BASE, request_id=RUN + "-prospect", input_id=INPUT_ID)
    r4 = invoke(event("49financial", b4))
    out["arms"]["4_prospect_input_id"] = {**r4, "checks": verdict(r4)}
    print("(4) PROSPECT   lambda=%s err=%s" % (r4.get("lambda_status"), r4.get("function_error")))
    print("    answer:", json.dumps(r4.get("answer"))[:300])

    # read 5a -- a VALID ticket_id must be accepted and carried
    b5 = dict(PROSPECT_BASE, request_id=RUN + "-ticket-ok", input_id=INPUT_ID,
              ticket_id="TCK-20261009-a1052909")
    r5 = invoke(event("49financial", b5))
    out["arms"]["5a_ticket_valid"] = {**r5, "checks": verdict(r5),
                                      "ticket_id_sent": "TCK-20261009-a1052909",
                                      "answer_carries_ticket": "TCK-20261009-a1052909" in json.dumps(r5)}
    print("(5a) TICKET OK lambda=%s carries=%s" % (r5.get("lambda_status"),
                                                   "TCK-20261009-a1052909" in json.dumps(r5)))
    print("    answer:", json.dumps(r5.get("answer"))[:300])

    # read 5b -- a MALFORMED ticket_id must refuse TICKET_REFERENCE
    b5b = dict(PROSPECT_BASE, request_id=RUN + "-ticket-bad", input_id=INPUT_ID,
               ticket_id="TCK-BADFORMAT-zz")
    r5b = invoke(event("49financial", b5b))
    out["arms"]["5b_ticket_malformed"] = {**r5b, "checks": verdict(r5b),
                                          "refuses_ticket_reference": "TICKET_REFERENCE" in json.dumps(r5b)}
    print("(5b) TICKET BAD refuses TICKET_REFERENCE=%s" % ("TICKET_REFERENCE" in json.dumps(r5b)))
    print("    answer:", json.dumps(r5b.get("answer"))[:300])

    p = ("C:/Users/Test/AppData/Local/Temp/claude/C--dev-ajb-workspace/"
         "32a60855-c63b-4e98-b745-fa87f5d02864/scratchpad/y77_reads345.json")
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print()
    print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
