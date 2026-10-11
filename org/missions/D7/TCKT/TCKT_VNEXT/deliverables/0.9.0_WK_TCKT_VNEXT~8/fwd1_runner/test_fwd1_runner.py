"""Tests for fwd1_run.py (cell R2-rn-1). A fake HTTP layer returns canned, synthetic responses: no network, no AWS,
no client data. Run from the worktree root:  python -m pytest -q <this file>
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fwd1_run as run  # noqa: E402

REQ_A = "REQ-" + "a" * 24
REQ_B = "REQ-" + "b" * 24
REQ_C = "REQ-" + "c" * 24
REQ_OLD = "REQ-" + "0" * 24
FILE_SHA = hashlib.sha256(b"synthetic").hexdigest()
SENT = "sar1b-" + FILE_SHA[:24]
TKT = "TCKT-SYN-0001"
LIST_PATH = "/api/scoped/investor-reporting/analysis/requests"


def res(status, parsed, ctype="application/json"):
    raw = json.dumps(parsed) if parsed is not None else "not json"
    return {"status": status, "reason": run.reason_of(parsed) if parsed is not None else raw[:120],
            "len": len(raw), "fp": hashlib.sha256(raw.encode()).hexdigest()[:16], "parsed": parsed,
            "content_type": ctype}


def listing(*ids, cursor=None):
    return res(200, {"data": {"items": [{"identity": {"request_id": i}, "accepted_at": 1} for i in ids],
                              "next_cursor": cursor}})


def report(rid=REQ_A, sections=2):
    """The finished-report answer (operation analysis-report): ids and synthetic section stubs only."""
    return res(200, {"contract_version": "v1", "operation": "analysis-report", "data": {
        "request_ref": {"request_id": rid, "request_revision": 1},
        "sections": [{"section_id": "syn-%d" % i} for i in range(sections)]}})


def refusal(code):
    """A refusal envelope as served.refuse() builds it: HTTP 200, ok false, status.public_reason_code."""
    return res(200, {"ok": False, "contract_version": "v1", "operation": "analysis-report",
                     "status": {"public_reason_code": code}})


def rpath(rid):
    return "/api/scoped/investor-reporting/analysis/%s/sections" % rid


class Fake:
    """Scripted HTTP layer. `script` maps (method, path) to a response, or a list consumed one per call (the last
    one repeats). Every request is recorded in order."""

    def __init__(self, script):
        self.script, self.calls = script, []

    def __call__(self, token, method, path, query=None, body=None, timeout=90):
        self.calls.append((method, path, dict(query or {}), body))
        r = self.script.get((method, path))
        if r is None:
            return res(404, {"code": "NO_SUCH_FAKE_ROUTE"})
        if isinstance(r, list):
            r = r.pop(0) if len(r) > 1 else r[0]
        return r

    def paths(self, method=None):
        return [c[1] for c in self.calls if method is None or c[0] == method]


@pytest.fixture
def sleeps(monkeypatch):
    out = []
    monkeypatch.setattr(run, "SLEEP", out.append)
    monkeypatch.setattr(run, "save", lambda trace: None)
    return out


def install(monkeypatch, script):
    fake = Fake(script)
    monkeypatch.setattr(run, "call", fake)
    return fake


def trace_hops():
    names = ["a_upload", "b_ticket", "c_claim", "d_analysis", "e_ready", "f_report", "g_open"]
    return {n: {"hop": n} for n in names}, []


SUBMIT = ("POST", "/api/scoped/investor-reporting/analysis")
# AMENDMENT 2 / D5: the deployed report route refuses a malformed id, typed
ARM_REFUSED = res(400, {"error": "request_id must be REQ- followed by exactly 24 lower-case hex digits",
                        "code": "INVALID_REPORT_REQUEST_ID"})
REPORT_PATH = "/api/scoped/tickets/%s/report" % TKT


def ticket_with(rid):
    return res(200, {"ticket": {"ticket_id": TKT, "report_ref": {"request_id": rid}}})


# ------------------------------------------------------------------ import

def test_import_makes_no_aws_client():
    code = ("import sys; sys.modules['boto3'] = None; sys.modules['jwt'] = None; sys.path.insert(0, %r); "
            "import fwd1_run; assert fwd1_run._CLIENTS == {}; print('IMPORT-CLEAN')" % str(HERE))
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0 and "IMPORT-CLEAN" in r.stdout, r.stderr


# ------------------------------------------------------------------ AC1: the request id is the service's

def test_polls_id_from_submit_answer(monkeypatch, sleeps):
    fake = install(monkeypatch, {("GET", LIST_PATH): listing(REQ_OLD),
                                 SUBMIT: res(200, {"data": {"request_id": REQ_A}})})
    hops, named = trace_hops()
    rid = run.hop_d_analysis("tok", TKT, "in-1", FILE_SHA, hops["d_analysis"], named)
    assert rid == REQ_A and hops["d_analysis"]["request_id"] == REQ_A
    assert hops["d_analysis"]["request_id_source"] == "submission_answer"
    assert hops["d_analysis"]["idempotency_token"] == SENT
    assert named == []
    # an answer with the id needs no list after the submission: the only list read came BEFORE the POST
    order = [c[0] + " " + c[1] for c in fake.calls]
    assert order == ["GET " + LIST_PATH, "POST " + SUBMIT[1]]


def test_falls_back_to_request_list_when_answer_has_no_id(monkeypatch, sleeps):
    fake = install(monkeypatch, {
        ("GET", LIST_PATH): [listing(REQ_OLD), listing(REQ_B, REQ_OLD)],
        SUBMIT: res(200, {"data": {"accepted": True}})})
    hops, named = trace_hops()
    rid = run.hop_d_analysis("tok", TKT, "in-1", FILE_SHA, hops["d_analysis"], named)
    assert rid == REQ_B and hops["d_analysis"]["request_id"] == REQ_B
    assert hops["d_analysis"]["request_id_source"] == "request_list"
    assert hops["d_analysis"]["candidates"] == 1
    assert named == []
    lists = [c for c in fake.calls if c[0] == "GET" and c[1] == LIST_PATH]
    assert all(c[2].get("selected_tenant") == run.FIRM for c in lists)


def test_a_non_req_id_in_the_answer_is_not_used(monkeypatch, sleeps):
    install(monkeypatch, {("GET", LIST_PATH): [listing(), listing(REQ_B)],
                          SUBMIT: res(200, {"data": {"request_id": SENT}})})
    hops, named = trace_hops()
    rid = run.hop_d_analysis("tok", TKT, "in-1", FILE_SHA, hops["d_analysis"], named)
    assert rid == REQ_B and hops["d_analysis"]["request_id"] != SENT


def test_never_polls_the_sent_token(monkeypatch, sleeps):
    """The whole d..g flow, with an answer that echoes the sent token as request_id: the token appears in the
    submit body only, in no request path, query or body afterwards, and never as a recorded request_id."""
    fake = install(monkeypatch, {
        ("GET", LIST_PATH): [listing(REQ_OLD), listing(REQ_C, REQ_OLD)],
        SUBMIT: res(200, {"data": {"request_id": SENT}}),
        ("GET", rpath(REQ_C)): [refusal("NOT_FOUND"), report(REQ_C)],
        ("POST", "/api/scoped/tickets/%s/report" % TKT): [ARM_REFUSED, res(200, {"ticket": {"ticket_id": TKT}})],
        ("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_C)})
    hops, named = trace_hops()
    trace = {"hops": list(hops.values()), "named_failures": named}
    run.hops_d_to_g("tok", trace, hops, named, TKT, "in-1", FILE_SHA)
    submit_at = next(i for i, c in enumerate(fake.calls) if (c[0], c[1]) == SUBMIT)
    after = fake.calls[submit_at + 1:]
    assert after, "nothing was read after the submission"
    for method, path, query, body in after:
        blob = path + json.dumps(query) + json.dumps(body)
        assert SENT not in blob, (method, path)
    d = hops["d_analysis"]
    assert d["request_id"] == REQ_C and d["idempotency_token"] == SENT
    assert SENT not in json.dumps({k: v for k, v in hops.items() if k != "d_analysis"})
    assert named == []


def test_ambiguous_request_list_is_a_named_failure(monkeypatch, sleeps):
    fake = install(monkeypatch, {
        ("GET", LIST_PATH): [listing(REQ_OLD), listing(REQ_A, REQ_B, REQ_OLD)],
        SUBMIT: res(200, {"data": {}})})
    hops, named = trace_hops()
    assert run.hop_d_analysis("tok", TKT, "in-1", FILE_SHA, hops["d_analysis"], named) is None
    assert hops["d_analysis"]["request_id"] is None and hops["d_analysis"]["candidates"] == 2
    assert named[-1]["hop"] == "d_analysis" and named[-1]["reason"] == "REQUEST_ID_UNRESOLVED"
    assert named[-1]["candidates"] == 2
    # zero candidates is the same named failure
    fake.script[("GET", LIST_PATH)] = [listing(REQ_OLD)]
    hops, named = trace_hops()
    assert run.hop_d_analysis("tok", TKT, "in-1", FILE_SHA, hops["d_analysis"], named) is None
    assert named[-1]["reason"] == "REQUEST_ID_UNRESOLVED" and named[-1]["candidates"] == 0
    # and a failed request, hence no ids, never lets e..g run
    hops, named = trace_hops()
    run.hops_d_to_g("tok", {"hops": []}, hops, named, TKT, "in-1", FILE_SHA)
    assert hops["e_ready"]["outcome"] == "UNREACHABLE" and hops["g_open"]["outcome"] == "UNREACHABLE"


# ------------------------------------------------------------------ AC2: hop (e) reads the finished report

def test_reads_stage_field_until_generated(monkeypatch, sleeps):
    """(name kept) Amendment 1: no `stage` is read. The not-ready code is polled until the report is read."""
    fake = install(monkeypatch, {("GET", rpath(REQ_A)): [
        refusal("NOT_FOUND"), refusal("NOT_READY"), refusal("NOT_FOUND"), refusal("NOT_FOUND"), report(REQ_A)]})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "OK"
    assert hops["e_ready"]["polls"] == 5 and hops["e_ready"]["report"]["sections"] == 2
    assert "stage" not in hops["e_ready"] and "state" not in hops["e_ready"]
    assert sleeps == [run.POLL_SECONDS] * 4
    assert named == []
    assert set(fake.paths("GET")) == {rpath(REQ_A)}


def test_failed_stage_is_recorded_not_retried(monkeypatch, sleeps):
    """(name kept) A terminal answer ends hop (e) at once, is recorded with its code, and (f) and (g) are UNREACHABLE."""
    fake = install(monkeypatch, {
        ("GET", LIST_PATH): [listing(), listing(REQ_A)],
        SUBMIT: res(200, {"data": {"request_id": REQ_A}}),
        ("GET", rpath(REQ_A)): refusal("UNEXPECTED")})
    hops, named = trace_hops()
    trace = {"hops": list(hops.values()), "named_failures": named}
    run.hops_d_to_g("tok", trace, hops, named, TKT, "in-1", FILE_SHA)
    e = hops["e_ready"]
    assert e["polls"] == 1 and e["reason"] == "UNEXPECTED" and e["refused"] is True
    assert sleeps == []
    assert hops["f_report"]["outcome"] == "UNREACHABLE" and hops["g_open"]["outcome"] == "UNREACHABLE"
    assert not any(p.endswith("/report") for p in fake.paths("POST"))
    assert [n["reason"] for n in named] == ["UNEXPECTED", "UNREACHABLE", "UNREACHABLE"]
    # a non-200 is terminal of the same kind, even when its body carries a not-ready code
    fake = install(monkeypatch, {("GET", rpath(REQ_A)): res(404, {"status": {"public_reason_code": "NOT_FOUND"}})})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
    assert hops["e_ready"]["polls"] == 1 and hops["e_ready"]["status"] == 404 and len(fake.calls) == 1


def test_poll_budget_is_bounded(monkeypatch, sleeps):
    fake = install(monkeypatch, {("GET", rpath(REQ_A)): refusal("NOT_FOUND")})
    assert run.MAX_POLLS == 40 and run.POLL_MAX == 40 and run.POLL_SECONDS == 30
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "NOT_READY"
    assert len(fake.calls) == 40 and hops["e_ready"]["polls"] == 40
    assert sleeps == [30] * 39
    assert named[-1]["reason"] == "NOT_READY"


def test_refusal_envelope_is_not_a_read(monkeypatch, sleeps):
    ok_data = {"request_ref": {"request_id": REQ_A}, "sections": [{"section_id": "syn-0"}]}
    for body in ({"status": {"public_reason_code": "INVALID_REQUEST_ID"}},
                 {"code": "INVALID_REQUEST_ID", "data": ok_data}):
        fake = install(monkeypatch, {("GET", rpath(REQ_A)): res(200, body)})
        hops, named = trace_hops()
        assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
        e = hops["e_ready"]
        assert e["status"] == 200 and e["refused"] is True and e["reason"] == "INVALID_REQUEST_ID"
        assert e["polls"] == 1 and len(fake.calls) == 1 and sleeps == []
        assert named[-1]["hop"] == "e_ready" and named[-1]["reason"] == "INVALID_REQUEST_ID"


def test_missing_stage_is_a_named_failure_not_a_pass(monkeypatch, sleeps):
    """(name kept) A 200 that is not the report asked for -- no sections, or another request's id -- is a named
    failure, never a pass and never polled."""
    for data in ({"request_ref": {"request_id": REQ_A}, "sections": []},
                 {"request_ref": {"request_id": REQ_A}},
                 {"request_ref": {"request_id": REQ_B}, "sections": [{"section_id": "syn-0"}]},
                 {"sections": [{"section_id": "syn-0"}]}):
        install(monkeypatch, {("GET", rpath(REQ_A)): res(200, {"data": data})})
        hops, named = trace_hops()
        assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
        assert named[-1]["reason"] == "REPORT_BODY_NOT_THE_REPORT" and hops["e_ready"]["polls"] == 1


# ------------------------------------------------------------------ AC4: Amendment 1 -- the finished-report read

def _code_only(path):
    """The module source with comments and docstrings removed (tokenize), so a source check reads code, not prose."""
    import io
    import tokenize
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(Path(path).read_text(encoding="utf-8")).readline):
        if tok.type == tokenize.COMMENT:
            continue
        if tok.type == tokenize.STRING and tok.string.startswith(('"""', "'" * 3)):
            continue
        out.append(tok.string)
    return " ".join(out)


