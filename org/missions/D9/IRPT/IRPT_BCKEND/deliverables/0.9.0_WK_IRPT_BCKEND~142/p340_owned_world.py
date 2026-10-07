"""p340_owned_world.py -- IB-pr-340: the gated routes served by an INSTALLED / OWNED entry, driven in-process with fixtures.

Run by battery_ib_pr_340.py as `python -m pytest -p no:cacheprovider p340_owned_world.py` (never by hand against anything live): the
process is NETWORK-BLOCKED at import (`battery_ib_pr_340._block_network`), the AWS credential chain points at nothing, and every
storage object is one of this repository's own offline doubles.

WHY PYTEST. Six gated routes (analysis/requests, analysis/requests/{requestId}, .../pdf, analysis/{jobId}/sections, status/{jobId}, and
POST analysis/inputs) are served by an entry the deployed function builds from its role's clients (`reports/status_installed.py`,
`reports/generate_installed.py` -> `ops/entry.py:build_owned_entry`), so no module-level Entry exists to call. The repository's own
tests build that entry over REAL readers/repositories on offline Dynamo/S3 doubles (fixtures `report_world`, `pdf_world`,
`_upload_world`); this module reuses exactly those worlds -- it re-implements no reader and no ownership rule -- and puts the
fixture files through the same Entry.handle the deployed handler wraps.

THE TWO PRINCIPAL CLASSES for these routes, which are OWNED reads (no directory grant): ALLOWED = the owner of the retained request (the
world's partner advisor); DENIED = anyone else (another email, another firm header, no edge marker, an object the owner never made).

Each fixture is `fixtures/<slug>.allowed.json` / `<slug>.denied.json`, the same shape the in-process worker reads; `event` is the API
Gateway shape (routeKey, pathParameters, queryStringParameters), `${NAME}` placeholders bind to the world's ids.
"""
from __future__ import annotations

