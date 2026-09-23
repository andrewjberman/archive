#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtr-e -- THE ONE OFFLINE ACTUAL-MODULE CHAIN.

Wires the REAL modules together end to end, calling the ACTUAL function from the ACTUAL file at
every step -- no hand-rolled restatement of what a function "would do":

  mint.py's mint_render_token()
    -> V3 evaluateRenderBranch (auth-validator-edge/index.mjs, render_auth.mjs), via edge.handler()
    -> V2 authorizeRenderToken (portal-authorizer/index.mjs), called directly
    -> resolve.py's trusted_only() / classify_principal()
    -> enforce.py's Enforcer.resolve_now() / _resolve_render_delegate()
    -> served.py's key_operation() and the Enforcer's cache_key_for() (no KEY_REFUSED)

Python and Node are bridged via `chain_bridge.mjs` (same directory), a subprocess that imports
the REAL V3/V2 files with only the AWS-SDK network edge blocked (module-loader hook, exactly the
CVO's own R17 probe's pattern -- see that file's own header comment, read-only reference for this
cell, never edited).

BOUNDS: offline only (no Secrets Manager entry, no SSM parameter, no AWS API call, no Lambda
deploy, no Terraform/CloudFront change, no key provisioning); no edit to any of the five real
modules' own logic; no edit to any sibling cell's own test file.

Criterion R118-AC5 is JUDGMENT-graded by the CVO at L9. This script proves the MECHANICAL bar:
rc=0, three fixture objects correctly resolved (non-overlapping), six negative arms correctly
refused/UNKNOWN. See result.md for the explicit PRD item-7 (a)-(k) [except g] arm-by-arm mapping
the CVO's L9 read is built on.
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwt as jose_jwt


# --------------------------------------------------------------------------- locate the worktree
def _find_root(start: Path) -> Path:
    p = start.resolve()
    for anc in [p] + list(p.parents):
        if (anc / "CLAUDE.md").exists() and (anc / "org").is_dir() and (anc / "infra").is_dir():
            return anc
    raise RuntimeError("could not locate worktree root walking up from %s" % start)


ROOT = _find_root(Path(__file__).parent)
IRPT = ROOT / "infra" / "aws" / "lambda" / "investor-reporting"
BRIDGE = Path(__file__).resolve().parent / "chain_bridge.mjs"

for _p in (
    IRPT / "_render_identity",
    IRPT / "_scope",
    IRPT / "_authz",
    IRPT / "_ids",
    IRPT / "_keys",
):
    sp = str(_p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

# THE REAL MODULES. Imported once, called many times below -- never re-implemented.
import mint as _mint          # noqa: E402  IB-rtq-1
import resolve as _scope      # noqa: E402  IB-s-2 / IB-rtq-2
import enforce as _enforce    # noqa: E402  IB-s-3 / IB-rtr-3
import served as _served      # noqa: E402  IB-rt-1 / IB-rt-4

FAILURES = []
RESULTS = {}


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print("[%s] %s%s" % (status, label, (" -- " + detail) if detail else ""))
    if not condition:
        FAILURES.append(label)
    return condition


# --------------------------------------------------------------------------- the shared render key
_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
PRIV_PEM = _KEY.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
).decode("ascii")
PUB_PEM = _KEY.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode("ascii")


def _hexid(prefix, n):
    return "%s_%024x" % (prefix, n)


