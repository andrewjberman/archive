"""Envelope-grading tests for fwd5_driver.py (IRPT_ANLREQ AR-tz-72, 0.9.0_WK_IRPT_ANLREQ~275).

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

GO = "IRPT_ANLREQ.TO-RUN-FWD5.envelope1"
EMAIL = "fwd5-envelope-test@opal.invalid"
PASSWORD = "PLANTED-PASSWORD-envelope-0123456789"
TOKEN = "PLANTED-TOKEN-envelope-5e1a"
COOKIE = "PLANTED-COOKIE-envelope-7d20"
PLANTED_BODY = "PLANTED-BODY-envelope-c4f9"
TICKET = "TKT-env72x"
FIRM_A = "firmalpha"
FIRM_B = "firmbeta"
REQ = "REQ-env0001"
JOB = "JOB-env0001"
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
REPORT_PATHS = (ORIG_PATH, SECTIONS_PATH, PDF_PATH, COMM_PDF_PATH)
REPORT_ROUTES = ("original-upload", "opal-report", "report-pdf", "commentary-pdf")
OPEN_TICKET = (200, b'{"ticket": {"title": "synthetic"}}', JSON_HEADERS)
OPEN_LIST = (200, json.dumps({"tickets": [{"ticket_id": TICKET}]}).encode("utf-8"), JSON_HEADERS)


class Fake(object):
    """A local HTTP server. answer(method, path, headers, body) returns (status, payload, extra) or None to drop.
    headers_seen keeps, per request, the method, the path and the X-Contract-Version value the request carried."""

    def __init__(self, answer):
        self.answer = answer
        self.seen = []
        self.headers_seen = []
        fake = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                return

            def _serve(self):
                size = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(size) if size else b""
                path = self.path.split("?", 1)[0]
                fake.seen.append((self.command, path))
                fake.headers_seen.append((self.command, path, self.headers.get(drv.CONTRACT_HEADER)))
                got = fake.answer(self.command, path, self.headers, body)
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


def envelope(ok, code=None, operation="synthetic"):
    """A v1 envelope as the served route answers it: ok, the contract version, the status with the reason code."""
    status = {"operation_id": operation, "state": "READY" if ok else "REFUSED"}
    if code is not None:
        status["public_reason_code"] = code
    return json.dumps({"ok": ok, "contract_version": "v1", "operation": operation, "status": status}).encode("utf-8")


def login_answer(method, path, body):
    """The sign-in route answers for the synthetic principal only; every other path returns None."""
    if method == "POST" and path == "/auth/login":
        data = json.loads(body.decode("utf-8") or "{}")
        if data.get("email") == EMAIL and data.get("password") == PASSWORD:
            return 200, json.dumps({"accessToken": TOKEN}).encode("utf-8"), JSON_HEADERS
        return 401, b'{"error":"bad credentials"}', JSON_HEADERS
    return None


def answers(report_reply, ticket_reply=(403, b"forbidden", []), listing=None):
    """Every report-side route answers report_reply; the ticket list answers listing when given; every other ticket
    route answers ticket_reply (a 403 by default: a refusal that says nothing of the ticket)."""
    def answer(method, path, headers, body):
        got = login_answer(method, path, body)
        if got is not None:
            return got
        if path in REPORT_PATHS:
            return report_reply
        if path == LIST_PATH and listing is not None:
            return listing
        return ticket_reply
    return answer


def drive(tmp_path, base, control=False):
    """One full run (or control) over the default ROUTES. Returns (rc, out directory)."""
    out = str(tmp_path / "out")
    argv = ["--go", GO, "--base", base, "--email", EMAIL, "--ticket", TICKET, "--firm-a", FIRM_A,
            "--firm-b", FIRM_B, "--request-id", REQ, "--job-id", JOB, "--out", out]
    if control:
        argv = ["--control"] + argv
    rc = drv.main(argv, stdin=io.StringIO(json.dumps({"password": PASSWORD})))
    return rc, out


def read_report(out, control=False):
    name = CONTROL_REPORT if control else RUN_REPORT
    with open(os.path.join(out, name), encoding="utf-8") as fh:
        return json.load(fh)


def by_route(rep, name):
    return [c for c in rep["calls"] if c["route"] == name][0]


def test_fwd5_envelope_every_get_carries_contract_version_run(tmp_path):
    with Fake(answers((200, envelope(True, "READY"), JSON_HEADERS))) as fake:
        drive(tmp_path, fake.base)
    gets = [v for m, _p, v in fake.headers_seen if m == "GET"]
    assert len(gets) == 13  # ticket-read, ticket-list, form-as-filled, the ten report-side routes (AR-tz-74)
    assert set(gets) == {"v1"}
    assert [v for m, _p, v in fake.headers_seen if m == "POST"] == [None]  # the sign-in POST is unchanged


def test_fwd5_envelope_every_get_carries_contract_version_control(tmp_path):
    with Fake(answers((200, envelope(True, "READY"), JSON_HEADERS), OPEN_TICKET, OPEN_LIST)) as fake:
        rc, _out = drive(tmp_path, fake.base, control=True)
    gets = [v for m, _p, v in fake.headers_seen if m == "GET"]
    assert rc == 0
    assert len(gets) == 13  # the same thirteen GETs as the run (AR-tz-74)
    assert set(gets) == {"v1"}


def test_fwd5_envelope_run_ok_true_report_is_leak_exit_one(tmp_path):
    with Fake(answers((200, envelope(True, "READY"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 1
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"LEAK"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"READY"}


def test_fwd5_envelope_run_firm_binding_is_refused(tmp_path):
    with Fake(answers((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"REFUSED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"FIRM_BINDING"}


def test_fwd5_envelope_run_not_authorized_is_refused(tmp_path):
    with Fake(answers((200, envelope(False, "NOT_AUTHORIZED"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"REFUSED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"NOT_AUTHORIZED"}


def test_fwd5_envelope_run_contract_version_is_unreached_exit_two(tmp_path):
    with Fake(answers((200, envelope(False, "CONTRACT_VERSION"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 2
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"UNREACHED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"CONTRACT_VERSION"}
    for name in REPORT_ROUTES:
        assert "not by the firm fence" in by_route(rep, name)["reason"]


def test_fwd5_envelope_run_other_code_is_unreached(tmp_path):
    with Fake(answers((200, envelope(False, "STATE_NOT_READY"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 2
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"UNREACHED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"STATE_NOT_READY"}


def test_fwd5_envelope_run_2xx_not_json_is_unreached(tmp_path):
    with Fake(answers((200, b"<html>ok</html>", [("Content-Type", "text/html")]))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 2
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"UNREACHED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"?"}


def test_fwd5_envelope_run_non_boolean_ok_is_unreached(tmp_path):
    body = b'{"ok": "false", "status": {"public_reason_code": "FIRM_BINDING"}}'
    with Fake(answers((200, body, JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 2
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"UNREACHED"}
    assert "LEAK" not in {c["verdict"] for c in rep["calls"]}


def test_fwd5_envelope_control_ok_true_is_allowed(tmp_path):
    with Fake(answers((200, envelope(True, "READY"), JSON_HEADERS), OPEN_TICKET, OPEN_LIST)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"ALLOWED"}


def test_fwd5_envelope_control_firm_binding_is_denied(tmp_path):
    with Fake(answers((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS), OPEN_TICKET, OPEN_LIST)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0  # the report-side routes are reported and do not change the control exit
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"DENIED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"FIRM_BINDING"}


def test_fwd5_envelope_control_contract_version_is_unreached(tmp_path):
    with Fake(answers((200, envelope(False, "CONTRACT_VERSION"), JSON_HEADERS), OPEN_TICKET, OPEN_LIST)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"UNREACHED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"CONTRACT_VERSION"}


def test_fwd5_envelope_ticket_route_200_still_leak_in_run(tmp_path):
    with Fake(answers((200, envelope(False, "CONTRACT_VERSION"), JSON_HEADERS), OPEN_TICKET)) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 1
    assert by_route(rep, "ticket-read")["verdict"] == "LEAK"
    assert by_route(rep, "ticket-read")["code"] == ""


def test_fwd5_envelope_marker_in_report_2xx_is_leak_before_envelope(tmp_path):
    body = envelope(False, "FIRM_BINDING", operation=TICKET)
    with Fake(answers((200, body, JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 1
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"LEAK"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {""}  # a marker LEAK is not graded by the envelope


def test_fwd5_envelope_report_non_2xx_keeps_grading_with_empty_code(tmp_path):
    with Fake(answers((403, envelope(False, "CONTRACT_VERSION"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in REPORT_ROUTES} == {"REFUSED"}
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {""}


def test_fwd5_envelope_reason_code_outside_closed_shape_reads_as_question_mark(tmp_path):
    with Fake(answers((200, envelope(False, "lower_case"), JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 2
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"?"}


def test_fwd5_envelope_report_rows_carry_code_and_no_body(tmp_path, capsys):
    body = envelope(False, "NOT_AUTHORIZED", operation=PLANTED_BODY)
    with Fake(answers((200, body, JSON_HEADERS))) as fake:
        rc, out = drive(tmp_path, fake.base)
    with open(os.path.join(out, RUN_REPORT), encoding="utf-8") as fh:
        text = fh.read()
    rep = json.loads(text)
    assert rc == 0
    assert all("code" in c for c in rep["calls"])
    assert {by_route(rep, n)["code"] for n in REPORT_ROUTES} == {"NOT_AUTHORIZED"}
    assert by_route(rep, "ticket-read")["code"] == ""
    assert by_route(rep, "meeting")["code"] == ""
    console = capsys.readouterr()
    for planted in (PASSWORD, TOKEN, COOKIE, PLANTED_BODY, EMAIL, TICKET):
        assert planted not in text
        assert planted not in console.out + console.err
    assert "PLANTED" not in text
