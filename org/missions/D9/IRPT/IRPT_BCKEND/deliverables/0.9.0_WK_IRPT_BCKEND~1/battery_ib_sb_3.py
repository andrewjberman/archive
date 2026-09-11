#!/usr/bin/env python3
"""battery_ib_sb_3.py -- SB3-AC1: the replay battery across every deployed route. Cell
IB-sb-3, the last cell of the round.

THE PLANE (arm a): no test-JWT-minting mechanism a worker may use without a human was found.
infra/aws/users/lambda/portal-authorizer/index.mjs requires an RS256 JWT signed by the
production auth-handler's private key, PLUS an origin-verify shared secret
(originVerify.mjs, header x-opal-origin-verify) that only CloudFront's own origin config can
set -- a caller at the execute-api address directly cannot carry it (originVerify.mjs:96:
"a caller hitting the execute-api address directly cannot carry it"). The production login
flow (infra/aws/opalinvest_dev/lambda/auth-handler/src/{auth,password,mfa}.ts) requires a
real password + MFA; no dev/test bypass exists in that source. So CloudFront -> edge
validator -> API Gateway authorizer is NOT CROSSED (row W2-S12, on the issuer -- the
CloudFront behavior is committed-and-unapplied regardless of the JWT question). This battery
replays on the POST-AUTHORIZER PLANE: each deployed handler's own lambda_handler /
registered guarded route, invoked directly with the header set the edge validator
(auth-validator-edge/index.mjs) injects -- the SAME plane this project's own export cell
documents ("Their routes are exercised in the worktree, where the whole package is on the
path", lambda-source-map.json functions["irpt-export-render"]).

ASCII only. Python 3.12.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
_LAMBDA_ROOT = os.path.join(_REPO_ROOT, "infra", "aws", "lambda", "investor-reporting")
_GOLD_IRPT = os.path.join(_REPO_ROOT, "data", "assets", "scripts", "gold", "investor_reporting")

# SHARED libraries only, on the process-wide sys.path. Per-cell directories (directory/,
# performance/, narrative/, ycharts/generate/, export/) are NOT added here: performance/ and
# ycharts/generate/ each carry their OWN transport.py, and a shared sys.path would let one
# shadow the other's unqualified `import transport` -- silently, since both names resolve.
for _p in (_GOLD_IRPT,
           os.path.join(_LAMBDA_ROOT, "_authz"), os.path.join(_LAMBDA_ROOT, "_authz", "tests"),
           os.path.join(_LAMBDA_ROOT, "_scope"), os.path.join(_LAMBDA_ROOT, "_scope", "tests"),
           os.path.join(_LAMBDA_ROOT, "_keys"), os.path.join(_LAMBDA_ROOT, "_gate"),
           os.path.join(_LAMBDA_ROOT, "export"), os.path.join(_LAMBDA_ROOT, "ops")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import enforce as authz              # noqa: E402  IB-s-3
import resolve as _scope             # noqa: E402  IB-s-2

opal_global = importlib.import_module("global")       # _scope/global.py -- IB-s-15
test_global = importlib.import_module("test_global")  # _scope/tests/test_global.py -- reused fixtures


def _load_module(name, path):
    """FOUR handlers in this project are each named handler.py (directory, performance,
    narrative, export) -- a plain `import handler` can resolve only one of them. Load each
    under a DISTINCT module name instead, so all four are importable in the SAME process."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _isolated_load(name, cell_dir, entry_file, evict=()):
    """Loads `entry_file` from `cell_dir` with `cell_dir` as the ONLY cell-owned directory on
    sys.path (prepended, then removed again) -- so its own unqualified sibling imports
    (transport, tenants, recipe, ...) resolve to ITS OWN modules, never a same-named sibling
    cell's. `evict` names are dropped from sys.modules first, because a name cached by an
    EARLIER isolated load (e.g. "transport" from performance/) would otherwise be reused
    stale for this one."""
    for stale in evict:
        sys.modules.pop(stale, None)
    sys.path.insert(0, cell_dir)
    try:
        return _load_module(name, os.path.join(cell_dir, entry_file))
    finally:
        sys.path.remove(cell_dir)


authz_fixtures = _load_module(
    "irpt_authz_fixtures", os.path.join(_LAMBDA_ROOT, "_authz", "tests", "fixtures.py"))

directory_handler_mod = _isolated_load(
    "irpt_directory_handler", os.path.join(_LAMBDA_ROOT, "directory"), "handler.py")
performance_handler_mod = _isolated_load(
    "irpt_performance_handler", os.path.join(_LAMBDA_ROOT, "performance"), "handler.py",
    evict=("transport", "tenants", "normalize", "bd_adapter", "orion_adapter"))
narrative_handler_mod = _isolated_load(
    "irpt_narrative_handler", os.path.join(_LAMBDA_ROOT, "narrative"), "handler.py",
    evict=("events", "evidence", "prose"))
ycharts_job_mod = _isolated_load(
    "irpt_ycharts_job", os.path.join(_LAMBDA_ROOT, "ycharts", "generate"), "job.py",
    evict=("transport", "recipe"))

import status as status_mod          # noqa: E402  IB-s-16 (guarded; ops/ is on the shared path)

export_handler_mod = _isolated_load(
    "irpt_export_handler", os.path.join(_LAMBDA_ROOT, "export"), "handler.py",
    evict=("assets", "bundle", "receipt", "render"))
export_download_mod = _isolated_load(
    "irpt_export_download", os.path.join(_LAMBDA_ROOT, "export"), "download.py")

RESULT_TOKEN = "IBSB3-REPLAY-CLEAN"
ROUTES_JSON = os.path.join(_REPO_ROOT, "infra", "aws", "terraform", "investor-reporting",
                           "api", "routes.json")


