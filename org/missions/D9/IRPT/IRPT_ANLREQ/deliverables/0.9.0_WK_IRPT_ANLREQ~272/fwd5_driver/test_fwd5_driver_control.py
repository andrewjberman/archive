"""Offline tests for the FWD-5 driver's positive control, --control (IRPT_ANLREQ AR-tz-70, 0.9.0_WK_IRPT_ANLREQ~272).

The driver is 0.9.0_WK_IRPT_ANLREQ~231's fwd5_driver.py, imported from its own folder. Every request goes to a local
fake HTTP server on 127.0.0.1 and a free port, or is refused before it is sent. Synthetic names only: no network beyond
the fake server, no AWS, no secret, no run, no mint, no deploy.
"""
import http.server
import io
import json
import os
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
DRIVER_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "0.9.0_WK_IRPT_ANLREQ~231", "fwd5_driver"))
if DRIVER_DIR not in sys.path:
    sys.path.insert(0, DRIVER_DIR)

import fwd5_driver as drv  # noqa: E402

GO = "IRPT_ANLREQ.TO-RUN-FWD5.control1"
EMAIL = "fwd5-entitled-test@opal.invalid"
PASSWORD = "PLANTED-PASSWORD-0123456789abcdefghij"
TOKEN = "PLANTED-TOKEN-7f3a9c"
COOKIE = "PLANTED-COOKIE-9b2e41"
PLANTED_BODY = "PLANTED-BODY-55d1"
TICKET = "TKT-zq7wx"
FIRM_A = "firmalpha"
FIRM_B = "firmbeta"
REQ = "REQ-syn0001"
JOB = "JOB-syn0001"
RUN_REPORT = "fwd5_run_report.json"
CONTROL_REPORT = "fwd5_control_report.json"
JSON_HEADERS = [("Content-Type", "application/json")]
TICKET_PATH = "/api/scoped/tickets/" + TICKET
LIST_PATH = "/api/scoped/tickets"
ATTACH_PATH = TICKET_PATH + "/attachment"
ORIG_PATH = "/api/scoped/investor-reporting/analysis/requests/" + REQ + "/original"
SECTIONS_PATH = "/api/scoped/investor-reporting/analysis/" + JOB + "/sections"
PDF_PATH = "/api/scoped/investor-reporting/analysis/requests/" + REQ + "/pdf"
COMM_PDF_PATH = "/api/scoped/investor-reporting/analysis/requests/" + REQ + "/commentary-pdf"
PACKAGE_PATHS = (ATTACH_PATH, ORIG_PATH, SECTIONS_PATH, PDF_PATH, COMM_PDF_PATH)
PACKAGE_ROUTES = ("form-as-filled", "original-upload", "opal-report", "report-pdf", "commentary-pdf")


class Fake(object):
    """A local HTTP server. answer(method, path, headers, body) returns (status, payload, extra) or None to drop."""

    def __init__(self, answer):
        self.answer = answer
        self.seen = []
        fake = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                return

            def _serve(self):
                size = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(size) if size else b""
                fake.seen.append((self.command, self.path.split("?", 1)[0]))
                got = fake.answer(self.command, self.path.split("?", 1)[0], self.headers, body)
                if got is None:
                    return
                status, payload, extra = got
                self.send_response(status)
                for k, v in extra:
                    self.send_header(k, v)
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            do_GET = _serve
            do_POST = _serve

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = "http://127.0.0.1:%d" % self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()
        return False


def login_answer(method, path, headers, body, password=PASSWORD):
    """The sign-in route: the synthetic entitled principal gets a bearer token and a refresh cookie."""
    if method == "POST" and path == "/auth/login":
        data = json.loads(body.decode("utf-8") or "{}")
        if data.get("email") == EMAIL and data.get("password") == password:
            return (200, json.dumps({"accessToken": TOKEN, "user": {"email": EMAIL}}).encode("utf-8"),
                    JSON_HEADERS + [("Set-Cookie", "refresh_token=%s; Path=/" % COOKIE)])
        return 401, b'{"error":"bad credentials"}', JSON_HEADERS
    return None


def routes_answer(table, default=(403, b"forbidden", []), password=PASSWORD):
    """table maps a request path (no query) to (status, payload, extra), or to None to drop the connection."""
    def answer(method, path, headers, body):
        got = login_answer(method, path, headers, body, password)
        if got is not None:
            return got
        return table.get(path, default)
    return answer


