"""New tests for cell IB-rtr-3 -- the enforcer's REAL operation names and the item-8 identity
adapter, in `_authz/enforce.py`'s `Enforcer` (`RENDER_DELEGATE_OPERATIONS`,
`_resolve_render_delegate`). Task order
IRPT_BCKEND.TO-IB-rtr-3.the-enforcer-real-operation-names-and-the-item-8-identity-adapter,
criterion R118-AC3.

Follows the SAME repo-root-walking / dual-`fixtures.py` pattern the sibling IB-rtq-2 deliverable
(`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~15/
test_render_delegate_resolver_enforcer.py`) already established, rather than diverging from it.
That file is NEVER imported or edited here (BOUNDS: it sits outside this order's <paths>, and
BOUNDS forbids editing an existing test's expected value regardless) -- this cell's own three-arm
scope-algebra coverage is reproduced FRESH below, using the CORRECTED real operation names, so
"the revocation control still passing" is demonstrated against THIS cell's own code, in THIS
cell's own deliverable (see `test_revocation_control_still_passes` and
`IRPT_BCKEND-W19-S1` in the project's surprise channel for why the old file's literal, unmodified
run now shows 4 new operation-name failures that are NOT an algebra regression).

BOUNDS: no edit to any EXISTING test's expected value anywhere -- every function below is NEW.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

import pytest


def _find_repo_root(start):
    """Walk up from THIS file until the real `_scope/resolve.py` is found -- robust to exactly
    how deep this deliverable sits, immune to a hardcoded parent-count going stale."""
    probe = start
    marker = os.path.normpath("infra/aws/lambda/investor-reporting/_scope/resolve.py")
    for _ in range(25):
        candidate = os.path.join(probe, marker)
        if os.path.isfile(candidate):
            return probe
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    raise RuntimeError("could not locate the repo root walking up from %r" % start)


_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = _find_repo_root(_HERE)
_IRPT = os.path.join(_REPO_ROOT, "infra", "aws", "lambda", "investor-reporting")
_SCOPE_DIR = os.path.join(_IRPT, "_scope")
_AUTHZ_DIR = os.path.join(_IRPT, "_authz")
_KEYS_DIR = os.path.join(_IRPT, "_keys")
_AUTHZ_TESTS_DIR = os.path.join(_AUTHZ_DIR, "tests")
_ROUTES_JSON = os.path.join(
    _REPO_ROOT, "docs", "contracts", "investor-reporting", "v1", "routes.json")


def _load_module(name, path):
    """Load a file as a module under an EXPLICIT, private name."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ----- the REAL `_scope` side -----
for _p in (_SCOPE_DIR,):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import resolve as rs                                                        # noqa: E402

# ----- the REAL `_authz` side: `enforce` FIRST, fully, so `served`'s own `import enforce as
# _enforce` (below) resolves against the COMPLETE module rather than a partially-initialized one
# -- enforce.py does not import served.py at its own top level for exactly this reason (see the
# comment beside RENDER_DELEGATE_OPERATIONS in enforce.py). -----
for _p in (_AUTHZ_DIR, _KEYS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import enforce as ez                                                        # noqa: E402
import served                                                               # noqa: E402
afx = _load_module("_ib_rtr3_authz_fixtures", os.path.join(_AUTHZ_TESTS_DIR, "fixtures.py"))


# =============================================================================================
# item (a): THE REAL OPERATION NAMES
# =============================================================================================
def _real_render_route_operations():
    """The published operation id for each of the three render-scoped GET routes, read from
    `docs/contracts/investor-reporting/v1/routes.json` (never hand-copied): performance,
    analysis-sections and narrative -- the routes named `performance-report`, `analysis-report`
    and `narrative-packet` respectively."""
    with open(_ROUTES_JSON, "r", encoding="utf-8") as fh:
        contract = json.load(fh)
    by_route_key = {r["route_key"]: r["operation"] for r in contract["routes"]}
    performance = by_route_key["GET /api/scoped/investor-reporting/performance/{accountSetId}"]
    analysis = by_route_key["GET /api/scoped/investor-reporting/analysis/{jobId}/sections"]
    narrative = by_route_key["GET /api/scoped/investor-reporting/narrative/{reportId}"]
    assert performance == "performance-report", performance
    assert analysis == "analysis-report", analysis
    assert narrative == "narrative-packet", narrative
    return performance, analysis, narrative


REAL_RENDER_OPERATIONS = tuple(
    served.key_operation(op) for op in _real_render_route_operations())


def test_real_render_operations_are_confirmed_from_routes_json_and_key_operation():
    """Sanity on the DERIVATION itself: the three published ids, transformed through the REAL
    `served.key_operation()` function (never hand-transformed)."""
    assert REAL_RENDER_OPERATIONS == (
        "performance_report", "analysis_report", "narrative_packet")


def test_render_delegate_operations_matches_the_real_served_vocabulary():
    """The enforcer's tuple PROVEN equal to what the real function produces from the real
    published route table -- a wrong hand-typed spelling in enforce.py fails HERE."""
    assert ez.Enforcer.RENDER_DELEGATE_OPERATIONS == REAL_RENDER_OPERATIONS


# =============================================================================================
# shared render-delegate request/enforcer helpers (fresh copies -- BOUNDS: no cross-file import
# of the sibling cell's deliverable)
# =============================================================================================
def _bundle_loader(pinned_account_ids, bundle_id=None):
    def _load(tenant, revision):
        out = {"account_ids": list(pinned_account_ids)}
        if bundle_id is not None:
            out["bundle_id"] = bundle_id
        return out
    return _load


def _render_request(delegator, revision="rev-1", operation="performance_report",
                    object_kind=None, object_id=None, bundle="bundle-1"):
    headers = {"X-Origin-Verify": "cloudfront", "X-User-Email": "render:r-1",
              "X-User-Role": "renderer", "X-Firm-Id": afx.TENANT}
    if delegator is not None:
        headers["X-Render-Delegator"] = delegator
    headers["X-Render-Bundle"] = bundle
    headers["X-Render-Revision"] = revision
    return ez.Request(headers, operation, object_kind, object_id)


def _render_enforcer(pinned_accounts, ownership=None, bundle_id=None,
                     load_delegator_identity=None):
    deps = afx.Deps(ownership=ownership)
    binding = ez.FirmBinding(afx.TENANT, afx.OPAQUE_FIRM)
    e = ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                    load_render_bundle=_bundle_loader(pinned_accounts, bundle_id=bundle_id),
                    load_delegator_identity=load_delegator_identity)
    return e, deps


