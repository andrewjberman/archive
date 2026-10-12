#!/usr/bin/env python3
"""submit_synthetic_request.py -- BUILD ONLY. Submits ONE synthetic analysis request in tenant cottonwood,
as the project's existing synthetic filer, naming a ticket (IRPT_ANLREQ.TO-AR-y-166; CTO msg 6575).

Modes (exactly one):
  --plan        print the two POST events as JSON lines. No network, no boto3 client.
  --self-test   in-memory fakes of the door and of the users table. Prints SUBMIT-SELFTEST-OK on success.
                No boto3 client.
  --run         the ONLY mode that creates a boto3 client. Needs the literal
                --i-have-the-ctos-word msg-6575 and --advisor-opaque adv-<12 hex>. Never run by the order
                that built it; a later executor runs it.

--plan and --run need --tenant cottonwood and --ticket TCK-<8 digits>-<8 lowercase hex>. Anything else exits
non-zero before any other work.

Every contract below was read from the code at base commit 41f8c03511 (paths relative to the repo root):
  event (i)  intake/uploads.py:102-109 (required and optional body keys; any other key refuses UPLOAD_FIELDS)
             intake/uploads.py:23 (token pattern), :113-130 (filename, encoding, size)
             _authz/served.py:1063-1067 and :1069-1098 (advisor_email is required on an on-behalf upload)
             _authz/served.py:307-319 (internal subject: x-firm-id opal-capital, nine trusted headers)
             _authz/served.py:1138-1166 and _scope/interactive_access.py:57-76 (allowedFirmIds from the users row)
  event (ii) ycharts/generate/submission.py:47-93 (validate_public_request: the eight custody fields, the
             ticket_id shape at :18 and :78-80, the input_id basis at :84-88)
             ycharts/generate/acceptance.py:120-121 (ticket_id stored on the record)
  schemas    docs/contracts/investor-reporting/v1/AnalysisUploadRequest.schema.json
             docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json
"""
import argparse
import base64
import contextlib
import hashlib
import io
import json
import re
import sys
from pathlib import Path

TENANT = "cottonwood"
WORD = "msg-6575"
FILER = "irpt-y75-testfiler-20261009@opal.invalid"
FILER_NAME = "IRPT Y75 synthetic test filer"
FUNCTION = "irpt-ycharts-generate"
USERS = "opal-users-v2"
ROUTE_INPUT = "POST /api/scoped/investor-reporting/analysis/inputs"
RAW_INPUT = "/api/scoped/investor-reporting/analysis/inputs"
ROUTE_ANALYSIS = "POST /api/scoped/investor-reporting/analysis"
RAW_ANALYSIS = "/api/scoped/investor-reporting/analysis"
CSV = b"Ticker,Dollars\nAAPL,10000\nMSFT,15000\n"
FILENAME = "ar166_y166_template.csv"
TICKET_RE = re.compile(r"TCK-[0-9]{8}-[0-9a-f]{8}")
ADVISOR_RE = re.compile(r"adv-[0-9a-f]{12}")
INPUT_RE = re.compile(r"portfolio_[0-9a-f]{64}")
PLACEHOLDER_ADVISOR = "<resolved at --run from --advisor-opaque>"
PLACEHOLDER_INPUT = "<input_id issued by event (i) at state NORMALIZED>"
REPO_ROOT = Path(__file__).resolve().parents[8]
UPLOAD_SCHEMA = REPO_ROOT / "docs/contracts/investor-reporting/v1/AnalysisUploadRequest.schema.json"
SUBMISSION_SCHEMA = REPO_ROOT / "docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json"


# ---------------------------------------------------------------- events (pure, no client)

def request_id_for_ticket(ticket):
    return "anlreq-y166-" + ticket


def upload_token_for_ticket(ticket):
    # Fixed per ticket: a re-run for the same ticket reads the same upload (uploads.py create, prior record).
    return "ar166" + ticket.replace("-", "")


def headers():
    return {"x-user-email": FILER, "x-user-name": FILER_NAME, "x-user-tier": "service",
            "x-user-role": "service", "x-firm-id": "opal-capital", "x-user-type": "service",
            "x-origin-verify": "cloudfront", "x-contract-version": "v1"}


def event(route, raw, query, body):
    return {"version": "2.0", "routeKey": route, "rawPath": raw, "headers": headers(),
            "queryStringParameters": query, "requestContext": {"http": {"method": "POST", "path": raw}},
            "body": json.dumps(body, sort_keys=True), "isBase64Encoded": False}


