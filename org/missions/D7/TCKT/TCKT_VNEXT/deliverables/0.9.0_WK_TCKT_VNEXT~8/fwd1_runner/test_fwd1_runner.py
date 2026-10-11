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


def read(stage, findings=None):
    body = {"identity": {"request_id": REQ_A}, "accepted_at": 1, "stage": stage}
    if findings:
        body["findings"] = [{"code": c} for c in findings]
    return res(200, {"data": body})


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
        ("GET", LIST_PATH + "/" + REQ_C): [read("RECEIVED"), read("GENERATED")],
        ("POST", "/api/scoped/tickets/%s/report" % TKT): res(200, {"ticket": {"ticket_id": TKT}}),
        ("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_C),
        ("GET", LIST_PATH + "/" + REQ_C + "/pdf"): res(200, {"data": {"sha256": "ab" * 32, "byte_length": 10}})})
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


# ------------------------------------------------------------------ AC2: hop (e) reads `stage`

def test_reads_stage_field_until_generated(monkeypatch, sleeps):
    fake = install(monkeypatch, {("GET", LIST_PATH + "/" + REQ_A): [
        read("RECEIVED"), read("PARSED"), read("READY"), read("SUBMITTING"), read("GENERATED")]})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "OK"
    assert hops["e_ready"]["polls"] == 5 and hops["e_ready"]["stage"] == "GENERATED"
    assert sleeps == [run.POLL_SECONDS] * 4
    assert named == []
    assert set(fake.paths("GET")) == {LIST_PATH + "/" + REQ_A}


def test_failed_stage_is_recorded_not_retried(monkeypatch, sleeps):
    fake = install(monkeypatch, {
        ("GET", LIST_PATH): [listing(), listing(REQ_A)],
        SUBMIT: res(200, {"data": {"request_id": REQ_A}}),
        ("GET", LIST_PATH + "/" + REQ_A): read("FAILED", ["SYN_FINDING"])})
    hops, named = trace_hops()
    trace = {"hops": list(hops.values()), "named_failures": named}
    run.hops_d_to_g("tok", trace, hops, named, TKT, "in-1", FILE_SHA)
    e = hops["e_ready"]
    assert e["polls"] == 1 and e["result"] == {"stage": "FAILED", "reason_codes": ["SYN_FINDING"]}
    assert sleeps == []
    assert hops["f_report"]["outcome"] == "UNREACHABLE" and hops["g_open"]["outcome"] == "UNREACHABLE"
    assert not any(p.endswith("/report") for p in fake.paths("POST"))
    assert [n["reason"] for n in named] == ["UNREACHABLE", "UNREACHABLE"]
    # NEEDS_CORRECTION is a result of the same kind
    install(monkeypatch, {("GET", LIST_PATH + "/" + REQ_A): read("NEEDS_CORRECTION")})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "RESULT"
    assert hops["e_ready"]["result"]["reason_codes"] == ["NEEDS_CORRECTION"]


def test_poll_budget_is_bounded(monkeypatch, sleeps):
    fake = install(monkeypatch, {("GET", LIST_PATH + "/" + REQ_A): read("SUBMITTING")})
    assert run.POLL_MAX == 40 and run.POLL_SECONDS == 30
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
    assert len(fake.calls) == 40 and hops["e_ready"]["polls"] == 40
    assert sleeps == [30] * 39
    assert named[-1]["reason"] == "STAGE_NOT_TERMINAL"


def test_refusal_envelope_is_not_a_read(monkeypatch, sleeps):
    for body in ({"status": {"public_reason_code": "INVALID_REQUEST_ID"}},
                 {"code": "INVALID_REQUEST_ID", "data": {"stage": "GENERATED"}}):
        fake = install(monkeypatch, {("GET", LIST_PATH + "/" + REQ_A): res(200, body)})
        hops, named = trace_hops()
        assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
        e = hops["e_ready"]
        assert e["status"] == 200 and e["refused"] is True and e["reason"] == "INVALID_REQUEST_ID"
        assert e["polls"] == 1 and len(fake.calls) == 1 and sleeps == []
        assert named[-1]["hop"] == "e_ready" and named[-1]["reason"] == "INVALID_REQUEST_ID"


def test_missing_stage_is_a_named_failure_not_a_pass(monkeypatch, sleeps):
    install(monkeypatch, {("GET", LIST_PATH + "/" + REQ_A): res(200, {"data": {
        "identity": {"request_id": REQ_A}, "accepted_at": 1}})})
    hops, named = trace_hops()
    assert run.hop_e_ready("tok", REQ_A, hops["e_ready"], named) == "FAILED"
    assert named[-1]["reason"] == "STAGE_ABSENT" and hops["e_ready"]["polls"] == 1


# ------------------------------------------------------------------ AC3: the ticket carries a REQ id

def test_records_req_id_on_ticket(monkeypatch, sleeps):
    fake = install(monkeypatch, {("POST", "/api/scoped/tickets/%s/report" % TKT): res(200, {"ticket": {}})})
    hops, named = trace_hops()
    assert run.hop_f_report("tok", TKT, REQ_A, hops["f_report"], named) is True
    posts = [c for c in fake.calls if c[0] == "POST"]
    assert len(posts) == 1 and posts[0][3] == {"request_id": REQ_A}
    assert hops["f_report"]["request_id"] == REQ_A and named == []


def test_opens_report_from_ticket_report_ref(monkeypatch, sleeps):
    """The id in memory is REQ_A; the ticket's report_ref names REQ_B. The pdf GET must use REQ_B."""
    fake = install(monkeypatch, {
        ("GET", "/api/scoped/tickets/%s" % TKT): ticket_with(REQ_B),
        ("GET", LIST_PATH + "/" + REQ_B + "/pdf"): res(200, {"data": {"sha256": "cd" * 32, "byte_length": 1234}})})
    hops, named = trace_hops()
    assert run.hop_g_open("tok", TKT, hops["g_open"], named) is True
    pdf_gets = [c[1] for c in fake.calls if c[1].endswith("/pdf")]
    assert pdf_gets == [LIST_PATH + "/" + REQ_B + "/pdf"]
    assert REQ_A not in " ".join(c[1] for c in fake.calls)
    g = hops["g_open"]
    assert g["report_ref_request_id"] == REQ_B and g["report_opened"] is True
    assert g["pdf"] == {"status": 200, "content_type": "application/json", "len": g["pdf"]["len"],
                        "sha256_prefix": "cd" * 8, "byte_length": 1234}
    assert named == []


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
    assert not any(c[1].endswith("/pdf") for c in fake.calls)
