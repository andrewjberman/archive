"""TCKT_VNEXT round 20, cell R20-lm-7 (the CTO's msg 11065, IRPT_ANLREQ v0.24 FWD-1 ACCEPT: "a commentary failure never withholds the other three"):
the package route admits pdf_ref and commentary_ref null TOGETHER, both keys present (the CTO's ruling msg 11078: pdf_ref is the commentary PDF),
each null skipping its I7 check; one null beside one set is 400; report_ref stays required; original_ref keeps I5'; everything else is unchanged.

Run from the repo root:
    python -m pytest -q org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/test_r20_package_commentary_null.py
The harness is the package route's own (infra/aws/lambda/ticket_center/tests/test_package_route.py). No network, nothing applied.
At the base the pair test and the replace test FAIL (a null commentary_ref reads 400) and the four control tests PASS.
"""
from __future__ import annotations

import importlib.util
import os

import pytest

ROOT = os.getcwd()
_TESTS = os.path.join(ROOT, "infra", "aws", "lambda", "ticket_center", "tests")
_spec = importlib.util.spec_from_file_location("package_route_harness", os.path.join(_TESTS, "test_package_route.py"))
PR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PR)

fresh, ticket, package, REFS = PR.fresh, PR.ticket, PR.package, PR.REFS


@pytest.fixture(autouse=True)
def _principal(monkeypatch):
    monkeypatch.setitem(PR.mod.TYPE_DEFINITIONS["analysis_request"], "package_principal", PR.PRINCIPAL)
    monkeypatch.setattr(PR.mod, "PACKAGE_ALLOWED_FIRMS", frozenset({"inflection", "49financial"}))


def _body(**kw):
    b = dict(REFS)
    b.update(kw)
    return b


def test_pdf_ref_and_commentary_ref_null_together_with_both_keys_present_are_admitted_and_stored_null():
    t = fresh()
    tid = ticket()
    code, b = package(tid, body=_body(pdf_ref=None, commentary_ref=None))
    assert code == 200, b
    pkg = b["package"]
    assert pkg["commentary_ref"] is None and "commentary_ref" in pkg and pkg["pdf_ref"] is None and "pdf_ref" in pkg
    stored = t.items[tid]["package"]
    assert stored["commentary_ref"] is None and stored["pdf_ref"] is None
    for k in ("report_ref", "original_ref"):
        assert stored[k] == REFS[k], k


def test_a_missing_pdf_ref_or_commentary_ref_key_is_still_refused_even_beside_a_null_partner():
    t = fresh()
    tid = ticket()
    for k, other in (("commentary_ref", "pdf_ref"), ("pdf_ref", "commentary_ref")):
        body = {a: v for a, v in _body(**{other: None}).items() if a != k}
        code, b = package(tid, body=body)
        assert code == 400 and k in b["error"], (k, code, b)
        body = {a: v for a, v in _body().items() if a != k}
        code, b = package(tid, body=body)
        assert code == 400 and k in b["error"], (k, code, b)
    assert "package" not in t.items[tid]


def test_a_non_string_non_null_or_empty_or_non_canonical_pdf_ref_or_commentary_ref_is_still_refused():
    t = fresh()
    tid = ticket()
    for k in ("commentary_ref", "pdf_ref"):
        for bad in (7, "", "   ", "plain/string.txt", "[]", {"a": 1}):
            code, b = package(tid, body=_body(**{k: bad}))
            assert code == 400 and k in b["error"], (k, bad, code, b)
    assert "package" not in t.items[tid]


def test_report_ref_stays_required_non_null_and_a_lone_null_of_the_pair_is_refused_naming_both():
    t = fresh()
    tid = ticket()
    code, b = package(tid, body=_body(report_ref=None))
    assert code == 400 and "report_ref" in b["error"], (code, b)
    missing = {a: v for a, v in _body().items() if a != "report_ref"}
    code, b = package(tid, body=missing)
    assert code == 400 and "report_ref" in b["error"], (code, b)
    # one null beside one set is refused, and the refusal names both members
    for k in ("pdf_ref", "commentary_ref"):
        code, b = package(tid, body=_body(**{k: None}))
        assert code == 400 and "pdf_ref" in b["error"] and "commentary_ref" in b["error"], (k, code, b)
    assert "package" not in t.items[tid]


def test_replace_path_is_unchanged_a_later_post_with_all_four_replaces_the_null_package():
    t = fresh()
    tid = ticket()
    code, b = package(tid, body=_body(pdf_ref=None, commentary_ref=None))
    assert code == 200, b
    first_at = b["package"]["attached_at"]
    # without prior_attached_at the stored package is not replaced
    code, b = package(tid, body=_body())
    assert code == 409 and b.get("code") == "PACKAGE_ALREADY_ATTACHED", (code, b)
    # with prior_attached_at equal to the stored attached_at all four are posted
    code, b = package(tid, body=_body(prior_attached_at=first_at))
    assert code == 200, b
    stored = t.items[tid]["package"]
    assert stored["commentary_ref"] == REFS["commentary_ref"] and stored["pdf_ref"] == REFS["pdf_ref"]
