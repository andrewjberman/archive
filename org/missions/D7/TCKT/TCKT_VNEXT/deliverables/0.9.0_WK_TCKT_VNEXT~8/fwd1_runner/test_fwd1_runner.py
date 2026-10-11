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
        ("POST", "/api/scoped/tickets/%s/report" % TKT): res(200, {"ticket": {"ticket_id": TKT}}),
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