def upload_body(ticket):
    return {"upload_token": upload_token_for_ticket(ticket), "filename": FILENAME,
            "file_base64": base64.b64encode(CSV).decode("ascii"), "file_type": "csv"}


def upload_event(ticket, advisor_email):
    return event(ROUTE_INPUT, RAW_INPUT, {"selected_tenant": TENANT, "advisor_email": advisor_email},
                 upload_body(ticket))


def submission_body(ticket, input_id):
    return {"request_id": request_id_for_ticket(ticket), "client_id": None, "account_ids": [],
            "snapshot_id": None, "variant": "overview", "comparison_keys": [],
            "report_title": "Synthetic analysis request (ticket test)",
            "prepared_for": "IRPT synthetic test recipient", "input_id": input_id, "ticket_id": ticket}


def submission_event(ticket, input_id):
    return event(ROUTE_ANALYSIS, RAW_ANALYSIS, {"selected_tenant": TENANT}, submission_body(ticket, input_id))


def adv_label(email):
    return "adv-" + hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()[:12]


def check_args(tenant, ticket):
    if tenant != TENANT:
        return "REFUSED: --tenant must be cottonwood"
    if ticket is None or not TICKET_RE.fullmatch(ticket):
        return "REFUSED: --ticket must match TCK-<8 digits>-<8 lowercase hex>"
    return None


def plan(ticket):
    print("PLAN tenant=%s ticket=%s -- two events, no network, no client" % (TENANT, ticket))
    print("PLAN placeholders: advisor_email=%s ; input_id=%s" % (PLACEHOLDER_ADVISOR, PLACEHOLDER_INPUT))
    for ev in (upload_event(ticket, PLACEHOLDER_ADVISOR), submission_event(ticket, PLACEHOLDER_INPUT)):
        print(json.dumps(ev, sort_keys=True))
    return 0


# ---------------------------------------------------------------- minimal JSON Schema reader (stdlib)

def _is_type(value, name):
    if name == "string":
        return isinstance(value, str)
    if name == "null":
        return value is None
    if name == "boolean":
        return isinstance(value, bool)
    if name == "array":
        return isinstance(value, list)
    if name == "object":
        return isinstance(value, dict)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ValueError("unsupported schema type " + name)


def schema_errors(value, schema, where="$"):
    """The keywords the two published contracts use, and nothing more. Returns a list of error strings."""
    errs = []
    if schema is True:
        return errs
    if schema is False:
        return [where + ": false schema"]
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_is_type(value, x) for x in types):
            return [where + ": type not in " + repr(types)]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(where + ": not in enum")
    if "const" in schema and value != schema["const"]:
        errs.append(where + ": not the const")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append(where + ": shorter than minLength")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append(where + ": longer than maxLength")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errs.append(where + ": pattern mismatch")
    if isinstance(value, dict):
        for name in schema.get("required", []):
            if name not in value:
                errs.append(where + ": missing required " + name)
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in props:
                    errs.append(where + ": unknown key " + name)
        for name, sub in props.items():
            if name in value:
                errs.extend(schema_errors(value[name], sub, where + "." + name))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append(where + ": fewer items than minItems")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append(where + ": more items than maxItems")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errs.append(where + ": items not unique")
        if "items" in schema:
            for i, x in enumerate(value):
                errs.extend(schema_errors(x, schema["items"], "%s[%d]" % (where, i)))
    for sub in schema.get("allOf", []):
        errs.extend(schema_errors(value, sub, where))
    if "anyOf" in schema and not any(not schema_errors(value, s, where) for s in schema["anyOf"]):
        errs.append(where + ": anyOf matched nothing")
    if "oneOf" in schema and sum(1 for s in schema["oneOf"] if not schema_errors(value, s, where)) != 1:
        errs.append(where + ": oneOf did not match exactly one")
    if "not" in schema and not schema_errors(value, schema["not"], where):
        errs.append(where + ": matched a not schema")
    if "if" in schema:
        branch = "then" if not schema_errors(value, schema["if"], where) else "else"
        if branch in schema:
            errs.extend(schema_errors(value, schema[branch], where))
    return errs