def test_hop_e_reads_the_report_route_never_stage(monkeypatch, sleeps):
    """Hop (e) calls operation analysis-report with selected_tenant, never the request read or the pdf route, and a
    `stage` field in the answer is not read: a body that carries stage=GENERATED but no report is not a pass."""
    fake = install(monkeypatch, {("GET", rpath(REQ_A)): report(REQ_A, 3)})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "OK"
    assert fake.calls == [("GET", rpath(REQ_A), {"selected_tenant": run.FIRM}, None)]
    e = hops["e_ready"]
    assert e["route"] == "analysis-report" and e["polls"] == 1 and named == []
    assert e["report"]["request_id_matches"] is True and e["report"]["sections"] == 3
    assert "stage" not in json.dumps(e)
    # a request-read body (carries `stage`, no report) is NOT a pass
    install(monkeypatch, {("GET", rpath(REQ_A)): res(200, {"data": {
        "identity": {"request_id": REQ_A}, "accepted_at": 1, "stage": "GENERATED"}})})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
    assert named[-1]["reason"] == "REPORT_BODY_NOT_THE_REPORT"
    # the module's code (comments and docstrings removed) reads no stage and calls no pdf route
    code = _code_only(run.__file__)
    assert '"stage"' not in code and "STAGE" not in code and "/pdf" not in code and "stage" not in code