def call_bridge(token, uri, method, route, timeout=30):
    """Subprocess into chain_bridge.mjs -- the REAL V3 edge.handler() and the REAL V2
    authorizeRenderToken(), never a restatement of either."""
    cmd = {
        "token": token, "uri": uri, "method": method, "route": route,
        "renderPublicKeyPem": PUB_PEM,
    }
    proc = subprocess.run(
        ["node", str(BRIDGE), str(ROOT)],
        input=json.dumps(cmd), capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError("chain_bridge.mjs rc=%s stderr=%s" % (proc.returncode, proc.stderr[-4000:]))
    # stdout may carry the bridge's own JSON PLUS console.log/warn lines the real modules emit
    # (e.g. index.mjs's own `console.log('Auth OK (render): ...')`). The bridge's JSON is always
    # the LAST line it writes (process.stdout.write with no trailing structured logging after
    # it), so parse from the last '{' that yields valid JSON, scanning from the end.
    out = proc.stdout
    last_brace = out.rfind("{")
    while last_brace != -1:
        try:
            return json.loads(out[last_brace:]), proc.stderr
        except json.JSONDecodeError:
            last_brace = out.rfind("{", 0, last_brace)
    raise RuntimeError("could not parse bridge JSON from stdout: %r" % out[-2000:])


# --------------------------------------------------------------------------- three fixture worlds
def make_world(tag, tenant, account_set_id, job_id, report_id, published_op, route_key, claim_name,
               claim_value, extra_delegator_account=None):
    """One self-contained bundle/account/directory/ownership fixture, never sharing an id with
    another world -- this is what proves the chain is genuinely parameterized (CELL arm (b))."""
    opaque = _hexid("fir", hash((tag, "firm")) & 0xFFFFFFFFFFFFFFFFFFFFFFFF)
    a = _hexid("acc", hash((tag, "A")) & 0xFFFFFFFFFFFFFFFFFFFFFFFF)
    b = _hexid("acc", hash((tag, "B")) & 0xFFFFFFFFFFFFFFFFFFFFFFFF)
    advisor_id = "ADV-%s-0001" % tag
    delegator_subject = "advisor.%s@%s.example" % (tag.lower(), tenant)

    granted_accounts = [a, b]
    if extra_delegator_account:
        c = _hexid("acc", hash((tag, "C")) & 0xFFFFFFFFFFFFFFFFFFFFFFFF)
        granted_accounts = [a, b, c]
    else:
        c = None

    directory = {
        "firm_id_opaque": opaque,
        "entries": [{
            "ids": {"firm_id": opaque, "client_id": "cli_%s" % tag.lower(),
                    "relationship_id": None, "account_ids": granted_accounts},
            "display_name": "%s Fixture Client" % tag,
            "masked_discriminator": "****%s" % tag,
        }],
    }
    ownership = {
        "schema_version": 1,
        "advisors": {advisor_id: {"accounts": granted_accounts, "relationships": []}},
    }
    bundle = {
        "firm_id": tenant, "bundle_id": "bundle-%s-1" % tag.lower(),
        "revision": "rev-%s-1" % tag.lower(), "account_set_id": account_set_id,
        "job_id": job_id, "report_id": report_id, "delegator_subject": delegator_subject,
    }

    def load_directory(_t):
        return directory

    def load_ownership(_t):
        return ownership

    def load_policy(_t):
        return {"policy_id": "irpt-viewer-v1", "policy_revision": "1"}, "ent-%s-1" % tag.lower()

    def load_render_bundle(_t, _rev):
        return {"account_ids": [a, b], "bundle_id": bundle["bundle_id"]}  # PINNED scope: a,b only

    def load_delegator_identity(_t, subject):
        return advisor_id if subject == delegator_subject else None

    return {
        "tag": tag, "tenant": tenant, "opaque": opaque, "a": a, "b": b, "c": c,
        "advisor_id": advisor_id, "delegator_subject": delegator_subject,
        "granted_accounts": granted_accounts, "bundle": bundle, "published_op": published_op,
        "route_key": route_key, "claim_name": claim_name, "claim_value": claim_value,
        "uri": "/api/scoped/investor-reporting/%s" % {
            "performance-report": "performance/%s" % account_set_id,
            "analysis-report": "analysis/%s/sections" % job_id,
            "narrative-packet": "narrative/%s" % report_id,
        }[published_op],
        "load_directory": load_directory, "load_ownership": load_ownership,
        "load_policy": load_policy, "load_render_bundle": load_render_bundle,
        "load_delegator_identity": load_delegator_identity,
    }


WORLD1 = make_world("W1", "49financial", "AS-W1-1", "JOB-W1-1", "REP-W1-1",
                     "performance-report",
                     "GET /api/scoped/investor-reporting/performance/{accountSetId}",
                     "accountSetId", "AS-W1-1", extra_delegator_account=True)
WORLD2 = make_world("W2", "cottonwood", "AS-W2-1", "JOB-W2-1", "REP-W2-1",
                     "analysis-report",
                     "GET /api/scoped/investor-reporting/analysis/{jobId}/sections",
                     "jobId", "JOB-W2-1")
WORLD3 = make_world("W3", "inflection", "AS-W3-1", "JOB-W3-1", "REP-W3-1",
                     "narrative-packet",
                     "GET /api/scoped/investor-reporting/narrative/{reportId}",
                     "reportId", "REP-W3-1")
WORLDS = [WORLD1, WORLD2, WORLD3]


def build_enforcer(world, ownership_override=None, render_bundle_override=None):
    binding = _enforce.FirmBinding(world["tenant"], world["opaque"])
    load_ownership = ownership_override or world["load_ownership"]
    load_render_bundle = render_bundle_override or world["load_render_bundle"]
    return _enforce.Enforcer(
        binding, world["load_directory"], load_ownership, world["load_policy"],
        load_render_bundle=load_render_bundle,
        load_delegator_identity=world["load_delegator_identity"],
    )


# --------------------------------------------------------------------------- POSITIVE: (a),(h)
def run_positive(world):
    mint_result = _mint.mint_render_token(world["bundle"], private_key_pem=PRIV_PEM)
    route = {"routeKey": world["route_key"], "pathParameters": {world["claim_name"]: world["claim_value"]}}
    out, stderr = call_bridge(mint_result.token, world["uri"], "GET", route)

    v3 = out["v3"]
    v2 = out["v2"]
    ok = True
    ok &= check("%s: V3 admits the minted token" % world["tag"], v3["admitted"] is True, str(v3.get("message")))
    ok &= check("%s: V2 authorizes independently" % world["tag"], v2["authorized"] is True)

    # resolve.py's REAL trusted_only / classify_principal, fed the REAL headers V3 injected.
    trusted, dropped = _scope.trusted_only(v3["headers"])
    principal_class, reason = _scope.classify_principal(trusted)
    ok &= check("%s: resolve.classify_principal -> RENDER_DELEGATE" % world["tag"],
                principal_class == "RENDER_DELEGATE", reason)

    # served.py's REAL key_operation boundary -- never hand-transformed.
    key_op = _served.key_operation(world["published_op"])
    ok &= check("%s: served.key_operation(%r) is in RENDER_DELEGATE_OPERATIONS" % (world["tag"], world["published_op"]),
                key_op in _enforce.Enforcer.RENDER_DELEGATE_OPERATIONS, key_op)

    e = build_enforcer(world)
    request = _enforce.Request(v3["headers"], key_op, "account", world["a"])
    scope, refusal = e.resolve_now(request)
    ok &= check("%s: Enforcer.resolve_now admits (no refusal)" % world["tag"], refusal is None,
                repr(refusal))
    ok &= check("%s: scope principal_class RENDER_DELEGATE" % world["tag"],
                bool(scope) and scope.get("principal_class") == "RENDER_DELEGATE")

    if scope is None:
        # A refusal here means this world's chain did not resolve at all (e.g. under a
        # mutant control) -- every downstream, scope-dependent check is UNREACHABLE, never
        # silently skipped as if it passed: fail them explicitly rather than crashing on a
        # None subscript, which would obscure WHICH check first detected the defect.
        check("%s: covers() the pinned account" % world["tag"], False, "UNREACHABLE: scope is None")
        check("%s: cache_key_for succeeds (no KEY_REFUSED)" % world["tag"], False, "UNREACHABLE: scope is None")
        if world.get("c"):
            check("%s: account outside the bundle's PINNED scope is NOT covered (item k, pt 1)"
                  % world["tag"], False, "UNREACHABLE: scope is None")
        RESULTS[world["tag"]] = {"permitted_account_set": None, "operation": key_op,
                                 "cache_key_prefix": None, "refusal": repr(refusal)}
        return False

    covered, why = e.covers(scope, "account", world["a"])
    ok &= check("%s: covers() the pinned account" % world["tag"], covered, why)

    try:
        cache_key = e.cache_key_for(scope, request)
        ok &= check("%s: cache_key_for succeeds (no KEY_REFUSED)" % world["tag"], bool(cache_key))
    except _enforce.KeyRefused as exc:
        ok &= check("%s: cache_key_for succeeds (no KEY_REFUSED)" % world["tag"], False, exc.public_reason())
        cache_key = None

    # item (k) part 1: an object the delegator HOLDS but that is OUTSIDE the bundle's pinned
    # scope (world1's extra account C) is refused, never served.
    outside_ok = None
    if world.get("c"):
        outside_covered, outside_why = e.covers(scope, "account", world["c"])
        outside_ok = check("%s: account outside the bundle's PINNED scope is NOT covered (item k, pt 1)"
                            % world["tag"], outside_covered is False, outside_why)
        ok &= outside_ok

    RESULTS[world["tag"]] = {
        "permitted_account_set": scope.get("permitted_account_set") if scope else None,
        "operation": key_op, "cache_key_prefix": (cache_key or "")[:16],
    }
    return ok


# --------------------------------------------------------------------------- NEGATIVES
def negative_1_forbidden_claim():
    """(c)(1) / PRD (d): a forbidden claim, refused at V3 AND independently at V2."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    claims = jose_jwt.get_unverified_claims(mint_result.token)
    claims["role"] = "admin"  # one of the four forbidden claims -- others covered by IB-rtr-2's own tests
    forged = jose_jwt.encode(claims, PRIV_PEM, algorithm="RS256")
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(forged, WORLD1["uri"], "GET", route)
    ok = check("N1: V3 refuses a render token with a forbidden claim (role=admin)",
               out["v3"]["admitted"] is False, out["v3"].get("message"))
    ok &= check("N1: V2 independently refuses the same forged token",
                out["v2"]["authorized"] is False)
    return ok


def negative_2_expired():
    """(c)(2) / PRD (c): a token past exp is refused."""
    stale_now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=1000)
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM, now=stale_now)
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", route)
    return check("N2: V3 refuses an expired render token", out["v3"]["admitted"] is False,
                 out["v3"].get("message"))


def negative_3_swapped_path_id():
    """(c)(3) / PRD (b) pt 2: same route, wrong path id -> V2 refuses; V3's URI-only admission
    is unaffected (arm shape from IB-rtq-2/IB-rtr-1)."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    wrong_route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: "SWAPPED-ID"}}
    out, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", wrong_route)
    ok = check("N3: V2 refuses a swapped path id", out["v2"]["authorized"] is False)
    ok &= check("N3: V3's uri-shape admission is unaffected by the route object passed to V2",
                out["v3"]["admitted"] is True)
    return ok


def negative_4_wrong_bundle_id():
    """(c)(4) / IB-rtr-3 item (c): the LOADED bundle's own declared id disagrees with the
    claimed X-Render-Bundle -- refused, never served against the wrong bundle."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", route)
    assert out["v3"]["admitted"] and out["v2"]["authorized"]

    def wrong_bundle_loader(_t, _rev):
        return {"account_ids": [WORLD1["a"], WORLD1["b"]], "bundle_id": "WRONG-BUNDLE-ID"}

    e = build_enforcer(WORLD1, render_bundle_override=wrong_bundle_loader)
    key_op = _served.key_operation(WORLD1["published_op"])
    request = _enforce.Request(out["v3"]["headers"], key_op, "account", WORLD1["a"])
    scope, refusal = e.resolve_now(request)
    return check("N4: Enforcer refuses a wrong-bundle-id loader mismatch",
                 scope is None and refusal is not None and refusal.code == "EMPTY_GRANT",
                 repr(refusal))


def negative_5_unlisted_operation():
    """(c)(5) / PRD (b) pt 1 + (k) pt 2: a fourth, unlisted operation is refused -- at the
    Enforcer's operation vocabulary AND at V2's route table."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", route)
    assert out["v3"]["admitted"] and out["v2"]["authorized"]

    e = build_enforcer(WORLD1)
    unlisted_key_op = _served.key_operation("summary-report")  # a plausible but never-published op
    ok = check("N5a: unlisted op key spelling is NOT in RENDER_DELEGATE_OPERATIONS",
               unlisted_key_op not in _enforce.Enforcer.RENDER_DELEGATE_OPERATIONS, unlisted_key_op)
    request = _enforce.Request(out["v3"]["headers"], unlisted_key_op, "account", WORLD1["a"])
    scope, refusal = e.resolve_now(request)
    ok &= check("N5b: Enforcer refuses the fourth operation OBJECT_NOT_COVERED",
                scope is None and refusal is not None and refusal.code == "OBJECT_NOT_COVERED",
                repr(refusal))

    fourth_route = {"routeKey": "GET /api/scoped/investor-reporting/summary/{summaryId}",
                     "pathParameters": {"summaryId": "S-1"}}
    out2, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", fourth_route)
    ok &= check("N5c: V2 refuses a route outside the three published GETs (PRD item b pt 1)",
                out2["v2"]["authorized"] is False)
    return ok


