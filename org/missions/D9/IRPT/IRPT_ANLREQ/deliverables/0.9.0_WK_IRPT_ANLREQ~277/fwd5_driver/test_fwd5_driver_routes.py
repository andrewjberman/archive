"""Route tests for fwd5_driver.py (IRPT_ANLREQ AR-tz-74, 0.9.0_WK_IRPT_ANLREQ~277).

The six report-side read routes on the same request and job, the call with no selected_tenant, and the served-body
and no-selection grading, run against a local fake HTTP server on 127.0.0.1 and a free port. The driver is
0.9.0_WK_IRPT_ANLREQ~231's fwd5_driver.py, imported from its own folder. Synthetic names only: no network beyond the
fake server, no AWS, no secret, no run, no mint, no deploy.
"""
import http.server
import io
import json
import os
import sys
import threading

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
DRIVER_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "0.9.0_WK_IRPT_ANLREQ~231", "fwd5_driver"))
if DRIVER_DIR not in sys.path:
    sys.path.insert(0, DRIVER_DIR)

import fwd5_driver as drv  # noqa: E402

GO = "IRPT_ANLREQ.TO-RUN-FWD5.routes1"
EMAIL = "fwd5-routes-test@opal.invalid"
PASSWORD = "PLANTED-PASSWORD-routes-0123456789"
TOKEN = "PLANTED-TOKEN-routes-6b3e"
COOKIE = "PLANTED-COOKIE-routes-2f91"
PLANTED_BODY = "PLANTED-BODY-routes-9a7c"
TICKET = "TKT-rt74x"
FIRM_A = "firmalpha"
FIRM_B = "firmbeta"
REQ = "REQ-rt0001"
JOB = "JOB-rt0001"
RUN_REPORT = "fwd5_run_report.json"
CONTROL_REPORT = "fwd5_control_report.json"
JSON_HEADERS = [("Content-Type", "application/json")]
FORBIDDEN = (403, b"forbidden", [])
SCOPED = "/api/scoped/investor-reporting"
TICKET_PATH = "/api/scoped/tickets/" + TICKET
LIST_PATH = "/api/scoped/tickets"
# The six new routes as the driver must send them: the full request target, query included.
NEW_PATHS = {
    "request-read": SCOPED + "/analysis/requests/" + REQ + "?selected_tenant=" + FIRM_B,
    "request-history": SCOPED + "/analysis/requests?selected_tenant=" + FIRM_B,
    "job-status": SCOPED + "/status/" + JOB + "?selected_tenant=" + FIRM_B,
    "narrative": SCOPED + "/narrative/" + REQ + "?selected_tenant=" + FIRM_B,
    "export-receipt": SCOPED + "/export/" + REQ + "?selected_tenant=" + FIRM_B,
    "request-read-no-selection": SCOPED + "/analysis/requests/" + REQ,
}
NEW_ROUTES = ("request-read", "request-history", "job-status", "narrative", "export-receipt",
              "request-read-no-selection")
MADE_ORDER = ("ticket-read", "ticket-list", "tickets-metrics", "form-as-filled", "original-upload", "opal-report",
              "report-pdf", "commentary-pdf") + NEW_ROUTES
ROW_KEYS = {"route", "method", "status", "verdict", "body_len", "reason", "code"}


class Fake(object):
    """A local HTTP server. answer(method, full_target, body) returns (status, payload, extra) or None to drop.
    seen keeps every request as (method, full request target), query included."""

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
                fake.seen.append((self.command, self.path))
                got = fake.answer(self.command, self.path, body)
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


def served_body(extra_text=""):
    """A 2xx JSON object with NO ok key: a served body, content for the other firm when it leaks (AR-tz-74)."""
    return json.dumps({"status": {"operation_id": "synthetic", "state": "READY"}, "items": [extra_text]}).encode("utf-8")


def table_answer(table):
    """The sign-in route answers the synthetic principal; every other target answers from table, else 403."""
    def answer(method, target, body):
        if method == "POST" and target == "/auth/login":
            data = json.loads(body.decode("utf-8") or "{}")
            if data.get("email") == EMAIL and data.get("password") == PASSWORD:
                return (200, json.dumps({"accessToken": TOKEN}).encode("utf-8"),
                        JSON_HEADERS + [("Set-Cookie", "refresh_token=%s; Path=/" % COOKIE)])
            return 401, b'{"error":"bad credentials"}', JSON_HEADERS
        return table.get(target, FORBIDDEN)
    return answer


def new_replies(reply, no_selection=None):
    """Each of the six new routes answers reply; the no-selection route answers no_selection when given."""
    table = {}
    for name, target in NEW_PATHS.items():
        if name == "request-read-no-selection" and no_selection is not None:
            table[target] = no_selection
        else:
            table[target] = reply
    return table