import base64
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, *([".."] * 7)))
LAMBDA = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
for _p in (HERE, os.path.join(LAMBDA, "ops", "tests"), os.path.join(LAMBDA, "reports", "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pytest  # noqa: E402

import battery_ib_pr_340 as B  # noqa: E402  the same battery: its network block, its slug rule, its placeholder resolver

BLOCKED = B._block_network()                           # hard-block BEFORE any world is built
OUT = os.environ.get("P340_B_OUT") or os.path.join(HERE, ".p340_b_out.jsonl")

# Two worlds, two interpreters: the owned-read world and the upload world each bind a different module named `entry`, so the
# battery runs this file twice (P340_WORLD=owned, then =upload) and each run collects only its own tests.
WORLD = os.environ.get("P340_WORLD", "owned")
if WORLD == "owned":
    from test_owned_report import report_world, retention_world, world  # noqa: E402,F401  (fixtures)
    from test_pdf_link import pdf_world, FakeSigner  # noqa: E402,F401
    import pdf_link  # noqa: E402

    _spec = importlib.util.spec_from_file_location("p340_owned_ops_entry", os.path.join(LAMBDA, "ops", "entry.py"))
    entry = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(entry)

OWNED = {  # route key -> which offline world serves it
    "GET " + B.SCOPED + "analysis/requests": "report_world",
    "GET " + B.SCOPED + "analysis/requests/{requestId}": "report_world",
    "GET " + B.SCOPED + "analysis/requests/{requestId}/pdf": "pdf_world",
    "GET " + B.SCOPED + "analysis/{jobId}/sections": "report_world",
    "GET " + B.SCOPED + "status/{jobId}": "report_world",
}
UPLOAD_ROUTE = "POST " + B.SCOPED + "analysis/inputs"


def _load(route_key):
    pa, pd = B.fixture_paths(route_key)
    return json.load(open(pa, encoding="utf-8")), json.load(open(pd, encoding="utf-8")), pa, pd


def _headers(base, spec):
    h = dict(base)
    for k in (spec or {}).get("drop_headers", []):
        h.pop(k, None)
    for k, v in ((spec or {}).get("set_headers") or {}).items():
        h[k] = v
    return h


def _code(ans):
    if not isinstance(ans, dict):
        return "NOT-A-DICT"
    if ans.get("ok") is False:
        return (ans.get("status") or {}).get("public_reason_code") or "REFUSED-NO-CODE"
    return "SERVED"


def _text(ans):
    k, v = B._flatten(ans)
    return "\n".join(sorted(k | v))


def _empty_page(ans):
    d = ans.get("data") if isinstance(ans, dict) else None
    return isinstance(d, dict) and d.get("items") == []


def _judge(route_key, allowed_fx, denied_fx, pa, pd, a_ans, bind, run_case, extra_ok=None):
    """Same verdict rules as the in-process worker: SERVED + values for the allowed arm; every denied case refused by its
    named code (or, for a HISTORY page, answered with NO item of the owner) with zero protected values, the difference control, and the
    injected-leak control run through the identical leak test."""
    exp = allowed_fx["expect"]
    a_code = _code(a_ans)
    a_text = _text(a_ans)
    problems = []
    if a_code != "SERVED":
        problems.append("authorized request answered %s" % a_code)
    tokens = [B._subst(t, bind) for t in exp.get("data_contains", [])]
    missing = [t for t in tokens if t not in a_text]
    if missing:
        problems.append("served answer lacks %s" % missing)
    fixed = ("inflection", "Whitfield", "other@example.invalid", "cottonwood")
    a_leaks = [t for t in fixed if t in a_text]
    if a_leaks:
        problems.append("authorized answer carries %s" % a_leaks)
    allowed_state = "FAIL" if problems else "PASS"
    protected = {t for t in tokens if isinstance(t, str)}

    def leaks_in(ans):
        t = _text(ans)
        return sorted(x for x in protected if x in t) + [x for x in fixed if x in t]
    d_problems, cases_out = [], []
    for case in denied_fx["cases"]:
        ans = run_case(case)
        code = _code(ans)
        okcodes = case["expect_codes"]
        shown = code
        if code == "SERVED" and "EMPTY_PAGE" in okcodes and _empty_page(ans):
            shown = "EMPTY_PAGE"
        cp = []
        if shown not in okcodes:
            cp.append("answered %s, the fixture names %s" % (shown, okcodes))
        lk = leaks_in(ans)
        if lk:
            cp.append("answer carried %s" % lk[:4])
        echoed = [t for t in B._subst(case.get("must_not_echo", []), bind) if isinstance(t, str) and t in _text(ans)]
        if echoed:
            cp.append("answer echoed the supplied value")
        if shown == "SERVED":
            cp.append("a denied case was served data")
        cases_out.append({"case": case["name"], "answer": shown, "expected": okcodes, "ok": not cp, "problems": cp})
        d_problems += ["%s: %s" % (case["name"], p) for p in cp]
    probe = sorted(protected)[0] if protected else fixed[0]
    control = bool(leaks_in({"ok": False, "status": {"public_reason_code": "NOT_AUTHORIZED"}, "detail": probe}))
    if not control:
        d_problems.append("INSTRUMENT DEFECT: the injected-leak control was not detected")
    if allowed_state != "PASS":
        d_problems.append("difference control failed: the owner's request was not served")
    if not cases_out:
        d_problems.append("no denied case")
    if extra_ok:
        d_problems += extra_ok()
    row = {"route": route_key, "function": "irpt-ycharts-generate" if route_key.endswith("analysis/inputs") else "irpt-status",
           "allowed_fixture": B._repo_rel(pa), "denied_fixture": B._repo_rel(pd),
           "allowed": {"state": allowed_state, "reason": ("; ".join(problems) if problems else
                       "in-process on the installed/owned Entry over the repository's real readers on offline doubles: the owner's "
                       "operation-shaped request is SERVED with the fixture's values present"),
                       "detail": {"answer": a_code}},
           "denied": {"state": "FAIL" if d_problems else "PASS",
                      "reason": ("; ".join(d_problems) if d_problems else
                                 "%d denied cases each refused by the declared code (or an empty page for the history list) with 0 protected "
                                 "values; the owner served on the same request shape; the injected-leak control is detected by the same test"
                                 % len(cases_out)),
                      "detail": {"cases": cases_out, "protected_values_checked": len(protected), "injected_control_detected": control}},
           "network_connects_blocked": BLOCKED["n"]}
    with open(OUT, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, default=str) + "\n")
    return row


@pytest.mark.parametrize("route_key", sorted(OWNED))
def test_owned_route(request, monkeypatch, route_key):
    if WORLD != "owned":
        pytest.skip("owned world not loaded in this run")
    kind = OWNED[route_key]
    allowed_fx, denied_fx, pa, pd = _load(route_key)
    r = request.getfixturevalue(kind)
    if kind == "pdf_world":
        monkeypatch.setattr(pdf_link, "PdfSigner", lambda *a, **k: FakeSigner())
    bind = {"REQUEST_ID": r.id, "SHA": "2" * 64}
    base_headers = dict(r.w.case.headers)

    def call(headers_spec, event_over):
        boundary = entry.build_owned_entry(requests=r.requests, reports=r.reader)
        ev = B._subst(allowed_fx.get("event") or {}, bind)
        for k, v in B._subst(event_over or {}, bind).items():
            ev[k] = v
        ev["routeKey"] = route_key
        ev.setdefault("version", "2.0")
        ev["headers"] = _headers(base_headers, headers_spec)
        return entry._entry.lambda_entry(boundary)(ev)

    a_ans = call(allowed_fx.get("principal"), None)
    _judge(route_key, allowed_fx, denied_fx, pa, pd, a_ans, bind,
           lambda case: call(case.get("principal"), case.get("event")))


def test_upload_route(monkeypatch):
    if WORLD != "upload":
        pytest.skip("upload world not loaded in this run")
    from test_generate_installed import _upload_world, GENERATE_ENTRY  # noqa: F401
    monkeypatch.setitem(sys.modules, "entry", GENERATE_ENTRY)         # generate_installed.build_boundary imports `entry`
    allowed_fx, denied_fx, pa, pd = _load(UPLOAD_ROUTE)
    monkeypatch.setenv("IRPT_DIRECTORY_BUCKET_MAP", json.dumps({"49financial": "opal-data-49financial"}))
    body = B._subst(allowed_fx["event"]["body_json"], {})
    body["file_base64"] = base64.b64encode(allowed_fx["event"]["csv"].encode()).decode()
    state = {}

    def run(headers_spec, ordinary=True, event_over=None):
        boundary, event, table, sent = _upload_world((lambda request, p, o: True) if ordinary else None)
        ev = dict(event)
        ev["body"] = json.dumps(dict(body, **(event_over or {})))
        ev["headers"] = _headers(event["headers"], headers_spec)
        ans = boundary.handle(ev)
        state["persisted"] = len(table.rows)
        state["sent"] = len(sent)
        return ans, len(table.rows), len(sent)
    a_ans, a_rows, a_sent = run(allowed_fx.get("principal"))
    writes = []

    def run_case(case):
        ans, rows, sent = run(case.get("principal"), ordinary=case.get("ordinary", True), event_over=case.get("event"))
        writes.append((case["name"], rows, sent))
        return ans

    def nothing_written():
        bad = [w for w in writes if w[1] or w[2]]
        return ["denied case(s) wrote %s" % bad] if bad else []
    _judge(UPLOAD_ROUTE, allowed_fx, denied_fx, pa, pd, a_ans, {}, run_case, extra_ok=nothing_written)