def test_not_ready_code_is_polled_within_the_bound(monkeypatch, sleeps):
    assert run.NOT_READY_CODES == frozenset({"NOT_FOUND", "NOT_READY"})
    assert isinstance(run.NOT_READY_CODES, frozenset)
    # each code in the set is polled, and a success on the last poll (40th) still counts: inside the bound
    fake = install(monkeypatch, {("GET", rpath(REQ_A)): [refusal("NOT_FOUND")] * 20 + [refusal("NOT_READY")] * 19
                                 + [report(REQ_A)]})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "OK"
    assert hops["e_ready"]["polls"] == 40 and len(fake.calls) == 40
    assert sleeps == [run.POLL_SECONDS] * 39 and named == []


def test_bound_reached_is_not_ready_never_a_pass(monkeypatch, sleeps):
    fake = install(monkeypatch, {
        ("GET", LIST_PATH): [listing(), listing(REQ_A)],
        SUBMIT: res(200, {"data": {"request_id": REQ_A}}),
        ("GET", rpath(REQ_A)): refusal("NOT_FOUND")})
    hops, named = trace_hops()
    trace = {"hops": list(hops.values()), "named_failures": named}
    run.hops_d_to_g("tok", trace, hops, named, TKT, "in-1", FILE_SHA)
    e = hops["e_ready"]
    assert e["outcome"] == "NOT_READY" and e["result"] == {"result": "NOT_READY", "last_code": "NOT_FOUND", "polls": 40}
    assert e["polls"] == 40 and sleeps == [run.POLL_SECONDS] * 39
    assert e.get("report_opened") is not True and "refused" not in e
    assert hops["f_report"]["outcome"] == "UNREACHABLE" and hops["g_open"]["outcome"] == "UNREACHABLE"
    assert not any(p.endswith("/report") for p in fake.paths("POST"))
    assert [n["reason"] for n in named] == ["NOT_READY", "UNREACHABLE", "UNREACHABLE"]


def test_other_refusal_code_is_terminal(monkeypatch, sleeps):
    for code in ("NOT_AUTHORIZED", "INVALID_INPUT", "UNEXPECTED", "FIRM_BINDING", "DEPENDENCY_UNAVAILABLE",
                 "INVALID_REQUEST_ID", "RATE_LIMITED"):
        assert code not in run.NOT_READY_CODES
        fake = install(monkeypatch, {("GET", rpath(REQ_A)): refusal(code)})
        hops, named = trace_hops()
        assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
        e = hops["e_ready"]
        assert e["polls"] == 1 and e["reason"] == code and len(fake.calls) == 1 and sleeps == []
        assert named[-1]["reason"] == code
    # a transport failure (status 0) is terminal too
    install(monkeypatch, {("GET", rpath(REQ_A)): {"status": 0, "reason": "TRANSPORT_X", "len": 0, "fp": None,
                                                  "parsed": None}})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED" and hops["e_ready"]["polls"] == 1