def allowed_table(listing=None):
    """Every ticket and package route answers 2xx; the ticket-list carries the ticket id."""
    if listing is None:
        listing = json.dumps({"tickets": [{"ticket_id": TICKET}]}).encode("utf-8")
    return {
        TICKET_PATH: (200, b'{"ticket": {"title": "synthetic"}}', JSON_HEADERS),
        LIST_PATH: (200, listing, JSON_HEADERS),
        ATTACH_PATH: (200, b"{}", JSON_HEADERS),
        ORIG_PATH: (200, b"%PDF", []),
        SECTIONS_PATH: (200, b"{}", JSON_HEADERS),
        PDF_PATH: (200, b"%PDF", []),
        COMM_PDF_PATH: (200, b"%PDF", []),
    }


def control_argv(out, base, go=GO, **omit):
    """The full --control argument list; a flag named in omit (e.g. firm_b="--firm-b") is left out."""
    pairs = [("--email", EMAIL), ("--ticket", TICKET), ("--firm-a", FIRM_A), ("--firm-b", FIRM_B),
             ("--request-id", REQ), ("--job-id", JOB)]
    argv = ["--control", "--go", go, "--base", base]
    for flag, val in pairs:
        if flag.lstrip("-").replace("-", "_") not in omit:
            argv += [flag, val]
    return argv + ["--out", out]


def run_control(tmp_path, base, stdin_text=None):
    out = str(tmp_path / "out")
    text = stdin_text if stdin_text is not None else json.dumps({"password": PASSWORD})
    rc = drv.main(control_argv(out, base), stdin=io.StringIO(text))
    return rc, out


def read_control(out):
    with open(os.path.join(out, CONTROL_REPORT), encoding="utf-8") as fh:
        return json.load(fh)


def by_route(rep, name):
    return [c for c in rep["calls"] if c["route"] == name][0]


def test_fwd5_control_all_allowed_exits_zero(tmp_path):
    table = allowed_table()
    # AR-tz-72: a report-side 2xx is read by its envelope, so the four report routes answer an ok-true envelope.
    ok_envelope = b'{"ok": true, "contract_version": "v1", "status": {"public_reason_code": "READY"}}'
    for path in (ORIG_PATH, SECTIONS_PATH, PDF_PATH, COMM_PDF_PATH):
        table[path] = (200, ok_envelope, JSON_HEADERS)
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 0
    assert rep["rc"] == 0
    assert by_route(rep, "ticket-read")["verdict"] == "ALLOWED"
    assert by_route(rep, "ticket-list")["verdict"] == "ALLOWED"
    assert {by_route(rep, name)["verdict"] for name in PACKAGE_ROUTES} == {"ALLOWED"}
    assert ("POST", TICKET_PATH + "/meeting") not in fake.seen


def test_fwd5_control_ticket_list_without_ticket_id_denied_exits_one(tmp_path):
    table = allowed_table(json.dumps({"tickets": [{"ticket_id": "TKT-other1"}]}).encode("utf-8"))
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 1
    assert by_route(rep, "ticket-list")["verdict"] == "DENIED"
    assert by_route(rep, "ticket-read")["verdict"] == "ALLOWED"


def test_fwd5_control_ticket_read_403_denied_exits_one(tmp_path):
    table = allowed_table()
    table[TICKET_PATH] = (403, b"forbidden", [])
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 1
    assert by_route(rep, "ticket-read")["verdict"] == "DENIED"
    assert by_route(rep, "ticket-read")["status"] == 403


def test_fwd5_control_ticket_read_dropped_exits_two(tmp_path):
    table = allowed_table()
    table[TICKET_PATH] = None  # the server drops the connection without an answer
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 2
    assert by_route(rep, "ticket-read")["verdict"] == "UNREACHED"
    assert by_route(rep, "ticket-read")["status"] is None
    assert by_route(rep, "ticket-list")["verdict"] == "ALLOWED"


def test_fwd5_control_package_404_reported_denied_exit_stays_zero(tmp_path):
    table = allowed_table()
    for path in PACKAGE_PATHS:
        table[path] = (404, b"not found", [])
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 0
    assert {by_route(rep, name)["verdict"] for name in PACKAGE_ROUTES} == {"DENIED"}
    assert by_route(rep, "ticket-read")["verdict"] == "ALLOWED"
    assert by_route(rep, "ticket-list")["verdict"] == "ALLOWED"


def test_fwd5_control_package_unreached_reported_exit_stays_zero(tmp_path):
    table = allowed_table()
    for path in PACKAGE_PATHS:
        table[path] = (500, b"server error", [])
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 0
    assert {by_route(rep, name)["verdict"] for name in PACKAGE_ROUTES} == {"UNREACHED"}