def open_table():
    """The ticket read and the ticket list answer 2xx, the list carries the ticket id (the control gate)."""
    return {
        TICKET_PATH: (200, b'{"ticket": {"title": "synthetic"}}', JSON_HEADERS),
        LIST_PATH: (200, json.dumps({"tickets": [{"ticket_id": TICKET}]}).encode("utf-8"), JSON_HEADERS),
    }


def drive(tmp_path, base, control=False):
    """One full run (or control) over the default ROUTES. Returns (rc, out directory)."""
    out = str(tmp_path / "out")
    argv = ["--go", GO, "--base", base, "--email", EMAIL, "--ticket", TICKET, "--firm-a", FIRM_A,
            "--firm-b", FIRM_B, "--request-id", REQ, "--job-id", JOB, "--report-id", REQ, "--export-id", REQ,
            "--out", out]
    if control:
        argv = ["--control"] + argv
    rc = drv.main(argv, stdin=io.StringIO(json.dumps({"password": PASSWORD})))
    return rc, out


def read_report(out, control=False):
    with open(os.path.join(out, CONTROL_REPORT if control else RUN_REPORT), encoding="utf-8") as fh:
        return json.load(fh)


def by_route(rep, name):
    return [c for c in rep["calls"] if c["route"] == name][0]


def test_fwd5_routes_run_makes_fourteen_calls_and_writes_sixteen_rows(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert len(rep["calls"]) == 16
    made = [c["route"] for c in rep["calls"] if c["verdict"] != "EXCLUDED"]
    assert made == list(MADE_ORDER)
    assert len(made) == 14
    assert [c["route"] for c in rep["calls"] if c["verdict"] == "EXCLUDED"] == ["commentary-draft", "meeting"]
    assert rep["counts"]["REFUSED"] == 14
    assert rep["counts"]["EXCLUDED"] == 2
    assert len([m for m, _p in fake.seen if m == "GET"]) == 14


def test_fwd5_routes_six_new_routes_send_the_path_the_record_names(tmp_path):
    with Fake(table_answer({})) as fake:
        drive(tmp_path, fake.base)
    gets = [p for m, p in fake.seen if m == "GET"]
    assert gets[8:] == [NEW_PATHS[n] for n in NEW_ROUTES]
    assert NEW_PATHS["request-history"] == SCOPED + "/analysis/requests?selected_tenant=firmbeta"
    assert NEW_PATHS["job-status"] == SCOPED + "/status/JOB-rt0001?selected_tenant=firmbeta"


def test_fwd5_routes_no_selection_call_carries_no_selected_tenant(tmp_path):
    with Fake(table_answer({})) as fake:
        drive(tmp_path, fake.base)
    target = NEW_PATHS["request-read-no-selection"]
    assert ("GET", target) in fake.seen
    assert "selected_tenant" not in target and "?" not in target
    bare = [p for m, p in fake.seen if m == "GET" and p.startswith(SCOPED) and "selected_tenant" not in p]
    assert bare == [target]


def test_fwd5_routes_guard_refuses_export_download_shape(tmp_path):
    with Fake(table_answer({})) as fake:
        opener = drv.build_opener()
        url = fake.base + SCOPED + "/export/" + REQ + "/download?selected_tenant=" + FIRM_B
        assert not drv.admit("GET", url, fake.base)
        with pytest.raises(drv.GuardRefused):
            drv.guarded_send("GET", url, fake.base, opener, {})
        assert fake.seen == []


def test_fwd5_routes_guard_refuses_bare_status_shape(tmp_path):
    with Fake(table_answer({})) as fake:
        opener = drv.build_opener()
        bare = fake.base + SCOPED + "/status"
        assert not drv.admit("GET", bare, fake.base)
        assert not drv.admit("GET", bare + "?selected_tenant=" + FIRM_B, fake.base)
        with pytest.raises(drv.GuardRefused):
            drv.guarded_send("GET", bare, fake.base, opener, {})
        assert fake.seen == []


def test_fwd5_routes_guard_admits_exactly_the_six_new_shapes(tmp_path):
    with Fake(table_answer({})) as fake:
        for target in NEW_PATHS.values():
            assert drv.admit("GET", fake.base + target, fake.base), target
        assert not drv.admit("GET", fake.base + SCOPED + "/export/" + REQ + "/download", fake.base)
        assert not drv.admit("POST", fake.base + SCOPED + "/status/" + JOB, fake.base)


def test_fwd5_routes_run_firm_binding_on_all_six_exits_zero(tmp_path):
    with Fake(table_answer(new_replies((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS)))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in NEW_ROUTES if n != "request-read-no-selection"} == {"REFUSED"}
    assert {by_route(rep, n)["code"] for n in NEW_ROUTES if n != "request-read-no-selection"} == {"FIRM_BINDING"}
    no_sel = by_route(rep, "request-read-no-selection")
    assert no_sel["verdict"] == "REFUSED"
    assert no_sel["reason"] == "no selection: refused by FIRM_BINDING in the caller's own tenant"


def test_fwd5_routes_no_selection_not_found_is_refused_in_own_tenant(tmp_path):
    table = new_replies((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS),
                        no_selection=(200, envelope(False, "NOT_FOUND"), JSON_HEADERS))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    no_sel = by_route(rep, "request-read-no-selection")
    assert rc == 0
    assert no_sel["verdict"] == "REFUSED"
    assert no_sel["code"] == "NOT_FOUND"
    assert no_sel["reason"] == "no selection: refused by NOT_FOUND in the caller's own tenant"


def test_fwd5_routes_served_body_on_each_new_route_is_leak_exit_one(tmp_path):
    for name in NEW_ROUTES:
        with Fake(table_answer({NEW_PATHS[name]: (200, served_body(), JSON_HEADERS)})) as fake:
            rc, out = drive(tmp_path / name, fake.base)
        rep = read_report(out)
        assert rc == 1, name
        assert by_route(rep, name)["verdict"] == "LEAK", name
        assert by_route(rep, name)["status"] == 200, name


def test_fwd5_routes_no_selection_contract_version_is_unreached_exit_two(tmp_path):
    table = new_replies((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS),
                        no_selection=(200, envelope(False, "CONTRACT_VERSION"), JSON_HEADERS))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    no_sel = by_route(rep, "request-read-no-selection")
    assert rc == 2
    assert no_sel["verdict"] == "UNREACHED"
    assert no_sel["reason"] == "no selection: refused by CONTRACT_VERSION, not an absence answer"
    assert "LEAK" not in {c["verdict"] for c in rep["calls"]}


def test_fwd5_routes_no_selection_ok_true_is_leak_exit_one(tmp_path):
    table = new_replies((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS),
                        no_selection=(200, envelope(True, "READY"), JSON_HEADERS))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 1
    assert by_route(rep, "request-read-no-selection")["verdict"] == "LEAK"


def test_fwd5_routes_no_selection_question_mark_code_is_unreached_exit_two(tmp_path):
    table = new_replies((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS),
                        no_selection=(200, b'{"ok": false, "status": {"state": "REFUSED"}}', JSON_HEADERS))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    no_sel = by_route(rep, "request-read-no-selection")
    assert rc == 2
    assert no_sel["verdict"] == "UNREACHED"
    assert no_sel["code"] == "?"


def test_fwd5_routes_control_served_body_is_allowed_exit_zero(tmp_path):
    table = open_table()
    table.update(new_replies((200, served_body(), JSON_HEADERS)))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0
    assert by_route(rep, "ticket-read")["verdict"] == "ALLOWED"
    assert by_route(rep, "ticket-list")["verdict"] == "ALLOWED"
    assert {by_route(rep, n)["verdict"] for n in NEW_ROUTES} == {"ALLOWED"}


def test_fwd5_routes_control_ok_true_is_allowed(tmp_path):
    table = open_table()
    table.update(new_replies((200, envelope(True, "READY"), JSON_HEADERS)))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in NEW_ROUTES} == {"ALLOWED"}
    assert {by_route(rep, n)["code"] for n in NEW_ROUTES} == {"READY"}