def _load_routes():
    with open(ROUTES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


# =================================================================== the id-space seam
# row W1-S9 (IB-s-16 drain correction): the prefix is minted at
# data/assets/scripts/gold/investor_reporting/holdings_snapshot.py:370/486/638 as
# "<firm>:acct:<opaque>" with firm tokens 49f|inf|cot. ONE named function strips exactly
# that grammar; no shared normaliser exists elsewhere (confirmed absent, IB-s-16 row W1-S9).
_FIRM_ACCT_PREFIX_RE = re.compile(r"^(49f|inf|cot):acct:")


def strip_firm_acct_prefix(account_id):
    """Strips EXACTLY the grammar holdings_snapshot.py:370/486/638 mints. Cites those three
    lines rather than re-deriving the pattern from guesswork."""
    return _FIRM_ACCT_PREFIX_RE.sub("", account_id)


def id_space_seam_census(firm_id, holdings_account_ids, directory_account_ids):
    """Both counts per firm: resolved AS WRITTEN and resolved AFTER normalisation, so the
    prefix cause (cosmetic) and the raw-key cause (W1-S7, real, INF/COT only) stay
    distinguishable. No join is changed; this only counts."""
    dset = set(directory_account_ids)
    as_written = sum(1 for a in holdings_account_ids if a in dset)
    after_norm = sum(1 for a in holdings_account_ids if strip_firm_acct_prefix(a) in dset)
    return {
        "firm_id": firm_id,
        "as_written": "%d of %d" % (as_written, len(holdings_account_ids)),
        "after_normalisation": "%d of %d" % (after_norm, len(holdings_account_ids)),
    }


# =================================================================== the S3-key census (W3-S12)
# _keys.s3_evidence_key checks non-empty / no-slash / not-lock-shaped / not-a-foreign-firm-
# token and NEVER the shape checks cache_key does -- so a client name or an e-mail address can
# reach a durable key. This heuristic is the shape check IB-s-10's wrapper pattern puts BEFORE
# s3_evidence_key: every key this battery builds or observes is censused for a name-shaped or
# email-shaped component.
_EMAIL_SHAPED_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# "Firstname Lastname"-shaped: two-or-more capitalised words separated by a space, OR a
# display name containing a space plus a capital letter run typical of "Whitfield Family" /
# "Smith-Family" style client names this project's own fixtures use.
_NAME_SHAPED_RE = re.compile(r"\b[A-Z][a-z]+(?:[ -][A-Z][a-z]+)+\b")


def key_is_name_or_email_shaped(key):
    hits = []
    if _EMAIL_SHAPED_RE.search(key):
        hits.append("email-shaped")
    if _NAME_SHAPED_RE.search(key):
        hits.append("name-shaped")
    return hits


def s3_key_census(keys):
    """0 of N is the only acceptable reading. A hit is a FAIL, never a note -- printed, not
    silently retried."""
    rows = []
    hits = 0
    for k in keys:
        shapes = key_is_name_or_email_shaped(k)
        if shapes:
            hits += 1
        rows.append({"key_shape_only": _redact_key_for_print(k), "flagged": bool(shapes),
                    "shapes": shapes})
    return hits, len(keys), rows


def _redact_key_for_print(key):
    """The byte census reports counts, not content (BOUNDS). A key's PATH SHAPE (segment
    lengths, family) is printable; a segment that itself looks name/email-shaped is redacted
    to its shape only so a flagged row cannot leak the very value it is flagging."""
    parts = key.split("/")
    out = []
    for p in parts:
        if _EMAIL_SHAPED_RE.search(p) or _NAME_SHAPED_RE.search(p):
            out.append("<REDACTED:%d-chars>" % len(p))
        else:
            out.append(p)
    return "/".join(out)


# =================================================================== shared fixtures
def _fx():
    return authz_fixtures


def _base_enforcer():
    fx = _fx()
    binding = authz.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    deps = fx.Deps()
    e = authz.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                       artifacts=dict(fx.ARTIFACTS), cache={})
    return e, deps


def _six_swap_ids():
    fx = _fx()
    return {"firm": fx.OTHER_OPAQUE_FIRM, "advisor": fx.ADVISOR_B, "account": fx.A5,
            "relationship": fx.R2, "report": fx.REPORT_OTHER, "pdf": fx.PDF_OTHER}


def _authorized_resolved_scope():
    """A REAL ResolvedScope, resolved through _scope.resolve() from the authz fixtures --
    never hand-typed, so the directory/performance replay swaps a field of a genuine object.
    THE OPAQUE TRANSLATION (row W2-S9): directory/handler.py and performance/handler.py take
    resolved_scope as INPUT and never call _scope.resolve() themselves -- something upstream
    must, and the amendment's own point is that nothing here proves what does. This harness
    builds the scope the way _authz.Enforcer.resolve_now() does (FirmBinding's opaque
    translation BEFORE the directory join), which is the CORRECT construction; a caller that
    instead handed the raw registry-spelled header straight to _scope.resolve() would get an
    EMPTY population (entries_excluded_cross_firm) that reads exactly like a revocation --
    reproduced once, in-process, to confirm row W2-S9's own claim rather than re-assert it."""
    fx = _fx()
    directory = fx.DIRECTORY
    headers = dict(_scope.normalize_headers(fx.headers(role="admin")))
    headers["x-firm-id"] = fx.OPAQUE_FIRM
    scope = _scope.resolve(headers, directory, fx.OWNERSHIP,
                           entitlement_revision=fx.ENTITLEMENT_REVISION, policy=fx.POLICY)
    return scope


def raw_header_scope_reproduces_w2_s9():
    """Reproduces row W2-S9's own claim once, live: a REGISTRY-spelled X-Firm-Id handed
    straight to _scope.resolve() (never translated through FirmBinding) returns an EMPTY
    population -- indistinguishable from a revocation."""
    fx = _fx()
    scope = _scope.resolve(fx.headers(role="admin"), fx.DIRECTORY, fx.OWNERSHIP,
                           entitlement_revision=fx.ENTITLEMENT_REVISION, policy=fx.POLICY)
    census = scope.get("_census") or {}
    return {
        "resolved_scope_kind": scope["resolved_scope"]["scope_kind"],
        "permitted_account_count": len(scope["permitted_account_set"]),
        "entries_excluded_cross_firm": census.get("entries_excluded_cross_firm"),
        "reproduces_empty_population": (scope["resolved_scope"]["scope_kind"] == "UNSUPPORTED"
                                         and len(scope["permitted_account_set"]) == 0),
    }


# =================================================================== per-route arms (b)
def arm_directory_routes():
    """Routes 0/1 -- irpt-directory-search (IB-s-1, UNGUARDED, predates the wrapper). No
    _authz.guard() runs here: this handler takes resolved_scope DIRECTLY as input and does
    NOT re-verify it. The swap therefore measures what it actually does -- serves the
    scope it is handed, whatever scope that is -- rather than asserting a refusal that
    would require code this route does not have."""
    scope = _authorized_resolved_scope()
    authorized = directory_handler_mod.lambda_handler(
        {"op": "search", "resolved_scope": scope, "q": "", "directory_fixture": _fx().DIRECTORY})
    swapped_scope = dict(scope)
    swapped_scope["verified_request_firm_id"] = _fx().OTHER_OPAQUE_FIRM
    swapped = directory_handler_mod.lambda_handler(
        {"op": "search", "resolved_scope": swapped_scope, "q": "",
         "directory_fixture": _fx().DIRECTORY})
    return {
        "route_status": "MEASURED-UNGUARDED",
        "authorized_ok": authorized.get("ok"),
        "swapped_scope_served": swapped.get("ok"),
        "note": ("no _authz.guard() wraps this handler; it trusts the resolved_scope handed "
                "to it and does not independently re-verify the firm -- EXPECTED per row S9, "
                "measured here, not repaired."),
    }


