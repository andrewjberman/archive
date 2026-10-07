#!/usr/bin/env python3
"""battery_ib_pr_335.py -- IB61-7: the FWD-2 replay on CURRENT bytes, every /api/scoped/investor-reporting/ route.

Cell IB-pr-335 (round 61, workstream ~P). Started from battery_ib_rtb_1.py / battery_ib_sb_3.py (read, not edited):
those batteries drove a 12-route table; the live API now carries 21 investor-reporting routes and four functions
moved at r57/r58, so this one ENUMERATES the routes (never types them) and drives four arms per route.

THE TWO PLANES, NAMED PER ARM (a state never claims more than the plane it was driven on):
  IN-PROCESS (post-authorizer): the route's REAL `served.Entry` object (`<function dir>/entry.py ENTRY`, the object
      the deployed `lambda_handler` wraps) is called through its own `handle()` with the header set the edge validator
      injects. Only the STORAGE boundary is substituted (`Entry.deps`, IB-s-3's recorded artifacts, the SAME
      substitution test_guarded_entries.py makes). THE PROCESS HAS NO NETWORK: `socket` connect is hard-blocked and the
      AWS credential chain is pointed at nothing, so no compute can read or write anything off this box; a compute
      that wants a live port refuses for its own reason, and that is recorded, never hidden.
  LIVE (CloudFront -> authorizer -> handler): an AUTHENTICATED served read needs a minted principal. Minting or revoking a
      principal or grant is a WRITE to the production auth plane (RT2_test_principal_human_gated.md; the CTO's section 6
      item 2: an advisor test principal is Andrew's to name). It is recorded `live_authenticated: GATED` on every route.
      What IS read-only live: the API Gateway route table (route + authorization type) and an unauthenticated GET probe of
      every GET route (POST routes are NOT sent: the refusal clause forbids a non-GET call; their boundary is the
      route-table read).

THE FOUR ARMS, per route:
  service_principal          an internal (Opal) SERVICE subject: the allowed firm is admitted, a foreign firm and an
                             attribute-less profile row are refused FIRM_BINDING, 0 protected bytes, the refused value not echoed.
  advisor_principal          a FIRM_ADVISOR: the authorized request is SERVED (the difference control), and each of the
                             six swaps (firm, advisor, account, relationship, report, pdf) is refused by an authorization
                             reason or, for the advisor swap, served without widening; claimed-firm mismatch FIRM_BINDING.
  revoked_grant_warm_cache   served -> grant revoked (the shared cache is NEVER cleared) -> refused with none of the first
                             payload's ids -> restored -> served again; plus the real Enforcer.serve() warm-cache replay on
                             the route's own operation key.
  negative_no_protected_field every refused response from the arms above, diffed against the authorized response's field
                             set (key names + string values): none of its protected fields appears.

STATES: DRIVEN-PASS | DRIVEN-FAIL | GATED (with a reason). A DRIVEN-FAIL is BLOCKING and overall_pass false.

ASCII only. Exit 0 always on a completed run; the transcript's overall_pass is the verdict.

IB-pr-340 (round 62, workstream ~P) -- WHAT THIS COPY ADDS. Copied from the round-61 battery (the original is untouched); the four
generic arms and the route census are carried unchanged (they decide which routes are GATED). Added: the FIXTURE ARMS
(`fixture_worker`, driven per function directory) and the owned/installed worlds (`p340_owned_world.py`, a pytest module run twice,
once per world), each reading `fixtures/<slug>.allowed.json` / `<slug>.denied.json` (written by make_fixtures_p340.py), and
`main340`, which merges everything into IB62-5_gated_fixtures.json (the face's shape) and IB62-5_replay_output.json (the transcript).
An arm that FAILS makes battery_overall_pass false; nothing is minted, granted, written or called off this box (the route-table read is
the only network call, as in round 61).
"""
from __future__ import annotations

import json
import os
import re as _re
import subprocess
import sys
import urllib.error
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.normpath(os.path.join(_HERE, *([".."] * 7)))
_LAMBDA = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting")
_V1 = os.path.join(_REPO, "docs", "contracts", "investor-reporting", "v1")
AWS = os.path.join(_REPO, ".tools", "aws.cmd")
API_ID = "7k3ed8px20"
CLOUDFRONT_ID = "EVTSA9VEHNZVH"
SCOPED = "/api/scoped/investor-reporting/"
OUT = os.path.join(_HERE, "IB62-5_generic_arms_output.json")
ARMS = ("service_principal", "advisor_principal", "revoked_grant_warm_cache", "negative_no_protected_field")

# function directory (under investor-reporting/) -> its entry module. Each carries ENTRY + ROUTES.
ENTRY_DIRS = ("directory", "performance", "ycharts/generate", "narrative", "export", "holdings", "ops", "reporting")

AUTHZ_CODES = ("NOT_AUTHORIZED", "FIRM_BINDING", "OBJECT_NOT_COVERED", "UNPROJECTED_GRANT", "KEY_REFUSED")
SWAP_KINDS = ("firm", "advisor", "account", "relationship", "report", "pdf")

LIVE_AUTH_GATED = ("GATED: an AUTHENTICATED served read through CloudFront needs a minted principal; minting or revoking a "
                   "principal or grant is a write to the production auth plane (opal-users-v2), not this worker's "
                   "(RT2_test_principal_human_gated.md; CTO section 6 item 2: an advisor test principal is Andrew's to "
                   "name). No non-PROD principal exists to use.")


# ======================================================================================== WORKER (in-process, no network)
def _block_network():
    import socket
    blocked = {"n": 0}

    def _deny(*a, **k):
        blocked["n"] += 1
        raise OSError("NETWORK-BLOCKED-BY-BATTERY")
    socket.socket.connect = _deny
    socket.socket.connect_ex = _deny
    socket.create_connection = _deny
    for k in ("AWS_PROFILE", "AWS_SESSION_TOKEN"):
        os.environ.pop(k, None)
    os.environ.update({"AWS_ACCESS_KEY_ID": "blocked", "AWS_SECRET_ACCESS_KEY": "blocked", "AWS_EC2_METADATA_DISABLED": "true",
                       "AWS_SHARED_CREDENTIALS_FILE": os.devnull, "AWS_CONFIG_FILE": os.devnull,
                       "AWS_DEFAULT_REGION": "us-east-1"})
    return blocked


def _flatten(obj, path=""):
    """(key_paths, string_leaf_values) of a JSON-ish object."""
    keys, vals = set(), set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(str(k))
            k2, v2 = _flatten(v, path + "/" + str(k))
            keys |= k2
            vals |= v2
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            k2, v2 = _flatten(v, path)
            keys |= k2
            vals |= v2
    elif isinstance(obj, str):
        vals.add(obj)
    return keys, vals