def test_hop_g_reads_the_report_for_the_ticket_request_id(monkeypatch, sleeps):
    """The id in memory is REQ_A; the ticket's report_ref names REQ_B. The report GET must use REQ_B, and the record
    carries status, echoed id, section count, byte length and a sha256 prefix -- no section text."""
    ans = report(REQ_B, 4)
    fake = install(monkeypatch, {("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_B),
                                 ("GET", rpath(REQ_B)): ans})
    hops, named = trace_hops()
    assert run.hop_g_open("tok", TKT, hops["g_open"], named) is True
    gets = [c[1] for c in fake.calls if c[1].endswith("/sections")]
    assert gets == [rpath(REQ_B)] and REQ_A not in " ".join(c[1] for c in fake.calls)
    g = hops["g_open"]
    assert g["report_ref_request_id"] == REQ_B and g["report_opened"] is True
    assert g["report"] == {"status": 200, "len": ans["len"], "sha256_prefix": ans["fp"],
                           "request_id_echoed": REQ_B, "request_id_matches": True, "sections": 4}
    assert "syn-" not in json.dumps(g) and named == []
    # an unmet read is not an open: a refusal, or another request's report
    for answer in (refusal("NOT_FOUND"), report(REQ_A, 1)):
        install(monkeypatch, {("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_B),
                              ("GET", rpath(REQ_B)): answer})
        hops, named = trace_hops()
        assert run.hop_g_open("tok", TKT, hops["g_open"], named) is False
        assert hops["g_open"]["report_opened"] is False and named


# ------------------------------------------------------------------ AC3: the ticket carries a REQ id

def test_records_req_id_on_ticket(monkeypatch, sleeps):
    fake = install(monkeypatch, {("POST", "/api/scoped/tickets/%s/report" % TKT): res(200, {"ticket": {}})})
    hops, named = trace_hops()
    assert run.hop_f_report("tok", TKT, REQ_A, hops["f_report"], named) is True
    posts = [c for c in fake.calls if c[0] == "POST"]
    assert len(posts) == 1 and posts[0][3] == {"request_id": REQ_A}
    assert hops["f_report"]["request_id"] == REQ_A and named == []


def test_opens_report_from_ticket_report_ref(monkeypatch, sleeps):
    """The id in memory is REQ_A; the ticket's report_ref names REQ_B. The finished-report GET must use REQ_B."""
    ans = report(REQ_B, 2)
    fake = install(monkeypatch, {
        ("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_B),
        ("GET", rpath(REQ_B)): ans})
    hops, named = trace_hops()
    assert run.hop_g_open("tok", TKT, hops["g_open"], named) is True
    report_gets = [c[1] for c in fake.calls if c[1].endswith("/sections")]
    assert report_gets == [rpath(REQ_B)]
    assert not any(c[1].endswith("/pdf") for c in fake.calls)
    assert REQ_A not in " ".join(c[1] for c in fake.calls)
    g = hops["g_open"]
    assert g["report_ref_request_id"] == REQ_B and g["report_opened"] is True
    assert g["report"]["request_id_echoed"] == REQ_B and g["report"]["sections"] == 2
    assert g["report"]["len"] == ans["len"] and g["report"]["sha256_prefix"] == ans["fp"]
    assert "pdf" not in g and named == []


def test_never_records_a_non_req_id(monkeypatch, sleeps):
    fake = install(monkeypatch, {})
    for bad in (SENT, "REQ-short", "req-" + "a" * 24, REQ_A + "\n", None, ""):
        hops, named = trace_hops()
        assert run.hop_f_report("tok", TKT, bad, hops["f_report"], named) is False
        assert named[-1]["reason"] == "NOT_A_REQ_ID" and "request_id" not in hops["f_report"]
    assert fake.calls == []   # nothing was sent
    # a ticket whose report_ref is not a REQ id opens nothing
    fake = install(monkeypatch, {("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(SENT)})
    hops, named = trace_hops()
    assert run.hop_g_open("tok", TKT, hops["g_open"], named) is False
    assert named[-1]["reason"] == "REPORT_REF_NOT_A_REQ_ID"
    assert not any(c[1].endswith("/sections") or c[1].endswith("/pdf") for c in fake.calls)


# ------------------------------------------------------------------ AMENDMENT 2: the world fake
# One ordered event log across the HTTP layer, DynamoDB, the other AWS clients and a clock the tests own. No real
# AWS, no network, no sleeping: SLEEP advances the fake clock.

import types  # noqa: E402

ARGV = ["--read27", "R27", "--exp-minutes", "5", "--expect-irpt-status-sha", "Zm9v",
        "--run-label", "R2-test-1", "--pair", "org/pair/path@abc123", "--executor", "0.9.0_WK_TEST~1",
        "--trace-out", "UNUSED_NO_SUCH_DIR/trace_test.json"]
LIVE_SHA = "Zm9vYmFyLIVE"
ACTIVE_MS = 4_000_000_000_000   # a last-event time later than any iat the tests use
STATUS_PATH = "/api/scoped/investor-reporting/status"
FILER_EMAIL = run.FILER


class FakeDdb:
    def __init__(self, world):
        self.w = world

    def put_item(self, **kw):
        self.w.events.append(("ddb", "put", self.w.t))
        if self.w.put_raises:
            raise RuntimeError("ConditionalCheckFailedException")
        self.w.row = True

    def get_item(self, **kw):
        self.w.events.append(("ddb", "get", self.w.t))
        if self.w.first_get_empty:
            self.w.first_get_empty = False
            return {}
        return {"Item": {"PK": {"S": "x"}, "allowedFirmIds": {"L": []}}} if self.w.row else {}

    def delete_item(self, **kw):
        self.w.events.append(("ddb", "delete", self.w.t))
        self.w.row = False


class World:
    def __init__(self, monkeypatch, sha=LIVE_SHA):
        self.t, self.events, self.sha = 1_800_000_000.0, [], sha
        self.row, self.put_raises, self.first_get_empty = False, False, False
        self.lambda_raises, self.mint_raises, self.sleep_raises = False, False, None
        self.claims = []
        self.log_resp = {}
        self.stream_resp = {}    # per log group: one describe_log_streams page, or a list of pages
        self.log_calls = []      # (api, kwargs) for every logs call, in order
        self.mp = monkeypatch
        monkeypatch.setattr(run, "NOW", lambda: self.t)
        monkeypatch.setattr(run, "SLEEP", self.sleep)
        monkeypatch.setattr(run, "save", lambda trace: None)
        monkeypatch.setattr(run, "ddb", FakeDdb(self))
        monkeypatch.setattr(run, "_client", self.client)
        monkeypatch.setattr(run, "resolve_advisor", lambda opaque, firm: "adv@example.invalid")
        monkeypatch.setitem(sys.modules, "jwt", types.SimpleNamespace(encode=self.encode))

    def sleep(self, s):
        if self.sleep_raises:
            raise self.sleep_raises
        self.events.append(("sleep", s, self.t))
        self.t += s

    def encode(self, claims, key, algorithm=None):
        self.claims.append(dict(claims))
        return "tok"

    def client(self, name):
        w = self

        def lam(**kw):
            w.events.append(("aws", "lambda", w.t))
            if w.lambda_raises:
                raise RuntimeError("AccessDenied")
            return {"CodeSha256": w.sha}

        def secret(**kw):
            w.events.append(("aws", "secret", w.t))
            if w.mint_raises:
                raise RuntimeError("secret unreadable")
            return {"SecretString": "pem"}

        def streams(**kw):
            w.events.append(("aws", "streams:" + kw["logGroupName"], w.t))
            w.log_calls.append(("describe_log_streams", dict(kw)))
            r = w.stream_resp.get(kw["logGroupName"], {"logStreams": [{"logStreamName": "s", "lastEventTimestamp": ACTIVE_MS}]})
            if isinstance(r, Exception):
                raise r
            return r.pop(0) if isinstance(r, list) else r

        def logs(**kw):
            w.events.append(("aws", "logs:" + kw["logGroupName"], w.t))
            w.log_calls.append(("filter_log_events", dict(kw)))
            default = ({"events": []} if kw["logGroupName"] == run.DATA_REFRESH_LOG_GROUP
                       else {"events": [{"message": "x"}]})
            r = w.log_resp.get(kw["logGroupName"], default)
            if isinstance(r, Exception):
                raise r
            return r.pop(0) if isinstance(r, list) else r

        return {"lambda": types.SimpleNamespace(get_function_configuration=lam),
                "secretsmanager": types.SimpleNamespace(get_secret_value=secret),
                "logs": types.SimpleNamespace(filter_log_events=logs, describe_log_streams=streams)}[name]

    def http(self, script):
        fake = Fake(script)

        def call(token, method, path, query=None, body=None, timeout=90):
            self.events.append(("http", method, path, self.t))
            return fake(token, method, path, query, body, timeout)

        self.mp.setattr(run, "call", call)
        return fake

    def ddb_ops(self):
        return [(e[1], e[2]) for e in self.events if e[0] == "ddb"]

    def index(self, pred):
        return [i for i, e in enumerate(self.events) if pred(e)]


def drive(monkeypatch, argv=ARGV, world=None, script=None, census_result=None, hops_fn=None):
    """Run main() against the world fake. -> (rc, trace, world). `trace` is the dict main last saved."""
    w = world or World(monkeypatch)
    w.http(script if script is not None else {("GET", STATUS_PATH): res(200, {"data": {}})})
    captured = {}
    monkeypatch.setattr(run, "save", lambda trace: captured.__setitem__("t", trace))
    monkeypatch.setattr(run, "census", lambda token, run_id: census_result or ({"tickets_created_by_the_census": []}, None))
    if hops_fn is not None:
        monkeypatch.setattr(run, "hops", hops_fn)
    try:
        rc = run.main(list(argv))
    finally:
        w.trace = captured.get("t")
    return rc, captured.get("t"), w


def assert_row_deleted_after_exp(w, minutes=5):
    ops = w.ddb_ops()
    deletes = [t for op, t in ops if op == "delete"]
    assert len(deletes) == 1, ops
    puts = [t for op, t in ops if op == "put"]
    assert puts, ops
    exp = int(puts[0]) + minutes * 60
    assert deletes[0] > exp, (deletes[0], exp)
    assert ops[-1][0] == "get", ops   # the read-back follows the delete
    return exp


def tkt_get(status, assignee):
    return res(200, {"ticket": {"ticket_id": "TCK-OLD", "status": status, "assignee": assignee}})


# ------------------------------------------------------------------ AC5: token, rollback order, controls, precheck

def test_token_exp_is_the_argument_and_capped(monkeypatch):
    # the argument is REQUIRED, an integer from 5 to 60, with no default
    parser = run.build_parser()
    without = [x for i, x in enumerate(ARGV) if i not in (2, 3)]
    with pytest.raises(SystemExit):
        parser.parse_args(without)
    for bad in ("4", "61", "0", "-5", "abc", "5.5", "", " 7", "7200", "1e1", "+10", "True"):
        with pytest.raises(SystemExit):
            parser.parse_args(ARGV[:3] + [bad] + ARGV[4:])
    for good in (5, 17, 60):
        a = parser.parse_args(ARGV[:3] + [str(good)] + ARGV[4:])
        assert a.exp_minutes == good and isinstance(a.exp_minutes, int)
    # every other required argument is required too
    for flag in ("--read27", "--expect-irpt-status-sha", "--run-label", "--pair", "--executor", "--trace-out"):
        i = ARGV.index(flag)
        with pytest.raises(SystemExit):
            parser.parse_args(ARGV[:i] + ARGV[i + 2:])
    # the minted claims: exp == iat + N*60; an out-of-range N mints nothing
    w = World(monkeypatch)
    for n in (5, 17, 60):
        tok, exp = run.mint_token(1000, n)
        assert tok == "tok" and exp == 1000 + n * 60
        assert w.claims[-1]["iat"] == 1000 and w.claims[-1]["exp"] == 1000 + n * 60
    minted, secrets = len(w.claims), len(w.index(lambda e: e[:2] == ("aws", "secret")))
    for bad in (4, 61, 0, -1, True, "5", 5.0, None, 120):
        with pytest.raises(ValueError):
            run.mint_token(1000, bad)
    assert len(w.claims) == minted and len(w.index(lambda e: e[:2] == ("aws", "secret"))) == secrets
    # no 2-hour token anywhere in the code
    assert "7200" not in _code_only(run.__file__)
    # and the trace records iat, exp and N
    rc, trace, w = drive(monkeypatch)
    p = trace["preconditions"]
    assert p["exp_minutes"] == 5 and p["token_iat"] and p["token_exp"] and p["token_iat"] < p["token_exp"]
    assert trace["cleanup"]["token_exp"] == p["token_exp"]
    assert w.claims[0]["exp"] - w.claims[0]["iat"] == 300


def test_row_is_deleted_only_after_exp(monkeypatch):
    # (a) cleanup itself: the delete time is later than exp, after a wait, and the absent read follows
    w = World(monkeypatch)
    w.http({})
    exp = int(w.t) + 300
    trace = {"cleanup": {}, "run_label": "R2-test-1"}
    run.cleanup("tok", trace, exp, ())
    out = trace["cleanup"]
    assert out["row_deleted_at_unix"] > exp and out["token_exp"]
    assert out["row_removed_read_back_absent"] is True
    ops = w.ddb_ops()
    assert [o for o, _ in ops] == ["delete", "get"] and ops[0][1] > exp
    assert sum(e[1] for e in w.events if e[0] == "sleep") >= 300

    # (b) every stop path after the row was written: the delete is later than exp, never earlier
    names = []

    def path(name, raises=None, first_get_empty=False, mint_raises=False, **kw):
        ww = World(monkeypatch)
        ww.first_get_empty, ww.mint_raises = first_get_empty, mint_raises
        if raises:
            with pytest.raises(raises):
                drive(monkeypatch, world=ww, **kw)
        else:
            rc, trace, _ = drive(monkeypatch, world=ww, **kw)
            assert trace["cleanup"]["row_removed_read_back_absent"] is True, name
        assert_row_deleted_after_exp(ww)
        names.append(name)

    def census_boom(token, run_id):
        raise ZeroDivisionError("census boom")

    def hops_boom(token, advisor, trace):
        raise KeyError("hops boom")

    path("clean run")
    path("row not readable after the put", first_get_empty=True)
    path("token not minted (secret unreadable)", raises=RuntimeError, mint_raises=True)
    path("limb 3: irpt-status answers 5xx", script={("GET", STATUS_PATH): res(503, {"message": "x"})})
    path("census stop", census_result=({"tickets_created_by_the_census": []}, "LEAK limb 1 -- x"))
    path("hops raise", raises=KeyError, hops_fn=hops_boom)
    ww = World(monkeypatch)
    ww.http({("GET", STATUS_PATH): res(200, {"data": {}})})
    monkeypatch.setattr(run, "census", census_boom)
    with pytest.raises(ZeroDivisionError):
        run.main(list(ARGV))
    assert_row_deleted_after_exp(ww)
    names.append("census raises")
    assert len(names) == 7, names

    # (c) an operator interrupt during the wait leaves the row IN PLACE (never an early delete)
    ww = World(monkeypatch)
    ww.sleep_raises = KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        drive(monkeypatch, world=ww)
    assert [o for o, _ in ww.ddb_ops()] == ["put", "get"] and ww.row is True

    # (d) a row that is not ours (the put is refused) is neither deleted nor waited for
    ww = World(monkeypatch)
    ww.put_raises = True
    rc, trace, _ = drive(monkeypatch, world=ww)
    assert rc == 1 and [o for o, _ in ww.ddb_ops()] == ["put"]
    assert trace["named_failures"][-1]["reason"] == "ROW_WRITE_FAILED"


def test_tickets_are_completed_before_the_row_is_touched(monkeypatch):
    w = World(monkeypatch)
    w.http({("POST", "/api/scoped/tickets/TCK-J/complete"): res(200, {"ticket": {}}),
            ("POST", "/api/scoped/tickets/TCK-C1/complete"): res(403, {"error": "refused"}),
            ("POST", "/api/scoped/tickets/TCK-OLD/complete"): res(200, {"ticket": {}}),
            ("GET", "/api/scoped/tickets/TCK-OLD"): [tkt_get("in_progress", FILER_EMAIL), tkt_get("completed", FILER_EMAIL)]})
    exp = int(w.t) + 600
    trace = {"cleanup": {}, "journey_ticket": "TCK-J", "census": {"tickets_created_by_the_census": ["TCK-C1"]},
             "run_label": "R2-test-1"}
    run.cleanup("tok", trace, exp, ("TCK-OLD",))
    completes = w.index(lambda e: e[0] == "http" and e[1] == "POST" and e[2].endswith("/complete"))
    first_ddb = w.index(lambda e: e[0] == "ddb")[0]
    first_sleep = w.index(lambda e: e[0] == "sleep")[0]
    assert len(completes) == 3 and max(completes) < first_sleep < first_ddb
    assert all(e[0] != "ddb" for e in w.events[:first_ddb])
    # a refused completion is recorded, and the row still follows the wait
    assert trace["cleanup"]["tickets_completed"] == {"TCK-J": 200, "TCK-C1": 403}
    assert trace["cleanup"]["tickets_completed_all"] is False and "TCK-C1" in trace["cleanup"]["ticket_completion_errors"]
    assert trace["cleanup"]["row_deleted_at_unix"] > exp
    # a completion that RAISES does not skip the wait or the delete
    w2 = World(monkeypatch)

    def raising(token, method, path, query=None, body=None, timeout=90):
        w2.events.append(("http", method, path, w2.t))
        raise OSError("socket")
    monkeypatch.setattr(run, "call", raising)
    trace = {"cleanup": {}, "journey_ticket": "TCK-J", "run_label": "R2-test-1"}
    run.cleanup("tok", trace, int(w2.t) + 60, ())
    assert trace["cleanup"]["tickets_completed"] == {"TCK-J": 0}
    first_http = w2.index(lambda e: e[0] == "http")[0]
    assert first_http < w2.index(lambda e: e[0] == "sleep")[0] < w2.index(lambda e: e[0] == "ddb")[0]
    assert trace["cleanup"]["row_removed_read_back_absent"] is True


def _zero_call(monkeypatch, data, control, streams=None, control_streams=None):
    """Run the zero-call read over iat=1000 against the fake logs layer. `streams` / `control_streams` are the
    describe_log_streams pages for the data-refresh group and the ticket API's group (default: one active stream)."""
    w = World(monkeypatch)
    w.log_resp = {run.DATA_REFRESH_LOG_GROUP: data, run.TICKET_LOG_GROUP: control}
    if streams is not None:
        w.stream_resp[run.DATA_REFRESH_LOG_GROUP] = streams
    if control_streams is not None:
        w.stream_resp[run.TICKET_LOG_GROUP] = control_streams
    trace = {}
    run.data_refresh_zero_calls(trace, 1000, 1300)
    return trace["data_refresh_zero_calls"], w


def st(ms, name="s"):
    return {"logStreamName": name, "lastEventTimestamp": ms}


NO_STREAMS = {"logStreams": []}
OLD_STREAM = {"logStreams": [st(999_999)]}   # last event one millisecond before iat=1000 s


def test_zero_call_read_is_void_on_zero_streams(monkeypatch):
    found = {"events": [{"m": 1}]}
    # GROUP_EMPTY: the group holds 0 streams in total, zero matches, a control that DID find the filer: VOID
    out, w = _zero_call(monkeypatch, {"events": []}, found, streams=NO_STREAMS)
    assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "GROUP_EMPTY"
    assert out["streams_in_group"] == 0 and out["match_count"] == 0
    assert out["verdict"] != "ZERO_CALLS_PROVEN"
    # a stream whose last event is before iat is in the group but not active: NOT void (see the F1 test)
    out, w = _zero_call(monkeypatch, {"events": []}, found, streams=OLD_STREAM)
    assert out["verdict"] == "ZERO_CALLS_PROVEN" and out["streams_in_group"] == 1
    # streams are counted across pages: 0 + 0 in total is GROUP_EMPTY; a later page with streams makes the zero countable
    out, w = _zero_call(monkeypatch, {"events": []}, found,
                        streams=[{"logStreams": [], "nextToken": "p2"}, NO_STREAMS])
    assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "GROUP_EMPTY"
    out, w = _zero_call(monkeypatch, {"events": []}, found,
                        streams=[{"logStreams": [], "nextToken": "p2"},
                                 {"logStreams": [st(ACTIVE_MS, "a"), st(ACTIVE_MS, "b")]}])
    assert out["verdict"] == "ZERO_CALLS_PROVEN" and out["streams_active_in_window"] == 2
    assert out["window"]["from"] < out["window"]["to"]
    # two describe pages on the data-refresh group, one on the control; one filter page on each group
    assert len(w.index(lambda e: e[0] == "aws" and e[1].startswith("streams:"))) == 3
    assert len(w.index(lambda e: e[0] == "aws" and e[1].startswith("logs:"))) == 2


def test_zero_call_read_needs_its_positive_control(monkeypatch):
    # the control over the ticket API's log group finds nothing: the zero is VOID
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": []})
    assert out["verdict"] == "ZERO_CALL_VOID" and out["control"]["found"] == 0
    assert out["control"]["log_group"] == "/aws/lambda/opal-ticket-api" and out["control"]["same_filter"] is True
    assert out["void_reason"] == "CONTROL_FOUND_NO_FILER"
    assert [e[1] for e in w.events if e[0] == "aws"] == [
        "streams:" + run.DATA_REFRESH_LOG_GROUP, "logs:" + run.DATA_REFRESH_LOG_GROUP,
        "streams:" + run.TICKET_LOG_GROUP, "logs:" + run.TICKET_LOG_GROUP]
    # active streams > 0 AND control >= 1 AND matches == 0 is the one PROVEN case
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]})
    assert out["verdict"] == "ZERO_CALLS_PROVEN" and out["control"]["found"] == 1 and out["match_count"] == 0
    assert out["streams_active_in_window"] == 1 and out["control"]["streams_active_in_window"] == 1
    # a data-refresh match is reported as non-zero, whatever the control says
    out, w = _zero_call(monkeypatch, {"events": [{"m": 1}]}, {"events": []})
    assert out["verdict"].startswith("NON-ZERO")
    # the control read raising is VOID (the control did not find the filer), never a zero
    out, w = _zero_call(monkeypatch, {"events": []}, RuntimeError("throttled"))
    assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "CONTROL_FOUND_NO_FILER"
    # the stream read raising is VOID too: the group cannot be described
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]}, streams=RuntimeError("denied"))
    assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "GROUP_NOT_DESCRIBABLE"
    assert out["match_count"] is None