def _ok_payload(scope):
    return {"accounts": list(scope["permitted_account_set"])}


# =============================================================================================
# item (a), continued: admission / refusal through the ACTUAL _resolve_render_delegate path
# =============================================================================================
@pytest.mark.parametrize("operation", REAL_RENDER_OPERATIONS)
def test_each_real_operation_is_admitted_through_the_actual_resolve_render_delegate_path(
        operation):
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    out = e.serve(_render_request(afx.ADVISOR_A, operation=operation, object_kind="account",
                                  object_id=afx.A1), _ok_payload)
    assert out.ok, (operation, out)
    assert set(out.payload["accounts"]) == {afx.A1, afx.A2}


def test_a_fourth_unrelated_operation_is_refused_object_not_covered():
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    out = e.serve(_render_request(afx.ADVISOR_A, operation="directory_search",
                                  object_kind="account", object_id=afx.A1), _ok_payload)
    assert not out.ok and out.code == "OBJECT_NOT_COVERED", out
    assert "RENDER_DELEGATE" in out.reason


# =============================================================================================
# item (b): THE DELEGATOR IDENTITY, WITHOUT THE SUBJECT-EQUALS-ADVISOR-ID ASSUMPTION
# =============================================================================================
DIFFERING_ADVISOR_ID = "ADV-C-0003"
DIFFERING_ADVISOR_EMAIL = "advisor.c@49financial.com"
OWNERSHIP_DIFFERING_SUBJECT = {
    "schema_version": 1,
    "advisors": {DIFFERING_ADVISOR_ID: {"accounts": [afx.A1, afx.A2], "relationships": []}},
}


def test_differing_subject_and_advisor_id_resolves_correct_grant():
    """The goal stated by the cell: a delegator whose REAL advisor id differs from their email
    subject still resolves to their REAL current grant -- via `load_delegator_identity`, never
    a bare substitution of the subject into the advisor-id slot."""
    def identity_lookup(tenant, subject):
        return {DIFFERING_ADVISOR_EMAIL: DIFFERING_ADVISOR_ID}.get(subject)

    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2],
                            ownership=OWNERSHIP_DIFFERING_SUBJECT,
                            load_delegator_identity=identity_lookup)
    out = e.serve(_render_request(DIFFERING_ADVISOR_EMAIL, object_kind="account",
                                  object_id=afx.A1), _ok_payload)
    assert out.ok, out
    assert set(out.payload["accounts"]) == {afx.A1, afx.A2}

    # "matching what that human would get resolving their own identity directly": the SAME
    # `_scope.resolve` path, called with the human's REAL advisor id header (never the render
    # branch at all), must produce the SAME permitted set. `firm=afx.OPAQUE_FIRM`: the directory
    # join needs the OPAQUE spelling (exactly what `Enforcer.resolve_now` substitutes in before
    # ever calling `_scope.resolve` -- `afx.headers()`'s own default is the REGISTRY id, which
    # would join against nothing in `afx.DIRECTORY`).
    direct_headers = afx.headers(advisor_id=DIFFERING_ADVISOR_ID, email=DIFFERING_ADVISOR_EMAIL,
                                 firm=afx.OPAQUE_FIRM)
    direct_scope = rs.resolve(direct_headers, afx.DIRECTORY, OWNERSHIP_DIFFERING_SUBJECT,
                              policy=afx.POLICY, entitlement_revision=afx.ENTITLEMENT_REVISION)
    assert set(direct_scope["permitted_account_set"]) == set(out.payload["accounts"])


