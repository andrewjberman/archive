"""IB-pr-399 replay (from IB-pr-394's runner): ONE extracted irpt-narrative zip, every case, offline, driving the zip's OWN entry.ENTRY
(so NarrativeEntry's binding is what is measured, not a bare served.Entry). Run as
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
import entry as narrative_entry  # noqa: E402  (the zip's own: ENTRY is the function's real Entry)

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
    entry = narrative_entry.ENTRY               # the function's real Entry (live zip: the old shared boundary; built zip: NarrativeEntry)
    entry.load_service_profile = (lambda email: row)
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


def error_probe(route_key, op, hdrs, row):
    """AMENDMENT 1 (row W201-S6): an INTERNAL ERROR crosses served._record through this zip's real entry.ENTRY. The enforcer
    stub raises an ordinary exception (not an AuthzError), which the boundary records and answers as a refusal; what is kept is
    the envelope's reason code, any exception that ESCAPED the boundary (a TypeError from errors.public_line), and the
    irpt_error JSON lines the boundary printed."""
    import contextlib
    import io
    entry = narrative_entry.ENTRY
    entry.load_service_profile = (lambda email: row)

    def enforcer_for(tenant, principals=None):
        raise RuntimeError("the enforcer could not be built")      # reaches served's error site: _record(...)

    entry.enforcer_for = enforcer_for
    buf, out, err = io.StringIO(), None, None
    try:
        with contextlib.redirect_stdout(buf):
            out = entry.handle({"headers": hdrs, "routeKey": route_key})
    except Exception as exc:  # noqa: BLE001 -- recorded, not hidden
        err = "%s" % type(exc).__name__
    lines = []
    for ln in buf.getvalue().splitlines():
        if ln.startswith("{"):
            try:
                lines.append(json.loads(ln))
            except ValueError:
                pass
    status = (out or {}).get("status") or {} if isinstance(out, dict) else {}
    return {"escaped": err, "ok": (out or {}).get("ok") if isinstance(out, dict) else None,
            "code": status.get("public_reason_code"), "has_internal_correlation_id": "internal_correlation_id" in status,
            "log_events": [dict(sorted(x.items())) for x in lines if x.get("event") == "irpt_error"]}


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
    cases[rk] = {"operation": op, "cases": c, "error_probe": error_probe(rk, op, op_hdr(), None)}

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
