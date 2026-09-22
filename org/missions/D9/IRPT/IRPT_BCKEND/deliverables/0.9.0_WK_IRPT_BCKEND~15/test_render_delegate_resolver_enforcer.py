"""New tests for cell IB-rtq-2 -- the RENDER_DELEGATE principal class in `_scope/resolve.py`,
its scope algebra in `_authz/enforce.py`'s `Enforcer.resolve_now`. Task order
IRPT_BCKEND.TO-IB-rtq-2, criterion R117-AC2.

Extends the SHAPE of the CVO's own offline reproducer
(`org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_PRD_v016_RENDER_PRINCIPAL_PROBE.py`)
rather than diverging from it: the same header set, the same classifier/enforcer call surface.
That file is NEVER imported here -- it PINS a historical commit and asserts the reviewed code
"has moved" if anything under `_scope`/`_authz` differs from it, so importing it against this
cell's now-fixed code would fail ITS OWN guard by design; `test_the_cvo_probes_exact_header_
set_now_flips_to_render_delegate_with_the_marker_added` below reproduces its header SHAPE by
hand instead.

BOUNDS: no existing assertion anywhere under `_scope/tests/` or `_authz/tests/` is edited by
this cell -- only NEW functions, in NEW files, are added by IB-rtq-2.
`test_the_pre_existing_scope_and_authz_suites_still_pass_unmodified` below is the direct proof
for arm (b)'s "runs the FULL existing test suite ... and confirms every pre-existing case
still classifies exactly as before": it shells out to `pytest` against the REAL
`_scope/tests/` and `_authz/tests/` directories and asserts rc == 0.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys

import pytest


def _find_repo_root(start):
    """Walk up from THIS file until the real `_scope/resolve.py` is found -- robust to
    exactly how deep this deliverable sits, immune to a hardcoded parent-count going stale."""
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
_SCOPE_TESTS_DIR = os.path.join(_SCOPE_DIR, "tests")
_AUTHZ_TESTS_DIR = os.path.join(_AUTHZ_DIR, "tests")


def _load_module(name, path):
    """Load a file as a module under an EXPLICIT, private name -- `_scope/tests/fixtures.py`
    and `_authz/tests/fixtures.py` share the basename `fixtures`, so a plain sys.path-based
    `import fixtures` can only ever hold ONE of the two at a time. This is needed for BOTH."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ----- the REAL `_scope` side: resolve.py + its own tests/fixtures.py -----