def negative_6_missing_render_marker():
    """(c)(6) / PRD (j): the token is real and admitted, but the edge-injected marker headers
    are absent (simulating a request that never actually passed through the real edge) --
    resolves UNKNOWN, never a best-effort RENDER_DELEGATE."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", route)
    assert out["v3"]["admitted"]

    stripped = dict(out["v3"]["headers"])
    for marker in ("x-render-delegator", "x-render-bundle", "x-render-revision"):
        stripped.pop(marker, None)
    trusted, dropped = _scope.trusted_only(stripped)
    principal_class, reason = _scope.classify_principal(trusted)
    return check("N6: classify_principal resolves UNKNOWN when the render marker is absent",
                 principal_class == "UNKNOWN", reason)


def extra_f_human_token_unaffected():
    """PRD (f), the negative-widening arm: a non-render-shaped token is NOT admitted by the
    render branch and falls through, unchanged, to the pre-existing human verification path.
    This cell's BOUNDS forbid any AWS call, so the human path's own Secrets Manager fetch is
    (deliberately) blocked -- observed here as the NETWORK FORBIDDEN signal from THIS test's own
    offline guard, never a render-specific refusal reason, which is the evidence that control
    reached the un-mutated human path rather than being intercepted by the render branch."""
    human_claims = {"sub": "advisor.a@49financial.com", "role": "user", "tier": "partner",
                     "firmId": "49financial", "aud": "opal-portal-api", "iss": "opal-portal-auth",
                     "iat": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
                     "exp": int(datetime.datetime.now(datetime.timezone.utc).timestamp()) + 3600}
    human_token = jose_jwt.encode(human_claims, PRIV_PEM, algorithm="RS256")
    route = {"routeKey": "GET /some/human/route", "pathParameters": {}}
    out, stderr = call_bridge(human_token, "/some/human/route", "GET", route)
    ok = check("Ef: a human-shaped token is not admitted by the render branch",
               out["v3"]["admitted"] is False)
    ok &= check("Ef: the render branch fell through -- the human path's own network call was "
                "reached (NETWORK FORBIDDEN in stderr, never a render-specific refusal)",
                "NETWORK FORBIDDEN" in stderr, stderr[-300:])
    return ok


def extra_b_non_admissible_uri():
    """PRD (b) pt 3: the same valid render token on a non-print, non-admissible CloudFront
    path is refused."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(mint_result.token, "/unrelated/non-admissible/path", "GET", route)
    return check("Eb: V3 refuses a non-admissible CloudFront path (PRD item b pt 3)",
                 out["v3"]["admitted"] is False, out["v3"].get("message"))