def test_fwd5_control_report_named_and_holds_no_body_cookie_token_password_address(tmp_path, capsys):
    table = allowed_table()
    table[TICKET_PATH] = (200, PLANTED_BODY.encode("utf-8"), JSON_HEADERS)
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    assert rc == 0
    assert os.path.isfile(os.path.join(out, CONTROL_REPORT))
    assert not os.path.exists(os.path.join(out, RUN_REPORT))
    with open(os.path.join(out, CONTROL_REPORT), encoding="utf-8") as fh:
        text = fh.read()
    assert json.loads(text)["mode"] == "control"
    console = capsys.readouterr()
    for planted in (PASSWORD, TOKEN, COOKIE, PLANTED_BODY, EMAIL, TICKET):
        assert planted not in text
        assert planted not in console.out + console.err
    assert "@" not in text
    assert "PLANTED" not in text


def test_fwd5_control_without_go_sends_nothing(tmp_path, capsys):
    out = str(tmp_path / "out")
    with Fake(routes_answer(allowed_table())) as fake:
        rc_plan = drv.main(["--control", "--plan"], stdin=io.StringIO("not read"))
        rc_short = drv.main(control_argv(out, fake.base, go="IRPT_ANLREQ.TO-RUN-FWD5"), stdin=io.StringIO("not read"))
        rc_other = drv.main(control_argv(out, fake.base, go="BAD.TO-RUN-FWD5.x"), stdin=io.StringIO("not read"))
        assert rc_plan == rc_short == rc_other == 0
        assert fake.seen == []
    assert not os.path.exists(os.path.join(out, CONTROL_REPORT))
    assert "CONTROL MODE (--control)" in capsys.readouterr().out


def test_fwd5_control_missing_firm_b_or_id_exits_two_before_any_request(tmp_path):
    out = str(tmp_path / "out")
    with Fake(routes_answer(allowed_table())) as fake:
        for omitted in ("firm_b", "request_id", "job_id", "ticket"):
            rc = drv.main(control_argv(out, fake.base, **{omitted: True}),
                          stdin=io.StringIO(json.dumps({"password": PASSWORD})))
            assert rc == 2, omitted
        assert fake.seen == []
    assert not os.path.exists(out)


def test_fwd5_control_list_carries_ticket_id_case_insensitive(tmp_path):
    listing = json.dumps({"tickets": [{"ticket_id": TICKET.lower()}]}).encode("utf-8")
    with Fake(routes_answer(allowed_table(listing))) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 0
    assert by_route(rep, "ticket-list")["verdict"] == "ALLOWED"


def test_fwd5_control_marker_in_2xx_is_allowed_not_leak(tmp_path):
    table = allowed_table()
    table[TICKET_PATH] = (200, ("ticket " + TICKET + " for " + FIRM_B).encode("utf-8"), JSON_HEADERS)
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 0
    assert by_route(rep, "ticket-read")["verdict"] == "ALLOWED"
    assert "LEAK" not in {c["verdict"] for c in rep["calls"]}


def test_fwd5_control_redirect_is_unreached_not_followed(tmp_path):
    table = allowed_table()
    table[TICKET_PATH] = (302, b"", [("Location", "/elsewhere")])
    with Fake(routes_answer(table)) as fake:
        rc, out = run_control(tmp_path, fake.base)
    rep = read_control(out)
    assert rc == 2
    assert by_route(rep, "ticket-read")["verdict"] == "UNREACHED"
    assert fake.seen.count(("GET", TICKET_PATH)) == 1


def test_fwd5_control_no_session_exits_two_no_ticket_request(tmp_path):
    with Fake(routes_answer(allowed_table(), password=PASSWORD)) as fake:
        rc, out = run_control(tmp_path, fake.base, stdin_text=json.dumps({"password": "wrong-password-0000"}))
    rep = read_control(out)
    assert rc == 2
    assert by_route(rep, "ticket-read")["verdict"] == "UNREACHED"
    assert by_route(rep, "ticket-list")["verdict"] == "UNREACHED"
    assert fake.seen == [("POST", "/auth/login")]


def test_fwd5_control_run_mode_unchanged_writes_run_report_without_mode(tmp_path):
    with Fake(routes_answer({})) as fake:
        rc = drv.main(["--go", "IRPT_ANLREQ.TO-RUN-FWD5.run1", "--base", fake.base, "--email", EMAIL,
                       "--ticket", TICKET, "--firm-a", FIRM_A, "--firm-b", FIRM_B, "--request-id", REQ,
                       "--job-id", JOB, "--out", str(tmp_path / "out")],
                      stdin=io.StringIO(json.dumps({"password": PASSWORD})))
    out = str(tmp_path / "out")
    with open(os.path.join(out, RUN_REPORT), encoding="utf-8") as fh:
        rep = json.load(fh)
    assert rc == 0
    assert "mode" not in rep
    assert rep["schema"] == "fwd5_run_report/1"
    assert not os.path.exists(os.path.join(out, CONTROL_REPORT))