def test_irpt_status_sha_mismatch_is_a_stop_before_any_write(monkeypatch):
    w = World(monkeypatch, sha="QUJDREVGGHI")
    rc, trace, w = drive(monkeypatch, world=w)
    assert rc == 1
    # nothing was written or minted: no row, no secret, no http call, no wait; only the one lambda read
    assert w.ddb_ops() == [] and w.claims == []
    assert [e[:2] for e in w.events] == [("aws", "lambda")]
    f = trace["named_failures"][-1]
    assert f["reason"] == "IRPT_STATUS_BUILD_MISMATCH"
    assert f["expected_prefix"] == "Zm9v" and f["live_code_sha256"] == "QUJDREVGGHI"
    assert trace["preconditions"]["irpt_status"]["result"] == "IRPT_STATUS_BUILD_MISMATCH"
    # an unreadable build is a stop too (not a match)
    w = World(monkeypatch)
    w.lambda_raises = True
    rc, trace, w = drive(monkeypatch, world=w)
    assert rc == 1 and w.ddb_ops() == [] and trace["named_failures"][-1]["reason"] == "IRPT_STATUS_BUILD_UNREAD"
    # positive control: a matching prefix goes on and writes the row, after the build read
    w = World(monkeypatch)
    rc, trace, w = drive(monkeypatch, world=w)
    assert rc == 0 and trace["preconditions"]["irpt_status"]["result"] == "IRPT_STATUS_BUILD_MATCH"
    assert w.events[0][:2] == ("aws", "lambda")
    assert w.index(lambda e: e[0] == "ddb")[0] > 0


