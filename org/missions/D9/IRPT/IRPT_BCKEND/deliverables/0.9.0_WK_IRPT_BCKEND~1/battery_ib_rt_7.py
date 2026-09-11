#!/usr/bin/env python3
"""battery_ib_rt_7.py -- RT7-AC1: the holdings route SERVED and GUARDED, the attribution
holdouts HELD, the two clocks DISTINCT, the custody total reconciled to the cent, the ids
NORMALIZED, and the deploy VERIFIED. Cell IB-rt-7 (CTO ruling 3(b)+7; slug rows C-S73, C-S75,
W2-S11's holdings half).

EVERY ARM'S SUBJECT IS THE REAL ARTIFACT (bound 12). Arm (a) reads the LIVE API's route table
and runs the REAL `snapshot.register_routes` over the REAL `_authz.Enforcer`; arm (b) and (c)
read the LANDED QA snapshots out of the three firm buckets through their own pointers; arm (d)
re-derives the id join against the landed directory artifacts; arm (e) reads the live function
configuration, the live plans and the committed ledger. Nothing here wraps, patches or
re-registers a copy of the thing it grades, every denominator is RE-DERIVED on each run (row
W3-S9), and a `0 of 0` is printed as VACUOUS rather than as a pass.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
_LAMBDA = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting")
_GOLD = os.path.join(_REPO, "data", "assets", "scripts", "gold", "investor_reporting")
_V1 = os.path.join(_REPO, "docs", "contracts", "investor-reporting", "v1")

for _p in (os.path.join(_LAMBDA, "holdings"), os.path.join(_LAMBDA, "_authz"),
           os.path.join(_LAMBDA, "_scope"), os.path.join(_LAMBDA, "_ids"),
           os.path.join(_LAMBDA, "_keys"), _GOLD):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import enforce as _authz    # noqa: E402  the REAL wrapper
import ids as _ids          # noqa: E402  the ONE normalizer
import snapshot as sn       # noqa: E402  the REAL handler module

RESULT_TOKEN = "IBRT7-HOLDINGS-SERVED"

FIRM_BUCKETS = {"49financial": "opal-data-bd", "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}
QA_HOLDINGS = "investor-reporting/qa/holdings/latest.json"
QA_DIRECTORY = "investor-reporting/qa/directory/latest.json"
API_ID = "7k3ed8px20"
AUTHORIZER = "naqxlm"
FUNCTION = "irpt-holdings"
LEDGER_SLUG = "irpt-bckend-rt7"
ROUND_1_NUMBERS = {"49financial": 7453, "inflection": 790, "cottonwood": 946}
# The six OBJECT_KINDS `_authz` declares. Read from the module rather than restated, so a
# seventh kind added there appears in this denominator instead of being silently uncounted.
SWAP_KINDS = tuple(_authz.OBJECT_KINDS)


def _aws(*args):
    """The estate's shim via aws.cmd -- a bash script handed to CreateProcess is 'not a valid
    Win32 application' under native Windows Python. NO `&` IN A JMESPATH: cmd.exe eats it as a
    command separator and returns an EMPTY string at rc=0 (measured in IB-rt-3's arm (f))."""
    exe = os.path.join(_REPO, ".tools", "aws.cmd")
    p = subprocess.run([exe] + list(args), capture_output=True, text=True, timeout=180)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def _s3():
    import boto3
    return boto3.client("s3", region_name="us-east-1")


def _landed(s3, firm_id, pointer_key):
    bucket = FIRM_BUCKETS[firm_id]
    ptr = json.loads(s3.get_object(Bucket=bucket, Key=pointer_key)["Body"].read())
    doc = json.loads(s3.get_object(Bucket=bucket, Key=ptr["key"])["Body"].read())
    return ptr, doc


# =================================================================== (a) SERVED AND GUARDED
def _fixture_directory(firm, account_ids):
    fo = _ids.opaque_firm(firm)
    return {"firm_id_opaque": fo,
            "entries": [{"ids": {"firm_id": fo, "client_id": _ids.opaque_client(firm, "C"),
                                 "account_ids": sorted(account_ids)}}]}


def _headers(fo, **over):
    h = {"X-User-Email": "ops@opalinvest.dev", "X-User-Name": "N", "X-User-Tier": "partner",
         "X-User-Role": "admin", "X-Firm-Id": fo, "X-User-Type": "Advisor",
         "X-Advisor-Id": "", "X-Advisor-Role": "", "X-Origin-Verify": "cloudfront"}
    h.update(over)
    return h


def arm_served(s3):
    # --- the LIVE route, read from the API itself ------------------------------------------
    _rc, out, _e = _aws("apigatewayv2", "get-routes", "--api-id", API_ID, "--region",
                        "us-east-1", "--output", "json")
    items = json.loads(out).get("Items", []) if out else []
    live = [r for r in items if "investor-reporting/holdings" in r.get("RouteKey", "")]
    _rc2, integ, _e2 = _aws("apigatewayv2", "get-integrations", "--api-id", API_ID,
                            "--region", "us-east-1", "--output", "json")
    integrations = {i["IntegrationId"]: i.get("IntegrationUri", "")
                    for i in (json.loads(integ).get("Items", []) if integ else [])}
    route = live[0] if live else {}
    target_id = (route.get("Target") or "").split("/")[-1]
    target_uri = integrations.get(target_id, "")
    route_ok = (len(live) == 1 and route.get("AuthorizationType") == "CUSTOM"
                and route.get("AuthorizerId") == AUTHORIZER and FUNCTION in target_uri)

    # --- the route table this cell OWNS, and the published file's denominator ---------------
    contract = json.loads(open(os.path.join(_V1, "routes.json"), encoding="utf-8").read())
    declared = [r for r in contract["routes"] if r["status"] == "DECLARED"]
    no_handler = [r for r in contract["routes"] if r["status"] == "NO-HANDLER-AT-HEAD"]

    # --- an authorized request, served, and six swaps, refused -----------------------------
    firm = "49financial"
    fo = _ids.opaque_firm(firm)
    _p, snap = _landed(s3, firm, QA_HOLDINGS)
    mine = sorted(snap["scope"]["account_ids"])[:40]
    binding = _authz.FirmBinding(firm, fo)
    enforcer = sn.make_holdings_enforcer(binding, lambda t: _fixture_directory(firm, mine),
                                         id_projection=_ids.projection_for(firm))
    routes = sn.register_routes(enforcer, lambda r, s: snap)
    guard_census = _authz.unguarded_routes(routes)

    served = routes[sn.ROUTE_KEY](_authz.Request(_headers(fo), sn.KEY_OPERATION, "account",
                                                 mine[0]))
    authorized_ok = bool(getattr(served, "ok", False))
    slice_census = sn.validate_slice(served.payload) if authorized_ok else {"valid": None}

    # FOREIGN ids for every kind, minted for ANOTHER firm by the real normalizer -- so a swap
    # is a genuinely foreign object rather than a string this battery invented.
    other = "inflection"
    foreign = {"firm": _ids.opaque_firm(other), "advisor": _ids.opaque_client(other, "ADV"),
               "account": _ids.opaque_account(other, "NOT-YOURS"),
               "relationship": _ids.opaque_relationship(other, "NOT-YOURS"),
               "report": _ids.opaque_client(other, "REPORT"),
               "pdf": _ids.opaque_client(other, "PDF")}

    def swap_run(headers, rts):
        """The six swaps against ONE viewer, with the AUTHORIZED request as its own control: a
        plane on which everything refuses proves nothing, so the pass requires BOTH that the
        authorized request is served AND that every swap is refused."""
        auth = rts[sn.ROUTE_KEY](_authz.Request(headers, sn.KEY_OPERATION, "account", mine[0]))
        rows_, refused_ = [], 0
        for kind in SWAP_KINDS:
            out_ = rts[sn.ROUTE_KEY](_authz.Request(headers, sn.KEY_OPERATION, kind,
                                                    foreign[kind]))
            is_ref = not getattr(out_, "ok", False)
            body = json.dumps(out_.as_envelope() if is_ref else {"payload": out_.payload},
                              default=str)
            # 0 PROTECTED BYTES IS A PROPERTY OF A REFUSAL, NOT OF AN ANSWER. A SERVED reply
            # carries the viewer's OWN account ids by definition -- counting those as a leak
            # would make every successful request look like one. So the census is over the
            # refusals, and a served swap is recorded as served with its own ids named as such.
            own = [a for a in mine if a in body]
            refused_ += 1 if is_ref else 0
            rows_.append({"kind": kind, "refused": is_ref,
                          "code": getattr(out_, "code", None),
                          "echoed_the_refused_value": foreign[kind] in body,
                          "protected_bytes_in_refusal": len(own) if is_ref else None,
                          "served_payload_carries_the_viewers_own_ids":
                              None if is_ref else len(own)})
        refusals = [r for r in rows_ if r["refused"]]
        return {"authorized_request_served": bool(getattr(auth, "ok", False)),
                "refused": "%d of %d" % (refused_, len(SWAP_KINDS)),
                "all_refused": refused_ == len(SWAP_KINDS),
                "refusals_carry_zero_protected_bytes":
                    "%d of %d" % (sum(1 for r in refusals
                                      if not r["protected_bytes_in_refusal"]), len(refusals)),
                "clean": not any(r["echoed_the_refused_value"] or
                                 r["protected_bytes_in_refusal"] for r in refusals),
                "swaps": rows_}

    # PLANE 1 -- FIRM_OPERATIONS (role=admin, no advisor id). This is the plane the route's own
    # fixture uses, and it refuses 5 of 6: `covers()` returns True for ANY advisor id when the
    # principal class is FIRM_OPERATIONS or OPAL_GLOBAL, without checking that the addressed
    # advisor belongs to the verified firm (enforce.py:319-320, whose own docstring says
    # "within the verified firm"). Filed as a row; no data crosses, because what is served is
    # still the viewer's own permitted slice.
    ops = swap_run(_headers(fo), routes)

    # PLANE 2 -- FIRM_ADVISOR, which is the plane the advisor axis is actually about. The
    # ownership map grants this advisor its own accounts through the REAL normalizer, so the
    # authorized request is SERVED and the 6 of 6 is not the vacuous "everything refuses".
    adv_id = "ADV-RT7"
    ownership = {"schema_version": 1,
                 "advisors": {adv_id: {"accounts": mine, "relationships": []}}}
    adv_binding = _authz.FirmBinding(firm, fo)
    adv_enforcer = sn.make_holdings_enforcer(
        adv_binding, lambda t: _fixture_directory(firm, mine),
        load_ownership=lambda t: ownership, id_projection=_ids.projection_for(firm))
    adv_routes = sn.register_routes(adv_enforcer, lambda r, s: snap)
    advisor = swap_run(_headers(fo, **{"X-User-Role": "user", "X-Advisor-Id": adv_id}),
                       adv_routes)

    ok = (route_ok and authorized_ok and slice_census.get("valid") is True
          and advisor["authorized_request_served"] and advisor["all_refused"]
          and advisor["clean"] and ops["clean"]
          and guard_census["unguarded"] == [])
    return ok, {
        "live_route": {"route_key": route.get("RouteKey"),
                       "authorization_type": route.get("AuthorizationType"),
                       "authorizer_id": route.get("AuthorizerId"),
                       "integration_uri_names_the_function": FUNCTION in target_uri,
                       "denominator": "%d of 1 holdings route on api %s" % (len(live), API_ID)},
        "published_route_table": {
            "declared": "%d of %d" % (len(declared), len(contract["routes"])),
            "no_handler_at_head": len(no_handler),
            "was": "11 DECLARED + 1 NO-HANDLER-AT-HEAD until this cell built the handler"},
        "unguarded_routes_over_this_cells_table":
            "%d of %d" % (len(guard_census["unguarded"]), guard_census["routes"]),
        "authorized_request_served": authorized_ok,
        "served_slice_contract_valid": slice_census.get("valid"),
        "served_slice_schema": slice_census.get("schema_path"),
        "six_swaps_FIRM_ADVISOR_plane": advisor,
        "six_swaps_FIRM_OPERATIONS_plane": ops,
        "why_two_planes": (
            "The advisor axis is only discriminating for a FIRM_ADVISOR viewer. For "
            "FIRM_OPERATIONS/OPAL_GLOBAL, _authz.covers() returns True for ANY advisor id "
            "without checking it belongs to the verified firm (enforce.py:319-320) -- so that "
            "plane reads 5 of 6 and the sixth is BY DESIGN, not a gap this cell can close from "
            "here. Both planes are printed rather than the passing one alone; the finding is "
            "filed as a surprise row against _authz, which is not this order's to edit."),
    }


# =================================================================== (b) BASES AND HOLDOUTS
def arm_holdouts(s3):
    import holdings_snapshot as hs
    rows, all_ok = {}, True
    for firm_id in sorted(FIRM_BUCKETS):
        ptr, snap = _landed(s3, firm_id, QA_HOLDINGS)
        nodes = snap["nodes"]

        # every node carries EXACTLY ONE basis -- the real producer's own assertion, run over
        # the landed artifact rather than over a fixture.
        bases = sorted({n["basis"] for n in nodes})
        one_basis = all(isinstance(n.get("basis"), str) and n["basis"] in
                        ("OBSERVED", "ASSIGNED", "TARGET") for n in nodes)
        try:
            hs.assert_bases_not_spliced(nodes)
            spliced = False
        except Exception as exc:  # noqa: BLE001 -- the refusal text IS the evidence
            spliced = str(exc)[:200]

        h = snap["attribution_holdouts"]
        u = h["unassigned"]
        account_ids = set(snap["scope"]["account_ids"])
        visible = [a for a in u["account_ids"] if a in account_ids]
        recon = h["reconcile"]

        # THE DIFFERENCE CONTROL, on the LANDED artifact. The wrong build must fail the same
        # check the honest one passes -- and must still reconcile, which is why the reconcile
        # alone is not a control.
        held_ok, held = hs.holdouts_held(snap, u["account_ids"])
        wrong = hs.redistribute_holdouts(snap)
        wrong_ok, wrong_census = hs.holdouts_held(wrong, u["account_ids"])
        wrong_total = round(sum(float(n["amount"]["value"]) for n in wrong["nodes"]
                                if n["node_kind"] == "ACCOUNT"), 2)
        control_vacuous = u["account_count"] == 0
        control_fires = (not wrong_ok) if not control_vacuous else None

        firm_ok = (one_basis and spliced is False and held_ok
                   and len(visible) == u["account_count"]
                   and recon["reconciled"] and abs(recon["difference"]) <= recon["tolerance"]
                   and (control_fires is True or control_vacuous))
        all_ok = all_ok and firm_ok
        rows[firm_id] = {
            "object": ptr["key"],
            "nodes": len(nodes),
            "bases_present": bases,
            "every_node_exactly_one_basis": one_basis,
            "bases_not_spliced": spliced is False,
            "unassigned_accounts": u["account_count"],
            "unassigned_value": u["value"],
            "unassigned_observable": u["observable"],
            "unassigned_denominator": u["denominator"],
            "unassigned_visible_as_account_nodes": "%d of %d" % (len(visible),
                                                                u["account_count"]),
            "assigned_without_custody": h.get("assigned_without_custody", {}).get(
                "account_count"),
            "custody_total_before": recon["total_before"],
            "custody_total_after": recon["total_after"],
            "reconciled_to_the_cent": recon["reconciled"],
            "holdouts_held": held,
            "difference_control": (
                "VACUOUS -- 0 unassigned accounts for this firm, so a redistributing build "
                "moves nothing and this control cannot fire; printed as vacuous, not as a pass"
                if control_vacuous else
                {"redistributing_build_holds_holdouts": wrong_ok,
                 "redistributing_build_census": wrong_census,
                 "value_moved_usd": wrong.get("_redistributed", {}).get("value"),
                 "total_after_redistribution": wrong_total,
                 "still_reconciles": abs(wrong_total - recon["total_after"]) <= 0.01,
                 "reading": "the wrong build moves the holdouts' value into the sleeves that "
                            "DO carry a model and the total is unchanged -- the reconcile is "
                            "not the control, this is"}),
            "ok": firm_ok,
        }
    return all_ok, rows


# =================================================================== (c) THE TWO CLOCKS
def arm_two_clocks(s3):
    import holdings_snapshot as hs
    rows, all_ok = {}, True
    for firm_id in sorted(FIRM_BUCKETS):
        _p, snap = _landed(s3, firm_id, QA_HOLDINGS)
        clocks = snap["clocks"]
        census = hs.assert_clocks_carried(snap)

        # the collapsing fixture, built from the SAME landed artifact so the control is over
        # the real shape rather than a hand-made one
        collapsed = json.loads(json.dumps(snap))
        collapsed["clocks"].pop("overlay_as_of")
        try:
            hs.assert_clocks_carried(collapsed)
            refuses_collapse = False
        except hs.ClocksCollapsed:
            refuses_collapse = True
        # ... and the same fixture through the SERVING boundary
        served_ok, served_why = sn.clocks_are_distinct(collapsed)

        # a node silently RE-DATED: the header still carries two clocks, so a header-only
        # check passes and only a per-node census catches it
        redated = json.loads(json.dumps(snap))
        if redated["nodes"]:
            redated["nodes"][0]["clocks"]["overlay_as_of"] = "2026-01-01"
        try:
            hs.assert_clocks_carried(redated)
            refuses_redate = False
        except hs.ClocksCollapsed:
            refuses_redate = True

        firm_ok = (bool(clocks.get("custody_as_of")) and bool(clocks.get("overlay_as_of"))
                   and census["denominator"] == "%d of %d" % (len(snap["nodes"]),
                                                              len(snap["nodes"]))
                   and refuses_collapse and refuses_redate and not served_ok)
        all_ok = all_ok and firm_ok
        rows[firm_id] = {
            "custody_as_of": clocks.get("custody_as_of"),
            "overlay_as_of": clocks.get("overlay_as_of"),
            "values_differ": clocks.get("custody_as_of") != clocks.get("overlay_as_of"),
            "source_as_of_entries": len(clocks.get("source_as_of") or []),
            "nodes_carrying_both": census["denominator"],
            "a_collapsed_fixture_is_refused_by_the_producer": refuses_collapse,
            "a_collapsed_fixture_is_refused_at_the_serving_boundary":
                (not served_ok, served_why),
            "a_silently_re_dated_node_is_refused": refuses_redate,
            "ok": firm_ok,
        }
    return all_ok, rows


# =================================================================== (d) NORMALIZED IDS
def arm_normalized(s3):
    rows, all_ok = {}, True
    for firm_id in sorted(FIRM_BUCKETS):
        _p, snap = _landed(s3, firm_id, QA_HOLDINGS)
        _d, ddoc = _landed(s3, firm_id, QA_DIRECTORY)
        hold = set(snap["scope"]["account_ids"])
        node_ids = {n["node_id"] for n in snap["nodes"]}
        dir_ids = set()
        for e in ddoc.get("entries", []):
            dir_ids.update(e["ids"]["account_ids"])

        prefixed = sorted(a for a in (hold | node_ids) if ":acct:" in a)
        unissued = sorted(a for a in hold if not _ids.is_issued("account", a))
        joined = hold & dir_ids

        firm_ok = (not prefixed) and (not unissued) and bool(joined)
        all_ok = all_ok and firm_ok
        rows[firm_id] = {
            "holdings_accounts": len(hold),
            "directory_accounts": len(dir_ids),
            "holdings_ids_found_in_the_directory": "%d of %d" % (len(joined), len(hold)),
            "directory_ids_found_in_holdings": "%d of %d" % (len(joined), len(dir_ids)),
            "acct_prefix_census": "%d of %d ids carry ':acct:'" % (len(prefixed),
                                                                  len(hold | node_ids)),
            "ids_not_of_issued_shape": len(unissued),
            "round_1_population_for_reference": ROUND_1_NUMBERS[firm_id],
            "note": ("the join is over the population BOTH producers hold; this cell ADDS the "
                     "unassigned custody accounts to the holdings side, so the holdings "
                     "denominator is larger than IB-rt-3's and the unmatched remainder is the "
                     "holdout population, not a normalization gap (row W1-S13)"),
            "ok": firm_ok,
        }
    return all_ok, rows


# =================================================================== (e) DEPLOYED
def arm_deployed():
    _rc, sha, _e = _aws("lambda", "get-function-configuration", "--function-name", FUNCTION,
                        "--region", "us-east-1", "--query", "CodeSha256", "--output", "text")
    _rc2, cfg, _e2 = _aws("lambda", "get-function-configuration", "--function-name", FUNCTION,
                          "--region", "us-east-1", "--output", "json")
    conf = json.loads(cfg) if cfg else {}
    built = json.loads(open(os.path.join(_REPO, "infra", "aws", "lambda", "ci",
                                         "lambda-source-map.json"),
                            encoding="utf-8").read())["functions"][FUNCTION]

    plans = {}
    tf = os.path.join(_REPO, ".tools", "terraform.exe")
    for root in ("holdings", "api"):
        p = subprocess.run([tf, "-chdir=infra/aws/terraform/investor-reporting/%s" % root,
                            "plan", "-no-color", "-input=false", "-lock=false"],
                           cwd=_REPO, capture_output=True, text=True, timeout=900)
        plans[root] = "No changes. Your infrastructure matches the configuration." in p.stdout

    sentinel_rel = "org/critical_paths/.open_deploys/%s.json" % LEDGER_SLUG
    sentinel_commits = subprocess.run(
        ["git", "-C", _REPO, "log", "--format=%h", "--full-history", "--", sentinel_rel],
        capture_output=True, text=True).stdout.split()
    cm = os.path.join(_REPO, "org", "critical_paths", "change_management")
    entry = None
    for name in sorted(os.listdir(cm)):
        if LEDGER_SLUG in name:
            entry = os.path.join(cm, name)
    text = open(entry, encoding="utf-8", errors="replace").read() if entry else ""

    # The BUILD INPUT, re-derived: the zip is not in the repo, so the oracle is the recorded
    # artifact sha256 in the source map compared against the LIVE CodeSha256 -- content, never
    # filename (bound 22a).
    ok = (sha == built.get("artifact_sha256")
          and conf.get("Handler") == "snapshot.lambda_handler"
          and any("irpt-common" in (ly.get("Arn") or "") for ly in conf.get("Layers") or [])
          and all(plans.values()) and "CLOSED" in text and text.count("| OPEN") == 0
          and bool(sentinel_commits)
          and not os.path.exists(os.path.join(_REPO, *sentinel_rel.split("/"))))
    return ok, {
        "live_code_sha256": sha,
        "build_input_sha256": built.get("artifact_sha256"),
        "sha_match_by_content_not_filename": sha == built.get("artifact_sha256"),
        "handler": conf.get("Handler"),
        "runtime": conf.get("Runtime"),
        "timeout_seconds": conf.get("Timeout"),
        "role": conf.get("Role"),
        "layers": [ly.get("Arn") for ly in conf.get("Layers") or []],
        "zero_diff_plans": plans,
        "ledger_entry": os.path.basename(entry) if entry else None,
        "ledger_closed": "CLOSED" in text,
        "legs_still_open": text.count("| OPEN"),
        "sentinel_commits_before_the_act": sentinel_commits,
        "sentinel_removed_by_the_close": not os.path.exists(
            os.path.join(_REPO, *sentinel_rel.split("/"))),
    }


# =================================================================== driver
def main():
    report = {"battery": "IB-rt-7",
              "token_printed_only_when_every_arm_holds": RESULT_TOKEN, "arms": {}}
    s3 = _s3()
    all_pass = True
    for key, fn in (("a_served_and_guarded", lambda: arm_served(s3)),
                    ("b_bases_and_holdouts", lambda: arm_holdouts(s3)),
                    ("c_two_clocks", lambda: arm_two_clocks(s3)),
                    ("d_normalized_ids", lambda: arm_normalized(s3)),
                    ("e_deployed", lambda: arm_deployed())):
        ok, detail = fn()
        report["arms"][key] = {"ok": ok, "detail": detail}
        all_pass = all_pass and ok

    report["overall_pass"] = all_pass
    print(json.dumps(report, default=str, indent=1))
    if all_pass:
        print(RESULT_TOKEN)
        return 0
    print("BLOCKED: one or more IB-rt-7 arms did not hold; see the per-arm detail above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