for _p in (_SCOPE_DIR, _SCOPE_TESTS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import resolve as rs                                                        # noqa: E402
fx = _load_module("_ib_rtq2_scope_fixtures", os.path.join(_SCOPE_TESTS_DIR, "fixtures.py"))

# ----- the REAL `_authz` side: enforce.py (which does its own internal sys.path insertion
# for `_scope`/`_keys`, already satisfied above) + its own tests/fixtures.py -----
for _p in (_AUTHZ_DIR, _KEYS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import enforce as ez                                                        # noqa: E402
afx = _load_module("_ib_rtq2_authz_fixtures", os.path.join(_AUTHZ_TESTS_DIR, "fixtures.py"))


# =============================================================================================
# arm (a): TRUSTED_HEADERS / trusted_only -- the CVO's v0.16 finding, reproduced and flipped
# =============================================================================================
def test_trusted_only_no_longer_drops_the_render_marker():
    """Reproduces the CVO's v0.16 finding (current code drops the three new markers) and
    confirms this cell's fix flips it -- same marker names as the L4-R review's 'Reproduced
    implementation boundary' section (synthetic X-Render-Delegator, X-Render-Bundle,
    X-Render-Revision)."""
    raw = {"X-Origin-Verify": "cloudfront", "X-User-Email": "render:fixture",
           "X-User-Role": "renderer", "X-Firm-Id": "49financial",
           "X-Render-Delegator": "advisor.a@49financial.com",
           "X-Render-Bundle": "bundle-1", "X-Render-Revision": "rev-1"}
    trusted, dropped = rs.trusted_only(raw)
    for marker in ("x-render-delegator", "x-render-bundle", "x-render-revision"):
        assert marker not in dropped, (marker, dropped)
        assert marker in trusted, (marker, trusted)


def test_render_markers_are_not_folded_into_trusted_headers_itself():
    """The three markers live in `RENDER_TRUSTED_HEADERS`, a SEPARATE table -- never a 10th,
    11th, 12th member of `TRUSTED_HEADERS`, which two pre-existing tests hard-code at exactly
    nine (BOUNDS forbids changing either test's expected value)."""
    assert len(rs.TRUSTED_HEADERS) == 9
    assert "x-render-delegator" not in rs.TRUSTED_HEADERS
    assert "x-render-bundle" not in rs.TRUSTED_HEADERS
    assert "x-render-revision" not in rs.TRUSTED_HEADERS
    assert set(rs.RENDER_TRUSTED_HEADERS) == {
        "x-render-delegator", "x-render-bundle", "x-render-revision"}


# =============================================================================================
# arm (b): the RENDER_DELEGATE branch in classify_principal
# =============================================================================================
def _render_headers(delegator="advisor.a@49financial.com", bundle="bundle-1", revision="rev-1",
                    role="renderer", email="render:r-1", extra=None):
    h = {"X-Origin-Verify": "cloudfront", "X-User-Email": email, "X-User-Role": role,
         "X-Firm-Id": "49financial"}
    if delegator is not None:
        h["X-Render-Delegator"] = delegator
    if bundle is not None:
        h["X-Render-Bundle"] = bundle
    if revision is not None:
        h["X-Render-Revision"] = revision
    h.update(extra or {})
    return h


def test_renderer_with_full_marker_classifies_render_delegate():
    trusted, _ = rs.trusted_only(_render_headers())
    cls, reason = rs.classify_principal(trusted)
    assert cls == "RENDER_DELEGATE", (cls, reason)
    assert "render marker" in reason


def test_renderer_without_any_marker_is_unknown_arm_j():
    trusted, _ = rs.trusted_only(_render_headers(delegator=None, bundle=None, revision=None))
    cls, reason = rs.classify_principal(trusted)
    assert cls == "UNKNOWN", (cls, reason)
    assert "renderer" in reason and "marker" in reason


@pytest.mark.parametrize("missing", ["delegator", "bundle", "revision"])
def test_renderer_with_a_partial_marker_is_unknown_never_a_best_effort_delegate(missing):
    kwargs = {"delegator": "advisor.a@49financial.com", "bundle": "bundle-1",
             "revision": "rev-1"}
    kwargs[missing] = None
    trusted, _ = rs.trusted_only(_render_headers(**kwargs))
    cls, reason = rs.classify_principal(trusted)
    assert cls == "UNKNOWN", (missing, cls, reason)
    assert ("x-render-" + missing) in reason


def test_renderer_with_no_origin_or_no_subject_is_unknown_like_anyone_else():
    """RENDER_DELEGATE sits AFTER branch 1 -- the edge marker and a subject are still
    required first, exactly as for every other class."""
    no_origin, _ = rs.trusted_only(_render_headers(extra={"X-Origin-Verify": ""}))
    assert rs.classify_principal(no_origin)[0] == "UNKNOWN"
    no_subject, _ = rs.trusted_only(_render_headers(email=""))
    assert rs.classify_principal(no_subject)[0] == "UNKNOWN"


def test_render_delegate_never_falls_through_to_a_human_class():
    """Even with an OPAL roster hit and a client user-type also present, the renderer branch
    is checked FIRST and returns before any later branch is consulted."""
    trusted, _ = rs.trusted_only(_render_headers(email="render:r-1",
                                                 extra={"X-User-Type": "Client"}))
    cls, _ = rs.classify_principal(trusted, opal_principal_ids={"render:r-1"})
    assert cls == "RENDER_DELEGATE"


def test_render_delegate_is_a_member_of_principal_classes():
    assert "RENDER_DELEGATE" in rs.PRINCIPAL_CLASSES


def test_the_cvo_probes_exact_header_set_now_flips_to_render_delegate_with_the_marker_added():
    """Same BASE header set as the CVO's v0.16 probe (x-origin-verify=cloudfront,
    x-firm-id=49financial, x-user-role=renderer, x-user-tier=render), which classified UNKNOWN
    with no subject AND with a subject alone -- reproduced here unchanged. This cell's fix
    adds ONLY the verified render marker and confirms RENDER_DELEGATE."""
    base = {"x-origin-verify": "cloudfront", "x-firm-id": "49financial",
            "x-user-role": "renderer", "x-user-tier": "render"}
    exact = rs.classify_principal(base)
    with_subject = rs.classify_principal(dict(base, **{"x-user-email": "render-fixture"}))
    assert exact[0] == with_subject[0] == "UNKNOWN", (exact, with_subject)

    with_marker = rs.classify_principal(dict(base, **{
        "x-user-email": "render-fixture", "x-render-delegator": "advisor.a@49financial.com",
        "x-render-bundle": "bundle-1", "x-render-revision": "rev-1"}))
    assert with_marker[0] == "RENDER_DELEGATE", with_marker


# =============================================================================================
# arm (b), continued: the FULL pre-existing suites still pass, UNMODIFIED
# =============================================================================================
def test_the_pre_existing_scope_and_authz_suites_still_pass_unmodified():
    """Runs the FULL existing `_scope/tests/` and `_authz/tests/` suites as a subprocess and
    asserts rc == 0 for each -- the direct proof that every pre-existing case still classifies
    (and enforces) exactly as before this cell's edits."""
    for tests_dir in (_SCOPE_TESTS_DIR, _AUTHZ_TESTS_DIR):
        result = subprocess.run(
            [sys.executable, "-m", "pytest", tests_dir, "-q"],
            cwd=_REPO_ROOT, capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, (
            tests_dir, result.returncode, result.stdout[-4000:], result.stderr[-2000:])


# =============================================================================================
# arm (c): the Enforcer's RENDER_DELEGATE scope algebra -- THREE ARMS
# =============================================================================================
def _bundle_loader(pinned_account_ids):
    def _load(tenant, revision):
        return {"account_ids": list(pinned_account_ids)}
    return _load


def _render_request(delegator, revision="rev-1", operation="performance",
                    object_kind=None, object_id=None, bundle="bundle-1"):
    headers = {"X-Origin-Verify": "cloudfront", "X-User-Email": "render:r-1",
              "X-User-Role": "renderer", "X-Firm-Id": afx.TENANT}
    if delegator is not None:
        headers["X-Render-Delegator"] = delegator
    headers["X-Render-Bundle"] = bundle
    headers["X-Render-Revision"] = revision
    return ez.Request(headers, operation, object_kind, object_id)


def _render_enforcer(pinned_accounts, ownership=None):
    deps = afx.Deps(ownership=ownership)
    binding = ez.FirmBinding(afx.TENANT, afx.OPAQUE_FIRM)
    e = ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                    load_render_bundle=_bundle_loader(pinned_accounts))
    return e, deps


def _ok_payload(scope):
    return {"accounts": list(scope["permitted_account_set"])}


def test_arm1_entitled_delegator_and_pinned_object_the_three_reads_succeed():
    """(1) delegator currently entitled + object inside the pinned/bundle scope -> the three
    read operations succeed."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    for operation, object_id in (("performance", afx.A1), ("analysis_sections", afx.A2),
                                 ("narrative", afx.A1)):
        req = _render_request(afx.ADVISOR_A, operation=operation, object_kind="account",
                              object_id=object_id)
        out = e.serve(req, _ok_payload)
        assert out.ok, (operation, out)
        assert set(out.payload["accounts"]) == {afx.A1, afx.A2}


def test_arm2_delegator_revoked_between_mint_and_read_is_refused():
    """(2) delegator's entitlement revoked (simulate by having the 'resolved now' call return
    an empty/narrower scope) -> refused. Proves the algebra re-resolves the delegator EVERY
    time rather than trusting a stale grant."""
    e, deps = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    first = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                    _ok_payload)
    assert first.ok, first

    deps.revoke()
    second = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                     _ok_payload)
    assert not second.ok and second.code == "EMPTY_GRANT", second


def test_arm3a_an_object_outside_the_bundles_pinned_scope_is_refused():
    """(3) an object outside the bundle's pinned scope ... is refused -- even though it IS
    inside the delegator's own current grant (A2 sits in advisor A's ownership, but is not
    pinned by THIS bundle)."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1])
    out = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A2),
                 _ok_payload)
    assert not out.ok and out.code == "OBJECT_NOT_COVERED", out