def test_fwd5_routes_control_not_found_is_denied_exit_stays_zero(tmp_path):
    table = open_table()
    table.update(new_replies((200, envelope(False, "NOT_FOUND"), JSON_HEADERS)))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0
    assert by_route(rep, "ticket-read")["verdict"] == "ALLOWED"
    assert by_route(rep, "ticket-list")["verdict"] == "ALLOWED"
    assert {by_route(rep, n)["verdict"] for n in NEW_ROUTES} == {"DENIED"}
    assert {by_route(rep, n)["code"] for n in NEW_ROUTES} == {"NOT_FOUND"}


def test_fwd5_routes_control_contract_version_is_unreached(tmp_path):
    table = open_table()
    table.update(new_replies((200, envelope(False, "CONTRACT_VERSION"), JSON_HEADERS)))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base, control=True)
    rep = read_report(out, control=True)
    assert rc == 0
    assert {by_route(rep, n)["verdict"] for n in NEW_ROUTES} == {"UNREACHED"}


def test_fwd5_routes_report_holds_no_body_cookie_token_or_password(tmp_path, capsys):
    table = new_replies((200, served_body(PLANTED_BODY), JSON_HEADERS))
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    with open(os.path.join(out, RUN_REPORT), encoding="utf-8") as fh:
        text = fh.read()
    console = capsys.readouterr()
    assert rc == 1
    for planted in (PASSWORD, TOKEN, COOKIE, PLANTED_BODY, EMAIL, TICKET):
        assert planted not in text
        assert planted not in console.out + console.err
    assert "PLANTED" not in text


def test_fwd5_routes_run_rows_keep_the_same_keys(tmp_path):
    with Fake(table_answer(new_replies((200, envelope(False, "FIRM_BINDING"), JSON_HEADERS)))) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert all(set(c) == ROW_KEYS for c in rep["calls"])