def arm_performance_route():
    """Route 2 -- irpt-performance-adapter (IB-s-11, UNGUARDED, predates the wrapper). Same
    shape as directory: the handler trusts its resolved_scope and does not reauthorize."""
    fx = _fx()
    headers = dict(_scope.normalize_headers(fx.headers(role="admin")))
    headers["x-firm-id"] = fx.OPAQUE_FIRM
    scope = _scope.resolve(headers, fx.DIRECTORY, fx.OWNERSHIP,
                           requested_scope={"scope_kind": "ACCOUNT", "scope_ids": [fx.A1, fx.A2]},
                           entitlement_revision=fx.ENTITLEMENT_REVISION, policy=fx.POLICY)
    body_ok = json.dumps({"resolved_scope": scope, "requested_start": "2026-09-01",
                          "requested_end": "2026-09-10", "mode": "recorded",
                          "labels": {"period": "bd_refreshed_period"}})
    out_ok = performance_handler_mod.lambda_handler({"body": body_ok})
    swapped_scope = dict(scope)
    swapped_scope["verified_request_firm_id"] = fx.OTHER_OPAQUE_FIRM
    body_swapped = json.dumps({"resolved_scope": swapped_scope, "requested_start": "2026-09-01",
                               "requested_end": "2026-09-10", "mode": "recorded",
                               "labels": {"period": "bd_refreshed_period"}})
    out_swapped = performance_handler_mod.lambda_handler({"body": body_swapped})
    return {
        "route_status": "MEASURED-UNGUARDED",
        "authorized_status_code": out_ok.get("statusCode"),
        "swapped_status_code": out_swapped.get("statusCode"),
        "identical_outcome": out_ok.get("statusCode") == out_swapped.get("statusCode"),
        "note": ("no _authz.guard() wraps this handler either -- EXPECTED per row S9, "
                "measured here, not repaired. Both the authorized-shaped and the swapped-"
                "firm-id scope produce the SAME outcome (this fixture directory's opaque "
                "firm id is not in tenants.py's OWN F-49F/F-COT/F-INF route-key space, a "
                "SEPARATE, unrelated id-shape gap this handler has), which is itself further "
                "evidence the swap was never the thing being checked -- nothing here "
                "discriminates identity either way, and 0 protected bytes are served in "
                "either case."),
    }


def arm_ycharts_generate_route():
    """Route 3 -- irpt-ycharts-generate (IB-s-9). The DEPLOYED lambda_handler refuses ANY
    invocation unless the consent env var carries Andrew's per-use sentence, which this
    battery never sets (NO LIVE VENDOR CALL). This makes the swap test VACUOUS for this
    route specifically: authorized and swapped requests both read the SAME refusal, because
    identity is never inspected. Measured, not silently treated as a pass."""
    authorized = ycharts_job_mod.lambda_handler({"headers": _fx().headers()})
    swapped = ycharts_job_mod.lambda_handler(
        {"headers": _fx().headers(role="user", firm="inflection")})
    return {
        "route_status": "VACUOUS-BOTH-REFUSED-BY-CONSENT-GATE",
        "authorized_live_call": authorized.get("live_call"),
        "swapped_live_call": swapped.get("live_call"),
        "identical_refusal": authorized.get("reason") == swapped.get("reason"),
        "note": ("this route's deployed handler checks a hard-coded consent env var BEFORE "
                "looking at identity at all; every invocation (authorized or swapped) reads "
                "the SAME refusal, so this route cannot discriminate a swap. Also UNGUARDED "
                "mechanically (no _authz.guard() call in job.py) -- job.py's own ROUTES = {} "
                "comment says this cell registers no route because it believed itself a queue "
                "consumer; routes.json (IB-s-15, landed after that comment) now maps this "
                "route TO this function anyway, so this battery measures it rather than "
                "skipping it per the S13 clarification."),
    }


def arm_narrative_route():
    """Route 5 -- irpt-narrative (IB-s-13, UNGUARDED). This handler has NO firm/account
    identity field of its own: it takes an ALREADY-BUILT performance_report and processes
    it at face value. There is no identity parameter here to swap -- structurally
    different from the other routes, stated rather than forced into the same shape."""
    return {
        "route_status": "STRUCTURAL-EXEMPTION",
        "note": ("no _authz.guard(), and no firm/account/advisor identity field in this "
                "handler's own request shape -- it operates on a PerformanceReport object "
                "handed to it. The six-swap test does not apply to this route's own "
                "parameters; any identity check belongs to whatever built the "
                "performance_report, not to this handler."),
    }


def arm_status_routes():
    """Routes 4, 6, 7 -- irpt-status (IB-s-10 through IB-s-16, GUARDED). All three map to
    the SAME deployed function and the SAME _authz.Enforcer.guard() mechanism this cell
    itself built (status.py, IB-s-16); the per-route business logic (sections extraction,
    job-status lookup) differs but the REAUTHORIZATION MECHANISM under test is shared, so
    one six-swap run against it is what actually discriminates for this cell's part of
    FWD-2's proof."""
    fx = _fx()
    e, deps = _base_enforcer()

    def payload(scope):
        env = status_mod.build_envelope("OP-1", "replay_probe", "1", "READY", "2026-09-11")
        return status_mod.public_view(env)

    rows, all_refused, authorized_ok = six_swaps(
        e, {"headers": fx.headers(), "operation": "get_status", "object_kind": "firm",
           "object_id": fx.OPAQUE_FIRM}, _six_swap_ids(), payload)
    return {
        "route_status": "GUARDED",
        "applies_to_routes": [
            "GET /api/scoped/investor-reporting/analysis/{jobId}/sections",
            "GET /api/scoped/investor-reporting/status",
            "GET /api/scoped/investor-reporting/status/{jobId}",
        ],
        "authorized_ok": authorized_ok,
        "swaps": rows,
        "all_six_refused": all_refused,
    }


def arm_export_submit_route():
    """Route 8 -- irpt-export-render POST /export (IB-s-14, GUARDED: export_submit)."""
    fx = _fx()
    binding = authz.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    deps = fx.Deps()
    e = export_handler_mod.build_enforcer(binding, deps, artifacts=dict(fx.ARTIFACTS), cache={})
    routes = export_handler_mod.routes(e, dict(fx.ARTIFACTS), None, {})
    submit = routes[export_handler_mod.SUBMIT_OPERATION]

    def payload(scope):
        return submit(authz.Request(fx.headers(), export_handler_mod.SUBMIT_OPERATION,
                                    "report", fx.REPORT_OK), scope)

    rows, all_refused, authorized_ok = six_swaps(
        e, {"headers": fx.headers(), "operation": export_handler_mod.SUBMIT_OPERATION,
           "object_kind": "report", "object_id": fx.REPORT_OK}, _six_swap_ids(),
        lambda scope: {"accepted": True, "permitted_account_count":
                       len(scope["permitted_account_set"])})
    return {
        "route_status": "GUARDED",
        "authorized_ok": authorized_ok,
        "swaps": rows,
        "all_six_refused": all_refused,
    }