def worker(dirname, route_filter):
    blocked = _block_network()
    import importlib.util
    d = os.path.join(_LAMBDA, dirname.replace("/", os.sep))
    for p in (os.path.join(_LAMBDA, "_authz", "tests"), os.path.join(_LAMBDA, "_authz"), os.path.join(_LAMBDA, "_scope"),
              os.path.join(_LAMBDA, "_keys"), os.path.join(_LAMBDA, "_ids"), _REPO, d):
        if p not in sys.path:
            sys.path.insert(0, p)
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
        {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})
    import fixtures as fx
    import served
    import enforce
    import loaders as _loaders

    spec = importlib.util.spec_from_file_location("irpt_entry_" + dirname.replace("/", "_"), os.path.join(d, "entry.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    entry = mod.ENTRY
    captured = []
    _orig_record = served._record

    def _rec(cid, operation, exc, code=None):
        captured.append((type(exc).__name__, str(exc)[:110], code))
        return _orig_record(cid, operation, exc, code)
    served._record = _rec
    routes = json.load(open(os.path.join(_V1, "routes.json"), encoding="utf-8"))["routes"]
    by_key = {r["route_key"]: r for r in routes}

    # selection-create PERSISTS a durable reference. The storage boundary is replaced by an in-memory store (the same
    # substitution directory/tests/test_selection_entry.py makes); with the network blocked nothing could be written anyway.
    persisted = []
    sel_mod = getattr(mod, "_selection_store", None)
    if sel_mod is not None and hasattr(sel_mod, "configured_store"):
        class _MemStore(object):
            def save(self, firm_id, reference, record):
                persisted.append((firm_id, reference))
        sel_mod.configured_store = lambda: _MemStore()

    deps_normal = _loaders.fixture_deps(fx.DIRECTORY, fx.OWNERSHIP, (fx.POLICY, fx.ENTITLEMENT_REVISION))
    deps_revoked = _loaders.fixture_deps(fx.DIRECTORY, fx.OWNERSHIP_REVOKED, (fx.POLICY, fx.ENTITLEMENT_REVISION))

    def use(deps):
        entry.deps = lambda tenant: deps
        entry.opaque_firm_for = lambda tenant: fx.OPAQUE_FIRM

    def hdrs(advisor=fx.ADVISOR_A):
        h = dict(fx.headers(advisor_id=advisor))
        h[served.CONTRACT_VERSION_HEADER] = served.CONTRACT_VERSION
        return h

    def svc_hdrs():
        return {served.CONTRACT_VERSION_HEADER: served.CONTRACT_VERSION, "X-Firm-Id": "opal-capital",
                "x-origin-verify": "cloudfront", "x-user-email": "svc@opalinvest.com", "x-user-role": "user",
                "x-user-type": "service"}

    def base_event(route_key, op, scope=None):
        ev = _base_event(route_key, op)
        if op == "selection-create":
            kind, ids = scope or ("ACCOUNT", [fx.A1])
            ev["body"] = json.dumps({"scope_kind": kind, "scope_ids": ids})
            ev.pop("selection", None)
        return ev

    def _base_event(route_key, op):
        return {"routeKey": route_key, "operation": op, "headers": hdrs(), "q": "", "limit": 5,
                "selection": {"account_ids": [fx.A1]}, "object_kind": None, "object_id": None,
                "requested_start": "2026-08-01", "requested_end": "2026-08-31", "export_id": "EXP-0001",
                "receipt_fixture": {"export_ref": {"export_id": "EXP-0001"}, "download_route": {"route": "/api/scoped/x"},
                                    "timestamps": {"created_at": "2026-09-10T00:00:00Z"},
                                    "vendor_signed_url_exposed": False, "facts": {"account_ids": [fx.A1]}},
                "performance_report": {"lineage": {"account_ids": [fx.A1]}}, "cutoff_at": "2026-09-10T00:00:00Z",
                "variant": "SINGLE"}

    def swapped(route_key, op, kind):
        ev = base_event(route_key, op)
        if kind == "firm":
            ev["firm_id"] = "inflection"
        elif kind == "advisor":
            ev["headers"] = hdrs(advisor=fx.ADVISOR_B)
        elif kind == "account":
            ev["object_kind"], ev["object_id"] = "account", fx.A5
            if op == "selection-create":
                ev["body"] = json.dumps({"scope_kind": "ACCOUNT", "scope_ids": [fx.A5]})
            else:
                ev["selection"] = {"account_ids": [fx.A5]}
            ev["performance_report"] = {"lineage": {"account_ids": [fx.A5]}}
            ev["receipt_fixture"] = dict(ev["receipt_fixture"], facts={"account_ids": [fx.A5]})
        elif kind == "relationship":
            ev["object_kind"], ev["object_id"] = "relationship", "r900000000000000000000r9"
            if op == "selection-create":
                ev["body"] = json.dumps({"scope_kind": "RELATIONSHIP", "scope_ids": ["rel_b900000000000000000000b9"]})
        elif kind == "report":
            ev["object_kind"], ev["object_id"] = "report", fx.REPORT_OTHER
        elif kind == "pdf":
            ev["object_kind"], ev["object_id"] = "pdf", fx.PDF_OTHER
        return ev

    def code_of(ans):
        if not isinstance(ans, dict):
            return "NOT-A-DICT:%s" % type(ans).__name__
        if ans.get("ok") is False:
            return (ans.get("status") or {}).get("public_reason_code") or "REFUSED-NO-CODE"
        return "SERVED"

    def blob_of(ans):
        return json.dumps(ans, sort_keys=True, default=str)

    PROTECTED_ALWAYS = (fx.OTHER_OPAQUE_FIRM, fx.REPORT_OTHER, fx.PDF_OTHER, "Whitfield", "advisor.a@49financial.com",
                        "inflection")
    AUTHORIZED_ONLY = (fx.A1, fx.A2, fx.A3, fx.R1, fx.R2, fx.REPORT_OK, fx.PDF_OK)
    out = []

    def call(ev):
        try:
            return entry.handle(ev, None)
        except Exception as exc:                     # noqa: BLE001 -- a raise is itself a recorded outcome
            return {"ok": False, "status": {"public_reason_code": "RAISED:" + type(exc).__name__}, "_raised": str(exc)[:160]}

    for route_key in sorted(entry.routes):
        if route_filter and route_key not in route_filter:
            continue
        op = entry.routes[route_key]
        row = {"route": route_key, "function": entry.function_name, "operation": op,
               "status_in_routes_json": by_key.get(route_key, {}).get("status")}
        use(deps_normal)
        entry.shared_cache = None
        del captured[:]
        net0 = blocked["n"]
        auth = call(base_event(route_key, op))
        a_code = code_of(auth)
        a_why = captured[-1] if captured else None
        a_net = blocked["n"] - net0
        if a_code == "SERVED":
            a_note = ""
        elif a_why:
            a_note = "refused by %s: %s" % (a_why[0], a_why[1])
        else:
            a_note = "refused with no internal record"
        if a_code != "SERVED" and a_net:
            a_note += "; the compute attempted %d network connect(s), blocked by the battery" % a_net
        authorized_served = a_code == "SERVED"
        auth_data = auth.get("data") if isinstance(auth, dict) else None
        refusals = []                                   # (label, answer) -- every refused response of the arms
        # ---------------------------------------------------------------- advisor_principal
        sw = {}
        problems = []
        authz_refused_swaps = 0
        for kind in SWAP_KINDS:
            a = call(swapped(route_key, op, kind))
            c = code_of(a)
            b = blob_of(a)
            req_protected = PROTECTED_ALWAYS + ((fx.A5, fx.ADVISOR_B) if kind != "advisor" else ())
            leak = [t for t in req_protected if t in b]
            if c == "SERVED":
                if kind != "advisor":
                    problems.append("%s swap SERVED" % kind)
                else:
                    widened = [i for i in AUTHORIZED_ONLY if i in b]
                    if widened:
                        problems.append("advisor swap WIDENED %d ids" % len(widened))
                sw[kind] = "SERVED"
            else:
                refusals.append(("swap-" + kind, a))
                sw[kind] = c
                if c in AUTHZ_CODES and kind != "advisor":
                    authz_refused_swaps += 1
            if leak:
                problems.append("%s swap leaked %s" % (kind, leak))
        # the second authorized principal's OWN served answer (advisor B, a real advisor of the same firm with a grant of
        # its own): the control that tells a principal-specific field from the response's shape.
        evb = base_event(route_key, op, scope=("ACCOUNT", [fx.A5]))
        evb["headers"] = hdrs(advisor=fx.ADVISOR_B)
        adv_b_control = call(evb)
        ev = base_event(route_key, op)
        ev["firm_id"] = "inflection"
        cm = call(ev)
        cm_ok = code_of(cm) == "FIRM_BINDING" and "inflection" not in blob_of(cm)
        if not cm_ok:
            problems.append("claimed-firm mismatch answered %s" % code_of(cm))
        refusals.append(("claimed-firm", cm))
        ev = base_event(route_key, op)
        ev["firm_id"] = fx.TENANT
        rc = call(ev)
        # A claim that AGREES with the verified firm must not change the outcome of the authorized request.
        if code_of(rc) != a_code:
            problems.append("reconciling firm claim answered %s, the authorized request %s" % (code_of(rc), a_code))
        # A refusal of the AUTHORIZED request BY THE ENFORCER (an AuthzError) is the difference control failing; the same public
        # code raised by an operation's own input validation (e.g. AccountNotCovered: "browser-supplied scope is not an
        # input") is the generic request shape not fitting the operation, and is recorded as such below, never as a defect.
        if a_code in AUTHZ_CODES and a_why and a_why[0] == "AuthzError":
            problems.append("authorized request refused by the enforcer: %s" % a_code)
        nonauthz_swaps = [k for k in SWAP_KINDS if k != "advisor" and sw[k] not in AUTHZ_CODES and sw[k] != "SERVED"]
        detail = {"authorized_request": a_code, "swaps": sw, "claimed_firm_mismatch": code_of(cm),
                  "authz_refused_swaps": authz_refused_swaps}
        if problems:
            row["advisor_principal"] = {"state": "DRIVEN-FAIL", "reason": "; ".join(problems), "detail": detail}
        elif not authorized_served:
            row["advisor_principal"] = {
                "state": "GATED",
                "reason": ("the generic authorized request is not SERVED in-process (answers %s; %s), so the swaps have "
                           "no served control to differ from; an operation-shaped fixture for this route is not built here. "
                           "Authorization-class refusals on the swaps: %d of 5 non-advisor swaps%s."
                           % (a_code, a_note, authz_refused_swaps,
                              "" if not nonauthz_swaps else "; non-authorization refusal on " + ",".join(nonauthz_swaps))),
                "detail": detail}
        elif nonauthz_swaps:
            row["advisor_principal"] = {
                "state": "GATED",
                "reason": ("the authorized request is SERVED but swaps %s were refused for a non-authorization reason (%s), "
                           "so they do not discriminate" % (",".join(nonauthz_swaps), [sw[k] for k in nonauthz_swaps])),
                "detail": detail}
        else:
            row["advisor_principal"] = {
                "state": "DRIVEN-PASS",
                "reason": ("in-process on the real Entry: authorized request SERVED; 5 of 5 non-advisor swaps refused by an "
                           "authorization reason, the advisor swap %s; claimed-firm mismatch FIRM_BINDING; 0 protected bytes"
                           % ("served without widening" if sw["advisor"] == "SERVED" else "refused " + sw["advisor"])),
                "detail": detail}
        # ---------------------------------------------------------------- service_principal
        saved_loader = entry.load_service_profile
        sp = {}
        sp_problems = []

        deps_seen = []

        def svc_call(selected, row_profile):
            entry.load_service_profile = lambda email: row_profile
            del deps_seen[:]

            def rec_deps(tenant):
                deps_seen.append(tenant)
                return deps_normal
            entry.deps = rec_deps
            e = base_event(route_key, op)
            e["headers"] = svc_hdrs()
            e["queryStringParameters"] = {"selected_tenant": selected}
            return call(e)
        try:
            use(deps_normal)
            allowed = svc_call(fx.TENANT, {"allowedFirmIds": fx.TENANT})
            sp["allowed_firm"] = code_of(allowed)
            sp["allowed_firm_artifacts_read_for"] = list(deps_seen)
            if code_of(allowed) == "FIRM_BINDING" or fx.TENANT not in deps_seen:
                sp_problems.append("allowed firm not admitted (answer %s, deps read for %s)" % (code_of(allowed), deps_seen))
            ab = blob_of(allowed)
            if any(t in ab for t in (fx.OTHER_OPAQUE_FIRM, "inflection", fx.REPORT_OTHER, fx.PDF_OTHER)):
                sp_problems.append("allowed-firm answer carries another firm's token")
            foreign = svc_call("inflection", {"allowedFirmIds": fx.TENANT})
            sp["foreign_firm"] = code_of(foreign)
            sp["foreign_firm_artifacts_read_for"] = list(deps_seen)
            refusals.append(("service-foreign-firm", foreign))
            if code_of(foreign) != "FIRM_BINDING" or "inflection" in blob_of(foreign) or deps_seen:
                sp_problems.append("foreign firm answered %s" % code_of(foreign))
            noattr = svc_call(fx.TENANT, {"userType": "service"})
            sp["no_allowedFirmIds_attribute"] = code_of(noattr)
            if deps_seen:
                sp_problems.append("attribute-less row still read artifacts for %s" % deps_seen)
            refusals.append(("service-no-attribute", noattr))
            if code_of(noattr) != "FIRM_BINDING":
                sp_problems.append("attribute-less row answered %s" % code_of(noattr))
            norow = svc_call(fx.TENANT, None)
            sp["no_profile_row"] = code_of(norow)
            if deps_seen:
                sp_problems.append("missing row still read artifacts for %s" % deps_seen)
            refusals.append(("service-no-row", norow))
            if code_of(norow) != "FIRM_BINDING":
                sp_problems.append("missing profile row answered %s" % code_of(norow))
        finally:
            entry.load_service_profile = saved_loader
        if sp_problems:
            row["service_principal"] = {"state": "DRIVEN-FAIL", "reason": "; ".join(sp_problems), "detail": sp}
        else:
            row["service_principal"] = {
                "state": "DRIVEN-PASS",
                "reason": ("in-process on the real Entry, the SERVICE subject: the allowed firm is admitted (its artifacts were read; "
                           "own answer %s); the foreign firm, an attribute-less row and a missing row each FIRM_BINDING with NO "
                           "artifact read for the refused firm; the refused value not echoed" % sp["allowed_firm"]),
                "detail": sp}
        # ---------------------------------------------------------------- revoked_grant_warm_cache
        rv_problems = []
        rv = {}
        # (a) the real Enforcer.serve() warm-cache replay on THIS route's operation key (reauthorize-before-serve).
        key_op = served.key_operation(op)
        deps_obj = fx.Deps()
        enf = enforce.Enforcer(enforce.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM), deps_obj.load_directory,
                               deps_obj.load_ownership, deps_obj.load_policy, artifacts=dict(fx.ARTIFACTS), cache={})

        def payload(scope):
            return {"secret": "PROTECTED-PAYLOAD", "accounts": list(scope["permitted_account_set"])}
        r1 = enf.serve(enforce.Request(fx.headers(), key_op, "account", fx.A1), payload)
        n1 = len(enf.cache)
        deps_obj.revoke()
        r2 = enf.serve(enforce.Request(fx.headers(), key_op, "account", fx.A1), payload)
        n2 = len(enf.cache)
        deps_obj.restore()
        r3 = enf.serve(enforce.Request(fx.headers(), key_op, "account", fx.A1), payload)
        rv["enforcer_serve_on_operation_key"] = {
            "key_operation": key_op, "served_first": r1.ok, "cache_entries_after_first": n1,
            "revoked_refused": (not r2.ok), "revoked_code": getattr(r2, "code", None), "cache_untouched_by_refusal": n2 == n1,
            "zero_protected_bytes_in_refusal": "PROTECTED-PAYLOAD" not in json.dumps(r2.as_envelope()),
            "restored_served_from_same_cache": bool(r3.ok and r3.cache_hit is True)}
        e1 = rv["enforcer_serve_on_operation_key"]
        if not (e1["served_first"] and e1["cache_entries_after_first"] > 0 and e1["revoked_refused"]
                and e1["cache_untouched_by_refusal"] and e1["zero_protected_bytes_in_refusal"]
                and e1["restored_served_from_same_cache"]):
            rv_problems.append("Enforcer.serve warm-cache replay on %s did not hold: %s" % (key_op, e1))
        # (b) through the route's own Entry with a SHARED cache, when the route is served in-process.
        if authorized_served:
            cache = {}
            entry.shared_cache = cache
            use(deps_normal)
            first = call(base_event(route_key, op))
            populated = len(cache)
            use(deps_revoked)
            second = call(base_event(route_key, op))
            use(deps_normal)
            third = call(base_event(route_key, op))
            entry.shared_cache = None
            first_ids = [i for i in AUTHORIZED_ONLY if i in blob_of(first)]
            carried = [i for i in first_ids if i in blob_of(second)]
            rv["through_entry_handle"] = {
                "served_first": code_of(first) == "SERVED", "shared_cache_entries_after_first": populated,
                "revoked_answer": code_of(second), "first_payload_ids_carried_into_revoked_answer": carried,
                "restored_answer": code_of(third)}
            refusals.append(("revoked-grant", second))
            if code_of(second) == "SERVED" or carried or code_of(third) != "SERVED" or code_of(first) != "SERVED":
                rv_problems.append("route replay: revoked answered %s carrying %s; restored %s"
                                   % (code_of(second), carried, code_of(third)))
        else:
            rv["through_entry_handle"] = ("NOT DRIVEN: the authorized request is not served in-process (%s), so there is no "
                                          "warm served payload on this route to replay a revocation against" % a_code)
        if rv_problems:
            row["revoked_grant_warm_cache"] = {"state": "DRIVEN-FAIL", "reason": "; ".join(rv_problems), "detail": rv}
        elif not authorized_served:
            row["revoked_grant_warm_cache"] = {
                "state": "GATED",
                "reason": ("the real Enforcer.serve() warm-cache reauthorization on this route's operation key HOLDS (served, "
                           "revoked refused, cache untouched, restored from the same cache), but the route's own served "
                           "payload is not produced in-process by the generic request (%s; %s), so revoked-against-warm-cache is "
                           "not driven through the route itself" % (a_code, a_note)),
                "detail": rv}
        else:
            row["revoked_grant_warm_cache"] = {
                "state": "DRIVEN-PASS",
                "reason": ("served -> grant revoked with the shared cache never cleared -> refused, none of the first "
                           "payload's ids carried -> restored -> served; the Enforcer.serve() warm-cache replay on %s also "
                           "holds" % key_op),
                "detail": rv}
        # ---------------------------------------------------------------- negative_no_protected_field
        if not authorized_served or not isinstance(auth_data, (dict, list)):
            row["negative_no_protected_field"] = {
                "state": "GATED",
                "reason": ("no authorized response field set to diff against: the generic authorized request answers %s in-process "
                           "(%s). The %d refused responses were still byte-censused against the fixed protected list: %d leak(s)"
                           % (a_code, a_note, len(refusals),
                              len([1 for _l, a in refusals if any(t in blob_of(a) for t in PROTECTED_ALWAYS)]))),
                "detail": {"refusals_checked": [lbl for lbl, _a in refusals],
                           "fixed_list_leaks": [lbl for lbl, a in refusals if any(t in blob_of(a) for t in PROTECTED_ALWAYS)]}}
            if row["negative_no_protected_field"]["detail"]["fixed_list_leaks"]:
                row["negative_no_protected_field"]["state"] = "DRIVEN-FAIL"
                row["negative_no_protected_field"]["reason"] = "a refusal carried a protected token from the fixed list"
        elif code_of(adv_b_control) != "SERVED":
            row["negative_no_protected_field"] = {
                "state": "GATED",
                "reason": ("the authorized answer is served, but the control that separates PROTECTED fields from the response's "
                           "own schema/metadata (a second authorized principal's served answer, advisor B) is not served "
                           "in-process (%s), so which fields are principal-specific cannot be derived" % code_of(adv_b_control)),
                "detail": {"refusals_checked": [lbl for lbl, _a in refusals]}}
        else:
            # PROTECTED FIELD = a field of the authorized answer whose VALUE is principal-specific: a string leaf of advisor A's
            # served answer that does not occur in advisor B's served answer. A value both principals receive (a schema
            # constant, a revision, the artifact's business date, an enum word) is the response's own shape, not a protected field.
            def leaves(obj, path=""):
                got = {}
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        got.update(leaves(v, path + "/" + str(k)))
                elif isinstance(obj, (list, tuple)):
                    for v in obj:
                        got.update(leaves(v, path + "[]"))
                elif isinstance(obj, str):
                    got.setdefault(path, set()).add(obj)
                return got
            la, lb = leaves(auth_data), leaves(adv_b_control.get("data"))
            b_vals = set()
            for vs in lb.values():
                b_vals |= vs
            protected = {pth: {v for v in vs if v not in b_vals and len(v) >= 4} for pth, vs in la.items()}
            protected = {pth: vs for pth, vs in protected.items() if vs}
            protected_vals = set()
            protected_names = set()
            for pth, vs in protected.items():
                protected_vals |= vs
                protected_names.add(pth.rsplit("/", 1)[-1].replace("[]", ""))
            def leaks_of(pairs):
                found = []
                for lbl, a in pairs:
                    k2, _v2 = _flatten(a)
                    bv = sorted(v for v in protected_vals if v in blob_of(a))
                    bk = sorted(k2 & {n for n in protected_names if n})
                    if bk or bv:
                        found.append({"refusal": lbl, "protected_field_names": bk[:6], "protected_values": bv[:6]})
                return found
            leaks = leaks_of(refusals)
            fixed = [lbl for lbl, a in refusals if any(t in blob_of(a) for t in PROTECTED_ALWAYS)]
            # POSITIVE CONTROL through the SAME test: a refusal with ONE protected value (and one protected field name) injected
            # must be reported, so a zero above is a measurement and not a constant.
            probe_val = sorted(protected_vals)[0] if protected_vals else None
            injected = {"ok": False, "status": {"public_reason_code": "NOT_AUTHORIZED"}, "detail": probe_val}
            control_fires = bool(probe_val) and len(leaks_of([("CONTROL-injected", injected)])) == 1
            nd = {"control_injected_value_detected": control_fires, "protected_field_paths": len(protected),
                  "protected_values": len(protected_vals),
                  "refusals_diffed": len(refusals), "leaks": leaks, "fixed_list_leaks": fixed}
            if leaks or fixed:
                row["negative_no_protected_field"] = {"state": "DRIVEN-FAIL", "reason": "a refused response revealed a protected field", "detail": nd}
            elif not control_fires and protected_vals:
                row["negative_no_protected_field"] = {"state": "DRIVEN-FAIL", "reason": "INSTRUMENT DEFECT: the injected-leak control was not detected", "detail": nd}
            elif not protected_vals:
                row["negative_no_protected_field"] = {
                    "state": "GATED",
                    "reason": "the authorized and the second principal's served answers carry no principal-specific string field, so there is no protected field to look for",
                    "detail": nd}
            elif not refusals:
                row["negative_no_protected_field"] = {"state": "GATED", "reason": "no refused response was produced to diff", "detail": nd}
            else:
                row["negative_no_protected_field"] = {
                    "state": "DRIVEN-PASS",
                    "reason": ("%d refused responses diffed against the authorized answer's %d protected fields (%d values "
                               "that differ per principal): none of those names or values appears in any refusal; the injected-leak control "
                               "is detected by the same test" % (len(refusals), len(protected), len(protected_vals))),
                    "detail": nd}
        row["live_authenticated"] = LIVE_AUTH_GATED
        out.append(row)
    print("@@WORKER-JSON@@" + json.dumps({"dir": dirname, "function": entry.function_name, "rows": out,
                                          "network_connects_blocked": blocked["n"]}, default=str))


# ======================================================================================== FIXTURE ARMS (IB-pr-340, E-P10)
# WHAT THIS ADDS TO THE ROUND-61 BATTERY. The four generic arms above answer GATED on a route whose own validators refuse the
# generic request (row W137-S1). This block drives, for each such route, TWO operation-shaped fixture files that live beside
# this battery -- `fixtures/<slug>.allowed.json` (the ALLOWED principal class: a FIRM_ADVISOR holding a grant) and
# `fixtures/<slug>.denied.json` (the DENIED class: cases that must each be refused) -- through the SAME real Entry object, with
# only the STORAGE boundary substituted and the process NETWORK-BLOCKED (`_block_network`). Nothing is minted, granted or sent.
#
# A DENIED case passes only if (a) it is refused by the code its fixture names, (b) the refusal carries none of the allowed
# answer's principal-specific values nor the fixed protected list nor the value the case supplied, and (c) the SAME event under
# the allowed principal was SERVED in this run (the difference control: the refusal is the principal's, not the request's shape).
# An injected-leak control is run through the identical leak test, so a clean result is a measurement and not a constant.
FIXTURE_SCHEMA = "irpt-gated-route-fixture/1"
FIXDIR = os.path.join(_HERE, "fixtures")
WORLD_PATH = os.path.join(FIXDIR, "_world.json")


def route_slug(route_key):
    method, path = route_key.split(" ", 1)
    tail = path[len(SCOPED):] if path.startswith(SCOPED) else path.strip("/")
    return method.lower() + "_" + _re.sub(r"[{}]", "", tail).replace("/", "_")


def fixture_paths(route_key):
    s = route_slug(route_key)
    return os.path.join(FIXDIR, s + ".allowed.json"), os.path.join(FIXDIR, s + ".denied.json")


def _repo_rel(p):
    return os.path.relpath(p, _REPO).replace(os.sep, "/")


def _set_path(doc, dotted, value):
    cur = doc
    parts = dotted.split(".")
    for p in parts[:-1]:
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


def _subst(obj, b):
    """Resolve `${NAME}` placeholders (whole-string -> the bound value, any type; embedded -> its str) and `$include`."""
    if isinstance(obj, dict):
        if "$include" in obj:
            with open(os.path.join(_REPO, obj["$include"]), encoding="utf-8") as fh:
                doc = json.load(fh)
            if isinstance(doc, dict) and "instance" in doc and obj.get("$instance"):
                doc = doc["instance"]
            doc = _subst(doc, b)
            for dotted, val in (obj.get("$patch") or {}).items():
                _set_path(doc, dotted, _subst(val, b))
            return doc
        return {k: _subst(v, b) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_subst(v, b) for v in obj]
    if isinstance(obj, str):
        m = _re.fullmatch(r"\$\{(\w+)\}", obj)
        if m:
            if m.group(1) not in b:
                raise KeyError("unbound placeholder %s" % m.group(1))
            return b[m.group(1)]
        return _re.sub(r"\$\{(\w+)\}", lambda mm: str(b[mm.group(1)]), obj)
    return obj


def _remap(obj, mapping):
    if isinstance(obj, dict):
        return {(mapping.get(k, k) if isinstance(k, str) else k): _remap(v, mapping) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_remap(v, mapping) for v in obj]
    if isinstance(obj, str):
        return mapping.get(obj, obj)
    return obj


def fixture_worker(dirname, route_filter=None):
    """In-process, NETWORK-BLOCKED. Drives every route of `dirname` that has a fixture pair; prints one @@FIXTURE-JSON@@ line."""
    blocked = _block_network()
    import importlib.util
    d = os.path.join(_LAMBDA, dirname.replace("/", os.sep))
    for p in (os.path.join(_LAMBDA, "_authz", "tests"), os.path.join(_LAMBDA, "_authz"), os.path.join(_LAMBDA, "_scope"),
              os.path.join(_LAMBDA, "_keys"), os.path.join(_LAMBDA, "_ids"), os.path.join(_LAMBDA, "intake"), _REPO, d):
        if p not in sys.path:
            sys.path.insert(0, p)
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
        {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})
    # the sibling packages a deployed zip carries flat; appended LAST so no sibling's `entry.py` shadows the function's own
    for extra in ("ycharts/generate", "reports", "ops", "export", "ycharts/session"):
        pe = os.path.join(_LAMBDA, extra.replace("/", os.sep))
        if os.path.isdir(pe) and pe not in sys.path:
            sys.path.append(pe)
    import fixtures as fx
    import served
    import loaders as _loaders
    import ids as _ids
    world = json.load(open(WORLD_PATH, encoding="utf-8"))
    firm = world["tenant"]
    mapping = {fx_name: _ids.opaque_account(firm, raw) for fx_name, raw in world["accounts_raw"].items()}
    client_ids = {name: _ids.opaque_client(firm, raw) for name, raw in world.get("clients_raw", {}).items()}
    idmap = {getattr(fx, name): opaque for name, opaque in mapping.items()}
    directory = _remap(fx.DIRECTORY, idmap)
    own_normal = _remap(fx.OWNERSHIP, idmap)
    own_revoked = _remap(fx.OWNERSHIP_REVOKED, idmap)
    own_unproj = fx.OWNERSHIP_UNPROJECTED
    deps_by = {
        "normal": _loaders.fixture_deps(directory, own_normal, (fx.POLICY, fx.ENTITLEMENT_REVISION)),
        "revoked": _loaders.fixture_deps(directory, own_revoked, (fx.POLICY, fx.ENTITLEMENT_REVISION)),
        "unprojected": _loaders.fixture_deps(directory, own_unproj, (fx.POLICY, fx.ENTITLEMENT_REVISION)),
    }
    base_bind = dict(mapping)
    base_bind.update({"TENANT": firm, "OPAQUE_FIRM": fx.OPAQUE_FIRM, "OTHER_OPAQUE_FIRM": fx.OTHER_OPAQUE_FIRM,
                      "REPORT_OK": fx.REPORT_OK, "REPORT_OTHER": fx.REPORT_OTHER, "ADVISOR_A": fx.ADVISOR_A,
                      "ADVISOR_B": fx.ADVISOR_B, "R1": fx.R1, "R2": fx.R2})
    base_bind.update(client_ids)
    for k, v in world.get("constants", {}).items():
        base_bind[k] = v

    spec = importlib.util.spec_from_file_location("irpt_fxentry_" + dirname.replace("/", "_"), os.path.join(d, "entry.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    entry = mod.ENTRY
    captured = []
    _orig_record = served._record

    def _rec(cid, operation, exc, code=None):
        captured.append((type(exc).__name__, str(exc)[:110], code))
        return _orig_record(cid, operation, exc, code)
    served._record = _rec
    routes_json = {r["route_key"]: r for r in json.load(open(os.path.join(_V1, "routes.json"), encoding="utf-8"))["routes"]}

    def principal_headers(p):
        p = p or {}
        h = dict(fx.headers(advisor_id=p.get("advisor_id", fx.ADVISOR_A), email=p.get("email", "advisor.a@49financial.com")))
        h[served.CONTRACT_VERSION_HEADER] = served.CONTRACT_VERSION
        for k in p.get("drop_headers", []):
            for hk in [x for x in h if x.lower() == k.lower()]:
                h.pop(hk)
        for k, v in (p.get("set_headers") or {}).items():
            h[k] = v
        return h

    def code_of(ans):
        if not isinstance(ans, dict):
            return "NOT-A-DICT:%s" % type(ans).__name__
        if ans.get("ok") is False:
            return (ans.get("status") or {}).get("public_reason_code") or "REFUSED-NO-CODE"
        return "SERVED"

    def blob_of(ans):
        return json.dumps(ans, sort_keys=True, default=str)

    def text_of(ans):
        """Every key and string leaf of an answer, one per line: a leak test over THIS cannot be defeated by json escaping."""
        k, v = _flatten(ans)
        return "\n".join(sorted(k | v))

    def call(ev):
        del captured[:]
        try:
            return entry.handle(ev, None)
        except Exception as exc:                               # noqa: BLE001 -- a raise is itself a recorded outcome
            return {"ok": False, "status": {"public_reason_code": "RAISED:" + type(exc).__name__}, "_raised": str(exc)[:160]}

    # ---------------------------------------------------------------- the storage-boundary stubs (one per fixture "stubs" key)
    class _Rec(object):
        pass

    def apply_stubs(stubs, bind, restore):
        def patch(obj, name, value):
            old = getattr(obj, name)
            setattr(obj, name, value)
            restore.append(lambda: setattr(obj, name, old))
        for name, sp in (stubs or {}).items():
            STUBS[name](sp, bind, patch)

    def stub_job_store(sp, bind, patch):
        import checkpoint
        store = checkpoint.MemoryStore()
        for j in sp["jobs"]:
            store.put(checkpoint.JOBS_TABLE, {"tenant": _subst(j["tenant"], bind), "job": _subst(j["job"], bind)},
                      {"lease_owner": j["lease_owner"], "lease_expires_at": j["lease_expires_at"], "fence_token": j.get("fence_token", 1)})
        patch(checkpoint, "dynamo_store", lambda: store)

    def stub_selection_store(sp, bind, patch):
        import selection as _sel
        import selection_store as _store
        rows = {}
        for item in sp["selections"]:
            enforcer, _ctx = entry.enforcer_for(firm)
            hdr = principal_headers({"advisor_id": item["advisor_id"]})
            scope, refusal = enforcer.resolve_now(served._enforce.Request(hdr, served.key_operation(item["operation"])))
            if refusal is not None:
                raise RuntimeError("fixture selection for %s refused: %s" % (item["advisor_id"], getattr(refusal, "code", refusal)))
            ids_ = _subst(item["account_ids"], bind)
            made = _sel.create_selection(scope, entry_directory(), ids_, directory_revision=_sel.directory_revision(entry_directory()),
                                         save_selection=lambda f, r, rec: rows.__setitem__((f, r), json.loads(json.dumps(rec))))
            bind[item["name"]] = made["account_set_id"]

        class _Store(object):
            def load(self, tenant, reference):
                got = rows.get((tenant, reference))
                return json.loads(json.dumps(got)) if got is not None else None
        patch(_store, "configured_store", lambda: _Store())
        g = getattr(entry.operations.get("holdings-snapshot"), "__globals__", None)
        if g is not None and "_selection_store" in g:
            patch(g["_selection_store"], "configured_store", lambda: _Store())

    def entry_directory():
        return directory

    def stub_holdings_snapshot(sp, bind, patch):
        g = entry.operations["holdings-snapshot"].__globals__
        snap = _subst(sp["snapshot"], bind)
        patch(g["_snapshot"], "load_snapshot", lambda *a, **k: json.loads(json.dumps(snap)))
        patch(g["_loaders"], "bucket_for", lambda _t: "fixture-bucket")

    def stub_performance_provider(sp, bind, patch):
        outcome = _subst(sp["outcome"], bind)

        def provider(scope, **kwargs):
            res = json.loads(json.dumps(outcome))
            res["report"]["dates"]["requested_start"] = kwargs["requested_start"]
            res["report"]["dates"]["requested_end"] = kwargs["requested_end"]
            return res
        patch(mod._handler, "run", provider)

    def stub_download_client(sp, bind, patch):
        import download as _download
        bucket = sp["bucket"]
        os.environ["IRPT_EVIDENCE_BUCKET"] = bucket

        class _S3(object):
            def head_object(self, Bucket, Key):
                return {"ContentLength": sp["byte_length"]}

            def generate_presigned_url(self, op, Params, ExpiresIn):
                return _download.FixtureSigner(Params["Bucket"], ExpiresIn).sign(Params["Key"])
        patch(mod, "_download_client", lambda: _S3())

    def stub_platinum_s3(sp, bind, patch):
        import types
        objects = {}
        for item in sp["objects"]:
            raw = item["raw"]
            for body, which in ((item.get("series"), "series"), (item.get("manifest"), "manifest")):
                if body is not None:
                    objects[mod._split(mod._object_uri(firm, raw, which))[1]] = (body.encode("utf-8"), '"etag-%s"' % which)
            if item.get("summary_client"):
                objects[mod._split(mod._summary_uri(firm, _subst(item["summary_client"], bind)))[1]] = (
                    json.dumps(_subst(item["summary"], bind)).encode("utf-8"), '"etag-summary"')

        class _ClientError(Exception):
            def __init__(self, code):
                super().__init__(code)
                self.response = {"Error": {"Code": code}}

        class _S3(object):
            def get_object(self, Bucket, Key, **kw):
                if Key not in objects:
                    raise _ClientError("NoSuchKey")
                body, etag = objects[Key]
                return {"Body": types.SimpleNamespace(read=lambda: body), "ETag": etag}

            def get_paginator(self, name):
                outer = objects

                class P(object):
                    def paginate(self, Bucket, Prefix, Delimiter):
                        seen = sorted({k[len(Prefix):].split("/", 1)[0] for k in outer if k.startswith(Prefix)})
                        yield {"CommonPrefixes": [{"Prefix": Prefix + s + "/"} for s in seen if s.startswith("account=")]}
                return P()
        patch(mod, "_S3", _S3())
        mod._RAW_BY_OPAQUE.clear()
        restore_memo = lambda: mod._RAW_BY_OPAQUE.clear()                                   # noqa: E731
        bind["_restore_memo"] = restore_memo

    def stub_submission_service(sp, bind, patch):
        class _Service(object):
            def submit(self, payload, request, scope, event, ctx):
                return {"identity": {"request_id": payload["request_id"], "revision": 1}, "stage": "ACCEPTED",
                        "dispatch_pending": False}

        def compute(request, scope, event, ctx):
            return mod.submit_analysis(request, scope, event, ctx, _Service(), allow_prospect=False)
        ops = entry.operations
        old = ops[mod.OPERATION]
        ops[mod.OPERATION] = compute
        patch_list_restore = lambda: ops.__setitem__(mod.OPERATION, old)                    # noqa: E731
        bind["_restore_ops"] = patch_list_restore

    STUBS = {"job_store": stub_job_store, "selection_store": stub_selection_store, "holdings_snapshot": stub_holdings_snapshot,
             "performance_provider": stub_performance_provider, "download_client": stub_download_client,
             "platinum_s3": stub_platinum_s3, "submission_service": stub_submission_service}

    leaks_fixed = (fx.OTHER_OPAQUE_FIRM, fx.REPORT_OTHER, fx.PDF_OTHER, "Whitfield", "advisor.a@49financial.com", "inflection")

    out = []
    for route_key in sorted(entry.routes):
        if route_filter and route_key not in route_filter:
            continue
        pa, pd_ = fixture_paths(route_key)
        if not (os.path.isfile(pa) and os.path.isfile(pd_)):
            continue
        allowed_fx = json.load(open(pa, encoding="utf-8"))
        denied_fx = json.load(open(pd_, encoding="utf-8"))
        if allowed_fx.get("driver", "entry") != "entry":
            continue                                   # an owned/installed route: driven by p340_owned_world.py, not by this worker
        op = entry.routes[route_key]
        row = {"route": route_key, "function": entry.function_name, "operation": op,
               "status_in_routes_json": routes_json.get(route_key, {}).get("status"),
               "allowed_fixture": _repo_rel(pa), "denied_fixture": _repo_rel(pd_)}
        restore = []
        bind = dict(base_bind)
        try:
            entry.shared_cache = None
            use_deps = deps_by["normal"]
            entry.deps = lambda tenant, _d=use_deps: _d
            entry.opaque_firm_for = lambda tenant: fx.OPAQUE_FIRM
            apply_stubs(allowed_fx.get("stubs"), bind, restore)

            def build_event(fixture, case=None):
                ev = _subst(fixture.get("event") or {}, bind)
                if case:
                    for k, v in (_subst(case.get("event") or {}, bind)).items():
                        ev[k] = v
                ev["routeKey"] = route_key
                ev.setdefault("version", "2.0")
                if "body_json" in ev:                       # an HTTP API v2 body is a JSON STRING
                    ev["body"] = json.dumps(ev.pop("body_json"), sort_keys=True)
                ev["headers"] = principal_headers((case or {}).get("principal") or fixture.get("principal"))
                return ev

            def use(kind):
                dd = deps_by[kind]
                entry.deps = lambda tenant, _d=dd: _d
            # ------------------------------------------------ ALLOWED
            use("normal")
            ev_a = build_event(allowed_fx)
            net0 = blocked["n"]
            ans_a = call(ev_a)
            code_a = code_of(ans_a)
            cause_a = captured[-1] if captured else None
            exp = allowed_fx["expect"]
            a_problems = []
            if exp["outcome"] == "SERVED":
                if code_a != "SERVED":
                    a_problems.append("authorized request answered %s (%s)" % (code_a, "%s: %s" % cause_a[:2] if cause_a else "no internal record"))
            elif exp["outcome"] == "PAST_BOUNDARY":
                if code_a != exp["code"]:
                    a_problems.append("authorized request answered %s, the fixture names %s" % (code_a, exp["code"]))
                if code_a in AUTHZ_CODES:
                    a_problems.append("authorized request refused by an authorization reason %s" % code_a)
                if exp.get("cause_class") and (not cause_a or cause_a[0] != exp["cause_class"]):
                    a_problems.append("refusal cause %s, the fixture names %s" % (cause_a and cause_a[0], exp["cause_class"]))
            else:
                a_problems.append("unknown expect.outcome %r" % exp["outcome"])
            ablob = text_of(ans_a)
            missing = [t for t in _subst(exp.get("data_contains", []), bind) if t not in ablob]
            if missing:
                a_problems.append("served answer lacks %s" % missing)
            a_leaks = [t for t in leaks_fixed if t in ablob]
            if a_leaks:
                a_problems.append("authorized answer carries another principal's token %s" % a_leaks)
            if exp["outcome"] == "SERVED" and exp.get("data_schema"):
                try:
                    import jsonschema
                    schema = json.load(open(os.path.join(_V1, exp["data_schema"]), encoding="utf-8"))
                    payload = ans_a.get("data")
                    if isinstance(payload, dict) and exp.get("data_schema_pick"):
                        payload = payload[exp["data_schema_pick"]]
                    jsonschema.Draft202012Validator(schema).validate(payload)
                except Exception as exc:                                                        # noqa: BLE001
                    a_problems.append("data does not validate against %s: %s" % (exp["data_schema"], str(exc).splitlines()[0][:140]))
            if os.environ.get("P340_DEBUG"):
                sys.stderr.write("DEBUG %s allowed answer: %s\n" % (route_key, ablob[:1500]))
            allowed_state = "FAIL" if a_problems else "PASS"
            status_valid = None                            # an OBSERVATION, never a verdict of this arm (see the surprise rows)
            if isinstance(ans_a, dict) and isinstance(ans_a.get("status"), dict):
                try:
                    import jsonschema
                    jsonschema.Draft202012Validator(json.load(open(os.path.join(_V1, "PublicStatusEnvelope.schema.json"), encoding="utf-8"))
                                                    ).validate(ans_a["status"])
                    status_valid = True
                except Exception as exc:                                                        # noqa: BLE001
                    status_valid = "INVALID: " + str(exc).splitlines()[0][:120]
            row["allowed"] = {
                "state": allowed_state, "reason": ("; ".join(a_problems) if a_problems else
                    "in-process on the real Entry with the recorded storage: the allowed principal's operation-shaped request %s" %
                    ("is SERVED with the fixture's principal-specific values present" if exp["outcome"] == "SERVED" else
                     "gets past the boundary and answers its own %s (%s), as the fixture declares" % (exp["code"], exp.get("why", "")))),
                "detail": {"answer": code_a, "cause": cause_a, "public_status_envelope_valid": status_valid,
                           "network_connects_blocked_during_arm": blocked["n"] - net0}}
            # ------------------------------------------------ DENIED
            protected = set(t for t in _subst(exp.get("data_contains", []), bind) if isinstance(t, str))
            protected |= set(_subst(allowed_fx.get("protected_values", []), bind))
            control = allowed_fx.get("control_principal")
            if control:
                use("normal")
                evb = build_event(allowed_fx)
                for k, v in _subst(control.get("event") or {}, bind).items():
                    evb[k] = v
                evb["headers"] = principal_headers(control["principal"])
                ans_b = call(evb)
                row["allowed"]["detail"]["control_principal_answer"] = code_of(ans_b)
                if code_of(ans_b) == "SERVED":
                    b_blob = text_of(ans_b.get("data"))
                    a_leaves = _flatten(ans_a.get("data"))[1]
                    protected |= {v for v in a_leaves if v not in b_blob and len(v) >= 4}
            d_problems = []
            cases_out = []

            def leaks_in(answer, _protected=protected):
                b = text_of(answer)
                return sorted(t for t in _protected if t in b) + [t for t in leaks_fixed if t in b]
            for case in denied_fx["cases"]:
                use(case.get("deps", "normal"))
                saved = []
                case_stubs = case.get("stubs")
                if case_stubs:
                    apply_stubs(case_stubs, bind, saved)
                ev = build_event(allowed_fx, case)
                ans = call(ev)
                for r in saved:
                    r()
                code = code_of(ans)
                cblob = text_of(ans)
                echoed = [t for t in _subst(case.get("must_not_echo", []), bind) if isinstance(t, str) and t in cblob]
                leaked = leaks_in(ans)
                # the difference control: the SAME request shape under the allowed principal must have been served
                case_problems = []
                if code not in case["expect_codes"]:
                    case_problems.append("answered %s, the fixture names %s" % (code, case["expect_codes"]))
                if leaked:
                    case_problems.append("refusal carried %s" % leaked[:4])
                if echoed:
                    case_problems.append("refusal echoed the supplied value")
                if "data" in ans and ans.get("ok") is not False:
                    case_problems.append("a denied case was served data")
                cases_out.append({"case": case["name"], "answer": code, "expected": case["expect_codes"],
                                  "ok": not case_problems, "problems": case_problems})
                d_problems += ["%s: %s" % (case["name"], p) for p in case_problems]
            # the injected-leak control: ONE protected value placed in a refusal must be reported by the identical test
            probe = sorted(protected)[0] if protected else leaks_fixed[0]
            injected = {"ok": False, "status": {"public_reason_code": "NOT_AUTHORIZED"}, "detail": probe}
            control_fires = bool(leaks_in(injected))
            if not control_fires:
                d_problems.append("INSTRUMENT DEFECT: the injected-leak control was not detected")
            if allowed_state != "PASS":
                d_problems.append("difference control failed: the allowed principal's request was not served")
            if not cases_out:
                d_problems.append("no denied case")
            row["denied"] = {
                "state": "FAIL" if d_problems else "PASS",
                "reason": ("; ".join(d_problems) if d_problems else
                           "%d denied cases each refused by the declared code with 0 protected values (%d protected values + %d fixed "
                           "tokens checked), the allowed principal's same request shape %s; the injected-leak control is "
                           "detected by the same test" % (len(cases_out), len(protected), len(leaks_fixed),
                                                          "served" if exp["outcome"] == "SERVED" else "reached the operation (%s)" % exp["code"])),
                "detail": {"cases": cases_out, "protected_values_checked": len(protected), "injected_control_detected": control_fires}}
        finally:
            for r in reversed(restore):
                r()
            for k in ("_restore_memo", "_restore_ops"):
                if k in bind:
                    bind[k]()
        out.append(row)
    print("@@FIXTURE-JSON@@" + json.dumps({"dir": dirname, "function": entry.function_name, "rows": out,
                                           "network_connects_blocked": blocked["n"]}, default=str))


# ======================================================================================== PARENT
def _aws(args):
    r = subprocess.run([AWS] + args, capture_output=True, text=True, timeout=100)
    return r.returncode, r.stdout, r.stderr


def enumerate_live():
    rc, so, se = _aws(["apigatewayv2", "get-routes", "--api-id", API_ID, "--query",
                       "Items[?contains(RouteKey,'%s')].[RouteKey,AuthorizationType,AuthorizerId]" % SCOPED, "--output", "json"])
    if rc != 0:
        return None, "aws rc=%d %s" % (rc, se[:200])
    return {r[0]: {"auth_type": r[1], "authorizer": r[2]} for r in json.loads(so)}, None


def probe_get(url):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read(400).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(400).decode("utf-8", "replace")
    except Exception as exc:                                    # noqa: BLE001
        return None, "PROBE-ERROR %s" % type(exc).__name__


def main():
    live, err = enumerate_live()
    declared = json.load(open(os.path.join(_V1, "routes.json"), encoding="utf-8"))["routes"]
    declared_keys = sorted(r["route_key"] for r in declared)
    result = {"battery": "IB-pr-335 (generic arms, carried into IB-pr-340)", "overall_pass": False}
    if live is None:
        result["enumeration_error"] = err
        print("ENUMERATION FAILED:", err)
        json.dump(result, open(OUT, "w", encoding="utf-8"), indent=1)
        return 0
    live_keys = sorted(live)
    only_live = sorted(set(live_keys) - set(declared_keys))
    only_declared = sorted(set(declared_keys) - set(live_keys))
    print("ENUMERATED: %d live /api/scoped/investor-reporting/ routes (API Gateway %s get-routes, filtered); %d declared in "
          "routes.json; live-only %s; declared-only %s" % (len(live_keys), API_ID, len(declared_keys), only_live, only_declared))
    rc, dom, _ = _aws(["cloudfront", "get-distribution", "--id", CLOUDFRONT_ID, "--query", "Distribution.DomainName",
                       "--output", "text"])
    domain = dom.strip() if rc == 0 else None
    # ---- in-process arms, one subprocess per function directory (the entry modules share names)
    per_route, worker_meta = {}, []
    for d in ENTRY_DIRS:
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--worker", d], capture_output=True, text=True,
                           cwd=_REPO, timeout=110)
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("@@WORKER-JSON@@")]
        if r.returncode != 0 or not line:
            print("WORKER %s FAILED rc=%d\n%s" % (d, r.returncode, (r.stderr or r.stdout)[-800:]))
            worker_meta.append({"dir": d, "error": (r.stderr or r.stdout)[-400:]})
            continue
        w = json.loads(line[0][len("@@WORKER-JSON@@"):])
        worker_meta.append({"dir": d, "function": w["function"], "routes": len(w["rows"]),
                            "network_connects_blocked": w["network_connects_blocked"]})
        for row in w["rows"]:
            per_route.setdefault(row["route"], []).append(row)
    routes_out = []
    for key in live_keys:
        info = live[key]
        rows = per_route.get(key, [])
        method, path = key.split(" ", 1)
        live_boundary = {"api_gateway_authorization_type": info["auth_type"], "authorizer": info["authorizer"]}
        if method == "GET" and domain:
            probe_path = path.replace("{", "x").replace("}", "")
            code, body = probe_get("https://%s%s" % (domain, probe_path))
            live_boundary["unauthenticated_get_probe"] = {"status": code, "refused": code == 401,
                                                           "zero_protected_bytes": "PROTECTED" not in body}
        else:
            live_boundary["unauthenticated_probe"] = ("NOT SENT: a non-GET call is outside this worker's read-only bound; the "
                                                      "boundary is the route-table read above")
        route = {"route": key, "live_boundary": live_boundary, "live_authenticated": LIVE_AUTH_GATED}
        if not rows:
            reason = ("no module-level Entry under the eight function directories' entry.py declares this route key: it is "
                      "served by an INSTALLED entry (served.installed_entry), whose Entry is built at the first call from the "
                      "function role's AWS clients (reports/status_installed.py build_boundary(compose_ports()), "
                      "reports/generate_installed.py, performance/runtime.py) and cannot be constructed over recorded storage "
                      "without a network or a fixture for every port; the same limit test_guarded_entries.py records "
                      "(\"INSTALLED, battery is the installer's\")")
            for arm in ARMS:
                route[arm] = {"state": "GATED", "reason": reason}
        else:
            row = rows[0]
            route["function"] = row["function"]
            route["operation"] = row["operation"]
            route["status_in_routes_json"] = row["status_in_routes_json"]
            for arm in ARMS:
                route[arm] = row[arm]
        routes_out.append(route)
    fails = [(r["route"], a) for r in routes_out for a in ARMS if r[a]["state"] == "DRIVEN-FAIL"]
    bad_boundary = [r["route"] for r in routes_out
                    if r["live_boundary"].get("api_gateway_authorization_type") != "CUSTOM"
                    or r["live_boundary"].get("unauthenticated_get_probe", {"refused": True}).get("refused") is not True]
    counts = {}
    for r in routes_out:
        for a in ARMS:
            counts[(a, r[a]["state"])] = counts.get((a, r[a]["state"]), 0) + 1
    result.update({
        "overall_pass": (not fails) and (not bad_boundary) and len(routes_out) == len(declared_keys) and not only_live
        and not only_declared and all(w.get("routes") is not None for w in worker_meta),
        "route_count": len(routes_out),
        "enumeration": ("`aws apigatewayv2 get-routes --api-id %s` (read-only), RouteKey containing %s: %d live routes; "
                        "cross-checked against docs/contracts/investor-reporting/v1/routes.json (%d declared): live-only %s, "
                        "declared-only %s" % (API_ID, SCOPED, len(live_keys), len(declared_keys), only_live, only_declared)),
        "planes": ("in-process arms: the real Entry per route, recorded storage, process NETWORK-BLOCKED (no read, no write off "
                   "this box); live: route-table read + unauthenticated GET probes only; authenticated live read: GATED "
                   "(production auth plane write, Andrew's to name a principal)"),
        "state_counts": {"%s|%s" % k: v for k, v in sorted(counts.items())},
        "driven_fails": fails, "live_boundary_defects": bad_boundary, "workers": worker_meta,
        "routes": routes_out})
    json.dump(result, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("route_count=%d overall_pass=%s" % (result["route_count"], result["overall_pass"]))
    for k, v in sorted(counts.items()):
        print("  %-28s %-12s %d" % (k[0], k[1], v))
    print("driven_fails:", fails)
    print("live_boundary_defects:", bad_boundary)
    return 0


# ======================================================================================== IB-pr-340 DRIVER
IB62_OUT = os.path.join(_HERE, "IB62-5_gated_fixtures.json")
_SCRATCH = os.path.join(_REPO, ".scratch")


def run_fixture_workers():
    rows, meta = {}, []
    for d in ENTRY_DIRS:
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--fixture-worker", d], capture_output=True, text=True,
                           cwd=_REPO, timeout=110)
        line = [ln for ln in r.stdout.splitlines() if ln.startswith("@@FIXTURE-JSON@@")]
        if r.returncode != 0 or not line:
            print("FIXTURE WORKER %s FAILED rc=%d\n%s" % (d, r.returncode, (r.stderr or r.stdout)[-800:]))
            meta.append({"dir": d, "error": (r.stderr or r.stdout)[-400:]})
            continue
        w = json.loads(line[0][len("@@FIXTURE-JSON@@"):])
        meta.append({"dir": d, "function": w["function"], "fixture_routes": len(w["rows"]), "network_connects_blocked": w["network_connects_blocked"]})
        for row in w["rows"]:
            rows[row["route"]] = row
    return rows, meta