def load_schema(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- --run (the only client user)

def plain(attr):
    """DynamoDB typed attribute -> plain Python value (only the types the users row carries)."""
    if not isinstance(attr, dict):
        return attr
    if "S" in attr:
        return attr["S"]
    if "N" in attr:
        return attr["N"]
    if "BOOL" in attr:
        return attr["BOOL"]
    if "NULL" in attr:
        return None
    if "L" in attr:
        return [plain(x) for x in attr["L"]]
    if "SS" in attr:
        return list(attr["SS"])
    if "M" in attr:
        return {k: plain(v) for k, v in attr["M"].items()}
    return None


def admits(allowed, tenant):
    """An explicit naming only. The string ALL and an absent value never admit (fail closed)."""
    if isinstance(allowed, str):
        items = allowed.split(",")
    elif isinstance(allowed, list):
        items = allowed
    else:
        return False
    return tenant in [i.strip() for i in items if isinstance(i, str)]


def scan_users(ddb):
    start = None
    while True:
        kwargs = {"TableName": USERS, "ConsistentRead": True}
        if start:
            kwargs["ExclusiveStartKey"] = start
        page = ddb.scan(**kwargs)
        for item in page.get("Items", []):
            yield item
        start = page.get("LastEvaluatedKey")
        if not start:
            return


def resolve_advisor(ddb, opaque):
    """The advisor's email, found by its opaque label among active cottonwood users. Held in memory only."""
    for item in scan_users(ddb):
        row = {k: plain(v) for k, v in item.items()}
        email = row.get("email")
        if not isinstance(email, str) or not email:
            continue
        if row.get("firmId") != TENANT or row.get("status") != "active":
            continue
        if adv_label(email) == opaque:
            return email
    return None


def unwrap(raw):
    text = raw.decode("utf-8", "replace")
    out = json.loads(text)
    inner = out
    if isinstance(out, dict) and isinstance(out.get("body"), str):
        try:
            inner = json.loads(out["body"])
        except ValueError:
            inner = out["body"]
    http = out.get("statusCode") if isinstance(out, dict) else None
    return http, inner


def find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj and not isinstance(obj[key], (dict, list)):
            return obj[key]
        for v in obj.values():
            found = find_key(v, key)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_key(v, key)
            if found is not None:
                return found
    return None


def invoke(lam, ev):
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev, sort_keys=True).encode("utf-8"))
    http, inner = unwrap(r["Payload"].read())
    return r.get("StatusCode"), r.get("FunctionError"), http, inner


def run_preflight(args):
    if args.i_have_the_ctos_word != WORD:
        return "REFUSED: --run needs the literal --i-have-the-ctos-word msg-6575"
    if not args.advisor_opaque or not ADVISOR_RE.fullmatch(args.advisor_opaque):
        return "REFUSED: --run needs --advisor-opaque adv-<12 hex> (an opaque label, never an address)"
    return None


