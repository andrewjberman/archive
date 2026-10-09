"""IB-pr-394 replay (from IB-pr-390's runner, + three plain-firm-user cases): ONE extracted Lambda zip, every case, offline. Run as
    python -I authz_case_runner.py <extracted_zip_dir> <routes_json> <label> <out_json> <function_name> [<layer_python_dir> ...]
It imports `served` FROM THE ZIP DIRECTORY (flat layout, as /var/task), builds served.Entry the way the _authz tests do
(load_service_profile injected, no AWS, no network), and records for every route of the function:
  noRow       an Opal internal caller (x-firm-id opal-capital), no profile row, selecting inflection
  rowCotCot   the same caller, profile row allowedFirmIds [cottonwood], selecting cottonwood
  rowCotInf   the same caller, profile row [cottonwood], selecting inflection
and the plain firm user (x-firm-id cottonwood, not an Opal internal caller):
  userOwn     no selection: bound to its own firm (cottonwood)
  userSelOther selecting inflection: refused FIRM_BINDING
  userClaimOther a restated firm_id of inflection in the query: refused FIRM_BINDING
and, for the three routes svc-custody-statement reaches (custody-report-persist, analysis-requests, submit-export):
  svcCot      svc-custody-statement, verified firm cottonwood
  svcInf      svc-custody-statement, verified firm inflection
  svc49       svc-custody-statement, verified firm 49financial
  svcCotSel   svc-custody-statement, cottonwood, selecting inflection
and, for one route outside those three: svcOther (cottonwood claim on a non-listed operation).
A case outcome = {reached_firm_check: firm the boundary bound the request to (firm_claims_match called with it),
roster: the Opal roster passed to enforcer_for or null, code: public_reason_code of the reply or null}.
ASCII only.
"""
import json
import os
import sys

zip_dir, routes_path, label, out_path, function = sys.argv[1:6]
# argv[6:] = extracted Lambda LAYER python/ directories (the /opt/python entries the function would see)
for _layer in reversed(sys.argv[6:]):
    sys.path.insert(0, _layer)
sys.path.insert(0, zip_dir)
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
    {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})
import served  # noqa: E402  (the zip's own)

SVC = "svc-custody-statement"
SVC_OPS = {"custody-report-persist", "analysis-requests", "submit-export"}
routes = json.load(open(routes_path, encoding="utf-8"))["routes"]
mine = [r for r in routes if r["handler"] == function]


class Reached(Exception):
    pass


def headers(email, firm, user_type="user"):
    return {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": firm, "x-origin-verify": "cloudfront",
            "x-user-email": email, "x-user-role": "user", "x-user-type": user_type}


def run(route_key, op, hdrs, selected, row, claim=None):
    seen = {"firm": None, "roster": None}
    kwargs = dict(function_name=function, operations={op: (lambda *a, **k: {})},
                  deps=lambda *a, **k: None, opaque_firm_for=lambda *a, **k: None,
                  routes={route_key: op}, global_context=None,
                  load_service_profile=(lambda email: row))
    # An older served.py (a live zip) may not take every keyword: pass only those its Entry declares.
    import inspect
    accepted = set(inspect.signature(served.Entry.__init__).parameters)
    entry = served.Entry(**{k: v for k, v in kwargs.items() if k in accepted})
    real = getattr(served, "firm_claims_match", None)   # an older served.py (a live zip) has no such seam

    def spy(event, verified):
        seen["firm"] = verified
        return real(event, verified)

    def enforcer_for(tenant, principals=None):
        # the old boundary calls enforcer_for(verified); the current one enforcer_for(verified, principals)
        if seen["firm"] is None:
            seen["firm"] = tenant
        seen["roster"] = sorted(principals) if principals is not None else None
        raise Reached()

    entry.enforcer_for = enforcer_for
    if real is not None:
        served.firm_claims_match = spy
    event = {"headers": hdrs, "routeKey": route_key}
    if selected is not None or claim:
        event["queryStringParameters"] = dict(claim or {})
        if selected is not None:
            event["queryStringParameters"]["selected_tenant"] = selected
    try:
        out = entry.handle(event)
    except Reached:
        out = {"ok": False, "status": {"public_reason_code": None}}
    except Exception as exc:  # noqa: BLE001 -- a harness fault is recorded, not hidden
        out = {"ok": False, "status": {"public_reason_code": "HARNESS_%s" % type(exc).__name__}}
    finally:
        if real is not None:
            served.firm_claims_match = real
    code = None
    if isinstance(out, dict):
        code = (out.get("status") or {}).get("public_reason_code")
    return {"reached_firm_check": seen["firm"], "roster": seen["roster"], "code": code}


cases = {}
op_hdr = lambda: headers("ops@opalinvest.com", "opal-capital")  # noqa: E731
for r in mine:
    rk, op = r["route_key"], r["operation"]
    c = {}
    ufirm = lambda: headers("adv@cottonwood.example", "cottonwood")  # noqa: E731
    c["userOwn"] = run(rk, op, ufirm(), None, None)
    c["userSelOther"] = run(rk, op, ufirm(), "inflection", None)
    c["userClaimOther"] = run(rk, op, ufirm(), None, None, claim={"firm_id": "inflection"})
    c["noRow"] = run(rk, op, op_hdr(), "inflection", None)
    c["rowCotCot"] = run(rk, op, op_hdr(), "cottonwood", {"allowedFirmIds": ["cottonwood"]})
    c["rowCotInf"] = run(rk, op, op_hdr(), "inflection", {"allowedFirmIds": ["cottonwood"]})
    if op in SVC_OPS:
        c["svcCot"] = run(rk, op, headers(SVC, "cottonwood", "service"), None, {"allowedFirmIds": "ALL"})
        c["svcInf"] = run(rk, op, headers(SVC, "inflection", "service"), None, {"allowedFirmIds": "ALL"})
        c["svc49"] = run(rk, op, headers(SVC, "49financial", "service"), None, {"allowedFirmIds": "ALL"})
        c["svcCotSel"] = run(rk, op, headers(SVC, "cottonwood", "service"), "inflection", {"allowedFirmIds": "ALL"})
    else:
        c["svcOther"] = run(rk, op, headers(SVC, "cottonwood", "service"), None, {"allowedFirmIds": "ALL"})
    cases[rk] = {"operation": op, "cases": c}

lookup = None
try:
    served._svc_custody_statement_firm  # noqa: B018
    lookup = served._svc_custody_statement_firm()
except Exception as exc:  # noqa: BLE001
    lookup = "ERR_%s" % type(exc).__name__
json.dump({"label": label, "function": function, "served_file": served.__file__,
           "has_svc_symbol": hasattr(served, "verified_svc_custody_statement"),
           "svc_firm_lookup": lookup, "routes": cases}, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s %s routes=%d" % (label, function, len(cases)))
