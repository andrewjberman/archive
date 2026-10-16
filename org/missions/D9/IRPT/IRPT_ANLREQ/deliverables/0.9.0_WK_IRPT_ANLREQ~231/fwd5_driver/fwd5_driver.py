#!/usr/bin/env python3
"""IRPT_ANLREQ FWD-5 cross-firm driver (0.9.0_WK_IRPT_ANLREQ~231, AR-tz-67). BUILD ONLY: this file is not run here.

It signs in as the scoped second-firm principal (POST /auth/login, JSON {email, password}; the bearer access token
is held in memory only) and, for ONE ticket of ANOTHER firm, makes each call the record lists. Every call is expected
to be REFUSED: a 401, 403 or 404 whose body carries nothing of the ticket. The run is a later WORLD act by the applier
under a pair, after 2.0.0_SA_COO~V2's release.

  --plan                      prints the plan and exits 0; no network, no stdin.
  --selftest                  offline checks of the guard and the verdicts; exits 0 when they hold.
  --base URL --email ADDR --ticket ID --firm-a ID --firm-b ID --out DIR --go IRPT_ANLREQ.TO-RUN-FWD5.<id>
                              [--request-id ID] [--job-id ID]
                              the run. Without a --go matching ^IRPT_ANLREQ\\.TO-RUN-FWD5\\.\\S+$ it prints the plan
                              and exits 0 with no request sent. The password is read from stdin as one JSON object
                              {"password": "..."}; it is never printed, logged or written.

Verdicts (a closed set): REFUSED, LEAK, UNREACHED.
  any 2xx on a ticket or package route           -> LEAK (a 2xx is never a refusal, an empty body included)
  a 2xx ticket-list whose JSON carries a tickets list and no marker -> REFUSED (the other firm's ticket is absent)
  any answer whose body carries a marker (the ticket id or the other firm's id, case-insensitive) -> LEAK
  401, 403 or 404 with no marker                  -> REFUSED
  anything else: 3xx, 400, 405, 5xx, a dropped connection, a call the guard refused, a route with no
  GET shape in the record, a missing request or job id                -> UNREACHED (not a pass)
Exit: 0 every call REFUSED; 1 any LEAK; 2 any UNREACHED, or a run with bad arguments or no session.
The report (fwd5_run_report.json in --out) holds, per call, the route name, the status, the verdict and the body
length only. It never holds a body, a cookie, a token, a password or an address (the principal is a digest).
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
TIMEOUT_S = 30
VERDICTS = ("REFUSED", "LEAK", "UNREACHED")
SEG = r"[A-Za-z0-9_-]+"

# The guard: GET only to these path shapes (the ticket routes and the package-file routes the record lists),
# POST only to the sign-in route. Matched on the path, after the origin is checked. The query is not matched.
GET_ALLOWED = (
    re.compile(r"/api/scoped/tickets"),
    re.compile(r"/api/scoped/tickets/" + SEG),
    re.compile(r"/api/scoped/tickets/" + SEG + r"/attachment"),
    re.compile(r"/api/scoped/investor-reporting/analysis/requests/" + SEG + r"/(?:original|pdf|commentary-pdf)"),
    re.compile(r"/api/scoped/investor-reporting/analysis/" + SEG + r"/sections"),
)
POST_ALLOWED = (re.compile(r"/auth/login"),)

# The calls, in order. method None = the record names no GET route for it (UNREAD; never sent).
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
     "plan": "UNREAD: no GET route for the draft is in the record; POST commentary-draft is outside the guard"},
    {"name": "commentary-pdf", "method": "GET",
     "template": "/api/scoped/investor-reporting/analysis/requests/{request_id}/commentary-pdf?selected_tenant={firm_b}",
     "needs": ("request_id", "firm_b"), "list": False, "plan": "the commentary PDF"},
    {"name": "meeting", "method": "POST", "template": "/api/scoped/tickets/{ticket}/meeting",
     "needs": ("ticket",), "list": False,
     "plan": "a POST to a ticket route: the guard refuses it before send, so the call is UNREACHED"},
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


def exit_code(rows):
    verdicts = [r["verdict"] for r in rows]
    if "LEAK" in verdicts:
        return 1
    if not verdicts or "UNREACHED" in verdicts:
        return 2
    return 0


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


def run_calls(routes, base, opener, token, ctx, markers):
    """Every route, in order. Returns (rows, guard-refused route names). A row never holds a body."""
    rows = []
    refused = []
    for r in routes:
        row = {"route": r["name"], "method": r["method"] or "-", "status": None,
               "verdict": "UNREACHED", "body_len": 0, "reason": ""}
        missing = [k for k in r["needs"] if not ctx.get(k)]
        if r["method"] is None:
            row["reason"] = "UNREAD: no GET route for it in the record"
        elif missing:
            row["reason"] = "no value supplied for " + ", ".join(missing)
        else:
            url = base + r["template"].format(**ctx)
            headers = {"Accept": "application/json", "Authorization": "Bearer " + token}
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


def print_plan(routes=ROUTES):
    print("FWD5 DRIVER PLAN (build only; the run is a WORLD act under a pair after 2.0.0_SA_COO~V2's release)")
    print("sign-in: POST /auth/login, JSON {email, password}; bearer access token and refresh cookie held in memory")
    for i, r in enumerate(routes, 1):
        print("  %d. %-17s %-4s %s  -- %s" % (i, r["name"], r["method"] or "--", r["template"] or "(no route)",
                                             r["plan"]))
    print("guard: same origin; GET only to the five listed shapes; POST only to /auth/login; else refused before send")
    print("verdicts: REFUSED, LEAK, UNREACHED. exit 0 every call REFUSED; 1 any LEAK; 2 any UNREACHED")
    print("a run needs --go IRPT_ANLREQ.TO-RUN-FWD5.<id> and the password on stdin; --plan sends nothing")


def _unreached_rows(routes, why):
    return [{"route": r["name"], "method": r["method"] or "-", "status": None, "verdict": "UNREACHED",
             "body_len": 0, "reason": why} for r in routes]


def do_run(ns, stdin, routes):
    required = (("--base", ns.base), ("--email", ns.email), ("--ticket", ns.ticket),
                ("--firm-a", ns.firm_a), ("--firm-b", ns.firm_b), ("--out", ns.out))
    missing = [flag for flag, val in required if not val]
    if missing:
        print("ERROR: a run needs " + " ".join(missing))
        return 2
    problem = (base_problem(ns.base) or email_problem(ns.email)
               or ("--ticket is not an id" if not ID_RE.match(ns.ticket) else None)
               or ("--firm-a or --firm-b is not a firm id" if not (FIRM_RE.match(ns.firm_a)
                                                                    and FIRM_RE.match(ns.firm_b)) else None)
               or ("--firm-a and --firm-b must differ" if ns.firm_a == ns.firm_b else None)
               or ("--request-id is not an id" if ns.request_id and not ID_RE.match(ns.request_id) else None)
               or ("--job-id is not an id" if ns.job_id and not ID_RE.match(ns.job_id) else None))
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
    print("RUN %s principal=%s firm-a=%s firm-b=%s" % (ns.go, digest(ns.email), ns.firm_a, ns.firm_b))
    if token is None:
        rows, refused = _unreached_rows(routes, why), []
    else:
        ctx = {"ticket": ns.ticket, "firm_b": ns.firm_b, "request_id": ns.request_id, "job_id": ns.job_id}
        markers = [ns.ticket.lower(), ns.firm_b.lower()]
        rows, refused = run_calls(routes, base, opener, token, ctx, markers)
    token = None
    rc = exit_code(rows)
    report = {
        "schema": "fwd5_run_report/1",
        "go": ns.go,
        "principal_digest": digest(ns.email),
        "firm_a": ns.firm_a,
        "firm_b": ns.firm_b,
        "sign_in": why,
        "calls": rows,
        "guard_refused": refused,
        "counts": {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS},
        "rc": rc,
    }
    os.makedirs(ns.out, exist_ok=True)
    path = os.path.join(ns.out, REPORT_NAME)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("FWD5-RUN rc=%d REFUSED=%d LEAK=%d UNREACHED=%d of %d calls report=%s" % (
        rc, report["counts"]["REFUSED"], report["counts"]["LEAK"], report["counts"]["UNREACHED"], len(rows), path))
    return rc


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
    p.add_argument("--firm-b", dest="firm_b")
    p.add_argument("--request-id", dest="request_id")
    p.add_argument("--job-id", dest="job_id")
    p.add_argument("--out")
    p.add_argument("--go")
    ns = p.parse_args(argv)
    if ns.selftest:
        return selftest()
    if ns.plan or not (ns.go and GO_RE.match(ns.go)):
        print_plan()
        return 0
    return do_run(ns, stdin if stdin is not None else sys.stdin, routes or ROUTES)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
