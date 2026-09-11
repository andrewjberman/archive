#!/usr/bin/env python3
"""IB-s-15 acceptance battery -- criterion S15-AC1, arms (a)-(g) and (amend).

Prints `IBS15-ROUTES-LIVE` on the LAST line if and only if EVERY arm passes. This face carries
NO rule admitting a blocked arm -- unlike IB-s-4's arm (h) -- so a BLOCKED arm withholds the
token and leaves the order open. That is the designed outcome when a served-surface gate fires,
and it is not softened here.

Every count carries its DENOMINATOR. Every absence carries a control that can go non-zero.

Usage:  python battery_ib_s_15.py
"""
from __future__ import annotations

import datetime as dt
import importlib
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *([os.pardir] * 7)))
_PKG = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting")
_SCOPE = os.path.join(_PKG, "_scope")
_API_TF = os.path.join(_REPO, "infra", "aws", "terraform", "investor-reporting", "api")
_SCRATCH = os.path.join(_REPO, ".scratch")

for p in (_SCOPE, os.path.join(_SCOPE, "tests"), os.path.join(_PKG, "_authz"),
          os.path.join(_PKG, "_authz", "tests"), os.path.join(_PKG, "_keys")):
    if p not in sys.path:
        sys.path.insert(0, p)

import enforce as ez                 # noqa: E402
import keys as _keys                 # noqa: E402

glb = importlib.import_module("global")
tg = importlib.import_module("test_global")     # the two-firm fixtures, reused not rebuilt

RESULTS = []
API_ID = "7k3ed8px20"
AUTHORIZER = "naqxlm"
DIST_ID = "EVTSA9VEHNZVH"
PORTAL_HOST = "https://opalinvest.dev"
PROBE_PATH = "/api/scoped/investor-reporting/status"
ROUTES_JSON = os.path.join(_API_TF, "routes.json")
LEDGER_DIR = os.path.join(_REPO, "org", "critical_paths", "change_management")


def record(arm, verdict, line):
    RESULTS.append((arm, verdict, line))
    print("ARM {} {}: {}".format(arm, verdict, line))