def test_arm3b_an_operation_outside_the_three_is_refused():
    """(3) ... or any operation outside the three, is refused -- before the scope algebra even
    runs."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    out = e.serve(_render_request(afx.ADVISOR_A, operation="directory_search",
                                  object_kind="account", object_id=afx.A1), _ok_payload)
    assert not out.ok and out.code == "OBJECT_NOT_COVERED", out
    assert "RENDER_DELEGATE" in out.reason


def test_an_empty_intersection_is_a_refusal_never_an_empty_but_successful_answer():
    """The bundle pins accounts the delegator does NOT currently hold -- intersection empty."""
    e, _ = _render_enforcer(pinned_accounts=[afx.A5])   # advisor B's account, not A's
    out = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A5),
                 _ok_payload)
    assert not out.ok and out.code == "EMPTY_GRANT", out


def test_no_delegator_subject_refuses_no_principal():
    e, _ = _render_enforcer(pinned_accounts=[afx.A1])
    out = e.serve(_render_request(None, object_kind="account", object_id=afx.A1), _ok_payload)
    assert not out.ok and out.code == "NO_PRINCIPAL", out


def test_no_bundle_loader_configured_refuses_rather_than_serving_unpinned():
    """`load_render_bundle` defaults to None -- an unconfigured Enforcer must REFUSE a
    RENDER_DELEGATE, never serve an unpinned (unlimited) scope."""
    binding = ez.FirmBinding(afx.TENANT, afx.OPAQUE_FIRM)
    deps = afx.Deps()
    e = ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy)
    out = e.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                 _ok_payload)
    assert not out.ok and out.code == "EMPTY_GRANT", out


def test_no_refusal_carries_protected_bytes_for_a_render_delegate():
    """COVERAGE over the render-delegate refusal paths, on the property that matters most."""
    import json
    e_revoked, deps = _render_enforcer(pinned_accounts=[afx.A1, afx.A2])
    e_revoked.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                    _ok_payload)
    deps.revoke()
    cases = [
        e_revoked.serve(_render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A1),
                        _ok_payload),
    ]
    e_outside, _ = _render_enforcer(pinned_accounts=[afx.A1])
    cases.append(e_outside.serve(
        _render_request(afx.ADVISOR_A, object_kind="account", object_id=afx.A2), _ok_payload))
    for out in cases:
        assert not out.ok
        blob = json.dumps(out.as_envelope())
        # The real property: no ACCOUNT ID VALUE leaks. (A field NAMED "granted_accounts"
        # carrying a zero COUNT is not a leak -- `_scope.resolve()`'s own generic census
        # vocabulary, harmless because it is a number, never an id.)
        assert afx.A1 not in blob and afx.A2 not in blob