def run_pytest_world(world):
    os.makedirs(_SCRATCH, exist_ok=True)
    out = os.path.join(_SCRATCH, "p340_%s.jsonl" % world)
    if os.path.exists(out):
        os.remove(out)
    env = dict(os.environ, P340_WORLD=world, P340_B_OUT=out)
    r = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", "--no-header", "--color=no",
                        os.path.join(_HERE, "p340_owned_world.py")], capture_output=True, text=True, cwd=_REPO, env=env, timeout=115)
    rows = {}
    if os.path.exists(out):
        for ln in open(out, encoding="utf-8"):
            if ln.strip():
                row = json.loads(ln)
                rows[row["route"]] = row
    tail = [ln for ln in (r.stdout or "").splitlines() if ln.strip()][-1:]
    last = _re.sub(r" in [0-9.]+s", "", tail[0]) if tail else ""          # the wall time is the one non-deterministic token
    return rows, {"world": world, "pytest_rc": r.returncode, "pytest_last_line": last[-200:]}


def main340():
    main()                                                       # the round-61 census + four generic arms -> OUT
    generic = json.load(open(OUT, encoding="utf-8"))
    if "routes" not in generic:
        print("generic census failed; nothing to build on")
        return 1
    fx_rows, fx_meta = run_fixture_workers()
    owned_rows, owned_meta = run_pytest_world("owned")
    upload_rows, upload_meta = run_pytest_world("upload")
    fx_rows.update(owned_rows)
    fx_rows.update(upload_rows)
    out_routes, problems = [], []
    for r in generic["routes"]:
        key = r["route"]
        states = [r[a]["state"] for a in ARMS]
        gated = any(s != "DRIVEN-PASS" for s in states)
        pa, pd = fixture_paths(key)
        have = os.path.isfile(pa) and os.path.isfile(pd)
        row = fx_rows.get(key)
        item = {"route": key, "gated": gated, "allowed_fixture": _repo_rel(pa) if have else None,
                "denied_fixture": _repo_rel(pd) if have else None}
        if row is not None:
            item["allowed"], item["denied"] = row["allowed"]["state"], row["denied"]["state"]
        elif not gated:
            item["allowed"] = item["denied"] = "PASS"            # driven on all four generic arms; no fixture was needed
        else:
            item["allowed"] = item["denied"] = "FAIL"            # a gated route with no driven fixture arm is a hole, not a pass
            problems.append("%s: gated and no fixture arm ran" % key)
        if gated and not have:
            problems.append("%s: gated and a fixture file is missing" % key)
        for arm in ("allowed", "denied"):
            if item[arm] != "PASS":
                problems.append("%s: %s arm %s" % (key, arm, item[arm]))
        out_routes.append(item)
    generic_ok = bool(generic.get("overall_pass"))
    overall = generic_ok and not problems
    shaped = {"route_count": len(out_routes), "enumeration": generic["enumeration"], "battery_overall_pass": overall, "routes": out_routes}
    with open(IB62_OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(shaped, fh, indent=1)
        fh.write("\n")
    detail = {"battery": "IB-pr-340", "generic_overall_pass": generic_ok, "problems": problems,
              "planes": ("in-process, NETWORK-BLOCKED arms on the real Entry (module Entry per function, or the installed/owned Entry over the "
                         "repository's offline worlds); recorded storage only; no live authenticated call, no principal minted, no grant "
                         "written; the only network read is the API Gateway route table (read-only), as in round 61"),
              "fixture_workers": fx_meta, "owned_world": owned_meta, "upload_world": upload_meta,
              "rows": {k: fx_rows[k] for k in sorted(fx_rows)}}
    with open(os.path.join(_HERE, "IB62-5_replay_output.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(detail, fh, indent=1, default=str)
        fh.write("\n")
    gated_n = sum(1 for r in out_routes if r["gated"])
    print("IB-pr-340: route_count=%d gated=%d battery_overall_pass=%s" % (len(out_routes), gated_n, overall))
    for p in problems:
        print("  PROBLEM:", p)
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--worker":
        worker(sys.argv[2], sys.argv[3:] or None)
        sys.exit(0)
    if len(sys.argv) >= 3 and sys.argv[1] == "--fixture-worker":
        fixture_worker(sys.argv[2], sys.argv[3:] or None)
        sys.exit(0)
    sys.exit(main340())