def extra_i_post_mint_revocation():
    """PRD (i): revoking the DELEGATOR's entitlement after the mint makes the next render read
    refuse -- same token, same headers, a SECOND resolve_now against a REVOKED ownership map."""
    mint_result = _mint.mint_render_token(WORLD1["bundle"], private_key_pem=PRIV_PEM)
    route = {"routeKey": WORLD1["route_key"], "pathParameters": {WORLD1["claim_name"]: WORLD1["claim_value"]}}
    out, _ = call_bridge(mint_result.token, WORLD1["uri"], "GET", route)
    assert out["v3"]["admitted"] and out["v2"]["authorized"]

    key_op = _served.key_operation(WORLD1["published_op"])
    e_before = build_enforcer(WORLD1)
    request = _enforce.Request(out["v3"]["headers"], key_op, "account", WORLD1["a"])
    scope_before, refusal_before = e_before.resolve_now(request)
    ok = check("Ei: first read (before revocation) is admitted", refusal_before is None)

    def revoked_ownership(_t):
        return {"schema_version": 1, "advisors": {WORLD1["advisor_id"]: {"accounts": [], "relationships": []}}}

    e_after = build_enforcer(WORLD1, ownership_override=revoked_ownership)
    request2 = _enforce.Request(out["v3"]["headers"], key_op, "account", WORLD1["a"])
    scope_after, refusal_after = e_after.resolve_now(request2)
    ok &= check("Ei: SAME token, second read AFTER revocation is refused (PRD item i)",
                scope_after is None and refusal_after is not None, repr(refusal_after))
    return ok


