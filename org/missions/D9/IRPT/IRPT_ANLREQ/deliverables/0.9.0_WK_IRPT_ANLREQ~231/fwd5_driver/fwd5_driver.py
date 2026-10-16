#!/usr/bin/env python3
"""IRPT_ANLREQ FWD-5 cross-firm driver (0.9.0_WK_IRPT_ANLREQ~231, AR-tz-67). BUILD ONLY: this file is not run here.

It signs in as the scoped second-firm principal (POST /auth/login, JSON {email, password}; the bearer access token
is held in memory only) and, for ONE ticket of ANOTHER firm, makes each call the record lists. Every call is expected
to be REFUSED: a 401, 403 or 404 whose body carries nothing of the ticket. The run is a later WORLD act by the applier
under a pair, after 2.0.0_SA_COO~V2's release.

  --plan                      prints the plan and exits 0; no network, no stdin.
  --selftest                  offline checks of the guard and the verdicts; exits 0 when they hold.
  --base URL --email ADDR --ticket ID --firm-a ID --firm-b ID --request-id ID --job-id ID --out DIR
                              --go IRPT_ANLREQ.TO-RUN-FWD5.<id>
                              the run. --firm-b, --request-id and --job-id are REQUIRED for a run: a missing one
                              exits 2 before any request is sent. Without a --go matching
                              ^IRPT_ANLREQ\\.TO-RUN-FWD5\\.\\S+$ it prints the plan and exits 0 with no request sent.
                              The password is read from stdin as one JSON object {"password": "..."}; it is never
                              printed, logged or written.
  --control                   with --go: the POSITIVE CONTROL (AR-tz-70). The SAME routes, order, guard, sign-in,
                              redirect handling and EXCLUDED rows, with --email as an identity ENTITLED to the ticket
                              (--firm-a its own firm label, --firm-b the ticket's owner firm). Without --go it prints
                              the plan and sends nothing. Without --control the run is unchanged.

Control verdicts (--control only, a closed set): ALLOWED, DENIED, UNREACHED, EXCLUDED.
  any 2xx on a ticket route                      -> ALLOWED (a 2xx is the pass here, not a leak; no marker scan)
  a 2xx on a report-side route (/api/scoped/investor-reporting/) is read by its ENVELOPE (AR-tz-72): ok true
      -> ALLOWED; a JSON object with NO ok key (a served body, AR-tz-74) -> ALLOWED; ok false with code
      CONTRACT_VERSION or ? -> UNREACHED; ok false with any other code -> DENIED (the reason names the code);
      not a JSON object or a non-boolean ok -> UNREACHED
  a 2xx ticket-list whose JSON carries a tickets list with the ticket id (case-insensitive) -> ALLOWED;
  a 2xx ticket-list without it                   -> DENIED
  401, 403 or 404                                -> DENIED
  3xx, 400, 405, 5xx, a dropped connection, a call the guard refused, a route with no GET shape, a missing id
                                                 -> UNREACHED
  EXCLUDED: the two excluded rows, never sent.
  Control exit: 0 when ticket-read AND ticket-list are both ALLOWED; 1 when either is DENIED; 2 when either is
  UNREACHED, no session was established, or a required id is missing (checked before sign-in, zero requests).
  The package routes are reported and do not change the exit. The report is fwd5_control_report.json in --out.

Verdicts (a closed set): REFUSED, LEAK, UNREACHED, EXCLUDED.
  any 2xx on a ticket route                      -> LEAK (a 2xx is never a refusal, an empty body included)
  a 2xx on a report-side route (/api/scoped/investor-reporting/) is read by its ENVELOPE (AR-tz-72), after the
      marker scan: a JSON object with NO ok key is a served body (AR-tz-74) -> LEAK; ok true -> LEAK; ok false with
      code FIRM_BINDING or NOT_AUTHORIZED -> REFUSED; ok false with any other code (CONTRACT_VERSION and ? included)
      -> UNREACHED, the reason says so; not a JSON object or a non-boolean ok -> UNREACHED
  on the route request-read-no-selection (no selected_tenant: the caller's own firm anchors the bucket, so absence
      is the answer): ok false with any code but CONTRACT_VERSION and ? -> REFUSED (the reason says "no selection:
      refused by <code> in the caller's own tenant"); CONTRACT_VERSION or ? -> UNREACHED; ok true or a served body
      -> LEAK
  every GET carries X-Contract-Version: v1 (the served route refuses a request without it before any read)
  the row's code is the envelope's reason code on a report-side route read by its envelope, else the empty string
  a 2xx ticket-list whose JSON carries a tickets list and no marker -> REFUSED (the other firm's ticket is absent)
  any answer whose body carries a marker (the ticket id or the other firm's id, case-insensitive) -> LEAK
  401, 403 or 404 with no marker                  -> REFUSED
  anything else a made call can answer: 3xx, 400, 405, 5xx, a dropped connection, a call the guard refused,
  a route with no GET shape in the record, a missing id                -> UNREACHED (not a pass)
  EXCLUDED: the meeting POST and the commentary draft. Never sent. Counted in neither the exit nor the pass;
  the row carries its one-line reason.
Exit (decided over the MADE calls only, every row but EXCLUDED): 0 every made call REFUSED; 1 any LEAK; 2 any
UNREACHED, no made call at all, or a run with bad arguments or no session.
The report (fwd5_run_report.json in --out) holds, per call, the route name, the status, the verdict, the body
length and the one-line reason. It never holds a body, a cookie, a token, a password or an address (the principal
is a digest).
"""
from __future__ import annotations

