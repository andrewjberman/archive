"""Exit-semantics tests for fwd5_driver.py (IRPT_ANLREQ AR-tz-68, 0.9.0_WK_IRPT_ANLREQ~232).

The driver is built in the round-52 worker's folder (0.9.0_WK_IRPT_ANLREQ~231/fwd5_driver); this file imports it from
there. Every request goes to a local fake HTTP server on 127.0.0.1 and a free port, or is refused before it is sent.
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
DRIVER_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "0.9.0_WK_IRPT_ANLREQ~231", "fwd5_driver"))
if DRIVER_DIR not in sys.path:
    sys.path.insert(0, DRIVER_DIR)

import fwd5_driver as drv  # noqa: E402

GO = "IRPT_ANLREQ.TO-RUN-FWD5.exit1"
EMAIL = "fwd5-exit-principal@opal.invalid"
PASSWORD = "PLANTED-PASSWORD-exit-0123456789"
TOKEN = "PLANTED-TOKEN-exit-4c8d"
TICKET = "TKT-exit9x"
FIRM_A = "firmalpha"
FIRM_B = "firmbeta"
REQ = "REQ-exit0001"
JOB = "JOB-exit0001"
REPORT = "fwd5_run_report.json"
TICKET_PATH = "/api/scoped/tickets/" + TICKET


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
                path = self.path.split("?", 1)[0]
                fake.seen.append((self.command, path))
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


def login_or_none(method, path, body):
    """The sign-in route answers for the synthetic principal only; every other path returns None."""
    if method == "POST" and path == "/auth/login":
        data = json.loads(body.decode("utf-8") or "{}")
        if data.get("email") == EMAIL and data.get("password") == PASSWORD:
            return (200, json.dumps({"accessToken": TOKEN}).encode("utf-8"),
                    [("Content-Type", "application/json")])
        return 401, b'{"error":"bad credentials"}', [("Content-Type", "application/json")]
    return None


def all_refused():
    """Every made call answers 403 with a body that names nothing of the ticket or the other firm."""
    def answer(method, path, headers, body):
        got = login_or_none(method, path, body)
        if got is not None:
            return got
        return 403, b"forbidden", [("Content-Type", "text/plain")]
    return answer


def run_with(tmp_path, base, drop=None, password=PASSWORD):
    """A full run over the default ROUTES. drop names one flag to leave out of the argument list."""
    argv = ["--go", GO, "--base", base, "--email", EMAIL, "--ticket", TICKET, "--firm-a", FIRM_A,
            "--firm-b", FIRM_B, "--request-id", REQ, "--job-id", JOB, "--report-id", REQ, "--export-id", REQ,
            "--out", str(tmp_path / "out")]
    if drop is not None:
        i = argv.index(drop)
        del argv[i:i + 2]
    rc = drv.main(argv, stdin=io.StringIO(json.dumps({"password": password})))
    return rc, str(tmp_path / "out")


def read_report(out):
    with open(os.path.join(out, REPORT), encoding="utf-8") as fh:
        return json.load(fh)


def by_route(rep, name):
    return [c for c in rep["calls"] if c["route"] == name][0]


def test_fwd5_driver_all_made_refused_and_excluded_exits_zero(tmp_path):
    with Fake(all_refused()) as fake:
        rc, out = run_with(tmp_path, fake.base)
    rep = read_report(out)
    made = [c["verdict"] for c in rep["calls"] if c["verdict"] != "EXCLUDED"]
    assert rc == 0
    assert rep["rc"] == 0
    assert made and set(made) == {"REFUSED"}
    assert [c["verdict"] for c in rep["calls"]].count("EXCLUDED") == 2
    assert rep["counts"]["EXCLUDED"] == 2


def test_fwd5_driver_one_unreached_made_call_exits_two_with_excluded_rows(tmp_path):
    def answer(method, path, headers, body):
        got = login_or_none(method, path, body)
        if got is not None:
            return got
        if path == TICKET_PATH:
            return None  # the server drops the connection without an answer
        return 403, b"forbidden", []
    with Fake(answer) as fake:
        rc, out = run_with(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 2
    assert by_route(rep, "ticket-read")["verdict"] == "UNREACHED"
    assert rep["counts"]["EXCLUDED"] == 2
    assert "LEAK" not in {c["verdict"] for c in rep["calls"]}


def test_fwd5_driver_leak_exits_one_even_with_excluded_rows(tmp_path):
    def answer(method, path, headers, body):
        got = login_or_none(method, path, body)
        if got is not None:
            return got
        if path == TICKET_PATH:
            return 200, b'{"ticket": {"title": "synthetic"}}', [("Content-Type", "application/json")]
        return 403, b"forbidden", []
    with Fake(answer) as fake:
        rc, out = run_with(tmp_path, fake.base)
    rep = read_report(out)
    assert rc == 1
    assert by_route(rep, "ticket-read")["verdict"] == "LEAK"
    assert rep["counts"]["EXCLUDED"] == 2


@pytest.mark.parametrize("flag", ["--firm-b", "--request-id", "--job-id"])
def test_fwd5_driver_missing_id_exits_two_sends_nothing(tmp_path, flag):
    with Fake(all_refused()) as fake:
        rc, out = run_with(tmp_path, fake.base, drop=flag)
    assert rc == 2
    assert fake.seen == []
    assert not os.path.exists(os.path.join(out, REPORT))


def test_fwd5_driver_plan_lists_the_three_ids(capsys):
    rc = drv.main(["--plan"], stdin=io.StringIO("not read"))
    text = capsys.readouterr().out
    assert rc == 0
    for flag in ("--firm-b", "--request-id", "--job-id"):
        assert flag in text
    assert "REQUIRED" in text


def test_fwd5_driver_excluded_rows_never_sent(tmp_path):
    with Fake(all_refused()) as fake:
        rc, out = run_with(tmp_path, fake.base)
    assert rc == 0
    assert not [p for _m, p in fake.seen if "/meeting" in p]
    assert not [p for _m, p in fake.seen if "commentary-draft" in p]
    assert [m for m, _p in fake.seen if m == "POST"] == ["POST"]  # the sign-in is the only POST
    rep = read_report(out)
    assert by_route(rep, "meeting")["status"] is None
    assert by_route(rep, "meeting")["body_len"] == 0


def test_fwd5_driver_excluded_rows_carry_one_line_reason(tmp_path):
    with Fake(all_refused()) as fake:
        rc, out = run_with(tmp_path, fake.base)
    rep = read_report(out)
    for name in ("meeting", "commentary-draft"):
        row = by_route(rep, name)
        assert row["verdict"] == "EXCLUDED"
        assert row["reason"]
        assert "\n" not in row["reason"]


def test_fwd5_driver_no_session_exits_two_and_excluded_rows_stay_excluded(tmp_path):
    with Fake(all_refused()) as fake:
        rc, out = run_with(tmp_path, fake.base, password="not-the-password")
    rep = read_report(out)
    assert rc == 2
    assert rep["counts"]["UNREACHED"] == len(drv.ROUTES) - 2
    assert rep["counts"]["EXCLUDED"] == 2
    assert [m for m, _p in fake.seen] == ["POST"]