def main():
    print("=" * 78)
    print("IRPT_BCKEND.TO-IB-rtr-e -- THE ONE OFFLINE ACTUAL-MODULE CHAIN")
    print("root:", ROOT)
    print("=" * 78)

    print("\n-- POSITIVE: 3 distinct fixture bundle/account objects --")
    pos_results = [run_positive(w) for w in WORLDS]

    permitted_sets = [tuple(sorted(RESULTS[w["tag"]]["permitted_account_set"] or [])) for w in WORLDS]
    check("all 3 positive results are non-overlapping (genuine parameterization, CELL arm b)",
          len(set(permitted_sets)) == 3, str(permitted_sets))

    print("\n-- NEGATIVES: 6 arms, each through the same real chain --")
    neg_results = [
        negative_1_forbidden_claim(),
        negative_2_expired(),
        negative_3_swapped_path_id(),
        negative_4_wrong_bundle_id(),
        negative_5_unlisted_operation(),
        negative_6_missing_render_marker(),
    ]

    print("\n-- EXTRA: additional item-7 arms beyond the 6 mandatory negatives --")
    extra_results = [
        extra_f_human_token_unaffected(),
        extra_b_non_admissible_uri(),
        extra_i_post_mint_revocation(),
    ]

    print("\n" + "=" * 78)
    total = len(pos_results) + len(neg_results) + len(extra_results)
    passed = sum(1 for r in pos_results + neg_results + extra_results if r)
    print("SUMMARY: %d of %d top-level checks passed; %d individual FAIL label(s): %s"
          % (passed, total, len(FAILURES), FAILURES))
    print("RESULTS:", json.dumps(RESULTS, indent=2, default=str))
    print("=" * 78)

    if FAILURES:
        print("FAIL: %d assertion(s) failed: %s" % (len(FAILURES), FAILURES))
        return 1
    print("PASS: the full chain test passed -- 3/3 positive fixtures resolved, 6/6 negative "
          "arms refused/UNKNOWN, plus 3 additional item-7 checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