import argparse
import hashlib
import http.cookiejar
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

GO_RE = re.compile(r"^IRPT_ANLREQ\.TO-RUN-FWD5\.\S+$")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{4,80}$")
FIRM_RE = re.compile(r"^[A-Za-z0-9_.-]{4,80}$")
EMAIL_SUFFIX = "@opal.invalid"
FWD1_EMAIL = "fwd1-staff-r41b@opal.invalid"
REPORT_NAME = "fwd5_run_report.json"
CONTROL_REPORT_NAME = "fwd5_control_report.json"
CONTROL_SCHEMA = "fwd5_control_report/1"
TIMEOUT_S = 30
VERDICTS = ("REFUSED", "LEAK", "UNREACHED", "EXCLUDED")
CONTROL_VERDICTS = ("ALLOWED", "DENIED", "UNREACHED", "EXCLUDED")
CONTROL_GATE = ("ticket-read", "ticket-list")
CONTRACT_HEADER = "X-Contract-Version"  # AR-tz-72: the served route refuses a GET without it, before any read
CONTRACT_VALUE = "v1"
REPORT_PREFIX = "/api/scoped/investor-reporting/"  # the four report-side routes: graded by their envelope on a 2xx
FENCE_CODES = ("FIRM_BINDING", "NOT_AUTHORIZED")  # the only refusals that say something about the firm fence
NOT_FENCE_CODES = ("CONTRACT_VERSION", "?")  # a refusal that says nothing about the firm fence
CODE_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,40}$")
SEG = r"[A-Za-z0-9_-]+"

# The guard: GET only to these path shapes (the ticket routes, the package-file routes the record lists, and the
# report-side read shapes of AR-tz-74), POST only to the sign-in route. Matched on the path, after the origin is
# checked. The query is not matched. Not admitted: .../export/<seg>/download and the bare .../status.
GET_ALLOWED = (
    re.compile(r"/api/scoped/tickets"),
    re.compile(r"/api/scoped/tickets/" + SEG),
    re.compile(r"/api/scoped/tickets/" + SEG + r"/attachment"),
    re.compile(r"/api/scoped/investor-reporting/analysis/requests/" + SEG + r"/(?:original|pdf|commentary-pdf)"),
    re.compile(r"/api/scoped/investor-reporting/analysis/" + SEG + r"/sections"),
    re.compile(r"/api/scoped/investor-reporting/analysis/requests"),
    re.compile(r"/api/scoped/investor-reporting/analysis/requests/" + SEG),
    re.compile(r"/api/scoped/investor-reporting/status/" + SEG),
    re.compile(r"/api/scoped/investor-reporting/narrative/" + SEG),
    re.compile(r"/api/scoped/investor-reporting/export/" + SEG),
)
POST_ALLOWED = (re.compile(r"/auth/login"),)

