"""IB-pr-416 call-site runner: ONE extracted Lambda zip, one process, offline, no client data, no AWS. Run as
    python -I live_call_runner_416.py <extracted_zip_dir> <label> <out_json> [<layer_python_dir> ...]
It drives the zip's OWN served.Entry code (the function's real entry.ENTRY object) at the three call sites row IRPT_BCKEND-D2-S60 names,
so a packaged callee that does not accept the keywords served.py passes surfaces as a TypeError exactly as in the live function:
  prospect_*      served.Entry._handle_prospect -> InteractiveAccess(profile_reader=) (CREATE_INPUT) and guard_prospect(authorize_owner=,
                  resolve_owner=) (any mode), for an Opal internal caller with NO profile row and for a plain firm user. served._record is
                  wrapped so the CLASS of the exception the boundary recorded is read, not guessed.
  enforcer_build  ENTRY.enforcer_for(tenant) with a 3-port render_ports factory (the load_report_owner port, IB-pr-293), which is the
                  Enforcer(load_report_owner=) call the live irpt-performance-adapter logs as TypeError.
A case outcome = {recorded: [exception class names _record saw], code: public_reason_code or null, escaped: class or null,
compute_reached: bool, built_enforcer: bool}. ASCII only.
"""
import json
import os
import sys

zip_dir, label, out_path = sys.argv[1:4]
for _layer in reversed(sys.argv[4:]):
    sys.path.insert(0, _layer)
sys.path.insert(0, zip_dir)
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
    {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})
import served  # noqa: E402  (the zip's own)
import entry as zip_entry  # noqa: E402  (the zip's own)
from prospect import resolve_prospect_owner  # noqa: E402  (the zip's own)

ENTRY = zip_entry.ENTRY
RECORDED = []
_real_record = served._record


def _spy_record(cid, operation, exc, code):
    RECORDED.append(type(exc).__name__)
    return _real_record(cid, operation, exc, code)


served._record = _spy_record


def headers(email, firm, user_type="user"):
    return {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": firm, "x-origin-verify": "cloudfront",
            "x-user-email": email, "x-user-role": "user", "x-user-type": user_type}


def prospect_case(mode, hdrs, tenant):
    del RECORDED[:]
    reached = {"compute": False}

    def compute(req, scope, event, ctx):
        reached["compute"] = True
        return {"_data": {"ok": True}}

    def load_owner(tenant_, input_id):
        return resolve_prospect_owner(hdrs, tenant_)

    ENTRY.load_prospect_owner = load_owner
    ENTRY.load_service_profile = (lambda email: None)
    basis = (mode, None if mode == "CREATE_INPUT" else "input-1")
    escaped, out = None, None
    try:
        out = served.Entry._handle_prospect(ENTRY, {"headers": hdrs}, hdrs, "prospect-probe", tenant, compute, basis)
    except Exception as exc:  # noqa: BLE001 -- recorded, not hidden
        escaped = type(exc).__name__
    code = ((out or {}).get("status") or {}).get("public_reason_code") if isinstance(out, dict) else None
    return {"recorded": list(RECORDED), "code": code, "escaped": escaped, "compute_reached": reached["compute"]}


def enforcer_case(tenant):
    del RECORDED[:]
    ENTRY.render_ports = lambda t: (lambda *a, **k: None, lambda *a, **k: None, lambda *a, **k: None)
    # the deps triple the way served.py's own probe stubs it (line "probe = _enforce.Enforcer(binding, lambda t: {}, ..."): no AWS read
    ENTRY.deps = lambda t: ((lambda x: {}), (lambda x: {}), (lambda x: ({}, "rev")))
    from ids import opaque_firm
    ENTRY.opaque_firm_for = opaque_firm              # the registry issuer, offline (the loaders' own would read S3)
    escaped, built = None, False
    try:
        out = ENTRY.enforcer_for(tenant)
        built = out is not None
    except Exception as exc:  # noqa: BLE001 -- recorded, not hidden
        escaped = "%s" % type(exc).__name__
    return {"escaped": escaped, "built_enforcer": built}


op_h = headers("ops@opalinvest.com", "opal-capital")
fu_h = dict(headers("adv@cottonwood.example", "cottonwood"), **{"x-advisor-id": "adv-1"})
cases = {}
for mode in ("CREATE_INPUT", "OWNED_INPUT"):
    cases["prospect_internal_no_row_" + mode] = prospect_case(mode, op_h, "cottonwood")
    cases["prospect_firm_user_" + mode] = prospect_case(mode, fu_h, "cottonwood")
cases["enforcer_build_with_report_owner_port"] = enforcer_case("cottonwood")
json.dump({"label": label, "served_file": served.__file__, "cases": cases}, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s %s" % (label, {k: (v.get("recorded"), v.get("escaped"), v.get("code")) for k, v in cases.items()}))