def test_without_the_loader_a_subject_that_is_not_the_real_advisor_id_still_refuses():
    """The FALLBACK (no `load_delegator_identity` configured) preserves the ORIGINAL behaviour
    -- a subject that is not itself a valid advisor id resolves to nothing, exactly as before
    this cell -- so BOUNDS (e)'s pre-existing fixtures (whose subject already equals the real
    advisor id) are unaffected, and this is not a silently-widened admission."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2],
                            ownership=OWNERSHIP_DIFFERING_SUBJECT)
    out = e.serve(_render_request(DIFFERING_ADVISOR_EMAIL, object_kind="account",
                                  object_id=afx.A1), _ok_payload)
    assert not out.ok and out.code == "EMPTY_GRANT", out


# =============================================================================================
# item (c): THE BUNDLE ID, ACTUALLY VERIFIED
# =============================================================================================
def test_bundle_id_mismatch_between_claimed_and_loaded_is_refused():
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2], bundle_id="bundle-real")
    out = e.serve(_render_request(afx.ADVISOR_A, bundle="bundle-claimed-wrong",
                                  object_kind="account", object_id=afx.A1), _ok_payload)
    assert not out.ok and out.code == "EMPTY_GRANT", out
    assert "bundle" in out.reason.lower()


def test_bundle_id_match_is_admitted():
    """Positive control beside the mismatch refusal above."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2], bundle_id="bundle-1")
    out = e.serve(_render_request(afx.ADVISOR_A, bundle="bundle-1",
                                  object_kind="account", object_id=afx.A1), _ok_payload)
    assert out.ok, out


def test_a_loader_that_declares_no_bundle_id_is_never_checked():
    """The pre-existing fixture shape (`{"account_ids": [...]}`, no `bundle_id` field) is left
    UNCHECKED -- never a refusal invented for a signal the loader never offered -- which is what
    keeps every pre-existing render-delegate fixture passing unmodified (BOUNDS (e))."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])   # bundle_id=None (default)
    out = e.serve(_render_request(afx.ADVISOR_A, bundle="whatever-the-caller-claims",
                                  object_kind="account", object_id=afx.A1), _ok_payload)
    assert out.ok, out


# =============================================================================================
# item (d): THE CACHE KEY, CLASS AND REVISION INCLUDED
# =============================================================================================
def test_cache_key_separates_by_revision_for_the_same_intersection():
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    req1 = _render_request(afx.ADVISOR_A, revision="rev-1", object_kind="account",
                           object_id=afx.A1)
    req2 = _render_request(afx.ADVISOR_A, revision="rev-2", object_kind="account",
                           object_id=afx.A1)
    scope1, refusal1 = e.resolve_now(req1)
    scope2, refusal2 = e.resolve_now(req2)
    assert refusal1 is None and refusal2 is None
    assert set(scope1["permitted_account_set"]) == set(scope2["permitted_account_set"]), (
        "the two requests must differ ONLY in revision for this to be a meaningful control")
    assert scope1["permitted_account_set_fingerprint"] != scope2["permitted_account_set_fingerprint"]
    key1 = e.cache_key_for(scope1, req1)
    key2 = e.cache_key_for(scope2, req2)
    assert key1 != key2


# =============================================================================================
# item (e): DO NOT REGRESS THE ALREADY-PASSING ARM -- the revocation control, reproduced fresh
# against THIS cell's corrected operation names (see IRPT_BCKEND-W19-S1: the OLD deliverable
# file's literal 'performance' default cannot pass post-rename, through no fault of the algebra)
# =============================================================================================
def test_revocation_control_still_passes():
    """A delegator whose entitlement is revoked between mint and read produces a narrower/empty
    intersection -- unmodified in expectation from IB-rtq-2's arm (2)."""
    e, deps = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    first = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                    _ok_payload)
    assert first.ok, first

    deps.revoke()
    second = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                     _ok_payload)
    assert not second.ok and second.code == "EMPTY_GRANT", second


def test_no_refusal_carries_protected_bytes():
    """COVERAGE over the refusal paths this cell touches, on the property that matters most: no
    account id leaks into a refusal's serialized envelope."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2], bundle_id="bundle-real")
    cases = [
        e.serve(_render_request(afx.ADVISOR_A, bundle="wrong-bundle",
                                object_kind="account", object_id=afx.A1), _ok_payload),
        e.serve(_render_request(DIFFERING_ADVISOR_EMAIL, object_kind="account",
                                object_id=afx.A1), _ok_payload),
    ]
    for out in cases:
        assert not out.ok
        blob = json.dumps(out.as_envelope())
        assert afx.A1 not in blob and afx.A2 not in blob
