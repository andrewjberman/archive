#!/usr/bin/env python3
"""IB-s-3 acceptance battery -- criterion S3-AC1, arms (a) through (e).

Prints `IBS3-AUTHZ-LIBRARY` on the LAST line if and only if EVERY arm passes. The token is
emitted from exactly one place at the very end, because it is the only thing the criterion
reads.

Every count carries its DENOMINATOR, and every arm that asserts an ABSENCE (no protected
bytes, no leak, no serve) carries a control that makes the same instrument go NON-ZERO on the
positive case. An assertion that cannot fail has not been tested.

Usage:  python battery_ib_s_3.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *([os.pardir] * 7)))
_PKG = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting")
AUTHZ = os.path.join(_PKG, "_authz")

for p in (AUTHZ, os.path.join(AUTHZ, "tests"), os.path.join(_PKG, "_scope"),
          os.path.join(_PKG, "_keys")):
    if p not in sys.path:
        sys.path.insert(0, p)

import enforce as ez        # noqa: E402
import fixtures as fx       # noqa: E402
import keys as _keys        # noqa: E402
import resolve as _scope    # noqa: E402

RESULTS = []
PROTECTED = "PROTECTED-PAYLOAD"


def record(arm, verdict, line):
    RESULTS.append((arm, verdict, line))
    print("ARM {} {}: {}".format(arm, verdict, line))


def section(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def payload(scope):
    """A handler that returns protected bytes AND the account ids it was allowed to see.

    Deliberately maximal: if a refusal ever leaked a payload, this is the string the byte
    census would find, and if a serve ever widened, these are the ids it would carry.
    """
    return {"secret": PROTECTED, "accounts": list(scope["permitted_account_set"]),
            "names": ["Whitfield Family", "Alder Holdings LLC"]}


def enforcer(deps=None, cache=None, artifacts=None):
    deps = deps or fx.Deps()
    binding = ez.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
    return ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                       artifacts=dict(artifacts if artifacts is not None else fx.ARTIFACTS),
                       cache=cache if cache is not None else {}), deps


# THE SECRET TOKENS a refusal must never carry. Written as the protected payload PLUS every id
# and name in the fixture directory -- derived from the fixture, not listed by hand, so a new
# fixture entry cannot silently fall outside the census.
def secret_tokens():
    toks = {PROTECTED}
    for entry in fx.DIRECTORY["entries"]:
        ids = entry["ids"]
        toks.add(ids["client_id"])
        if ids.get("relationship_id"):
            toks.add(ids["relationship_id"])
        toks.update(ids["account_ids"])
        toks.add(entry["display_name"])
        toks.add(entry["masked_discriminator"])
    return sorted(toks)


def leaks(envelope, tokens):
    blob = json.dumps(envelope, sort_keys=True)
    return sorted(t for t in tokens if t and t in blob)


# ============================================================================ arm (a)
def arm_a():
    section("ARM (a) -- SIX SWAPS, SIX REFUSALS, AND A BYTE CENSUS ON EVERY REFUSAL")
    ok = True
    tokens = secret_tokens()
    print("  the wrapped handler returns {} protected token(s) when it runs; a refusal must "
          "carry NONE of them".format(len(tokens)))
    print("  DENOMINATOR: {} object kinds the wrapper knows: {}".format(
        len(ez.OBJECT_KINDS), list(ez.OBJECT_KINDS)))

    # THE AUTHORIZED BASELINE. Without it, six refusals could mean the wrapper refuses
    # everything -- which would pass this arm and be useless.
    e, _ = enforcer()
    base = e.serve(ez.Request(fx.headers(), "directory_search", "account", fx.A1), payload)
    print("  BASELINE (must SERVE, else six refusals prove only that nothing works): "
          "ok={} cache_hit={} accounts={}".format(
              base.ok, base.cache_hit, len(base.payload["accounts"]) if base.ok else "-"))
    if not base.ok:
        ok = False

    swaps = [
        ("firm", fx.OTHER_OPAQUE_FIRM, "a second firm's opaque id"),
        ("advisor", fx.ADVISOR_B, "another advisor's id"),
        ("account", fx.A5, "an account outside the grant"),
        ("relationship", fx.R2, "a relationship reaching one permitted and one unpermitted"),
        ("report", fx.REPORT_OTHER, "a report built over another advisor's account"),
        ("pdf", fx.PDF_OTHER, "a PDF built over another advisor's account"),
    ]
    refused = 0
    clean = 0
    for kind, oid, why in swaps:
        e, _ = enforcer()
        out = e.serve(ez.Request(fx.headers(), "directory_search", kind, oid), payload)
        env = out.as_envelope() if not out.ok else {"ok": True, "payload": out.payload}
        found = leaks(env, tokens)
        refused += 0 if out.ok else 1
        clean += 1 if not found else 0
        print("    SWAP {:<13} ({:<52}) -> {:<24} leaked {} of {} protected token(s)".format(
            kind, why, ("REFUSED " + out.code) if not out.ok else "SERVED -- FAIL",
            len(found), len(tokens)))
        if out.ok or found:
            ok = False
            if found:
                print("      LEAKED: {}".format(found[:3]))
    print("  {} of {} swaps REFUSED; {} of {} refusals carry 0 protected tokens".format(
        refused, len(swaps), clean, len(swaps)))

    # POSITIVE CONTROL on the byte census: it must find the tokens when they ARE there.
    control = leaks({"ok": True, "payload": base.payload} if base.ok else {}, tokens)
    print("  POSITIVE CONTROL on the byte census: the SERVED response trips it at {} of {} "
          "token(s) -- the census can go non-zero".format(len(control), len(tokens)))
    if not control:
        ok = False
    record("a", "PASS" if ok else "FAIL",
           "{} of {} swaps refused; {} of {} refusals leaked 0 of {} protected tokens; the "
           "served baseline trips the same census at {}".format(
               refused, len(swaps), clean, len(swaps), len(tokens), len(control)))


# ============================================================================ arm (b)
def arm_b():
    section("ARM (b) -- REVOKED AGAINST A WARM CACHE: THE DIFFERENCE CONTROL")
    ok = True
    e, deps = enforcer()
    req = lambda: ez.Request(fx.headers(), "directory_search", "account", fx.A1)  # noqa: E731

    first = e.serve(req(), payload)
    print("  OUTCOME 1 -- BEFORE revocation: ok={} cache_hit={} key={}...".format(
        first.ok, first.cache_hit, first.key[:46]))
    warm_keys = sorted(e.cache.keys())
    print("    cache now holds {} entry(ies)".format(len(e.cache)))
    if not first.ok or first.cache_hit:
        ok = False

    deps.revoke()
    print("    REVOKED in the fixture POLICY only: the ownership map now grants advisor A "
          "{} account(s); the cache was NOT touched".format(
              len(fx.OWNERSHIP_REVOKED["advisors"][fx.ADVISOR_A]["accounts"])))
    second = e.serve(req(), payload)
    env = second.as_envelope() if not second.ok else {"payload": second.payload}
    found = leaks(env, secret_tokens())
    print("  OUTCOME 2 -- AFTER revocation, SAME request, cache still warm: ok={} code={} "
          "leaked {} protected token(s)".format(
              second.ok, getattr(second, "code", "-"), len(found)))
    print("    cache STILL holds {} entry(ies), keys unchanged: {}".format(
        len(e.cache), sorted(e.cache.keys()) == warm_keys))
    if second.ok or found or sorted(e.cache.keys()) != warm_keys:
        ok = False

    deps.restore()
    third = e.serve(req(), payload)
    print("  OUTCOME 3 -- grant RESTORED, same request: ok={} cache_hit={} (must be True: the "
          "entry was never evicted, so outcome 2 was a REFUSAL and not a cold cache)".format(
              third.ok, third.cache_hit))
    if not (third.ok and third.cache_hit):
        ok = False
    print("  the three outcomes differ ONLY in the grant: same request, same cache, same key "
          "on 1 and 3")
    record("b", "PASS" if ok else "FAIL",
           "3 of 3 outcomes as specified -- served, refused-while-warm ({} cache entries "
           "untouched), then served FROM THE STILL-WARM CACHE".format(len(e.cache)))


# ============================================================================ arm (c)
def arm_c():
    section("ARM (c) -- REAUTHORIZE AT CONSUMPTION")
    ok = True
    e, deps = enforcer()
    sub = e.submit_job(ez.Request(fx.headers(), "build_report", "account", fx.A1), "JOB-1")
    print("  job JOB-1 submitted under scope S: ok={} fingerprint={}...".format(
        sub.ok, sub.fingerprint[:16]))
    if not sub.ok:
        ok = False
    print("    the job record stores the submission fingerprint as EVIDENCE, never as a grant")

    deps.revoke()
    out = e.consume_job(ez.Request(fx.headers(), "build_report"), "JOB-1",
                        {"secret": PROTECTED})
    env = out.as_envelope() if not out.ok else {"payload": out.payload}
    found = leaks(env, secret_tokens())
    print("  consumed AFTER S was revoked: ok={} code={} leaked {} protected token(s)".format(
        out.ok, getattr(out, "code", "-"), len(found)))
    if out.ok or found:
        ok = False

    # CONTROL: a job whose scope still covers it IS delivered, so the refusal above is not
    # "consumption never works".
    deps.restore()
    e.submit_job(ez.Request(fx.headers(), "build_report", "account", fx.A1), "JOB-2")
    good = e.consume_job(ez.Request(fx.headers(), "build_report"), "JOB-2", {"ok": 1})
    print("  CONTROL: a job still covered at consumption -> ok={} reauthorized_at_consumption={}"
          .format(good.ok, good.census.get("reauthorized_at_consumption")))
    if not good.ok:
        ok = False
    record("c", "PASS" if ok else "FAIL",
           "a job submitted under S and consumed after S was revoked is REFUSED with 0 "
           "protected tokens; a job still covered is delivered (1 of 1 control)")


# ============================================================================ arm (d)
def arm_d():
    section("ARM (d) -- EVERY KEY THROUGH THE GRAMMAR; A CLIENT-NAME KEY RAISES")
    ok = True
    e, _ = enforcer()
    built = []
    cases = [
        ("directory_search", {"as_of": "2026-09-10", "view": "OVERVIEW"}),
        ("build_report", {"as_of": "2026-09-10", "pages": 12, "linked": True}),
        ("holdings_snapshot", {"as_of": "2026-09-10"}),
    ]
    for op, params in cases:
        out = e.serve(ez.Request(fx.headers(), op, "account", fx.A1, params=params), payload)
        if not out.ok:
            ok = False
            print("    {:<20} REFUSED unexpectedly: {}".format(op, out.reason[:60]))
            continue
        built.append(out.key)
        print("    {:<20} -> {}".format(op, out.key))
    print("  {} of {} operations produced a key; every one was built by _keys.cache_key "
          "(the wrapper has no other key path)".format(len(built), len(cases)))

    # Each built key is re-admitted by the grammar's own digest check, and each carries the
    # five required components.
    admitted = 0
    for k in built:
        digest = _keys.key_digest(k)
        parts = k.split("/")
        has = all(x in k for x in ("asf=", "src=", "sch=", "cfg=")) and parts[2] == fx.TENANT
        admitted += 1 if (digest and has) else 0
    print("  {} of {} keys carry tenant + fingerprint + source/schema/config revisions and are "
          "accepted by _keys.key_digest".format(admitted, len(built)))
    if admitted != len(built) or not built:
        ok = False

    # A HANDLER THAT TRIES TO KEY BY CLIENT NAME.
    name_cases = [("client", "Whitfield Family"), ("owner", "Smith-Family"),
                  ("cohort", "49FINANCIAL"), ("label", "advisor.a@49financial.com")]
    refused = 0
    for pname, pval in name_cases:
        out = e.serve(ez.Request(fx.headers(), "directory_search", "account", fx.A1,
                                 params={pname: pval}), payload)
        leaked = leaks(out.as_envelope() if not out.ok else {"p": out.payload}, [pval])
        refused += 1 if (not out.ok and out.code == "KEY_REFUSED") else 0
        print("    param {:<7}={:<28} -> {:<22} the value appears in the refusal: {}".format(
            pname, pval[:28], ("REFUSED " + out.code) if not out.ok else "KEYED -- FAIL",
            bool(leaked)))
        if out.ok or leaked:
            ok = False
    print("  {} of {} name-shaped key components REFUSED by the grammar".format(
        refused, len(name_cases)))

    # NEGATIVE CONTROL: the grammar admits well-shaped components, so the refusals above are
    # not "every parameter is refused".
    control = e.serve(ez.Request(fx.headers(), "directory_search", "account", fx.A1,
                                 params={"as_of": "2026-09-10", "kind": "PORTRAIT"}), payload)
    print("  NEGATIVE CONTROL: well-shaped components (an ISO date and an enum token) are "
          "ADMITTED: ok={}".format(control.ok))
    if not control.ok:
        ok = False
    record("d", "PASS" if ok else "FAIL",
           "{} of {} operations keyed through _keys with all five required components; {} of {} "
           "name-shaped components refused; well-shaped components still admitted".format(
               len(built), len(cases), refused, len(name_cases)))


# ============================================================================ arm (e)
def arm_e():
    section("ARM (e) -- THE FIRM-AUTHORIZED VIEWER, UNDER THE SAME RULES")
    ok = True
    e, _ = enforcer()
    population, census = _scope.firm_population(fx.DIRECTORY, fx.OPAQUE_FIRM)
    print("  the firm's directory population: {} account rows -> {} unique account(s)".format(
        census["account_rows"], census["unique_accounts"]))

    advisor = e.serve(ez.Request(fx.headers(), "directory_search", "account", fx.A1), payload)
    admin = e.serve(ez.Request(fx.headers(role="admin"), "directory_search", "account", fx.A5),
                    payload)
    print("  ADVISOR viewer    : principal={:<16} sees {} of {} firm accounts".format(
        "FIRM_ADVISOR", len(advisor.payload["accounts"]) if advisor.ok else 0,
        census["unique_accounts"]))
    print("  FIRM-AUTH viewer  : principal={:<16} sees {} of {} firm accounts (ok={})".format(
        "FIRM_OPERATIONS", len(admin.payload["accounts"]) if admin.ok else 0,
        census["unique_accounts"], admin.ok))
    if not admin.ok or set(admin.payload["accounts"]) != set(population):
        ok = False
    if not advisor.ok or len(advisor.payload["accounts"]) >= census["unique_accounts"]:
        ok = False

    print("  SAME RULES, not a bypass -- the firm-authorized viewer is still refused on:")
    checks = [
        ("another firm's id", "firm", fx.OTHER_OPAQUE_FIRM),
        ("an artifact of another firm", "report", "REP-FOREIGN"),
    ]
    e.artifacts["REP-FOREIGN"] = {"kind": "report", "firm": fx.OTHER_OPAQUE_FIRM,
                                  "account_ids": [fx.A1]}
    refused = 0
    for why, kind, oid in checks:
        out = e.serve(ez.Request(fx.headers(role="admin"), "directory_search", kind, oid),
                      payload)
        refused += 0 if out.ok else 1
        print("    {:<30} -> {}".format(why, ("REFUSED " + out.code) if not out.ok
                                             else "SERVED -- FAIL"))
        if out.ok:
            ok = False
    print("    {} of {} cross-firm attempts by the firm-authorized viewer refused".format(
        refused, len(checks)))

    # The key differs too: a wider account set is a different fingerprint, so the admin cannot
    # be served the advisor's cached answer or vice versa.
    print("  cache keys differ between the two viewers: {}".format(
        advisor.key != admin.key))
    if advisor.key == admin.key:
        ok = False
    record("e", "PASS" if ok else "FAIL",
           "the firm-authorized viewer sees {} of {} firm accounts (the advisor sees {}), is "
           "refused on {} of {} cross-firm attempts, and does not share the advisor's cache "
           "key".format(len(admin.payload["accounts"]) if admin.ok else 0,
                        census["unique_accounts"],
                        len(advisor.payload["accounts"]) if advisor.ok else 0,
                        refused, len(checks)))


# ============================================================================ AC2 evidence
def ac2_evidence():
    section("S3-AC2 EVIDENCE (recorded for 3.0.0_SA_CVO -- NOT an arm, NOT self-graded)")
    e, _ = enforcer()

    @e.guard("directory_search", "account")
    def guarded(request, scope):
        return payload(scope)

    def unguarded(request, scope=None):
        return {"secret": PROTECTED}

    print("  CAN A HANDLER BYPASS THE WRAPPER? Yes -- nothing in Python can stop a route table")
    print("  pointing at an unwrapped function. The wrapper therefore MARKS what it wraps, and")
    print("  the census reads the ROUTE TABLE (what is reachable), not a module's functions:")
    clean = ez.unguarded_routes({"GET /directory": guarded})
    dirty = ez.unguarded_routes({"GET /directory": guarded, "GET /leak": unguarded})
    print("    clean table: {}".format(json.dumps(clean, sort_keys=True)))
    print("    one unwrapped route: {}".format(json.dumps(dirty, sort_keys=True)))
    print("  is_guarded(guarded)={} is_guarded(unguarded)={}".format(
        ez.is_guarded(guarded), ez.is_guarded(unguarded)))
    print("")
    print("  WHAT AN IN-MEMORY HANDLER CANNOT SHOW (IB-sb-3's job, over DEPLOYED routes):")
    for line in (
        "the EDGE VALIDATOR actually injecting the nine headers -- here they are a dict a test wrote",
        "the API GATEWAY AUTHORIZER (partners-api CUSTOM pattern) and its own result cache",
        "API Gateway / CloudFront RESPONSE caching, which can serve bytes before any Lambda runs",
        "the Lambda EXECUTION ENVIRONMENT cache: a module-level cache surviving across invocations",
        "IAM on the read path -- whether the role can even fetch the directory it authorizes against",
        "concurrency: a revocation landing BETWEEN the authorize and the serve of one request",
    ):
        print("    - {}".format(line))


# ============================================================================ main
def main():
    print("IB-s-3 BATTERY -- {}".format(
        dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    print("repo: {}".format(_REPO))
    for fn in (arm_a, arm_b, arm_c, arm_d, arm_e):
        fn()
    ac2_evidence()
    section("SUMMARY")
    for arm, verdict, line in RESULTS:
        print("  ARM ({}) {}: {}".format(arm, verdict, line))
    passed = sum(1 for _, v, _ in RESULTS if v == "PASS")
    print("  {} of 5 arms PASS".format(passed))
    if passed == 5 and len(RESULTS) == 5:
        print("IBS3-AUTHZ-LIBRARY")
        return 0
    print("TOKEN WITHHELD -- {} of 5 arms PASS".format(passed))
    return 1


if __name__ == "__main__":
    sys.exit(main())