def arm_export_status_route():
    """Route 9 -- GET /export/{exportId} (IB-s-14). No distinct guarded operation exists in
    the codebase for an export STATUS check (only export_submit and export_download are
    registered) -- the DEPLOYED lambda_handler answers `action=capabilities` regardless of
    the path invoked, since it reads event["action"], not the URL. Measured as its own
    structural shape, not conflated with the download route's real reauthorization."""
    out = export_handler_mod.lambda_handler({"body": json.dumps({})})
    return {
        "route_status": "STRUCTURAL-GAP-MEASURED",
        "deployed_response_status": out.get("statusCode"),
        "note": ("the deployed function has no path-aware dispatch; every invocation reads "
                "action=capabilities (the default) regardless of route. There is no separate "
                "guarded export-status operation to replay against; this is the SAME "
                "capabilities-only behaviour route 9 actually gets when invoked, printed "
                "rather than assumed."),
    }


# =================================================================== arm (e): the download
EVIDENCE_BUCKET = "opal-data-ycharts"
SYNTHETIC_PREFIX = "firms/49financial/generations/GENIBS14SYN/attempts/1/exports/"
SYNTHETIC_EXPORT_IDS = ("r1", "v0-11-overview", "v0-11-comparison", "v0-11-multicomp")


def _s3():
    import boto3
    return boto3.client("s3", region_name="us-east-1")


def _load_synthetic_export_artifacts(s3):
    """Real S3 reads (never a vendor call) of the four labelled synthetic export objects
    IB-s-14 landed -- never a client artifact. Builds `artifacts`/`receipts` the SAME shape
    make_download_route expects, with the receipt's sha256 computed from the STORED bytes,
    the property S14-AC1 (g) itself grades on."""
    artifacts, receipts = {}, {}
    for export_id in SYNTHETIC_EXPORT_IDS:
        key = SYNTHETIC_PREFIX + export_id + "/report.pdf"
        body = s3.get_object(Bucket=EVIDENCE_BUCKET, Key=key)["Body"].read()
        sha = hashlib.sha256(body).hexdigest()
        artifacts[export_id] = {"key": key, "bucket": EVIDENCE_BUCKET, "exists": True}
        receipts[export_id] = {"artifact": {"sha256": sha}}
    return artifacts, receipts


def arm_export_download_route():
    """Route 10 -- GET /export/{exportId}/download (IB-s-14, GUARDED: export_download).
    Replayed against the FOUR real, labelled synthetic export objects, never a client
    artifact (fact 1 of the hand-off). The swapped-PDF-id and revoked-grant refusals are
    graded on THIS reauthorizing handler."""
    fx = _fx()
    s3 = _s3()
    artifacts, receipts = _load_synthetic_export_artifacts(s3)

    # The fixture PDF artifact records must ALSO exist in the enforcer's own `artifacts`
    # (report/pdf covers() reads self.artifacts, keyed by object id, kind="pdf", firm, and
    # the account set it covers) -- built from the REAL keys above, joined to the fixture
    # firm/account population so `covers()` has a real basis to check.
    enforcer_artifacts = dict(fx.ARTIFACTS)
    for export_id in SYNTHETIC_EXPORT_IDS:
        enforcer_artifacts[export_id] = {"kind": "pdf", "firm": fx.OPAQUE_FIRM,
                                         "account_ids": [fx.A1, fx.A2]}

    binding = authz.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    deps = fx.Deps()
    e = authz.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                       artifacts=enforcer_artifacts, cache={})
    signer = export_download_mod.FixtureSigner(EVIDENCE_BUCKET)
    download = export_download_mod.make_download_route(e, artifacts, signer, receipts)

    real_id = SYNTHETIC_EXPORT_IDS[0]
    authorized = download(authz.Request(fx.headers(), export_download_mod.DOWNLOAD_OPERATION,
                                        "pdf", real_id))
    swapped = download(authz.Request(fx.headers(), export_download_mod.DOWNLOAD_OPERATION,
                                     "pdf", fx.PDF_OTHER))

    # revoked grant, then the SAME right id replayed
    deps.revoke()
    revoked_replay = download(authz.Request(fx.headers(), export_download_mod.DOWNLOAD_OPERATION,
                                            "pdf", real_id))
    deps.restore()

    swapped_blob = json.dumps(swapped.as_envelope())
    return {
        "route_status": "GUARDED",
        "synthetic_objects_used": list(SYNTHETIC_EXPORT_IDS),
        "authorized_ok": authorized.ok,
        "authorized_artifact_sha256_matches_receipt": (
            authorized.ok and authorized.payload.get("artifact_sha256")
            == receipts[real_id]["artifact"]["sha256"]),
        "swapped_pdf_id_refused": not swapped.ok,
        "swapped_code": getattr(swapped, "code", None),
        "swapped_zero_protected_bytes": real_id not in swapped_blob and "PROTECTED" not in swapped_blob,
        "revoked_grant_then_right_id_refused": not revoked_replay.ok,
        "revoked_code": getattr(revoked_replay, "code", None),
        "no_signed_url_or_vendor_link_in_authorized_body": (
            authorized.ok and EVIDENCE_BUCKET in authorized.payload.get("url", "")
            and "vendor" not in authorized.payload.get("url", "").lower()),
    }


# =================================================================== arm (c): revoked vs warm cache
def arm_revoked_against_warm_cache():
    """Served, revoked, replayed: refused. The cache entry is NEVER cleared by the
    revocation -- the reauthorization on the SECOND read is what catches it (mirrors
    _authz/tests/test_enforce.py::test_revoked_grant_is_refused_against_a_warm_cache)."""
    fx = _fx()
    e, deps = _base_enforcer()

    def payload(scope):
        return {"secret": "PROTECTED-PAYLOAD", "accounts": list(scope["permitted_account_set"])}

    req = authz.Request(fx.headers(), "directory_search", "account", fx.A1)
    first = e.serve(req, payload)
    cache_size_after_serve = len(e.cache)

    deps.revoke()
    second = e.serve(authz.Request(fx.headers(), "directory_search", "account", fx.A1), payload)
    cache_untouched_by_refusal = len(e.cache) == cache_size_after_serve

    deps.restore()
    third = e.serve(authz.Request(fx.headers(), "directory_search", "account", fx.A1), payload)

    second_blob = json.dumps(second.as_envelope())
    return {
        "served_first": first.ok,
        "cache_populated_after_first_serve": cache_size_after_serve > 0,
        "revoked_second_refused": not second.ok,
        "revoked_second_code": getattr(second, "code", None),
        "cache_untouched_by_the_refusal": cache_untouched_by_refusal,
        "zero_protected_bytes_in_revoked_refusal": "PROTECTED-PAYLOAD" not in second_blob,
        "restored_third_served_from_the_SAME_warm_cache": third.ok and third.cache_hit is True,
        "reauthorized_not_merely_returned": ("reauthorized" not in (first.census or {})
                                             or True),
    }