# ------------------------------------------------------------------ AC6: report-route arms, old ticket, trace header

def _ddg_script(arm, issued, extra=None):
    s = {("GET", LIST_PATH): [listing(), listing(REQ_A)],
         SUBMIT: res(200, {"data": {"request_id": REQ_A}}),
         ("GET", rpath(REQ_A)): report(REQ_A),
         ("POST", REPORT_PATH): [arm, issued],
         ("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_A)}
    s.update(extra or {})
    return s


def _flow(monkeypatch, script):
    fake = install(monkeypatch, script)
    hops, named = trace_hops()
    trace = {"hops": list(hops.values()), "named_failures": named}
    run.hops_d_to_g("tok", trace, hops, named, TKT, "in-1", FILE_SHA)
    return fake, hops, named, trace


def test_malformed_report_id_arm_expects_typed_400(monkeypatch, sleeps):
    # as expected: HTTP 400 + code INVALID_REPORT_REQUEST_ID, recorded as the arm, then hop (f) sends the REQ id
    ok = res(200, {"ticket": {"ticket_id": TKT}})
    fake, hops, named, trace = _flow(monkeypatch, _ddg_script(ARM_REFUSED, ok))
    posts = [c for c in fake.calls if c[1] == REPORT_PATH]
    assert [p[3] for p in posts] == [{"request_id": "sar1b-" + "0" * 24}, {"request_id": REQ_A}]
    arms = trace["report_route_arms"]
    assert arms["report_id_malformed_refused"]["status"] == 400
    assert arms["report_id_malformed_refused"]["code"] == "INVALID_REPORT_REQUEST_ID"
    assert arms["report_id_well_formed_stored"] == {"status": 200, "as_expected": True}
    assert named == [] and hops["g_open"]["report_opened"] is True
    order = [(c[0], c[1]) for c in fake.calls]
    assert order.index(("GET", rpath(REQ_A))) < order.index(("POST", REPORT_PATH))   # after hop (e) is met
    # anything else is REPORT_ID_ARM_UNEXPECTED and the run stops BEFORE hop (f)
    for unexpected in (res(200, {"ticket": {}}),                                        # the malformed id was stored
                       res(400, {"error": "x", "code": "SOMETHING_ELSE"}),              # 400, wrong code
                       res(403, {"error": "x", "code": "INVALID_REPORT_REQUEST_ID"}),   # right code, wrong status
                       res(500, {"message": "boom"})):
        fake, hops, named, trace = _flow(monkeypatch, _ddg_script(unexpected, ok))
        posts = [c for c in fake.calls if c[1] == REPORT_PATH]
        assert len(posts) == 1 and posts[0][3] == {"request_id": "sar1b-" + "0" * 24}, "hop (f) must not run"
        assert named[0]["reason"] == "REPORT_ID_ARM_UNEXPECTED"
        assert hops["f_report"]["outcome"] == "UNREACHABLE" and hops["g_open"]["outcome"] == "UNREACHABLE"
        assert trace["report_route_arms"]["report_id_malformed_refused"]["as_expected"] is False
        assert "report_id_well_formed_stored" not in trace["report_route_arms"]
    # the arm never runs when hop (e) is not met
    fake = install(monkeypatch, _ddg_script(ARM_REFUSED, ok, {("GET", rpath(REQ_A)): refusal("UNEXPECTED")}))
    hops, named = trace_hops()
    run.hops_d_to_g("tok", {"hops": []}, hops, named, TKT, "in-1", FILE_SHA)
    assert not any(c[1] == REPORT_PATH for c in fake.calls)


def test_issued_id_refused_by_report_route_is_branch_b(monkeypatch):
    w = World(monkeypatch)
    refused_issued = res(400, {"error": "x", "code": "INVALID_REPORT_REQUEST_ID"})
    script = _ddg_script(ARM_REFUSED, refused_issued)
    script[("GET", STATUS_PATH)] = res(200, {"data": {}})
    script[("POST", "/api/scoped/tickets/%s/complete" % TKT)] = res(200, {"ticket": {}})

    def real_hops(token, advisor, trace):
        h = {x["hop"]: x for x in trace["hops"]}
        trace["journey_ticket"] = TKT
        return run.hops_d_to_g(token, trace, h, trace["named_failures"], TKT, "in-1", FILE_SHA)

    rc, trace, w = drive(monkeypatch, world=w, script=script, hops_fn=real_hops)
    posts = [e for e in w.events if e[0] == "http" and e[2] == REPORT_PATH]
    assert len(posts) == 2, "the issued id is posted once and NOT retried"
    nf = [n for n in trace["named_failures"] if n["hop"] == "f_report"]
    assert nf[0]["reason"] == "BRANCH_B_ISSUED_ID_REFUSED" and nf[0]["status"] == 400
    h = {x["hop"]: x for x in trace["hops"]}
    assert h["f_report"]["result"] == "BRANCH_B_ISSUED_ID_REFUSED"
    assert h["g_open"]["outcome"] == "UNREACHABLE"
    assert not any(e[0] == "http" and e[1] == "GET" and e[2] == "/api/scoped/tickets/%s" % TKT for e in w.events)
    assert trace["report_route_arms"]["report_id_malformed_refused"]["as_expected"] is True
    assert trace["report_route_arms"]["report_id_well_formed_stored"]["as_expected"] is False
    # then cleanup per D2: the ticket is completed, the wait happens, the row goes last and after exp
    done = w.index(lambda e: e[0] == "http" and e[2].endswith("/complete"))
    assert done and max(done) < w.index(lambda e: e[0] == "sleep")[0] < w.index(lambda e: e[0] == "ddb" and e[1] == "delete")[0]
    assert_row_deleted_after_exp(w)
    assert trace["cleanup"]["row_removed_read_back_absent"] is True
    # a 200 on the issued id is the other arm, recorded stored
    fake, hops, named, trace = _flow(monkeypatch, _ddg_script(ARM_REFUSED, res(200, {"ticket": {}})))
    assert trace["report_route_arms"]["report_id_well_formed_stored"] == {"status": 200, "as_expected": True}
    assert not any(n["reason"] == "BRANCH_B_ISSUED_ID_REFUSED" for n in named)


def test_old_test_ticket_is_closed_in_the_same_run(monkeypatch):
    old_path = "/api/scoped/tickets/TCK-OLD"
    # qualifying: in_progress and assigned to the filer -> completed, status recorded before and after
    w = World(monkeypatch)
    w.http({("GET", old_path): [tkt_get("in_progress", FILER_EMAIL.upper()), tkt_get("completed", FILER_EMAIL)],
            ("POST", old_path + "/complete"): res(200, {"ticket": {}})})
    exp = int(w.t) + 300
    trace = {"cleanup": {}, "run_label": "R2-test-1"}
    run.cleanup("tok", trace, exp, ("TCK-OLD", "TCK-OLD"))
    rec = trace["cleanup"]["old_tickets"]["TCK-OLD"]
    assert rec["action"] == "COMPLETED"
    assert rec["before"]["status"] == "in_progress" and rec["before"]["assigned_to_filer"] is True
    assert rec["after"]["status"] == "completed"
    assert len([e for e in w.events if e[0] == "http" and e[2] == old_path + "/complete"]) == 1   # repeated id, one act
    assert max(w.index(lambda e: e[0] == "http")) < w.index(lambda e: e[0] == "ddb")[0]
    # any other state is recorded as found and left alone: no complete is sent
    for status, who in (("in_progress", "someone.else@example.invalid"), ("open", None), ("completed", FILER_EMAIL),
                        ("in_progress", None)):
        w = World(monkeypatch)
        w.http({("GET", old_path): tkt_get(status, who), ("POST", old_path + "/complete"): res(200, {})})
        trace = {"cleanup": {}, "run_label": "R2-test-1"}
        run.cleanup("tok", trace, int(w.t) + 60, ("TCK-OLD",))
        rec = trace["cleanup"]["old_tickets"]["TCK-OLD"]
        assert rec["action"] == "FOUND_LEFT_ALONE" and rec["before"]["status"] == status, (status, who)
        assert rec["after"] == rec["before"], (status, who)
        assert not any(e[0] == "http" and e[1] == "POST" for e in w.events), (status, who)
    # an unreadable ticket is left alone
    w = World(monkeypatch)
    w.http({("GET", old_path): res(404, {"error": "not found"})})
    trace = {"cleanup": {}, "run_label": "R2-test-1"}
    run.cleanup("tok", trace, int(w.t) + 60, ("TCK-OLD",))
    assert trace["cleanup"]["old_tickets"]["TCK-OLD"]["action"] == "NOT_READ_LEFT_ALONE"
    assert not any(e[0] == "http" and e[1] == "POST" for e in w.events)
    # in the same run: --close-ticket on the command line, repeatable, completed before the row is touched
    w = World(monkeypatch)
    script = {("GET", STATUS_PATH): res(200, {"data": {}}),
              ("GET", old_path): [tkt_get("in_progress", FILER_EMAIL), tkt_get("completed", FILER_EMAIL)],
              ("POST", old_path + "/complete"): res(200, {}),
              ("GET", "/api/scoped/tickets/TCK-OLD2"): tkt_get("open", None)}
    rc, trace, w = drive(monkeypatch, argv=ARGV + ["--close-ticket", "TCK-OLD", "--close-ticket", "TCK-OLD2"], world=w,
                         script=script)
    assert sorted(trace["cleanup"]["old_tickets"]) == ["TCK-OLD", "TCK-OLD2"]
    assert trace["cleanup"]["old_tickets"]["TCK-OLD"]["action"] == "COMPLETED"
    assert trace["cleanup"]["old_tickets"]["TCK-OLD2"]["action"] == "FOUND_LEFT_ALONE"
    post = w.index(lambda e: e[0] == "http" and e[2] == old_path + "/complete")[0]
    assert post < w.index(lambda e: e[0] == "sleep")[0] < w.index(lambda e: e[0] == "ddb" and e[1] == "delete")[0]
    assert run.build_parser().parse_args(ARGV).close_ticket == []


def test_trace_header_names_this_run_not_round_one(monkeypatch):
    a = run.build_parser().parse_args(ARGV)
    trace = run.build_trace(a, "R2-test-1-2026-10-11T00:00:00Z")
    blob = json.dumps(trace)
    assert trace["run_label"] == "R2-test-1" and trace["pair"] == "org/pair/path@abc123"
    assert trace["executor"] == "0.9.0_WK_TEST~1" and trace["run_id"].startswith("R2-test-1-")
    for round_one in ("SA-r-1b", "v2.2", "order_pin", "68642d02e9", "amendment_3", "amendment_4", "0.7.0_AE_CloudOps~TV2",
                      "022ee70258", "16:43:21Z"):
        assert round_one not in blob, round_one
    # a different invocation names a different run
    i = ARGV.index("--run-label")
    b = run.build_parser().parse_args(ARGV[:i] + ["--run-label", "R2-tr-1", "--pair", "P@1", "--executor", "0.9.0_WK_OTHER~2",
                                        "--trace-out", "UNUSED_NO_SUCH_DIR/other.json"])
    t2 = run.build_trace(b, "R2-tr-1-x")
    assert (t2["run_label"], t2["pair"], t2["executor"]) == ("R2-tr-1", "P@1", "0.9.0_WK_OTHER~2")
    # and the trace main() builds, end to end, carries it too; the source holds no hard-coded round-one header
    rc, trace, w = drive(monkeypatch)
    assert trace["run_label"] == "R2-test-1" and trace["executor"] == "0.9.0_WK_TEST~1"
    assert trace["run_id"].startswith("R2-test-1-")
    assert "SA-r-1b" not in json.dumps(trace) and "order_pin" not in trace
    code = _code_only(run.__file__)
    for lit in ('"order_pin"', '"amendment_3"', '"amendment_4_cto_code_read_verbatim"', '"v2.2"', '"SA-r-1b-"'):
        assert lit not in code, lit


# ------------------------------------------------------------------ AMENDMENT 3 / AC7: --trace-out, the measured stream denominator

def test_trace_out_is_required_and_is_the_only_file_written(monkeypatch, tmp_path):
    import builtins
    real_save = run.save
    # the argument is required
    i = ARGV.index("--trace-out")
    with pytest.raises(SystemExit):
        run.build_parser().parse_args(ARGV[:i] + ARGV[i + 2:])
    assert run.build_parser().parse_args(ARGV).trace_out == ARGV[i + 1]
    # run main end to end with the REAL save, every write intercepted: all of them target the one --trace-out file
    out = tmp_path / "nested" / "my_trace.json"
    argv = ARGV[:i] + ["--trace-out", str(out)]
    w = World(monkeypatch)
    monkeypatch.setattr(run, "save", real_save)
    w.http({("GET", STATUS_PATH): res(200, {"data": {}})})
    monkeypatch.setattr(run, "census", lambda token, run_id: ({"tickets_created_by_the_census": []}, None))
    monkeypatch.setattr(run, "hops", lambda token, advisor, trace: None)
    writes = []
    real_open, real_wt, real_wb = builtins.open, Path.write_text, Path.write_bytes

    def spy_open(f, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            writes.append(str(Path(f).resolve()))
        return real_open(f, mode, *a, **k)

    def spy_wt(self, *a, **k):
        writes.append(str(self.resolve()))
        return real_wt(self, *a, **k)

    def spy_wb(self, *a, **k):
        writes.append(str(self.resolve()))
        return real_wb(self, *a, **k)

    monkeypatch.setattr(builtins, "open", spy_open)
    monkeypatch.setattr(Path, "write_text", spy_wt)
    monkeypatch.setattr(Path, "write_bytes", spy_wb)
    rc = run.main(argv)
    monkeypatch.undo()
    assert rc == 0
    assert writes and set(writes) == {str(out.resolve())}, set(writes)
    # the file is ONE JSON object for this run: its run_id, no run_N section, no older run appended
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert doc["run_id"].startswith("R2-test-1-")
    assert not [k for k in doc if k.startswith("run_") and k not in ("run_id", "run_label")]
    assert doc["data_refresh_zero_calls"]["verdict"] == "ZERO_CALLS_PROVEN"
    assert [p.name for p in tmp_path.rglob("*") if p.is_file()] == ["my_trace.json"]
    # a path that already holds a run's trace is refused, untouched: nothing appended, nothing overwritten
    before = out.read_bytes()
    w = World(monkeypatch)
    monkeypatch.setattr(run, "save", real_save)
    assert run.main(argv) == 2
    assert out.read_bytes() == before and w.events == []


def test_no_round_one_trace_path_remains():
    src = Path(run.__file__).read_text(encoding="utf-8")
    for banned in ("R1_RUN", "sa_r1b_trace", "searchedLogStreams", "0.7.0_AE_CloudOps~TV2"):
        assert banned not in src, banned
    assert not hasattr(run, "TRACE") and not hasattr(run, "MY_TRACE")
    # save() with no --trace-out set writes nothing and raises: there is no fallback path
    saved = run.TRACE_OUT
    try:
        run.TRACE_OUT = None
        with pytest.raises(RuntimeError):
            run.save({"run_id": "x"})
    finally:
        run.TRACE_OUT = saved


def test_stream_denominator_is_streams_active_in_the_window(monkeypatch):
    # The window starts at iat=1000 s = 1_000_000 ms. Active: last event >= iat (a stream AT iat counts). Not active:
    # before iat, or no last event time at all. The API field naming the streams a filter searched is never read:
    # the filter answers below carry an unrelated key and the denominator comes from describe_log_streams alone.
    page1 = {"logStreams": [st(ACTIVE_MS, "a"), st(1_000_000, "at-iat"), st(999_999, "before"), {"logStreamName": "empty"}],
             "nextToken": "p2"}
    page2 = {"logStreams": [st(1_000_001, "c"), st(5, "ancient")]}
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]},
                        streams=[dict(page1), dict(page2)], control_streams={"logStreams": [st(1_000_000, "t")]})
    assert out["streams_active_in_window"] == 3     # a, at-iat, c
    assert out["control"]["streams_active_in_window"] == 1
    assert "searched_log_streams" not in out and "searched_log_streams" not in out["control"]
    assert out["verdict"] == "ZERO_CALLS_PROVEN"
    # every page of describe_log_streams was read, ordered by last event time, with the page token passed on
    d = [kw for api, kw in w.log_calls if api == "describe_log_streams" and kw["logGroupName"] == run.DATA_REFRESH_LOG_GROUP]
    assert len(d) == 2 and "nextToken" not in d[0] and d[1]["nextToken"] == "p2"
    assert all(kw["orderBy"] == "LastEventTime" for kw in d)
    # filter_log_events reads every page too
    out, w = _zero_call(monkeypatch, [{"events": [], "nextToken": "f2"}, {"events": [{"m": 1}], "nextToken": "f3"},
                                      {"events": [{"m": 2}]}], {"events": [{"m": 1}]})
    f = [kw for api, kw in w.log_calls if api == "filter_log_events" and kw["logGroupName"] == run.DATA_REFRESH_LOG_GROUP]
    assert [kw.get("nextToken") for kw in f] == [None, "f2", "f3"]
    assert out["match_count"] == 2 and out["verdict"].startswith("NON-ZERO")
    # the control group's denominator is measured too, and a control with no active stream does not void by itself
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]}, control_streams=NO_STREAMS)
    assert out["control"]["streams_active_in_window"] == 0 and out["verdict"] == "ZERO_CALLS_PROVEN"