def run_flow(args, clients):
    ddb, lam = clients["ddb"], clients["lam"]
    item = ddb.get_item(TableName=USERS, Key={"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}},
                        ConsistentRead=True).get("Item")
    row = {k: plain(v) for k, v in (item or {}).items()}
    if row.get("email") != FILER or not admits(row.get("allowedFirmIds"), TENANT):
        print("STOP: the synthetic filer's users row does not list or admit cottonwood. No invoke was made.")
        print("STOP: this order writes no users row; the row's owner must name cottonwood.")
        return 1
    print("FILER-ROW: lists cottonwood (read only)")
    advisor = resolve_advisor(ddb, args.advisor_opaque)
    if advisor is None:
        print("STOP: no active cottonwood user carries the advisor opaque label. No invoke was made.")
        return 1
    print("ADVISOR: resolved from the opaque label (address not printed)")
    ls, fe, http, inner = invoke(lam, upload_event(args.ticket, advisor))
    upload_id = find_key(inner, "upload_id")
    input_id = find_key(inner, "input_id")
    state = find_key(inner, "state")
    print("EVENT-I lambda=%s function_error=%s http=%s state=%s" % (ls, fe, http, state))
    print("upload_id=%s" % upload_id)
    if not isinstance(upload_id, str) or not upload_id:
        print("STOP: the upload answer carries no upload id. Event (ii) is not sent.")
        return 1
    if not isinstance(input_id, str) or not INPUT_RE.fullmatch(input_id):
        print("STOP: no input_id in the upload answer (state=%s). Event (ii) needs input_id, which the upload"
              " answers only at NORMALIZED. Re-run --run for the same ticket later; the upload token is fixed per"
              " ticket, so the same upload is read." % state)
        return 1
    print("input_id=%s" % input_id)
    ls, fe, http, inner = invoke(lam, submission_event(args.ticket, input_id))
    print("EVENT-II lambda=%s function_error=%s http=%s" % (ls, fe, http))
    print("request_id=%s" % find_key(inner, "request_id"))
    try:
        ok = http is not None and 200 <= int(http) < 300
    except (TypeError, ValueError):
        ok = False
    if not ok:
        print("STOP: event (ii) was not accepted (http=%s). The public reason is in the answer and is not printed."
              % http)
        return 1
    print("RUN-OK")
    return 0


def make_clients():
    import boto3  # lazy: only the --run path reaches this line
    return {"ddb": boto3.client("dynamodb", region_name="us-east-1"),
            "lam": boto3.client("lambda", region_name="us-east-1")}


# ---------------------------------------------------------------- --self-test (in-memory fakes)

SELF_TICKET = "TCK-20261012-0123abcd"
SELF_ADVISOR = "advisor-y166-selftest@opal.invalid"


class FakeLambda(object):
    def __init__(self, states):
        self.states = list(states)
        self.calls = []

    def invoke(self, FunctionName, Payload):
        ev = json.loads(Payload.decode("utf-8"))
        self.calls.append(ev)
        if ev["routeKey"] == ROUTE_INPUT:
            state = self.states.pop(0) if self.states else "NORMALIZED"
            inner = {"upload_id": "UP-" + "b" * 64, "state": state,
                     "input_id": ("portfolio_" + "c" * 64) if state == "NORMALIZED" else None}
            status = 200
        else:
            inner = {"data": {"identity": {"request_id": "anlreq-selftest-0001"}, "status": {"state": "RECEIVED"}}}
            status = 202
        body = json.dumps({"statusCode": status, "body": json.dumps(inner)})
        return {"StatusCode": 200, "Payload": io.BytesIO(body.encode("utf-8"))}


class FakeDDB(object):
    def __init__(self, allowed, advisor_status="active"):
        self.filer = {"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}, "email": {"S": FILER},
                      "allowedFirmIds": {"L": [{"S": x} for x in allowed]}} if allowed is not None else None
        self.users = [{"email": {"S": SELF_ADVISOR}, "firmId": {"S": TENANT},
                       "status": {"S": advisor_status}}]

    def get_item(self, TableName, Key, ConsistentRead):
        return {"Item": self.filer} if self.filer else {}

    def scan(self, TableName, ConsistentRead, ExclusiveStartKey=None):
        return {"Items": self.users}


def _arm(name, ok, detail, results):
    results.append(ok)
    print("ARM %s: %s%s" % (name, "OK" if ok else "FAIL", "" if ok else " " + detail))


def self_test():
    results = []
    up_schema = load_schema(UPLOAD_SCHEMA)
    sub_schema = load_schema(SUBMISSION_SCHEMA)
    # 1. both bodies validate against the published contracts; negative controls must refuse
    e = schema_errors(upload_body(SELF_TICKET), up_schema)
    _arm("upload-body-validates", not e, str(e), results)
    bad = dict(upload_body(SELF_TICKET), csv_base64="AAAA")
    _arm("upload-body-negative-control", bool(schema_errors(bad, up_schema)), "mixed lanes accepted", results)
    e = schema_errors(submission_body(SELF_TICKET, "portfolio_" + "c" * 64), sub_schema)
    _arm("submission-body-validates", not e, str(e), results)
    no_basis = dict(submission_body(SELF_TICKET, "portfolio_" + "c" * 64))
    del no_basis["input_id"]
    _arm("submission-ticket-needs-input-basis", bool(schema_errors(no_basis, sub_schema)),
         "ticket without input_id accepted", results)
    _arm("ticket-pattern-matches-schema",
         sub_schema["properties"]["ticket_id"]["pattern"] == "^TCK-[0-9]{8}-[0-9a-f]{8}$",
         "schema pattern differs from the script", results)
    # 2. refusals before any other work
    _arm("tenant-other-refused", check_args("49financial", SELF_TICKET) is not None, "accepted", results)
    _arm("tenant-missing-refused", check_args(None, SELF_TICKET) is not None, "accepted", results)
    _arm("ticket-malformed-refused", check_args(TENANT, "TCK-1") is not None, "accepted", results)
    _arm("ticket-uppercase-refused", check_args(TENANT, "TCK-20261012-0123ABCD") is not None, "accepted", results)
    # 3. --run needs the literal word and an opaque advisor label (no client exists in this process)
    ns = argparse.Namespace(i_have_the_ctos_word=None, advisor_opaque=adv_label(SELF_ADVISOR), ticket=SELF_TICKET)
    _arm("run-without-literal-refused", run_preflight(ns) is not None, "accepted", results)
    ns.i_have_the_ctos_word = WORD
    ns.advisor_opaque = None
    _arm("run-without-advisor-refused", run_preflight(ns) is not None, "accepted", results)
    # 4. users row that does not admit cottonwood stops the run before any invoke
    for label, allowed in (("other-firm", ["49financial"]), ("ALL-not-explicit", ["ALL"]), ("absent", None)):
        lam = FakeLambda([])
        ns = argparse.Namespace(i_have_the_ctos_word=WORD, advisor_opaque=adv_label(SELF_ADVISOR), ticket=SELF_TICKET)
        with contextlib.redirect_stdout(io.StringIO()):
            rc = run_flow(ns, {"ddb": FakeDDB(allowed), "lam": lam})
        _arm("admission-stop-" + label, rc == 1 and not lam.calls,
             "rc=%s invokes=%d" % (rc, len(lam.calls)), results)
    # 5. deferred lane: the upload answers RESOLVING, so event (ii) is never sent
    lam = FakeLambda(["RESOLVING"])
    ns = argparse.Namespace(i_have_the_ctos_word=WORD, advisor_opaque=adv_label(SELF_ADVISOR), ticket=SELF_TICKET)
    with contextlib.redirect_stdout(io.StringIO()):
        rc = run_flow(ns, {"ddb": FakeDDB(["49financial", TENANT]), "lam": lam})
    _arm("deferred-stops-before-event-ii", rc == 1 and len(lam.calls) == 1,
         "rc=%s invokes=%d" % (rc, len(lam.calls)), results)
    # 6. happy path against the fake door: the advisor is named, event (ii) names the ticket and validates
    lam = FakeLambda(["NORMALIZED"])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run_flow(ns, {"ddb": FakeDDB(["49financial", TENANT]), "lam": lam})
    _arm("normalized-runs-both-events", rc == 0 and len(lam.calls) == 2, "rc=%s invokes=%d" % (rc, len(lam.calls)),
         results)
    ev_i = lam.calls[0] if lam.calls else {}
    ev_ii = lam.calls[1] if len(lam.calls) > 1 else {}
    _arm("event-i-names-advisor",
         ev_i.get("queryStringParameters", {}).get("advisor_email") == SELF_ADVISOR, "advisor not named", results)
    _arm("event-ii-validates-and-names-ticket",
         not schema_errors(json.loads(ev_ii.get("body", "{}")), sub_schema)
         and json.loads(ev_ii.get("body", "{}")).get("ticket_id") == SELF_TICKET,
         "event (ii) body wrong", results)
    _arm("run-prints-no-address", SELF_ADVISOR not in buf.getvalue() and FILER not in buf.getvalue(),
         "an address reached stdout", results)
    # 7. plan events: two POST lines, ticket in the submission, filer on the reserved domain
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        plan(SELF_TICKET)
    lines = [json.loads(x) for x in buf.getvalue().splitlines() if x.startswith("{")]
    _arm("plan-prints-two-post-events",
         len(lines) == 2 and all(x["routeKey"].startswith("POST ") for x in lines)
         and SELF_TICKET in lines[1]["body"], "plan shape wrong", results)
    total = len(results)
    passed = sum(1 for r in results if r)
    print("SELFTEST arms=%d of %d passed" % (passed, total))
    if passed == total:
        print("SUBMIT-SELFTEST-OK")
        return 0
    return 1


# ---------------------------------------------------------------- entry

def main(argv):
    ap = argparse.ArgumentParser(description="Submit ONE synthetic analysis request naming a ticket (build only).")
    ap.add_argument("--tenant", default=None)
    ap.add_argument("--ticket", default=None)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--run", action="store_true")
    ap.add_argument("--i-have-the-ctos-word", default=None)
    ap.add_argument("--advisor-opaque", default=None)
    args = ap.parse_args(argv[1:])
    if args.self_test:
        return self_test()
    err = check_args(args.tenant, args.ticket)
    if err:
        print(err)
        return 2
    if args.plan:
        return plan(args.ticket)
    err = run_preflight(args)
    if err:
        print(err)
        return 2
    return run_flow(args, make_clients())


if __name__ == "__main__":
    sys.exit(main(sys.argv))
