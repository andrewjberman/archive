"""Real-id and ticket-metrics tests for fwd5_driver.py (IRPT_ANLREQ AR-tz-76, 0.9.0_WK_IRPT_ANLREQ~279).

The narrative route takes the report id from --report-id and the export-receipt route takes the export id from
--export-id (never the request id), and the run drives GET /api/scoped/tickets/metrics. Every request goes to a local
fake HTTP server on 127.0.0.1 and a free port, or is refused before it is sent. The driver is
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

GO = "IRPT_ANLREQ.TO-RUN-FWD5.real1"
EMAIL = "fwd5-real-ids-test@opal.invalid"
PASSWORD = "PLANTED-PASSWORD-real-ids-0123456789"
TOKEN = "PLANTED-TOKEN-real-ids-3d6a"
COOKIE = "PLANTED-COOKIE-real-ids-8e04"
PLANTED_BODY = "PLANTED-BODY-real-ids-b52f"
TICKET = "TKT-rl76x"
FIRM_A = "firmalpha"
FIRM_B = "firmbeta"
REQ = "REQ-rl0001"
JOB = "JOB-rl0001"
RPT = "RPT-rl0001"
EXP = "EXP-rl0001"
SCOPED = "/api/scoped/investor-reporting"
METRICS_PATH = "/api/scoped/tickets/metrics"
TICKET_PATH = "/api/scoped/tickets/" + TICKET
LIST_PATH = "/api/scoped/tickets"
NARRATIVE_TARGET = SCOPED + "/narrative/" + RPT + "?selected_tenant=" + FIRM_B
EXPORT_TARGET = SCOPED + "/export/" + EXP + "?selected_tenant=" + FIRM_B
RUN_REPORT = "fwd5_run_report.json"
CONTROL_REPORT = "fwd5_control_report.json"
JSON_HEADERS = [("Content-Type", "application/json")]
FORBIDDEN = (403, b"forbidden", [])
MADE_ORDER = ("ticket-read", "ticket-list", "tickets-metrics", "form-as-filled", "original-upload", "opal-report",
              "report-pdf", "commentary-pdf", "request-read", "request-history", "job-status", "narrative",
              "export-receipt", "request-read-no-selection")
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


def open_table(metrics=None):
    """The ticket read and the ticket list answer 2xx and the list carries the ticket id (the control gate)."""
    table = {
        TICKET_PATH: (200, b'{"ticket": {"title": "synthetic"}}', JSON_HEADERS),
        LIST_PATH: (200, json.dumps({"tickets": [{"ticket_id": TICKET}]}).encode("utf-8"), JSON_HEADERS),
    }
    if metrics is not None:
        table[METRICS_PATH] = metrics
    return table


def drive(tmp_path, base, control=False, report_id=RPT, export_id=EXP):
    """One full run (or control) over the default ROUTES. A None id is left out of the argument list."""
    out = str(tmp_path / "out")
    argv = ["--go", GO, "--base", base, "--email", EMAIL, "--ticket", TICKET, "--firm-a", FIRM_A,
            "--firm-b", FIRM_B, "--request-id", REQ, "--job-id", JOB]
    if report_id is not None:
        argv += ["--report-id", report_id]
    if export_id is not None:
        argv += ["--export-id", export_id]
    argv += ["--out", out]
    if control:
        argv = ["--control"] + argv
    rc = drv.main(argv, stdin=io.StringIO(json.dumps({"password": PASSWORD})))
    return rc, out


def read_report(out, control=False):
    with open(os.path.join(out, CONTROL_REPORT if control else RUN_REPORT), encoding="utf-8") as fh:
        return json.load(fh)


def by_route(rep, name):
    return [c for c in rep["calls"] if c["route"] == name][0]


def test_fwd5_real_run_makes_fourteen_calls_and_writes_sixteen_rows(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    made = [c["route"] for c in rep["calls"] if c["verdict"] != "EXCLUDED"]
    assert rc == 0
    assert len(rep["calls"]) == 16
    assert made == list(MADE_ORDER)
    assert len(made) == 14
    assert rep["counts"]["EXCLUDED"] == 2
    assert rep["counts"]["REFUSED"] == 14
    assert len([m for m, _t in fake.seen if m == "GET"]) == 14


def test_fwd5_real_narrative_sends_the_report_id_value_not_the_request_id(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert ("GET", NARRATIVE_TARGET) in fake.seen
    assert not [t for m, t in fake.seen if m == "GET" and "/narrative/" + REQ in t]
    assert by_route(rep, "narrative")["status"] == 403
    assert by_route(rep, "narrative")["verdict"] == "REFUSED"


def test_fwd5_real_export_receipt_sends_the_export_id_value_not_the_request_id(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert ("GET", EXPORT_TARGET) in fake.seen
    assert not [t for m, t in fake.seen if m == "GET" and "/export/" + REQ in t]
    assert by_route(rep, "export-receipt")["status"] == 403
    assert by_route(rep, "export-receipt")["verdict"] == "REFUSED"


def test_fwd5_real_run_without_report_id_leaves_narrative_unreached_exits_two(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base, report_id=None)
    rep = read_report(out)
    row = by_route(rep, "narrative")
    assert rc == 2
    assert row["verdict"] == "UNREACHED"
    assert row["reason"] == "no value supplied for report_id"
    assert row["status"] is None
    assert not [t for _m, t in fake.seen if "/narrative/" in t]


def test_fwd5_real_run_without_export_id_leaves_export_receipt_unreached_exits_two(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base, export_id=None)
    rep = read_report(out)
    row = by_route(rep, "export-receipt")
    assert rc == 2
    assert row["verdict"] == "UNREACHED"
    assert row["reason"] == "no value supplied for export_id"
    assert row["status"] is None
    assert not [t for _m, t in fake.seen if "/export/" in t]


def test_fwd5_real_tickets_metrics_sends_bare_path_with_no_selected_tenant(tmp_path):
    with Fake(table_answer({})) as fake:
        drive(tmp_path, fake.base)
    assert ("GET", METRICS_PATH) in fake.seen
    assert [t for m, t in fake.seen if m == "GET" and "metrics" in t] == [METRICS_PATH]
    assert "selected_tenant" not in METRICS_PATH and "?" not in METRICS_PATH


def test_fwd5_real_tickets_metrics_route_sits_right_after_ticket_list(tmp_path):
    names = [r["name"] for r in drv.ROUTES]
    route = drv.ROUTES[names.index("tickets-metrics")]
    assert names.index("tickets-metrics") == names.index("ticket-list") + 1
    assert route["method"] == "GET"
    assert route["template"] == METRICS_PATH
    assert route["needs"] == ()


def test_fwd5_real_tickets_metrics_403_is_refused_and_run_exits_zero(tmp_path):
    with Fake(table_answer({"/api/scoped/tickets/metrics": FORBIDDEN})) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 0
    assert by_route(rep, "tickets-metrics")["verdict"] == "REFUSED"
    assert by_route(rep, "tickets-metrics")["status"] == 403


def test_fwd5_real_tickets_metrics_200_is_leak_and_run_exits_one(tmp_path):
    table = {METRICS_PATH: (200, b'{"open": 3}', JSON_HEADERS)}
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 1
    assert by_route(rep, "tickets-metrics")["verdict"] == "LEAK"
    assert by_route(rep, "tickets-metrics")["status"] == 200


def test_fwd5_real_control_tickets_metrics_200_allowed_and_403_denied(tmp_path):
    table = open_table(metrics=(200, b'{"open": 3}', JSON_HEADERS))
    with Fake(table_answer(table)) as fake:
        rc_allowed, out_allowed = drive(tmp_path / "a", fake.base, control=True)
    table = open_table(metrics=FORBIDDEN)
    with Fake(table_answer(table)) as fake:
        rc_denied, out_denied = drive(tmp_path / "b", fake.base, control=True)
    allowed = by_route(read_control(out_allowed), "tickets-metrics")
    denied = by_route(read_control(out_denied), "tickets-metrics")
    assert rc_allowed == 0 and rc_denied == 0
    assert allowed["verdict"] == "ALLOWED"
    assert denied["verdict"] == "DENIED"
    assert denied["status"] == 403


def test_fwd5_real_guard_admits_only_the_exact_metrics_path(tmp_path):
    with Fake(table_answer({})) as fake:
        assert drv.admit("GET", fake.base + METRICS_PATH, fake.base)
        assert not drv.admit("GET", fake.base + METRICS_PATH + "/", fake.base)
        assert not drv.admit("POST", fake.base + METRICS_PATH, fake.base)
        assert fake.seen == []


def test_fwd5_real_guard_refuses_metrics_extra_segment_and_claim(tmp_path):
    with Fake(table_answer({})) as fake:
        opener = drv.build_opener()
        for path in (METRICS_PATH + "/anything", "/api/scoped/tickets/claim"):
            url = fake.base + path
            assert not drv.admit("GET", url, fake.base), path
            with pytest.raises(drv.GuardRefused):
                drv.guarded_send("GET", url, fake.base, opener, {})
        assert fake.seen == []


def test_fwd5_real_report_holds_no_body_cookie_token_or_password(tmp_path, capsys):
    table = {METRICS_PATH: (200, PLANTED_BODY.encode("utf-8"), JSON_HEADERS)}
    with Fake(table_answer(table)) as fake:
        rc, out = drive(tmp_path, fake.base)
    with open(os.path.join(out, RUN_REPORT), encoding="utf-8") as fh:
        text = fh.read()
    console = capsys.readouterr()
    rep = json.loads(text)
    assert rc == 1
    assert all(set(c) == ROW_KEYS for c in rep["calls"])
    for planted in (PASSWORD, TOKEN, COOKIE, PLANTED_BODY, EMAIL):
        assert planted not in text
        assert planted not in console.out + console.err
    assert "PLANTED" not in text


def test_fwd5_real_malformed_report_id_exits_two_and_sends_nothing(tmp_path):
    with Fake(table_answer({})) as fake:
        rc, out = drive(tmp_path, fake.base, report_id="bad/id")
    assert rc == 2
    assert fake.seen == []
    assert not os.path.exists(os.path.join(out, RUN_REPORT))


def test_fwd5_real_selftest_holds_with_the_added_checks(monkeypatch, capsys):
    def no_network(*args, **kwargs):
        raise AssertionError("the selftest made a request")
    monkeypatch.setattr(drv, "send_raw", no_network)
    assert drv.selftest() == 0
    assert "FWD5-SELFTEST-OK" in capsys.readouterr().out


def read_control(out):
    with open(os.path.join(out, CONTROL_REPORT), encoding="utf-8") as fh:
        return json.load(fh)