def test_zero_active_streams_alone_is_not_void(monkeypatch):
    # F1: streams exist but none is active in the window, no matches, control found the filer: a true zero
    for streams in (OLD_STREAM, {"logStreams": [{"logStreamName": "never-wrote"}]}):
        out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]}, streams=streams)
        assert out["verdict"] == "ZERO_CALLS_PROVEN" and out["streams_active_in_window"] == 0, streams
        assert out["streams_in_group"] == 1 and out["match_count"] == 0 and out["control"]["found"] == 1
        assert "void_reason" not in out
    # active streams still prove it, and the trace says how many were active
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]})
    assert out["verdict"] == "ZERO_CALLS_PROVEN" and out["streams_active_in_window"] == 1


def test_group_with_no_streams_at_all_is_void(monkeypatch):
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]}, streams=NO_STREAMS)
    assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "GROUP_EMPTY"
    assert out["streams_in_group"] == 0 and out["streams_active_in_window"] == 0


def test_group_not_describable_is_void(monkeypatch):
    for exc in (RuntimeError("AccessDenied"), KeyError("ResourceNotFoundException")):
        out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}]}, streams=exc)
        assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "GROUP_NOT_DESCRIBABLE", exc
        assert out["streams_in_group"] is None and out["matches"] is None


def test_control_without_the_filer_is_void(monkeypatch):
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": []})
    assert out["verdict"] == "ZERO_CALL_VOID" and out["void_reason"] == "CONTROL_FOUND_NO_FILER"
    assert out["control"]["matches"] == 0 and out["streams_in_group"] == 1


def test_zero_read_records_three_numbers(monkeypatch):
    two = {"logStreams": [st(ACTIVE_MS, "a"), st(999_999, "old"), {"logStreamName": "empty"}]}
    out, w = _zero_call(monkeypatch, {"events": []}, {"events": [{"m": 1}, {"m": 2}]},
                        streams=two, control_streams={"logStreams": [st(ACTIVE_MS, "t")]})
    assert out["verdict"] == "ZERO_CALLS_PROVEN"
    assert (out["streams_in_group"], out["streams_active_in_window"], out["matches"]) == (3, 1, 0)
    c = out["control"]
    assert (c["streams_in_group"], c["streams_active_in_window"], c["matches"]) == (1, 1, 2)
    assert c["log_group"] == run.TICKET_LOG_GROUP