# The calls, in order. "excluded" = the row is EXCLUDED with its one-line reason and is never sent (ruled by the
# issuer, TO-AR-tz-68). method None = the record names no GET route for it.
ROUTES = (
    {"name": "ticket-read", "method": "GET", "template": "/api/scoped/tickets/{ticket}",
     "needs": ("ticket",), "list": False, "plan": "the ticket read (the whole record if it leaked)"},
    {"name": "ticket-list", "method": "GET", "template": "/api/scoped/tickets",
     "needs": (), "list": True, "plan": "the principal's list: the other firm's ticket must be absent"},
    {"name": "form-as-filled", "method": "GET", "template": "/api/scoped/tickets/{ticket}/attachment",
     "needs": ("ticket",), "list": False, "plan": "the trade form as filled (the attachment presign route)"},
    {"name": "original-upload", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests/{request_id}/original?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False, "plan": "the retained original upload"},
    {"name": "opal-report", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/{job_id}/sections?selected_tenant={firm_b}",
     "needs": ("job_id", "firm_b"), "list": False, "plan": "the Opal report sections"},
    {"name": "report-pdf", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests/{request_id}/pdf?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False, "plan": "the report PDF"},
    {"name": "commentary-draft", "method": None, "template": "",
     "needs": (), "list": False,
     "plan": "EXCLUDED: no GET route for the draft is in the record",
     "excluded": "the commentary draft has no GET route; it rides the ticket read body, which the LEAK check inspects"},
    {"name": "commentary-pdf", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests/{request_id}/commentary-pdf?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False, "plan": "the commentary PDF"},
    {"name": "request-read", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests/{request_id}?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False,
     "plan": "the analysis request read (the request record, whole if it leaked)"},
    {"name": "request-history", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests?selected_tenant={firm_b}",
     "needs": (), "list": False,
     "plan": "the request history list (needs no id: the other firm's request must be absent)"},
    {"name": "job-status", "method": "GET",
     "template": "/api/scoped/investor-reporting/status/{job_id}?selected_tenant={firm_b}",
     "needs": ("job_id", "firm_b"), "list": False, "plan": "the job status read"},
    {"name": "narrative", "method": "GET",
     "template": "/api/scoped/investor-reporting/narrative/{request_id}?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False,
     "plan": "the report narrative; the request id stands in for the report id (the firm fence refuses before any "
             "id is read)"},
    {"name": "export-receipt", "method": "GET",
     "template": "/api/scoped/investor-reporting/export/{request_id}?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False,
     "plan": "the export receipt; the request id stands in for the report id (the firm fence refuses before any "
             "id is read)"},
    {"name": "request-read-no-selection", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests/{request_id}",
     "needs": ("request_id",), "list": False, "no_selection": True,
     "plan": "the request read with NO selected_tenant: the caller's own firm anchors the bucket, so absence is the "
             "answer"},
    {"name": "meeting", "method": "POST", "template": "/api/scoped/tickets/{ticket}/meeting",
     "needs": ("ticket",), "list": False,
     "plan": "EXCLUDED: a POST of a meeting is never sent",
     "excluded": "a POST of a meeting is a write attempt on another firm's ticket, outside the DONE WHEN (its scope "
                 "refusal is proved offline by infra/aws/lambda/ticket_center/tests/test_cross_firm_meeting_scope.py)"},
)


class GuardRefused(Exception):
    """The guard refused a request before it was sent."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """A 3xx is an answer, not a path to follow: it is UNREACHED, never a refusal."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401 -- urllib hook
        return None


def build_opener():
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.ProxyHandler({}),
                                       urllib.request.HTTPCookieProcessor(jar), _NoRedirect())


def admit(method, url, base):
    """The route guard. Same origin as the base; GET to a listed shape; POST to the sign-in route; else refused."""
    m = str(method).upper()
    try:
        u = urllib.parse.urlsplit(url)
        b = urllib.parse.urlsplit(base)
    except ValueError:
        return False
    if u.scheme not in ("http", "https") or (u.scheme, u.netloc) != (b.scheme, b.netloc):
        return False
    if u.username or u.password or u.fragment:
        return False
    if m == "GET":
        return any(p.fullmatch(u.path) for p in GET_ALLOWED)
    if m == "POST":
        return any(p.fullmatch(u.path) for p in POST_ALLOWED)
    return False


def send_raw(method, url, headers, body, opener):
    """One request. Returns (status, body bytes). A 4xx or 5xx is an answer; a dropped connection raises OSError."""
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = opener.open(req, timeout=TIMEOUT_S)
    except urllib.error.HTTPError as err:
        try:
            return err.code, err.read()
        finally:
            err.close()
    with resp:
        return resp.status, resp.read()


def guarded_send(method, url, base, opener, headers, body=None):
    """The only way a request leaves this file. A refused request is never sent."""
    if not admit(method, url, base):
        raise GuardRefused(str(method).upper())
    return send_raw(method, url, headers, body, opener)


def _is_ticket_list(body):
    try:
        obj = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(obj, dict) and isinstance(obj.get("tickets"), list)


def classify(is_list, status, body, markers):
    """The closed verdict for one answer. The body is read for markers and never kept."""
    if status is None:
        return "UNREACHED"
    low = body.decode("utf-8", "replace").lower()
    if any(mk and mk in low for mk in markers):
        return "LEAK"
    if 200 <= status < 300:
        if is_list and _is_ticket_list(body):
            return "REFUSED"
        return "LEAK"
    if status in (401, 403, 404):
        return "REFUSED"
    return "UNREACHED"


def has_marker(body, markers):
    low = body.decode("utf-8", "replace").lower()
    return any(mk and mk in low for mk in markers)


def envelope_of(body):
    """(ok, code) of a report-side 2xx answer. ok is the boolean, or None when the body is not a JSON object with a
    boolean ok. code is status.public_reason_code when it is a string of the closed shape, else "?". Read, never kept."""
    try:
        obj = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None, "?"
    if not isinstance(obj, dict):
        return None, "?"
    status = obj.get("status")
    code = status.get("public_reason_code") if isinstance(status, dict) else None
    if not isinstance(code, str) or not CODE_RE.fullmatch(code):
        code = "?"
    ok = obj.get("ok")
    return (ok if isinstance(ok, bool) else None), code


def ok_key_absent(body):
    """True when a 2xx answer is a JSON object that carries NO ok key at all: a served body (AR-tz-74). A non-object,
    a body that is not JSON, and a present but non-boolean ok are not this case. Read, never kept."""
    try:
        obj = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return False
    return isinstance(obj, dict) and "ok" not in obj