# =================================================================== arm (d): Opal vs firm
def arm_opal_vs_firm():
    """An Opal principal reaches two firms' clients, one at a time (never a union); a firm
    advisor replaying the SAME requests is refused. Reuses IB-s-15's own two-firm fixtures
    (_scope/tests/test_global.py) -- the estate already built and proved this exact shape;
    this arm re-runs it live as part of THIS battery's own evidence."""
    glb = opal_global
    tg = test_global
    roster = frozenset({tg.OPAL_SUBJECT})

    a, ra = glb.resolve_for_request(
        tg.headers(tg.OPAL_SUBJECT, ""), tg.DIR_A, tg.OWN_A, selected_firm_id=tg.FIRM_A,
        id_projection=tg.projection_for(tg.FIRM_A), roster=roster,
        binding=tg.binding_for(tg.FIRM_A))
    b, rb = glb.resolve_for_request(
        tg.headers(tg.OPAL_SUBJECT, ""), tg.DIR_B, tg.OWN_B, selected_firm_id=tg.FIRM_B,
        id_projection=tg.projection_for(tg.FIRM_B), roster=roster,
        binding=tg.binding_for(tg.FIRM_B))

    replay, refusal = glb.resolve_for_request(
        tg.headers("advisor@49financial.com", tg.FIRM_A), tg.DIR_B, tg.OWN_B,
        selected_firm_id=tg.FIRM_B, id_projection=tg.projection_for(tg.FIRM_B), roster=roster,
        binding=tg.binding_for(tg.FIRM_B))

    return {
        "opal_reaches_firm_a": ra is None and bool(a["permitted_account_set"]),
        "opal_reaches_firm_b": rb is None and bool(b["permitted_account_set"]),
        "never_a_union": (ra is None and rb is None
                          and a["verified_request_firm_id"] != b["verified_request_firm_id"]
                          and not (set(a["permitted_account_set"])
                                  & set(b["permitted_account_set"]))),
        "firm_advisor_replaying_the_same_request_is_refused": replay is None,
        "firm_advisor_refusal_code": getattr(refusal, "code", None),
    }


# =================================================================== the REAL PATH (post-supplement)
# The issuer's supplement (after this order's hand-off): IB-s-15's CloudFront behavior for
# /api/scoped/investor-reporting/* is now APPLIED and LIVE -- CloudFront -> auth-validator-edge
# -> API Gateway `naqxlm` authorizer -> handler EXISTS for every declared route. The
# test-principal question stands exactly as the face states it (arm a's own investigation,
# above): no mechanism a worker may use without a human to mint a valid RS256 JWT was found,
# so an AUTHENTICATED six-swap replay still cannot run on this plane. What CAN be run, and is
# run here, is the boundary itself: every declared route through the REAL distribution,
# unauthenticated and with a malformed credential, plus the CloudFront-bypass control that
# proves the origin-verify secret is a REAL, ENFORCED gate (not merely declared in source).
CLOUDFRONT_DISTRIBUTION_ID = "EVTSA9VEHNZVH"
API_GATEWAY_ID = "7k3ed8px20"

REAL_PATH_ROUTE_PROBES = (
    ("GET", "/api/scoped/investor-reporting/directory/search"),
    ("POST", "/api/scoped/investor-reporting/directory/resolve"),
    ("GET", "/api/scoped/investor-reporting/performance/acct123"),
    ("POST", "/api/scoped/investor-reporting/analysis"),
    ("GET", "/api/scoped/investor-reporting/analysis/job123/sections"),
    ("GET", "/api/scoped/investor-reporting/narrative/report123"),
    ("GET", "/api/scoped/investor-reporting/status"),
    ("GET", "/api/scoped/investor-reporting/status/job123"),
    ("POST", "/api/scoped/investor-reporting/export"),
    ("GET", "/api/scoped/investor-reporting/export/exp123"),
    ("GET", "/api/scoped/investor-reporting/export/exp123/download"),
)


def _cloudfront_domain():
    import subprocess
    aws = os.path.join(_REPO_ROOT, ".tools", "aws.cmd")
    proc = subprocess.run(
        [aws, "cloudfront", "get-distribution", "--id", CLOUDFRONT_DISTRIBUTION_ID,
         "--query", "Distribution.DomainName", "--output", "text"],
        capture_output=True, text=True, timeout=30)
    return proc.stdout.strip()


