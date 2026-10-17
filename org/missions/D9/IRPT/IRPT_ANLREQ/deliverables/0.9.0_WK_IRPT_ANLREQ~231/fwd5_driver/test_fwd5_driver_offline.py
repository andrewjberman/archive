"""Offline tests for fwd5_driver.py (IRPT_ANLREQ AR-tz-67, 0.9.0_WK_IRPT_ANLREQ~231).

Every request goes to a local fake HTTP server on 127.0.0.1 and a free port, or is refused before it is sent.
Synthetic names only: no network beyond the fake server, no AWS, no secret, no browser.
"""
import http.server
import io
import json
import os
import sys
import threading

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import fwd5_driver as drv  # noqa: E402

GO = "IRPT_ANLREQ.TO-RUN-FWD5.offline1"
EMAIL = "fwd5-principal-test@opal.invalid"
PASSWORD = "PLANTED-PASSWORD-0123456789abcdefghij"
TOKEN = "PLANTED-TOKEN-7f3a9c"
COOKIE = "PLANTED-COOKIE-9b2e41"
PLANTED_BODY = "PLANTED-BODY-55d1"
TICKET = "TKT-zq7wx"
FIRM_A = "firmalpha"
FIRM_B = "firmbeta"
REQ = "REQ-syn0001"
JOB = "JOB-syn0001"
REPORT = "fwd5_run_report.json"
SHORT_ROUTES = [r for r in drv.ROUTES if r["name"] not in ("meeting", "commentary-draft")]


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
                fake.seen.append((self.command, self.path))
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
            do_PUT = _serve
            do_DELETE = _serve

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


def login_answer(method, path, headers, body):
    """The sign-in route: the synthetic principal gets a bearer token and a refresh cookie; nothing else answers."""
    if method == "POST" and path == "/auth/login":
        data = json.loads(body.decode("utf-8") or "{}")
        if data.get("email") == EMAIL and data.get("password") == PASSWORD:
            return (200, json.dumps({"accessToken": TOKEN, "user": {"email": EMAIL}}).encode("utf-8"),
                    [("Content-Type", "application/json"), ("Set-Cookie", "refresh_token=%s; Path=/" % COOKIE)])
        return 401, b'{"error":"bad credentials"}', [("Content-Type", "application/json")]
    return None


def refusing(status=403, payload=b"forbidden"):
    def answer(method, path, headers, body):
        got = login_answer(method, path, headers, body)
        if got is not None:
            return got
        return status, payload, [("Content-Type", "text/plain")]
    return answer


def run_main(tmp_path, base, routes=None, stdin_text=None, extra=()):
    out = str(tmp_path / "out")
    argv = ["--go", GO, "--base", base, "--email", EMAIL, "--ticket", TICKET, "--firm-a", FIRM_A,
            "--firm-b", FIRM_B, "--request-id", REQ, "--job-id", JOB, "--report-id", REQ, "--export-id", REQ,
            "--out", out] + list(extra)
    text = stdin_text if stdin_text is not None else json.dumps({"password": PASSWORD})
    rc = drv.main(argv, stdin=io.StringIO(text), routes=routes)
    return rc, out


def read_report(out):
    with open(os.path.join(out, REPORT), encoding="utf-8") as fh:
        return json.load(fh)


def by_route(rep, name):
    return [c for c in rep["calls"] if c["route"] == name][0]


def test_fwd5_driver_all_refused_exits_zero_report_only_refused(tmp_path):
    with Fake(refusing(403)) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    rep = read_report(out)
    assert rc == 0
    assert {c["verdict"] for c in rep["calls"]} == {"REFUSED"}
    assert len(rep["calls"]) == len(SHORT_ROUTES)


def test_fwd5_driver_one_200_with_body_exits_one_leak(tmp_path):
    def answer(method, path, headers, body):
        got = login_answer(method, path, headers, body)
        if got is not None:
            return got
        if path == "/api/scoped/tickets/" + TICKET:
            return 200, b'{"ticket": {"title": "synthetic"}}', [("Content-Type", "application/json")]
        return 403, b"forbidden", []
    with Fake(answer) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    rep = read_report(out)
    assert rc == 1
    assert by_route(rep, "ticket-read")["verdict"] == "LEAK"


def test_fwd5_driver_dropped_call_exits_two_unreached(tmp_path):
    def answer(method, path, headers, body):
        got = login_answer(method, path, headers, body)
        if got is not None:
            return got
        if path == "/api/scoped/tickets/" + TICKET:
            return None  # the server drops the connection without an answer
        return 403, b"forbidden", []
    with Fake(answer) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    rep = read_report(out)
    assert rc == 2
    assert by_route(rep, "ticket-read")["verdict"] == "UNREACHED"
    assert by_route(rep, "ticket-read")["status"] is None
    assert "LEAK" not in {c["verdict"] for c in rep["calls"]}


def test_fwd5_driver_refused_body_naming_other_firm_is_leak(tmp_path):
    with Fake(refusing(403, ("no access to " + FIRM_B).encode("utf-8"))) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    rep = read_report(out)
    assert rc == 1
    assert "LEAK" in {c["verdict"] for c in rep["calls"]}