def _run_envelope(body, no_selection=False):
    """The RUN verdict for a report-side 2xx that carries no marker: (verdict, reason, code). A JSON object with no ok
    key is a served body and LEAK (AR-tz-74). Only FIRM_BINDING and NOT_AUTHORIZED are the firm fence; any other
    refusal code is UNREACHED, never REFUSED. The no-selection route (no selected_tenant) reads absence: any refusal
    but CONTRACT_VERSION or ? is REFUSED there, because the caller's own tenant is the bucket."""
    ok, code = envelope_of(body)
    if ok is None:
        if ok_key_absent(body):
            return "LEAK", "2xx served body with no ok key (content for the other firm)", code
        return "UNREACHED", "2xx answer is not a JSON object with a boolean ok", code
    if ok:
        return "LEAK", "2xx envelope with ok true", code
    if no_selection:
        if code in NOT_FENCE_CODES:
            return "UNREACHED", "no selection: refused by %s, not an absence answer" % code, code
        return "REFUSED", "no selection: refused by %s in the caller's own tenant" % code, code
    if code in FENCE_CODES:
        return "REFUSED", "refused by the firm fence (%s)" % code, code
    return "UNREACHED", "refused by %s, not by the firm fence" % code, code


def classify_report(status, body, markers, no_selection=False):
    """The RUN verdict for a report-side route: (verdict, reason, code). The marker scan runs first, as classify does;
    a non-2xx answer keeps classify's grading and carries no code; only a marker-free 2xx is read by its envelope."""
    if status is None or not 200 <= status < 300 or has_marker(body, markers):
        return classify(False, status, body, markers), "", ""
    return _run_envelope(body, no_selection)


def control_report_answer(status, body, ticket):
    """The CONTROL verdict for a report-side route: (verdict, reason, code). A non-2xx keeps control_answer's grading.
    A 2xx is read by its envelope: a JSON object with no ok key (a served body, AR-tz-74) ALLOWED; ok true ALLOWED;
    code CONTRACT_VERSION or ? UNREACHED; any other code DENIED; a non-boolean ok UNREACHED. No marker scan: an
    entitled identity may see the ticket id."""
    if status is None or not 200 <= status < 300:
        verdict, reason = control_answer(False, status, body, ticket)
        return verdict, reason, ""
    ok, code = envelope_of(body)
    if ok is None:
        if ok_key_absent(body):
            return "ALLOWED", "2xx served body with no ok key", code
        return "UNREACHED", "2xx answer is not a JSON object with a boolean ok", code
    if ok:
        return "ALLOWED", "2xx envelope with ok true", code
    if code in NOT_FENCE_CODES:
        return "UNREACHED", "refused by %s, not by the firm fence" % code, code
    return "DENIED", "refused by %s" % code, code


def exit_code(rows):
    """Decided over the MADE calls only: every row whose verdict is not EXCLUDED."""
    made = [r["verdict"] for r in rows if r["verdict"] != "EXCLUDED"]
    if "LEAK" in made:
        return 1
    if not made or "UNREACHED" in made:
        return 2
    return 0


def _holds_id(node, want):
    """True when a string value of the node equals the ticket id, case-insensitive. Keys are not read."""
    if isinstance(node, str):
        return node.lower() == want
    if isinstance(node, dict):
        return any(_holds_id(v, want) for v in node.values())
    if isinstance(node, list):
        return any(_holds_id(v, want) for v in node)
    return False


def list_carries_ticket(body, ticket):
    """A ticket-list answer that is a JSON object whose tickets list has an entry holding the ticket id."""
    try:
        obj = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return False
    if not isinstance(obj, dict) or not isinstance(obj.get("tickets"), list):
        return False
    want = ticket.lower()
    return any(_holds_id(item, want) for item in obj["tickets"])


def control_answer(is_list, status, body, ticket):
    """The control verdict for one answer, as (verdict, fixed one-line reason). The body is read for the ticket id
    on ticket-list only, never scanned for markers (an entitled identity may see the id), and never kept."""
    if status is None:
        return "UNREACHED", "no answer (dropped connection)"
    if 200 <= status < 300:
        if not is_list:
            return "ALLOWED", "2xx answer"
        if list_carries_ticket(body, ticket):
            return "ALLOWED", "2xx ticket list carries the ticket id"
        return "DENIED", "2xx ticket list does not carry the ticket id"
    if status in (401, 403, 404):
        return "DENIED", "%d answer" % status
    return "UNREACHED", "%d answer is not a verdict" % status


def control_exit_code(rows):
    """Decided over the two gate routes only (ticket-read, ticket-list); the package routes are reported and do not
    change it. 1 when either gate route is DENIED; 0 when both are ALLOWED; else 2 (UNREACHED, no session, a gate
    row missing)."""
    gate = [r["verdict"] for r in rows if r["route"] in CONTROL_GATE]
    if "DENIED" in gate:
        return 1
    if len(gate) == len(CONTROL_GATE) and all(v == "ALLOWED" for v in gate):
        return 0
    return 2