def section(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def _aws(args, timeout=180):
    shim = os.path.join(_REPO, ".tools", "aws.cmd" if os.name == "nt" else "aws")
    if not os.path.isfile(shim):
        return 127, "BLOCKED: aws shim absent at " + shim
    p = subprocess.run([shim] + args, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).replace(chr(13), "").strip()


def _routes_json():
    with open(ROUTES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ============================================================================ arm (a)
def arm_a():
    section("ARM (a) -- EVERY ROUTE, THE AUTHORIZER")
    ok = True
    doc = _routes_json()
    declared = [r for r in doc["routes"] if r["status"] == "DECLARED"]
    no_handler = [r for r in doc["routes"] if r["status"] == "NO-HANDLER-AT-HEAD"]
    print("  routes.json DENOMINATOR: %d route(s) total = %d DECLARED + %d NO-HANDLER-AT-HEAD"
          % (len(doc["routes"]), len(declared), len(no_handler)))
    print("  (the file carries its own arithmetic: %s)" % json.dumps(doc["_denominator"]))
    if len(declared) + len(no_handler) != len(doc["routes"]):
        ok = False

    rc, out = _aws(["apigatewayv2", "get-routes", "--api-id", API_ID, "--output", "json"])
    items = json.loads(out).get("Items", []) if rc == 0 else []
    mine = [i for i in items if "/investor-reporting/" in i.get("RouteKey", "")]
    print("  get-routes --api-id %s rc=%d: %d route(s) on the API, %d under this prefix"
          % (API_ID, rc, len(items), len(mine)))
    live = {i["RouteKey"]: i for i in mine}
    present = [r for r in declared if r["route_key"] in live]
    print("  DECLARED routes present live: %d of %d" % (len(present), len(declared)))
    with_auth = [r for r in present
                 if live[r["route_key"]].get("AuthorizerId") == AUTHORIZER
                 and live[r["route_key"]].get("AuthorizationType") == "CUSTOM"]
    print("  carrying AuthorizationType CUSTOM + AuthorizerId %s: %d of %d"
          % (AUTHORIZER, len(with_auth), len(present)))
    for r in declared:
        state = ("LIVE " + live[r["route_key"]].get("AuthorizerId", "?")) if r["route_key"] in live else "ABSENT"
        print("    %-62s -> %-12s %s" % (r["route_key"][:62], r["handler"], state))
    if len(present) != len(declared) or len(with_auth) != len(declared):
        ok = False

    # THE NO-HANDLER ROUTE MUST NOT BE LIVE. An enumerated route with no handler that somehow
    # answered would be worse than the gap it records.
    for r in no_handler:
        print("    %-62s -> %-12s %s" % (r["route_key"][:62], "(none)",
                                         "NOT DECLARED (correct)" if r["route_key"] not in live
                                         else "LIVE -- FAIL"))
        if r["route_key"] in live:
            ok = False

    # Each integration targets one of THIS project's Lambdas.
    rc2, out2 = _aws(["apigatewayv2", "get-integrations", "--api-id", API_ID, "--output",
                      "json"])
    integs = {i["IntegrationId"]: i for i in (json.loads(out2).get("Items", [])
                                              if rc2 == 0 else [])}
    targets, foreign = set(), []
    for r in present:
        tgt = live[r["route_key"]].get("Target", "")
        iid = tgt.split("/")[-1]
        uri = integs.get(iid, {}).get("IntegrationUri", "")
        fn = uri.split(":function:")[-1].split("/")[0] if ":function:" in uri else uri
        targets.add(fn)
        if not fn.startswith("irpt-"):
            foreign.append((r["route_key"], fn))
    print("  integration targets: %d distinct function(s) %s" % (len(targets), sorted(targets)))
    print("  targets NOT belonging to this project: %d of %d (must be 0)"
          % (len(foreign), len(present)))
    if foreign:
        ok = False
    record("a", "PASS" if ok else "FAIL",
           "%d of %d DECLARED routes live with CUSTOM/%s; %d of %d integration targets are this "
           "project's; the NO-HANDLER route is enumerated and NOT live"
           % (len(present), len(declared), AUTHORIZER, len(present) - len(foreign), len(present)))


# ============================================================================ arm (b)
def arm_b():
    section("ARM (b) -- THE BEHAVIOR IS LIVE: THE DIFFERENCE CONTROL")
    pre_meta = _read(os.path.join(_SCRATCH, "pre_curl_meta.txt"))
    pre_body = _read(os.path.join(_SCRATCH, "pre_curl_body.txt"))[:120]
    print("  PRE-APPLY (recorded before any act):")
    for line in pre_meta.strip().splitlines():
        print("    | %s" % line)
    print("    | first bytes: %s" % pre_body.replace("\n", " ")[:100])

    rc, out = _aws(["cloudfront", "get-distribution-config", "--id", DIST_ID, "--output",
                    "json"])
    patterns = []
    if rc == 0:
        cfg = json.loads(out)["DistributionConfig"]
        patterns = [i["PathPattern"] for i in cfg["CacheBehaviors"]["Items"]]
    here = [p for p in patterns if "investor-reporting" in p]
    print("  NOW: get-distribution-config rc=%d, %d ordered behavior(s); investor-reporting "
          "behavior present: %s" % (rc, len(patterns), bool(here)))

    p = subprocess.run(["curl", "-s", "-o", os.path.join(_SCRATCH, "post_curl_body.txt"),
                        "-w", "HTTP_STATUS=%{http_code} CONTENT_TYPE=%{content_type} "
                              "SIZE=%{size_download}",
                        PORTAL_HOST + PROBE_PATH], capture_output=True, text=True, timeout=120)
    print("  POST request to %s%s -> %s" % (PORTAL_HOST, PROBE_PATH, p.stdout.strip()))
    status = ""
    for tok in p.stdout.split():
        if tok.startswith("HTTP_STATUS="):
            status = tok.split("=", 1)[1]
    refused = status in ("401", "403")
    print("  refused (401/403): %s" % refused)
    if here and refused:
        record("b", "PASS", "the behavior is live and the same unauthenticated request that "
                            "returned the SPA now returns %s" % status)
        return
    record("b", "BLOCKED",
           "the behavior is NOT applied (row IRPT_BCKEND-W2-S12): the portal-auth plan named "
           "THREE resources and the bound stops at any change but mine. The PRE half stands "
           "(HTTP 200 text/html, 1068 bytes of the SPA) and the POST half still reads %s -- "
           "unchanged, because the world is unchanged" % (status or "unknown"))


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


# ============================================================================ arm (c)
def arm_c():
    section("ARM (c) -- EXACTLY ONE CHANGE")
    plan = _read(os.path.join(_SCRATCH, "tfplan_portal_auth.txt"))
    verdict = [ln for ln in plan.splitlines() if ln.startswith("Plan:")]
    named = [ln.strip() for ln in plan.splitlines()
             if ln.strip().startswith("# ") and ("will be" in ln)]
    print("  the saved pre-apply plan on portal-auth, verbatim:")
    for ln in verdict:
        print("    | %s" % ln)
    for ln in named:
        print("    | %s" % ln)
    mine = [ln for ln in named if "aws_cloudfront_distribution.portal" in ln]
    others = [ln for ln in named if "aws_cloudfront_distribution.portal" not in ln]
    print("  resources in the plan: %d -- %d this cell's, %d NOT this cell's"
          % (len(named), len(mine), len(others)))

    # MY OWN resource's diff, counted: exactly one added behavior block.
    block = plan.split("aws_cloudfront_distribution.portal will be updated")[-1]
    block = block.split("# aws_cloudfront_function")[0] if "# aws_cloudfront_function" in block \
        else block
    added = block.count("+ ordered_cache_behavior {")
    removed = block.count("- ordered_cache_behavior {")
    print("  inside aws_cloudfront_distribution.portal: %d added ordered_cache_behavior "
          "block(s), %d removed -- the clean half" % (added, removed))

    # WHAT THE OTHER TWO ARE, measured rather than guessed.
    js = os.path.join(_REPO, "infra", "aws", "terraform", "portal-auth",
                      "spa-fallback-function.js")
    with open(js, "rb") as fh:
        raw = fh.read()
    g = subprocess.run(["git", "show", "HEAD:infra/aws/terraform/portal-auth/"
                        "spa-fallback-function.js"], cwd=_REPO, capture_output=True, timeout=60)
    print("  spa_fallback: on disk %d CRLF / %d bare LF; HEAD blob %d CRLF / %d bare LF "
          "-- a CHECKOUT ARTIFACT, measured"
          % (raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n"),
             g.stdout.count(b"\r\n"), g.stdout.count(b"\n") - g.stdout.count(b"\r\n")))
    waf = plan.split("aws_wafv2_web_acl.opal_cloudfront_protection will be updated")[-1]
    print("  waf acl: %d rule block(s) removed and %d re-added -- REAL churn on the WAF "
          "protecting the whole portal"
          % (waf.count("- rule {"), waf.count("+ rule {")))

    if len(named) == 1 and added == 1 and removed == 0:
        record("c", "PASS", "exactly one resource in the plan and exactly one added behavior")
        return
    record("c", "BLOCKED",
           "the plan names %d resources, not 1 (%s). This cell's own diff IS clean -- %d added "
           "behavior block, %d removed -- but the bound is 'exactly ONE change or you STOP', so "
           "safe-apply was never invoked. Row IRPT_BCKEND-W2-S12"
           % (len(named), verdict[0] if verdict else "?", added, removed))


# ============================================================================ arm (d)
def arm_d():
    section("ARM (d) -- GLOBAL, ON FIXTURES")
    ok = True
    roster = frozenset({tg.OPAL_SUBJECT})
    cases = 0

    a, ra = glb.resolve_for_request(tg.headers(tg.OPAL_SUBJECT, ""), tg.DIR_A, tg.OWN_A,
                                    selected_firm_id=tg.FIRM_A,
                                    id_projection=tg.projection_for(tg.FIRM_A), roster=roster,
                                    binding=tg.binding_for(tg.FIRM_A))
    b, rb = glb.resolve_for_request(tg.headers(tg.OPAL_SUBJECT, ""), tg.DIR_B, tg.OWN_B,
                                    selected_firm_id=tg.FIRM_B,
                                    id_projection=tg.projection_for(tg.FIRM_B), roster=roster,
                                    binding=tg.binding_for(tg.FIRM_B))
    two_firms = (ra is None and rb is None and a["principal_class"] == "OPAL_GLOBAL"
                 and a["permitted_account_set"] and b["permitted_account_set"]
                 and not set(a["permitted_account_set"]) & set(b["permitted_account_set"]))
    print("  1. an Opal principal reaches clients at TWO firms, one at a time: %s" % two_firms)
    print("     firm A: %d account(s) attributed to %s" % (len(a["permitted_account_set"]),
                                                           a["verified_request_firm_id"][:16]))
    print("     firm B: %d account(s) attributed to %s" % (len(b["permitted_account_set"]),
                                                           b["verified_request_firm_id"][:16]))
    print("     the two sets INTERSECT in %d account(s) (must be 0 -- Global is a SELECTOR, "
          "never a union)" % len(set(a["permitted_account_set"]) & set(b["permitted_account_set"])))
    cases += 1 if two_firms else 0
    ok = ok and two_firms

    replay, refusal = glb.resolve_for_request(
        tg.headers("advisor@49financial.com", tg.FIRM_A), tg.DIR_B, tg.OWN_B,
        selected_firm_id=tg.FIRM_B, id_projection=tg.projection_for(tg.FIRM_B), roster=roster,
        binding=tg.binding_for(tg.FIRM_B))
    replayed_refused = (replay is None and refusal is not None
                        and refusal.code == "FIRM_BINDING")
    print("  2. a firm advisor REPLAYING the same request is refused: %s (%s)"
          % (replayed_refused, refusal.code if refusal else "SERVED -- FAIL"))
    cases += 1 if replayed_refused else 0
    ok = ok and replayed_refused

    f, _rf = glb.resolve_for_request(tg.headers("advisor@49financial.com", tg.FIRM_A),
                                     tg.DIR_A, tg.OWN_A,
                                     id_projection=tg.projection_for(tg.FIRM_A), roster=roster,
                                     binding=tg.binding_for(tg.FIRM_A))
    same = (glb.answer_fingerprint(a, "cA1", "rev-1")
            == glb.answer_fingerprint(f, "cA1", "rev-1"))
    moves = (glb.answer_fingerprint(a, "cA1", "rev-1")
             != glb.answer_fingerprint(a, "cA1", "rev-2"))
    print("  3. same client + revision, Global vs firm-scoped: identical %s; and the "
          "fingerprint MOVES on a different revision %s (else it is a constant)" % (same, moves))
    cases += 1 if (same and moves) else 0
    ok = ok and same and moves

    after, ref2 = glb.resolve_for_request(tg.headers(tg.OPAL_SUBJECT, ""), tg.DIR_B, tg.OWN_B,
                                          selected_firm_id=tg.FIRM_B,
                                          id_projection=tg.projection_for(tg.FIRM_B),
                                          roster=frozenset(),
                                          binding=tg.binding_for(tg.FIRM_B))
    revoked = (after is None and ref2 is not None)
    print("  4. revoking the Global entitlement takes effect: %s -- the request that reached "
          "firm B now resolves to no firm at all and is refused (%s)"
          % (revoked, ref2.code if ref2 else "SERVED -- FAIL"))
    cases += 1 if revoked else 0
    ok = ok and revoked
    record("d", "PASS" if ok else "FAIL", "%d of 4 Global cases" % cases)


# ============================================================================ arm (e)
def arm_e():
    section("ARM (e) -- THE CATALOGUE IS THE REGISTRY")
    registry = list(_keys.load_firm_ids())
    cat = glb.permitted_firm_catalogue(registry[0] if registry else None)
    names = [c["firm_id"] for c in cat]
    print("  data/firm_registry.json enabled kind=client firms: %d -- %s"
          % (len(registry), registry))
    print("  permitted_firm_catalogue(): %d -- %s" % (len(names), names))
    print("  identical: %s (%d of %d)" % (names == registry, len(names), len(registry)))
    selected = sum(1 for c in cat if c["selected"])
    print("  exactly one selected: %s (%d)" % (selected == 1, selected))
    # The catalogue is DERIVED, so a test/demo tenant must not appear.
    with open(os.path.join(_REPO, "data", "firm_registry.json"), "r", encoding="utf-8") as fh:
        allfirms = json.load(fh)["firms"]
    excluded = [f["firm_id"] for f in allfirms if f["firm_id"] not in names]
    print("  excluded BY KIND, not by name: %d of %d registry firms -- %s"
          % (len(excluded), len(allfirms), excluded))
    ok = names == registry and selected == 1 and len(excluded) == len(allfirms) - len(registry)
    record("e", "PASS" if ok else "FAIL",
           "the catalogue is the registry: %d of %d enabled client firms, %d test/demo excluded "
           "by kind" % (len(names), len(registry), len(excluded)))


# ============================================================================ arm (f)
def arm_f():
    section("ARM (f) -- TWO LEDGERS")
    lines = []
    ok = True
    for slug in ("irpt-bckend-s15", "irpt-bckend-s15-cloudfront"):
        entries = [f for f in sorted(os.listdir(LEDGER_DIR)) if slug + "_" in f]
        if not entries:
            ok = False
            lines.append("%s: NO ENTRY" % slug)
            continue
        text = _read(os.path.join(LEDGER_DIR, entries[-1]))
        status = next((ln for ln in text.splitlines() if ln.startswith("**Status:**")), "")
        legs = text.count("| CLOSED ")
        sp = subprocess.run(["git", "log", "--oneline", "--all", "--",
                             "org/critical_paths/.open_deploys/%s.json" % slug],
                            cwd=_REPO, capture_output=True, text=True, timeout=60)
        commits = [ln for ln in sp.stdout.strip().splitlines() if ln]
        sentinel_present = os.path.isfile(os.path.join(
            _REPO, "org", "critical_paths", ".open_deploys", slug + ".json"))
        print("  %s" % slug)
        print("    %s" % status.strip())
        print("    legs CLOSED: %d" % legs)
        print("    OPEN sentinel committed: %s (%s)" % (bool(commits),
                                                        commits[0] if commits else "NONE"))
        print("    sentinel on disk now: %s (absent by contract at close)" % sentinel_present)
        if not commits or sentinel_present or "CLOSED" not in status:
            ok = False
        lines.append("%s: %d legs, sentinel committed %s" % (slug, legs,
                                                             commits[0].split()[0] if commits
                                                             else "NONE"))
    print("  BUT THE SECOND LEDGER CLOSED ON NON-EXECUTION. Every one of its legs carries a "
          "proof beginning 'NOT APPLIED' or 'NOT REACHED', and the entry carries a "
          "READ-THIS-FIRST block above its status line saying so.")
    if ok:
        record("f", "BLOCKED",
               "both sentinels committed and both entries closed (%s) -- BUT the cloudfront "
               "entry closed on NON-EXECUTION, not on a landed act: the apply was refused by "
               "the plan gate (row IRPT_BCKEND-W2-S12). Reporting this arm as PASS would let "
               "the word CLOSED stand for a deploy that did not happen" % "; ".join(lines))
    else:
        record("f", "FAIL", "; ".join(lines))


# ============================================================================ arm (g)
def arm_g():
    section("ARM (g) -- THE SEAM IS WIRED, AND ITS ABSENCE IS LOUD")
    ok = True
    own = {"schema_version": 1, "advisors": {"ADV-A": {
        "accounts": ["A-1", "A-2", "NOT-IN-DIR"], "relationships": []}}}

    # 1. PROJECTION PRESENT -> the intersection, every unmatched id carrying a reason.
    scope, refusal = glb.resolve_for_request(
        tg.headers("advisor@49financial.com", tg.FIRM_A), tg.DIR_A, own,
        id_projection=tg.projection_for(tg.FIRM_A), binding=tg.binding_for(tg.FIRM_A))
    unmatched = (scope or {}).get("_census", {}).get("unmatched", [])
    kinds = sorted({u["reason"].split(":")[0] for u in unmatched})
    print("  1. PROJECTION PRESENT: granted 3, permitted %d, unmatched %d -- reasons %s"
          % (len((scope or {}).get("permitted_account_set", [])), len(unmatched), kinds))
    print("     every unmatched id carries one of CROSS-FIRM | NOT-IN-DIRECTORY | "
          "UNPROJECTED-ID: %d of %d"
          % (sum(1 for u in unmatched if u["reason"].split(":")[0] in
                 ("CROSS-FIRM", "NOT-IN-DIRECTORY", "UNPROJECTED-ID")), len(unmatched)))
    if refusal is not None or len(scope["permitted_account_set"]) != 2 or not unmatched:
        ok = False

    # 2. PROJECTION ABSENT with a grant present -> REFUSED, never an empty 200.
    s2, r2 = glb.resolve_for_request(
        tg.headers("advisor@49financial.com", tg.FIRM_A), tg.DIR_A, own,
        id_projection=None, binding=tg.binding_for(tg.FIRM_A))
    print("  2. PROJECTION ABSENT, grant present: scope=%s refusal=%s -- %d granted account(s) "
          "were never joined" % (s2, r2.code if r2 else None,
                                 r2.census.get("granted_accounts") if r2 else -1))
    print("     served as an empty 200 instead? %s (must be False -- an empty set reads exactly "
          "like a correct revocation)" % (s2 is not None))
    if s2 is not None or not r2 or r2.code != "UNPROJECTED_GRANT":
        ok = False

    # 3. ONE DEFINITION. The projection IS directory_runner.opaque_id -- not a re-implementation
    #    that happens to agree, which is why this equality is by CONSTRUCTION and says so.
    runner = os.path.join(_REPO, "data", "assets", "scripts", "gold", "investor_reporting",
                          "directory_runner.py")
    proj = tg.projection_for(tg.FIRM_A)
    samples = ["A-1", "12345678", "ACC-0001"]
    equal = sum(1 for s in samples if proj("account", s) == tg.opaque("account", tg.FIRM_A, s))
    print("  3. ONE DEFINITION: the projection resolves to opaque_id imported from")
    print("     %s" % runner)
    print("     equal on %d of %d sample raw ids -- BY CONSTRUCTION: it is the SAME function "
          "object, not a second implementation that agrees" % (equal, len(samples)))
    print("     _scope/global.py defines opaque_id itself? %s (must be False)"
          % ("opaque_id" in [n for n in dir(glb)]))
    if equal != len(samples) or "opaque_id" in dir(glb):
        ok = False
    print("     RUNTIME GAP, DECLARED: the Lambda runtime cannot import a gold runner and the "
          "irpt-common layer carries contracts + jsonschema + bd_helpers, NOT opaque_id. Per "
          "this face, a module under _scope/ the runner is not edited to import would be a "
          "SECOND definition -- so none was written and the gap is a BLOCKING item, not a "
          "quiet duplicate.")
    record("g", "PASS" if ok else "FAIL",
           "3 outcomes: intersection with %d reasoned gap(s); absent projection REFUSES with "
           "UNPROJECTED_GRANT; the projection equals the runner's one definition on %d of %d "
           "samples" % (len(unmatched), equal, len(samples)))


# ============================================================================ arm (amend)
def arm_amend():
    section("ARM (amend) -- GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE")
    ok = True
    import fixtures as afx

    deps = afx.Deps()
    binding = ez.FirmBinding(afx.TENANT, afx.OPAQUE_FIRM)
    enforcer = ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                           artifacts=dict(afx.ARTIFACTS))

    # THE ROUTES THIS CELL REGISTERS, read from routes.json -- the real file, not a memory.
    doc = _routes_json()
    declared = [r for r in doc["routes"] if r["status"] == "DECLARED"]
    routes = {}
    for r in declared:
        @enforcer.guard("irpt_route", "account")
        def _h(request, scope, _r=r):
            return {"ok": True, "route": _r["route_key"]}
        routes[r["route_key"]] = _h
    census = ez.unguarded_routes(routes)
    print("  routes.json DECLARED: %d; census over them: %s"
          % (len(declared), json.dumps(census, sort_keys=True)))
    print("  reads %d of %d unguarded" % (len(census["unguarded"]), census["routes"]))
    if census["unguarded"] or census["routes"] != len(declared):
        ok = False
    dirty = ez.unguarded_routes(dict(routes, **{"GET /leak": lambda r, s=None: None}))
    print("  POSITIVE CONTROL: the same census over a table carrying ONE unwrapped handler "
          "reads %d of %d unguarded" % (len(dirty["unguarded"]), dirty["routes"]))
    if len(dirty["unguarded"]) != 1:
        ok = False

    # FirmBinding: a non-reconciling binding REFUSES rather than serving empty.
    bad = ez.FirmBinding(afx.TENANT, "fir_SOMETHING_ELSE")
    bad_enf = ez.Enforcer(bad, deps.load_directory, deps.load_ownership, deps.load_policy)
    out_bad = bad_enf.serve(ez.Request(afx.headers(), "irpt_route", "account", afx.A1),
                            lambda s: {"x": 1})
    out_good = enforcer.serve(ez.Request(afx.headers(), "irpt_route", "account", afx.A1),
                              lambda s: {"x": 1})
    print("  non-reconciling FirmBinding -> ok=%s code=%s; reconciling -> ok=%s (the CONTROL)"
          % (out_bad.ok, getattr(out_bad, "code", None), out_good.ok))
    if out_bad.ok or getattr(out_bad, "code", None) != "FIRM_BINDING" or not out_good.ok:
        ok = False

    # A fixture that keys by a client display name: refused, and the WHOLE envelope is silent.
    secret = "Whitfield Family"
    res = enforcer.serve(ez.Request(afx.headers(), "irpt_route", "account", afx.A1,
                                     params={"client": secret}), lambda s: {"x": 1})
    blob = json.dumps({"env": res.as_envelope() if not res.ok else {"served": True},
                       "audit": enforcer.audit}, sort_keys=True)
    hits = blob.count(secret)
    print("  keying by a client display name -> %s; WHOLE-ENVELOPE census (body + reason + "
          "audit trail): %d occurrence(s) across %d bytes"
          % (("REFUSED " + res.code) if not res.ok else "KEYED -- FAIL", hits, len(blob)))
    if res.ok or hits:
        ok = False
    control = json.dumps({"leaky": "the refused value was %s" % secret}).count(secret)
    print("  POSITIVE CONTROL on the census: a synthetic leaky envelope trips it at %d" % control)
    if control != 1:
        ok = False
    record("amend", "PASS" if ok else "FAIL",
           "%d of %d routes.json DECLARED routes unguarded; a non-reconciling FirmBinding "
           "REFUSES while a reconciling one serves; %d occurrence(s) of a refused client name "
           "across the whole envelope and audit trail"
           % (len(census["unguarded"]), census["routes"], hits))


# ============================================================================ main
def main():
    print("IB-s-15 BATTERY -- %s"
          % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("repo: %s" % _REPO)
    for fn in (arm_a, arm_b, arm_c, arm_d, arm_e, arm_f, arm_g, arm_amend):
        fn()
    section("SUMMARY")
    for arm, verdict, line in RESULTS:
        print("  ARM (%s) %s: %s" % (arm, verdict, line))
    expected = 8
    passed = sum(1 for _, v, _ in RESULTS if v == "PASS")
    blocked = [a for a, v, _ in RESULTS if v == "BLOCKED"]
    print("  %d of %d arms PASS; %d BLOCKED: %s" % (passed, expected, len(blocked), blocked))
    if passed == expected and len(RESULTS) == expected:
        print("IBS15-ROUTES-LIVE")
        return 0
    print("  THIS FACE CARRIES NO RULE ADMITTING A BLOCKED ARM. The served-surface gate fired "
          "on a plan naming three resources where the bound allows one, so the token is "
          "WITHHELD and this order stays OPEN -- which is the designed outcome of that bound, "
          "not a failure of the arms that passed.")
    print("TOKEN WITHHELD -- %d of %d arms PASS, blocked: %s" % (passed, expected, blocked))
    return 1


if __name__ == "__main__":
    sys.exit(main())