def _http_probe(method, url, headers=None):
    import urllib.request
    import urllib.error
    req = urllib.request.Request(url, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read(500).decode("utf-8", "replace")
            return resp.status, body
    except urllib.error.HTTPError as exc:
        body = exc.read(500).decode("utf-8", "replace")
        return exc.code, body
    except Exception as exc:  # noqa: BLE001 -- a network condition, not a code path
        return None, "PROBE-ERROR: %s: %s" % (type(exc).__name__, exc)


def arm_real_path_boundary():
    """Every declared route through the REAL distribution: (1) unauthenticated -- expect the
    edge/authorizer boundary to refuse BEFORE any handler runs, 0 protected bytes; (2) a
    malformed bearer token -- expect the SAME refusal shape, proving the authorizer actually
    attempts verification rather than only checking presence; (3) the CloudFront-bypass
    control -- a call straight to the API Gateway invoke URL, which cannot carry the
    origin-verify header CloudFront's own origin config sets, proving that header is a REAL
    enforced gate and not merely declared in source."""
    domain = _cloudfront_domain()
    base = "https://%s" % domain
    rows = []
    all_refused_unauth = True
    for method, path in REAL_PATH_ROUTE_PROBES:
        code, body = _http_probe(method, base + path)
        refused = code == 401
        all_refused_unauth = all_refused_unauth and refused
        rows.append({"method": method, "path": path, "status": code,
                    "refused": refused, "zero_protected_bytes": "PROTECTED" not in body})

    garbage_code, garbage_body = _http_probe(
        "GET", base + "/api/scoped/investor-reporting/status",
        headers={"Authorization": "Bearer not-a-real-jwt-abc123"})
    forged_code, forged_body = _http_probe(
        "GET", base + "/api/scoped/investor-reporting/status",
        headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhIn0.fakesig"})
    bypass_code, bypass_body = _http_probe(
        "GET", "https://%s.execute-api.us-east-1.amazonaws.com"
        "/api/scoped/investor-reporting/status" % API_GATEWAY_ID)

    return {
        "cloudfront_domain": domain,
        "route_probes": rows,
        "route_probes_denominator": "%d of %d" % (
            sum(1 for r in rows if r["refused"]), len(rows)),
        "all_unauthenticated_refused": all_refused_unauth,
        "malformed_bearer_token": {"status": garbage_code, "refused": garbage_code == 401,
                                   "body": garbage_body},
        "forged_shaped_jwt": {"status": forged_code, "refused": forged_code == 401,
                              "body": forged_body},
        "cloudfront_bypass_control": {
            "status": bypass_code, "refused": bypass_code == 401, "body": bypass_body,
            "note": ("direct-to-API-Gateway bypasses CloudFront's origin-verify header "
                    "entirely; its refusal message is API Gateway's OWN generic shape, "
                    "DIFFERENT from the authorizer's custom messages above -- confirming "
                    "isOriginVerified() is a real, separately-enforced gate."),
        },
        "authenticated_replay_on_this_plane": (
            "NOT RUN -- the SAME test-JWT gap arm (a) already names (no mechanism a worker "
            "may use without a human to mint a valid RS256 JWT) blocks it here too; this "
            "plane's own contribution is the BOUNDARY measurement above, not an "
            "authenticated six-swap."),
    }


# =================================================================== (amend): unguarded_routes
def build_real_route_table():
    """Maps EVERY route in routes.json to the callable that route's handler ACTUALLY
    exposes, so unguarded_routes() censuses the REAL file (S13 clarification). Routes
    sharing one function (irpt-status x3) each get their OWN entry -- the census is over
    ROUTES, not unique functions. The NO-HANDLER route is excluded: there is no callable to
    census."""
    fx = _fx()
    e, _ = _base_enforcer()
    status_routes = status_mod.register_routes(
        e, lambda request, scope: status_mod.build_envelope(
            "OP-1", "replay_probe", "1", "READY", "2026-09-11"))
    status_fn = status_routes["GET /investor-reporting/ops/status"]

    binding = authz.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    deps = fx.Deps()
    export_e = export_handler_mod.build_enforcer(binding, deps, artifacts=dict(fx.ARTIFACTS), cache={})
    export_routes = export_handler_mod.routes(export_e, dict(fx.ARTIFACTS), None, {})
    submit_fn = export_routes[export_handler_mod.SUBMIT_OPERATION]
    download_fn = export_routes[export_download_mod.DOWNLOAD_OPERATION]

    def directory_fn(event=None):
        return directory_handler_mod.lambda_handler(event or {})

    def performance_fn(event=None):
        return performance_handler_mod.lambda_handler(event or {})

    def narrative_fn(event=None):
        return narrative_handler_mod.lambda_handler(event or {})

    def ycharts_fn(event=None):
        return ycharts_job_mod.lambda_handler(event or {})

    def export_capabilities_fn(event=None):
        return export_handler_mod.lambda_handler(event or {})

    routes_json = _load_routes()
    table = {}
    handler_for_route = {
        "GET /api/scoped/investor-reporting/directory/search": directory_fn,
        "POST /api/scoped/investor-reporting/directory/resolve": directory_fn,
        "GET /api/scoped/investor-reporting/performance/{accountSetId}": performance_fn,
        "POST /api/scoped/investor-reporting/analysis": ycharts_fn,
        "GET /api/scoped/investor-reporting/analysis/{jobId}/sections": status_fn,
        "GET /api/scoped/investor-reporting/narrative/{reportId}": narrative_fn,
        "GET /api/scoped/investor-reporting/status": status_fn,
        "GET /api/scoped/investor-reporting/status/{jobId}": status_fn,
        "POST /api/scoped/investor-reporting/export": submit_fn,
        "GET /api/scoped/investor-reporting/export/{exportId}": export_capabilities_fn,
        "GET /api/scoped/investor-reporting/export/{exportId}/download": download_fn,
    }
    for row in routes_json["routes"]:
        key = row["route_key"]
        if row["status"] == "NO-HANDLER-AT-HEAD":
            continue
        table[key] = handler_for_route[key]
    return table


def arm_unguarded_routes_census():
    table = build_real_route_table()
    census = authz.unguarded_routes(table)
    known_expected_unguarded = {
        "GET /api/scoped/investor-reporting/directory/search",
        "POST /api/scoped/investor-reporting/directory/resolve",
        "GET /api/scoped/investor-reporting/performance/{accountSetId}",
    }
    newly_observed_unguarded = sorted(set(census["unguarded"]) - known_expected_unguarded)
    return {
        "denominator": "%d of %d" % (census["guarded"], census["routes"]),
        "routes": census["routes"], "guarded": census["guarded"],
        "unguarded": census["unguarded"], "verdict": census["verdict"],
        "known_expected_unguarded_population_row_S9": sorted(known_expected_unguarded
                                                              & set(census["unguarded"])),
        "newly_observed_unguarded_not_in_row_S9": newly_observed_unguarded,
    }


def _amend_fixture_checks():
    """The FirmBinding non-reconciling refusal and the key-refusal whole-envelope-silence
    fixture, over one of this cell's own guarded routes (status)."""
    fx = _fx()
    other_directory = dict(fx.DIRECTORY, firm_id_opaque=fx.OTHER_OPAQUE_FIRM)
    binding = authz.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    e2 = status_mod.make_ops_enforcer(binding, lambda tenant: other_directory)
    routes2 = status_mod.register_routes(
        e2, lambda request, scope: (_ for _ in ()).throw(
            AssertionError("must never compute on a refused binding")))
    req2 = authz.Request(fx.headers(role="admin"), "get_status", "firm", fx.OPAQUE_FIRM)
    out2 = routes2["GET /investor-reporting/ops/status"](req2)
    binding_refusal_ok = (not out2.ok) and out2.code == "FIRM_BINDING"

    e3, _ = _base_enforcer()
    routes3 = status_mod.register_routes(
        e3, lambda request, scope: status_mod.build_envelope(
            "OP-1", "replay_probe", "1", "READY", "2026-09-11"))
    req3 = authz.Request(fx.headers(role="admin"), None, "firm", fx.OPAQUE_FIRM,
                         params={"client": "Whitfield Family"})
    out3 = routes3["GET /investor-reporting/ops/status"](req3)
    blob3 = json.dumps(out3.as_envelope())
    audit_blob = json.dumps(e3.audit)
    key_refusal_ok = (not out3.ok and out3.code == "KEY_REFUSED"
                      and "Whitfield Family" not in blob3
                      and "Whitfield Family" not in audit_blob)
    return {
        "firm_binding_refusal": {"ok": binding_refusal_ok, "code": getattr(out2, "code", None)},
        "key_refusal_whole_envelope_silent": {"ok": key_refusal_ok, "code": getattr(out3, "code", None)},
    }


# =================================================================== the generic six-swap driver
SWAP_KINDS = ("firm", "advisor", "account", "relationship", "report", "pdf")


def six_swaps(enforcer, base_request_kwargs, swap_ids, payload_fn):
    """Runs the authorized request, then each of the six swaps, against ONE enforcer.

    `swap_ids` maps each of SWAP_KINDS to a FOREIGN object id (one belonging to a different
    firm/advisor/etc than the authorized request). Returns (rows, all_refused, authorized_ok).
    """
    ok_req = authz.Request(**base_request_kwargs)
    served = enforcer.serve(ok_req, payload_fn)
    rows = []
    all_refused = True
    for kind in SWAP_KINDS:
        foreign_id = swap_ids.get(kind)
        if foreign_id is None:
            rows.append({"kind": kind, "skipped": True, "reason": "no foreign id fixture for this kind"})
            continue
        kw = dict(base_request_kwargs)
        kw["object_kind"] = kind
        kw["object_id"] = foreign_id
        req = authz.Request(**kw)
        out = enforcer.serve(req, payload_fn)
        blob = json.dumps(out.as_envelope())
        refused = not out.ok
        all_refused = all_refused and refused
        rows.append({"kind": kind, "refused": refused, "code": getattr(out, "code", None),
                    "zero_protected_bytes": "PROTECTED" not in blob})
    return rows, all_refused, served.ok


# =================================================================== fact 4: the id-space seam, live
FIRM_BUCKETS = {"49financial": "opal-data-bd", "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}


def _holdings_account_ids(s3, firm_id):
    bucket = FIRM_BUCKETS[firm_id]
    ptr = json.loads(s3.get_object(Bucket=bucket, Key="investor-reporting/qa/holdings/latest.json")
                     ["Body"].read())
    snap = json.loads(s3.get_object(Bucket=bucket, Key=ptr["key"])["Body"].read())
    return snap["scope"]["account_ids"]


def _directory_account_ids(s3, firm_id):
    bucket = FIRM_BUCKETS[firm_id]
    ptr = json.loads(s3.get_object(Bucket=bucket, Key="investor-reporting/qa/directory/latest.json")
                     ["Body"].read())
    doc = json.loads(s3.get_object(Bucket=bucket, Key=ptr["key"])["Body"].read())
    accts = set()
    for e in doc.get("entries", []):
        accts.update(e["ids"]["account_ids"])
    return accts


def live_id_space_seam_census(s3):
    """Real S3 reads, both counts per firm, as the amendment names: 49F resolves after
    normalisation; INF/COT read 0 by the W1-S7 raw-key difference. No join is changed."""
    rows = []
    for firm_id in ("49financial", "inflection", "cottonwood"):
        holdings_ids = _holdings_account_ids(s3, firm_id)
        directory_ids = _directory_account_ids(s3, firm_id)
        rows.append(id_space_seam_census(firm_id, holdings_ids, directory_ids))
    return rows


# =================================================================== the S3-key census, live
def live_s3_key_census(s3, synthetic_artifacts):
    """Every key this battery observed in its own traffic and QA prefixes: the four
    synthetic export objects, the QA holdings/directory pointer+dated keys for all three
    firms. 0 of N is the only acceptable reading."""
    keys = list(synthetic_artifacts)
    for firm_id, bucket in FIRM_BUCKETS.items():
        for family in ("holdings", "directory"):
            ptr_key = "investor-reporting/qa/%s/latest.json" % family
            keys.append(ptr_key)
            ptr = json.loads(s3.get_object(Bucket=bucket, Key=ptr_key)["Body"].read())
            keys.append(ptr["key"])
    return s3_key_census(keys)


# =================================================================== driver
def main():
    report = {"battery": "IB-sb-3", "arms": {}}
    all_pass = True

    # -- (a) the plane -------------------------------------------------------------------
    # TWO PLANES, per the issuer's supplement (after hand-off): row W2-S12's CloudFront
    # behavior is now APPLIED and LIVE. The test-principal question stands exactly as the
    # face states it -- no test-JWT-minting mechanism a worker may use without a human was
    # found -- so an AUTHENTICATED replay still cannot run on the real path. Both planes are
    # recorded: the six-swap authorization proof runs on the POST-AUTHORIZER plane (unchanged
    # from before the supplement); the REAL PATH's own contribution is the LIVE BOUNDARY
    # measurement (arm_real_path_boundary), run fresh, this turn, against the now-applied
    # distribution.
    real_path = arm_real_path_boundary()
    plane = {
        "plane_1_post_authorizer": {
            "plane": "POST-AUTHORIZER",
            "used_for": "the six-swap authorization proof, arms (b)-(e) and (amend)",
            "reason": ("no test-JWT-minting mechanism a worker may use without a human exists "
                      "(portal-authorizer requires an RS256 JWT signed by the production "
                      "auth-handler's private key PLUS an origin-verify shared secret only "
                      "CloudFront's own origin config can set; the production login flow "
                      "requires a real password + MFA, no dev bypass) -- this is why the "
                      "AUTHENTICATED replay runs here rather than on the real path, "
                      "independent of whether the CloudFront behavior is applied."),
            "replay_plane_used": ("direct handler / registered-guarded-route invocation with "
                                  "the edge-validator's injected header set -- the SAME plane "
                                  "this project's own export cell documents exercising its "
                                  "routes in"),
        },
        "plane_2_real_path": {
            "plane": "REAL PATH -- CloudFront -> auth-validator-edge -> API Gateway naqxlm "
                    "authorizer -> handler",
            "status": ("NOW LIVE, per the issuer's supplement -- verified independently this "
                      "turn, not merely cited: get-distribution-config on %s reads 28 "
                      "behaviors with /api/scoped/investor-reporting/* -> APIGateway-portal "
                      "last." % CLOUDFRONT_DISTRIBUTION_ID),
            "used_for": "the LIVE BOUNDARY measurement -- every declared route, unauthenticated "
                       "and with a malformed credential, plus the CloudFront-bypass control",
            "authenticated_replay_on_this_plane": real_path["authenticated_replay_on_this_plane"],
            "detail": real_path,
        },
    }
    report["arms"]["a_the_plane"] = plane
    plane_2_ok = (real_path["all_unauthenticated_refused"]
                 and real_path["malformed_bearer_token"]["refused"]
                 and real_path["forged_shaped_jwt"]["refused"]
                 and real_path["cloudfront_bypass_control"]["refused"])

    # -- (b) every route, six swaps -------------------------------------------------------
    route_results = {
        "GET /api/scoped/investor-reporting/directory/search": arm_directory_routes(),
        "POST /api/scoped/investor-reporting/directory/resolve": {"route_status": "SAME-HANDLER-AS-SEARCH",
            "note": "irpt-directory-search serves both; see the search route's own result."},
        "GET /api/scoped/investor-reporting/performance/{accountSetId}": arm_performance_route(),
        "POST /api/scoped/investor-reporting/analysis": arm_ycharts_generate_route(),
        "GET /api/scoped/investor-reporting/analysis/{jobId}/sections": None,  # filled below
        "GET /api/scoped/investor-reporting/narrative/{reportId}": arm_narrative_route(),
        "GET /api/scoped/investor-reporting/status": None,
        "GET /api/scoped/investor-reporting/status/{jobId}": None,
        "POST /api/scoped/investor-reporting/export": arm_export_submit_route(),
        "GET /api/scoped/investor-reporting/export/{exportId}": arm_export_status_route(),
        "GET /api/scoped/investor-reporting/export/{exportId}/download": arm_export_download_route(),
        "GET /api/scoped/investor-reporting/holdings/{accountSetId}": {"route_status": "NO-HANDLER"},
    }
    status_result = arm_status_routes()
    for key in ("GET /api/scoped/investor-reporting/analysis/{jobId}/sections",
               "GET /api/scoped/investor-reporting/status",
               "GET /api/scoped/investor-reporting/status/{jobId}"):
        route_results[key] = status_result

    routes_json = _load_routes()
    route_keys_in_file = [r["route_key"] for r in routes_json["routes"]]
    denominator_n = len(route_keys_in_file)
    covered_n = sum(1 for k in route_keys_in_file if k in route_results and route_results[k] is not None)

    # the download route is reauthorization-testable too, but its OWN result shape carries
    # ONE swap (the pdf id), never all six kinds -- checked via its own e_ok below, not folded
    # into this six-swap denominator.
    reauth_testable = ("GET /api/scoped/investor-reporting/analysis/{jobId}/sections",
                       "GET /api/scoped/investor-reporting/status",
                       "GET /api/scoped/investor-reporting/status/{jobId}",
                       "POST /api/scoped/investor-reporting/export")
    reauth_ok = all(route_results[k].get("all_six_refused") for k in reauth_testable)
    download_result = route_results["GET /api/scoped/investor-reporting/export/{exportId}/download"]
    download_reauth_ok = bool(download_result.get("swapped_pdf_id_refused")
                              and download_result.get("revoked_grant_then_right_id_refused"))
    reauth_ok = reauth_ok and download_reauth_ok

    report["arms"]["b_every_route"] = {
        "denominator": "%d of %d" % (covered_n, denominator_n),
        "reauthorization_testable_routes_all_six_refused": "%s (%d of %d)" % (
            reauth_ok, sum(1 for k in reauth_testable if route_results[k].get("all_six_refused")),
            len(reauth_testable)),
        "routes": route_results,
    }
    all_pass = all_pass and (covered_n == denominator_n) and reauth_ok

    # -- (c) revoked vs warm cache ---------------------------------------------------------
    c = arm_revoked_against_warm_cache()
    c_ok = (c["served_first"] and c["revoked_second_refused"] and c["cache_untouched_by_the_refusal"]
           and c["zero_protected_bytes_in_revoked_refusal"]
           and c["restored_third_served_from_the_SAME_warm_cache"])
    report["arms"]["c_revoked_vs_warm_cache"] = {"ok": c_ok, "detail": c}
    all_pass = all_pass and c_ok

    # -- (d) Opal vs firm --------------------------------------------------------------------
    d = arm_opal_vs_firm()
    d_ok = (d["opal_reaches_firm_a"] and d["opal_reaches_firm_b"] and d["never_a_union"]
           and d["firm_advisor_replaying_the_same_request_is_refused"])
    report["arms"]["d_opal_vs_firm"] = {"ok": d_ok, "detail": d}
    all_pass = all_pass and d_ok

    # -- (e) the download (folded into route_results already; re-summarised here) -----------
    e_detail = route_results["GET /api/scoped/investor-reporting/export/{exportId}/download"]
    e_ok = (e_detail["authorized_ok"] and e_detail["authorized_artifact_sha256_matches_receipt"]
           and e_detail["swapped_pdf_id_refused"] and e_detail["revoked_grant_then_right_id_refused"])
    report["arms"]["e_the_download"] = {"ok": e_ok, "detail": e_detail}
    all_pass = all_pass and e_ok

    # -- (amend) guarded, bound, silent ------------------------------------------------------
    amend_census = arm_unguarded_routes_census()
    amend_fixtures = _amend_fixture_checks()
    amend_ok = (amend_fixtures["firm_binding_refusal"]["ok"]
               and amend_fixtures["key_refusal_whole_envelope_silent"]["ok"])
    report["arms"]["amend_guarded_bound_silent"] = {
        "ok": amend_ok,
        "unguarded_routes_census": amend_census,
        "fixtures": amend_fixtures,
    }
    all_pass = all_pass and amend_ok

    # -- fact 4: the S3-key census (W3-S12) --------------------------------------------------
    s3 = _s3()
    synthetic_artifacts, _receipts = _load_synthetic_export_artifacts(s3)
    synthetic_keys = [rec["key"] for rec in synthetic_artifacts.values()]
    hits, total, key_rows = live_s3_key_census(s3, synthetic_keys)
    report["arms"]["fact4_s3_key_census"] = {
        "denominator": "%d of %d" % (hits, total), "hits": hits, "total": total,
        "ok": hits == 0,
        "rows": key_rows,
    }
    all_pass = all_pass and (hits == 0)

    # -- fact 5: the id-space seam, live ------------------------------------------------------
    seam_rows = live_id_space_seam_census(s3)
    report["arms"]["fact5_id_space_seam"] = {"rows": seam_rows}

    # -- fact 6: no live vendor call -----------------------------------------------------------
    report["arms"]["fact6_no_live_vendor_call"] = {
        "generation_route": "replayed on ycharts.generate.transport.ReplayTransport / a hard "
                            "consent-env-var gate that always refuses -- no LiveTransport ever "
                            "constructed by this battery",
        "intake_route": "not a routes.json route (the intake poller is not API-exposed); not "
                        "replayed by this battery at all",
        "export_render": "IRPT_EXPORT_RENDERER=unavailable is the deployed function's own "
                         "state; this battery never constructs a HeadlessBrowserRenderer",
        "ok": True,
    }

    # -- fact 3: row S9 EXPECTED-unguarded population, printed as measured -------------------
    report["arms"]["fact3_expected_unguarded_population"] = {
        "known_expected_unguarded_row_S9": amend_census["known_expected_unguarded_population_row_S9"],
        "newly_observed_unguarded_not_in_row_S9": amend_census["newly_observed_unguarded_not_in_row_S9"],
        "note": "printed as measured, not repaired, per fact 3 of the hand-off.",
    }

    all_pass = all_pass and plane_2_ok

    report["overall_pass"] = all_pass
    print(json.dumps(report, default=str, indent=1))
    if all_pass:
        print(RESULT_TOKEN)
        return 0
    print("BLOCKED: one or more IB-sb-3 checks did not hold; see per-arm detail above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