def sign_in(base, email, password, opener):
    """POST /auth/login. Returns (access token or None, a fixed reason). The password is never echoed."""
    body = json.dumps({"email": email, "password": password}).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        status, data = guarded_send("POST", base + "/auth/login", base, opener, headers, body)
    except (GuardRefused, OSError):
        return None, "the sign-in call was not made"
    if not 200 <= status < 300:
        return None, "the sign-in answered %d" % status
    try:
        obj = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None, "the sign-in answer was not JSON"
    if not isinstance(obj, dict) or obj.get("mfaRequired") is True:
        return None, "the sign-in did not establish a session"
    token = obj.get("accessToken")
    if not isinstance(token, str) or not token:
        return None, "the sign-in answer carried no access token"
    return token, "signed in"


def _excluded_row(r):
    """An EXCLUDED row: never sent, carries the one-line reason the issuer ruled."""
    return {"route": r["name"], "method": r["method"] or "-", "status": None, "verdict": "EXCLUDED",
            "body_len": 0, "reason": r["excluded"], "code": ""}


def run_calls(routes, base, opener, token, ctx, markers, control=False):
    """Every route, in order. Returns (rows, guard-refused route names). A row never holds a body. control=True reads
    each answer with control_answer (AR-tz-70): no marker scan, and the verdict carries a fixed reason."""
    rows = []
    refused = []
    for r in routes:
        if r.get("excluded"):
            rows.append(_excluded_row(r))
            continue
        row = {"route": r["name"], "method": r["method"] or "-", "status": None,
               "verdict": "UNREACHED", "body_len": 0, "reason": "", "code": ""}
        missing = [k for k in r["needs"] if not ctx.get(k)]
        if r["method"] is None:
            row["reason"] = "no GET route for it in the record"
        elif missing:
            row["reason"] = "no value supplied for " + ", ".join(missing)
        else:
            url = base + r["template"].format(**ctx)
            headers = {"Accept": "application/json", "Authorization": "Bearer " + token,
                       CONTRACT_HEADER: CONTRACT_VALUE}
            try:
                status, body = guarded_send(r["method"], url, base, opener, headers)
            except GuardRefused:
                refused.append(r["name"])
                row["reason"] = "guard refused before send"
            except OSError:
                row["reason"] = "transport error, no answer"
            else:
                row["status"] = status
                row["body_len"] = len(body)
                report = r["template"].startswith(REPORT_PREFIX)
                if control and report:
                    row["verdict"], row["reason"], row["code"] = control_report_answer(status, body, ctx["ticket"])
                elif control:
                    row["verdict"], row["reason"] = control_answer(r["list"], status, body, ctx["ticket"])
                elif report:
                    row["verdict"], row["reason"], row["code"] = classify_report(
                        status, body, markers, no_selection=r.get("no_selection", False))
                else:
                    row["verdict"] = classify(r["list"], status, body, markers)
        rows.append(row)
    return rows, refused


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def base_problem(base):
    try:
        u = urllib.parse.urlsplit(base)
    except ValueError:
        return "base is not a URL"
    if u.scheme not in ("http", "https") or not u.netloc:
        return "base must be an http(s) origin"
    if u.username or u.password:
        return "no credentials in the base"
    if u.path not in ("", "/") or u.query or u.fragment:
        return "base must be an origin with no path"
    return None


def email_problem(email):
    low = email.lower()
    if any(c.isspace() or c == "," for c in email) or not low.endswith(EMAIL_SUFFIX) \
            or len(low) == len(EMAIL_SUFFIX) or low == FWD1_EMAIL:
        return "email must be a synthetic @opal.invalid principal, not the FWD-1 helper's"
    return None


def read_password(stream):
    """One JSON object on stdin. A failure names no input content."""
    try:
        obj = json.loads(stream.read())
    except ValueError:
        raise ValueError("stdin is not one JSON object")
    pw = obj.get("password") if isinstance(obj, dict) else None
    if not isinstance(pw, str) or not pw:
        raise ValueError("stdin carries no password field")
    return pw


def print_plan(routes=ROUTES, control=False):
    print("FWD5 DRIVER PLAN (build only; the run is a WORLD act under a pair after 2.0.0_SA_COO~V2's release)")
    print("sign-in: POST /auth/login, JSON {email, password}; bearer access token and refresh cookie held in memory")
    for i, r in enumerate(routes, 1):
        print("  %d. %-17s %-4s %s  -- %s" % (i, r["name"], r["method"] or "--", r["template"] or "(no route)",
                                             r["plan"]))
    print("EXCLUDED rows (never sent, counted in neither the exit nor the pass):")
    for r in routes:
        if r.get("excluded"):
            print("  - %s: %s" % (r["name"], r["excluded"]))
    print("guard: same origin; GET only to the listed shapes; POST only to /auth/login; else refused before send")
    print("verdicts: REFUSED, LEAK, UNREACHED, EXCLUDED. exit 0 every made call REFUSED; 1 any LEAK; 2 any UNREACHED")
    print("a run needs --firm-b <id> --request-id <id> --job-id <id> (all REQUIRED: a missing one exits 2 before any "
          "request)")
    print("a run needs --go IRPT_ANLREQ.TO-RUN-FWD5.<id> and the password on stdin; --plan sends nothing")
    if control:
        print("CONTROL MODE (--control): the same routes, guard and sign-in as an identity ENTITLED to the ticket; verdicts "
              "ALLOWED, DENIED, UNREACHED, EXCLUDED (the run verdict line above does not apply); no marker scan; exit 0 "
              "ticket-read and ticket-list both ALLOWED, 1 either DENIED, 2 either UNREACHED or no session; report "
              "fwd5_control_report.json")