def test_fwd5_driver_empty_2xx_is_not_refused(tmp_path):
    def answer(method, path, headers, body):
        got = login_answer(method, path, headers, body)
        if got is not None:
            return got
        return 204, b"", []
    with Fake(answer) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    rep = read_report(out)
    assert rc == 1
    assert by_route(rep, "ticket-read")["verdict"] == "LEAK"
    assert by_route(rep, "ticket-list")["verdict"] == "LEAK"


def test_fwd5_driver_list_absent_ticket_is_refused_present_is_leak(tmp_path):
    def listing(payload):
        def answer(method, path, headers, body):
            got = login_answer(method, path, headers, body)
            if got is not None:
                return got
            if path == "/api/scoped/tickets":
                return 200, payload, [("Content-Type", "application/json")]
            return 403, b"forbidden", []
        return answer
    with Fake(listing(b'{"tickets": [{"ticket_id": "TKT-other1"}]}')) as fake:
        rc_absent, out_absent = run_main(tmp_path / "a", fake.base, routes=SHORT_ROUTES)
    with Fake(listing(json.dumps({"tickets": [{"ticket_id": TICKET}]}).encode("utf-8"))) as fake:
        rc_present, out_present = run_main(tmp_path / "b", fake.base, routes=SHORT_ROUTES)
    assert by_route(read_report(out_absent), "ticket-list")["verdict"] == "REFUSED"
    assert rc_absent == 0
    assert by_route(read_report(out_present), "ticket-list")["verdict"] == "LEAK"
    assert rc_present == 1


def test_fwd5_driver_guard_refuses_put_and_post_to_ticket_route(tmp_path):
    with Fake(refusing(403)) as fake:
        opener = drv.build_opener()
        url = fake.base + "/api/scoped/tickets/" + TICKET
        for method, target in (("PUT", url), ("DELETE", url), ("POST", url), ("POST", url + "/meeting")):
            with pytest.raises(drv.GuardRefused):
                drv.guarded_send(method, target, fake.base, opener, {})
        assert fake.seen == []


def test_fwd5_driver_guard_refuses_other_host_and_unlisted_get(tmp_path):
    with Fake(refusing(403)) as fake:
        opener = drv.build_opener()
        assert not drv.admit("GET", "http://127.0.0.1:1/api/scoped/tickets", fake.base)
        assert not drv.admit("GET", fake.base + "/api/scoped/tickets/" + TICKET + "/claim", fake.base)
        assert not drv.admit("POST", fake.base + "/auth/refresh", fake.base)
        with pytest.raises(drv.GuardRefused):
            drv.guarded_send("GET", "http://example.invalid/api/scoped/tickets", fake.base, opener, {})
        assert fake.seen == []


def test_fwd5_driver_meeting_route_excluded_exits_zero(tmp_path):
    with Fake(refusing(403)) as fake:
        rc, out = run_main(tmp_path, fake.base)
    rep = read_report(out)
    meeting = by_route(rep, "meeting")
    assert rc == 0
    assert meeting["verdict"] == "EXCLUDED"
    assert meeting["reason"]
    assert by_route(rep, "commentary-draft")["verdict"] == "EXCLUDED"
    assert ("POST", "/api/scoped/tickets/" + TICKET + "/meeting") not in fake.seen
    assert rep["guard_refused"] == []


def test_fwd5_driver_report_holds_no_body_cookie_token_or_password(tmp_path, capsys):
    with Fake(refusing(403, PLANTED_BODY.encode("utf-8"))) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    with open(os.path.join(out, REPORT), encoding="utf-8") as fh:
        text = fh.read()
    console = capsys.readouterr()
    for planted in (PASSWORD, TOKEN, COOKIE, PLANTED_BODY, EMAIL, TICKET):
        assert planted not in text
        assert planted not in console.out + console.err
    assert "PLANTED" not in text


def test_fwd5_driver_plan_and_unmatched_go_send_nothing(tmp_path):
    with Fake(refusing(403)) as fake:
        rc_plan = drv.main(["--plan"], stdin=io.StringIO("not read"))
        rc_short = drv.main(["--go", "IRPT_ANLREQ.TO-RUN-FWD5", "--base", fake.base, "--email", EMAIL,
                             "--ticket", TICKET, "--firm-a", FIRM_A, "--firm-b", FIRM_B, "--out", str(tmp_path)],
                            stdin=io.StringIO("not read"))
        rc_other = drv.main(["--go", "BAD.TO-RUN-FWD5.x", "--base", fake.base, "--email", EMAIL,
                             "--ticket", TICKET, "--firm-a", FIRM_A, "--firm-b", FIRM_B, "--out", str(tmp_path)],
                            stdin=io.StringIO("not read"))
        assert rc_plan == rc_short == rc_other == 0
        assert fake.seen == []


def test_fwd5_driver_stdin_password_never_in_stdout(tmp_path, capsys):
    with Fake(refusing(403)) as fake:
        rc, out = run_main(tmp_path, fake.base, routes=SHORT_ROUTES)
    console = capsys.readouterr()
    assert rc == 0
    assert PASSWORD not in console.out and PASSWORD not in console.err
    assert TOKEN not in console.out and "Bearer" not in console.out


def test_fwd5_driver_selftest_runs_offline(monkeypatch, capsys):
    def no_network(*args, **kwargs):
        raise AssertionError("the selftest made a request")
    monkeypatch.setattr(drv, "send_raw", no_network)
    assert drv.selftest() == 0
    assert "FWD5-SELFTEST-OK" in capsys.readouterr().out