def _unreached_rows(routes, why):
    return [_excluded_row(r) if r.get("excluded") else
            {"route": r["name"], "method": r["method"] or "-", "status": None, "verdict": "UNREACHED",
             "body_len": 0, "reason": why, "code": ""} for r in routes]


def do_run(ns, stdin, routes, control=False):
    required = (("--base", ns.base), ("--email", ns.email), ("--ticket", ns.ticket),
                ("--firm-a", ns.firm_a), ("--firm-b", ns.firm_b), ("--request-id", ns.request_id),
                ("--job-id", ns.job_id), ("--out", ns.out))
    missing = [flag for flag, val in required if not val]
    if missing:
        print("ERROR: a run needs " + " ".join(missing))
        return 2
    problem = (base_problem(ns.base) or email_problem(ns.email)
               or ("--ticket is not an id" if not ID_RE.match(ns.ticket) else None)
               or ("--firm-a or --firm-b is not a firm id" if not (FIRM_RE.match(ns.firm_a)
                                                                    and FIRM_RE.match(ns.firm_b)) else None)
               or ("--firm-a and --firm-b must differ" if ns.firm_a == ns.firm_b else None)
               or ("--request-id is not an id" if not ID_RE.match(ns.request_id) else None)
               or ("--job-id is not an id" if not ID_RE.match(ns.job_id) else None))
    if problem:
        print("ERROR: " + problem)
        return 2
    try:
        password = read_password(stdin)
    except ValueError as err:
        print("ERROR: " + str(err))
        return 2
    base = ns.base.rstrip("/")
    opener = build_opener()
    token, why = sign_in(base, ns.email, password, opener)
    password = None
    print("%s %s principal=%s firm-a=%s firm-b=%s" % ("CONTROL" if control else "RUN", ns.go, digest(ns.email),
                                                     ns.firm_a, ns.firm_b))
    if token is None:
        rows, refused = _unreached_rows(routes, why), []
    else:
        ctx = {"ticket": ns.ticket, "firm_b": ns.firm_b, "request_id": ns.request_id, "job_id": ns.job_id}
        markers = [ns.ticket.lower(), ns.firm_b.lower()]
        rows, refused = run_calls(routes, base, opener, token, ctx, markers, control=control)
    token = None
    rc = control_exit_code(rows) if control else exit_code(rows)
    verdicts = CONTROL_VERDICTS if control else VERDICTS
    report = {
        "schema": "fwd5_run_report/1",
        "go": ns.go,
        "principal_digest": digest(ns.email),
        "firm_a": ns.firm_a,
        "firm_b": ns.firm_b,
        "sign_in": why,
        "calls": rows,
        "guard_refused": refused,
        "counts": {v: sum(1 for r in rows if r["verdict"] == v) for v in verdicts},
        "rc": rc,
    }
    name = REPORT_NAME
    if control:
        report["schema"] = CONTROL_SCHEMA
        report["mode"] = "control"
        name = CONTROL_REPORT_NAME
    os.makedirs(ns.out, exist_ok=True)
    path = os.path.join(ns.out, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    for r in rows:
        if r["verdict"] == "EXCLUDED":
            print("EXCLUDED %s: %s" % (r["route"], r["reason"]))
    if control:
        gate = {r["route"]: r["verdict"] for r in rows}
        print("FWD5-CONTROL rc=%d ticket-read=%s ticket-list=%s ALLOWED=%d DENIED=%d UNREACHED=%d EXCLUDED=%d "
              "of %d rows report=%s" % (
                  rc, gate.get("ticket-read"), gate.get("ticket-list"), report["counts"]["ALLOWED"],
                  report["counts"]["DENIED"], report["counts"]["UNREACHED"], report["counts"]["EXCLUDED"],
                  len(rows), path))
    else:
        print("FWD5-RUN rc=%d REFUSED=%d LEAK=%d UNREACHED=%d EXCLUDED=%d of %d rows report=%s" % (
            rc, report["counts"]["REFUSED"], report["counts"]["LEAK"], report["counts"]["UNREACHED"],
            report["counts"]["EXCLUDED"], len(rows), path))
    return rc


def _gate(ticket_read, ticket_list):
    """Two gate rows as control_exit_code reads them (selftest only)."""
    return [{"route": "ticket-read", "verdict": ticket_read}, {"route": "ticket-list", "verdict": ticket_list}]


def _env(ok, code, operation="x"):
    """A synthetic v1 refusal or success envelope, as the served route answers it (selftest only)."""
    status = {"operation_id": operation, "state": "REFUSED"}
    if code is not None:
        status["public_reason_code"] = code
    return json.dumps({"ok": ok, "contract_version": CONTRACT_VALUE, "operation": operation,
                       "status": status}).encode("utf-8")


def selftest():
    base = "https://h.example"
    checks = [
        ("admit GET ticket", admit("GET", base + "/api/scoped/tickets/TKT-a1b2", base), True),
        ("refuse PUT ticket", admit("PUT", base + "/api/scoped/tickets/TKT-a1b2", base), False),
        ("refuse POST meeting", admit("POST", base + "/api/scoped/tickets/TKT-a1b2/meeting", base), False),
        ("admit POST sign-in", admit("POST", base + "/auth/login", base), True),
        ("refuse GET claim path", admit("GET", base + "/api/scoped/tickets/TKT-a1b2/claim", base), False),
        ("refuse other origin", admit("GET", "https://other.example/api/scoped/tickets", base), False),
        ("classify 403 plain", classify(False, 403, b"forbidden", ["tkt-a1b2"]), "REFUSED"),
        ("classify 200 with body", classify(False, 200, b"{}", []), "LEAK"),
        ("classify empty 2xx", classify(False, 204, b"", []), "LEAK"),
        ("classify marker in 404", classify(False, 404, b"no TKT-A1B2", ["tkt-a1b2"]), "LEAK"),
        ("classify dropped call", classify(False, None, b"", []), "UNREACHED"),
        ("classify 302 not followed", classify(False, 302, b"", []), "UNREACHED"),
        ("classify list absent", classify(True, 200, b'{"tickets": []}', ["tkt-a1b2"]), "REFUSED"),
        ("exit 0 all refused", exit_code([{"verdict": "REFUSED"}]), 0),
        ("exit 1 leak", exit_code([{"verdict": "REFUSED"}, {"verdict": "LEAK"}]), 1),
        ("exit 2 unreached", exit_code([{"verdict": "UNREACHED"}]), 2),
        ("exit 0 excluded rows ignored", exit_code([{"verdict": "REFUSED"}, {"verdict": "EXCLUDED"},
                                                    {"verdict": "EXCLUDED"}]), 0),
        ("exit 1 leak beats excluded", exit_code([{"verdict": "LEAK"}, {"verdict": "EXCLUDED"}]), 1),
        ("exit 2 no made call", exit_code([{"verdict": "EXCLUDED"}]), 2),
        ("control 2xx answer allowed", control_answer(False, 200, b"", "TKT-a1b2")[0], "ALLOWED"),
        ("control marker in 2xx not a leak", control_answer(False, 200, b"TKT-a1b2", "TKT-a1b2")[0], "ALLOWED"),
        ("control list carries id allowed", control_answer(True, 200, b'{"tickets": [{"ticket_id": "tkt-a1b2"}]}',
                                                           "TKT-a1b2")[0], "ALLOWED"),
        ("control list lacks id denied", control_answer(True, 200, b'{"tickets": [{"ticket_id": "TKT-other"}]}',
                                                        "TKT-a1b2")[0], "DENIED"),
        ("control list not json denied", control_answer(True, 200, b"<html>", "TKT-a1b2")[0], "DENIED"),
        ("control 403 denied", control_answer(False, 403, b"", "TKT-a1b2")[0], "DENIED"),
        ("control 404 denied", control_answer(False, 404, b"", "TKT-a1b2")[0], "DENIED"),
        ("control 302 unreached", control_answer(False, 302, b"", "TKT-a1b2")[0], "UNREACHED"),
        ("control 500 unreached", control_answer(False, 500, b"", "TKT-a1b2")[0], "UNREACHED"),
        ("control dropped unreached", control_answer(False, None, b"", "TKT-a1b2")[0], "UNREACHED"),
        ("control exit 0 both allowed", control_exit_code(_gate("ALLOWED", "ALLOWED")), 0),
        ("control exit 0 package denied ignored", control_exit_code(_gate("ALLOWED", "ALLOWED")
                                                                    + [{"route": "form-as-filled",
                                                                        "verdict": "DENIED"}]), 0),
        ("control exit 1 ticket-read denied", control_exit_code(_gate("DENIED", "ALLOWED")), 1),
        ("control exit 1 ticket-list denied", control_exit_code(_gate("ALLOWED", "DENIED")), 1),
        ("control exit 1 denied beats unreached", control_exit_code(_gate("DENIED", "UNREACHED")), 1),
        ("control exit 2 ticket-read unreached", control_exit_code(_gate("UNREACHED", "ALLOWED")), 2),
        ("control exit 2 no session", control_exit_code(_gate("UNREACHED", "UNREACHED")), 2),
        ("envelope run ok true leaks", classify_report(200, _env(True, "READY"), [])[0], "LEAK"),
        ("envelope run FIRM_BINDING refused", classify_report(200, _env(False, "FIRM_BINDING"), [])[0], "REFUSED"),
        ("envelope run NOT_AUTHORIZED refused", classify_report(200, _env(False, "NOT_AUTHORIZED"), [])[0],
         "REFUSED"),
        ("envelope run CONTRACT_VERSION unreached", classify_report(200, _env(False, "CONTRACT_VERSION"), [])[0],
         "UNREACHED"),
        ("envelope run other code unreached", classify_report(200, _env(False, "STATE_NOT_READY"), [])[0],
         "UNREACHED"),
        ("envelope run 2xx not json unreached", classify_report(200, b"<html>", [])[0], "UNREACHED"),
        ("envelope run non-boolean ok unreached", classify_report(200, b'{"ok": "false"}', [])[0], "UNREACHED"),
        ("envelope run marker before envelope leaks", classify_report(200, _env(False, "FIRM_BINDING",
                                                                             operation="TKT-A1B2"),
                                                                     ["tkt-a1b2"])[0], "LEAK"),
        ("envelope run 403 keeps classify", classify_report(403, _env(False, "FIRM_BINDING"), [])[0], "REFUSED"),
        ("envelope control ok true allowed", control_report_answer(200, _env(True, "READY"), "TKT-a1b2")[0],
         "ALLOWED"),
        ("envelope control FIRM_BINDING denied", control_report_answer(200, _env(False, "FIRM_BINDING"),
                                                                       "TKT-a1b2")[0], "DENIED"),
        ("envelope control CONTRACT_VERSION unreached", control_report_answer(200, _env(False, "CONTRACT_VERSION"),
                                                                              "TKT-a1b2")[0], "UNREACHED"),
        ("envelope code outside closed shape is ?", envelope_of(_env(False, "lower_case"))[1], "?"),
        ("envelope code with newline is ?", envelope_of(_env(False, "FIRM_BINDING\n"))[1], "?"),
        ("served body no ok key leaks", classify_report(200, b'{"status": {"state": "READY"}}', [])[0], "LEAK"),
        ("served body no ok key is not a fence refusal", classify_report(200, b'{"items": []}', [])[0], "LEAK"),
        ("control served body no ok key allowed", control_report_answer(200, b'{"items": []}', "TKT-a1b2")[0],
         "ALLOWED"),
        ("no selection NOT_FOUND refused", classify_report(200, _env(False, "NOT_FOUND"), [],
                                                           no_selection=True)[0], "REFUSED"),
        ("no selection CONTRACT_VERSION unreached", classify_report(200, _env(False, "CONTRACT_VERSION"), [],
                                                                    no_selection=True)[0], "UNREACHED"),
        ("no selection ok true leaks", classify_report(200, _env(True, "READY"), [], no_selection=True)[0], "LEAK"),
        ("guard refuses export download", admit("GET", base + "/api/scoped/investor-reporting/export/REQ-a1b2"
                                                "/download", base), False),
        ("guard refuses bare status", admit("GET", base + "/api/scoped/investor-reporting/status", base), False),
        ("guard admits status segment", admit("GET", base + "/api/scoped/investor-reporting/status/JOB-a1b2", base),
         True),
    ]
    for name, got, want in checks:
        if got != want:
            print("FWD5-SELFTEST-FAIL %s: got %r want %r" % (name, got, want))
            return 1
    print("FWD5-SELFTEST-OK checks=%d (offline: no request, no AWS, no browser)" % len(checks))
    return 0


def main(argv=None, stdin=None, routes=None):
    p = argparse.ArgumentParser(prog="fwd5_driver.py", description="IRPT_ANLREQ FWD-5 cross-firm driver (build only)")
    p.add_argument("--plan", action="store_true")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--base")
    p.add_argument("--email")
    p.add_argument("--ticket")
    p.add_argument("--firm-a", dest="firm_a")
    p.add_argument("--firm-b", dest="firm_b",
                   help="REQUIRED for a run: the other firm's id (also a LEAK marker)")
    p.add_argument("--request-id", dest="request_id",
                   help="REQUIRED for a run: the request id, sourced from the ticket the FWD-1 run files")
    p.add_argument("--job-id", dest="job_id",
                   help="REQUIRED for a run: the job id, sourced from the ticket the FWD-1 run files")
    p.add_argument("--out")
    p.add_argument("--go")
    p.add_argument("--control", action="store_true",
                   help="the positive control (AR-tz-70): --email is an identity ENTITLED to the ticket")
    ns = p.parse_args(argv)
    if ns.selftest:
        return selftest()
    if ns.plan or not (ns.go and GO_RE.match(ns.go)):
        print_plan(control=ns.control)
        return 0
    return do_run(ns, stdin if stdin is not None else sys.stdin, routes or ROUTES, control=ns.control)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
