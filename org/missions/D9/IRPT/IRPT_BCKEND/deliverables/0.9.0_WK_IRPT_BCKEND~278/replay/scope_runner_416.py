"""IB-pr-416 enforcer-scope runner (from IB-pr-409's, the route key is an argument so it drives any of the three hosts) (the method of row IRPT_BCKEND-D2-S48): ONE extracted irpt-narrative zip, one process, offline.
    python -I scope_runner_416.py <extracted_zip_dir> <label> <out_json> <route_key> [<layer_python_dir> ...]
For each case the zip's OWN entry.ENTRY runs handle() with an enforcer_for stub that records the roster the boundary hands it; then
THAT TREE's own `resolve.resolve` is driven with exactly that roster (a None roster is what Enforcer reads as the Entry's own empty
roster, frozenset()). The header set is the resolver's own TRUSTED_HEADERS table, not invented: x-origin-verify='cloudfront', x-user-email=
subject, x-firm-id='opal-capital'; x-advisor-id, x-user-role and x-user-type deliberately ABSENT, which is what makes the caller the no-row
internal one. The directory is SYNTHETIC (no client data, no AWS read): two opal-capital accounts and one account of another firm, so a
class that grants the firm population shows as a non-empty permitted_account_set and a class that grants nothing shows as empty.
ASCII only.
"""
import json
import os
import sys

zip_dir, label, out_path, ROUTE = sys.argv[1:5]
for _layer in reversed(sys.argv[5:]):
    sys.path.insert(0, _layer)
sys.path.insert(0, zip_dir)
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
    {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})
import served  # noqa: E402  (the zip's own)
import entry as narrative_entry  # noqa: E402
import resolve  # noqa: E402  (the zip's own _scope.resolve)

SUBJECT = "ops@opalinvest.com"
DIRECTORY = {"entries": [
    {"ids": {"firm_id": "opal-capital", "account_ids": ["SYN-OC-1", "SYN-OC-2"]}},
    {"ids": {"firm_id": "inflection", "account_ids": ["SYN-INF-1"]}},
]}


class Reached(Exception):
    pass


def drive(row, selected):
    seen = {"roster": "NOT_CALLED", "tenant": None}
    entry = narrative_entry.ENTRY
    entry.load_service_profile = (lambda email: row)

    def enforcer_for(tenant, principals=None):
        seen["tenant"] = tenant
        seen["roster"] = sorted(principals) if principals is not None else None
        raise Reached()

    entry.enforcer_for = enforcer_for
    hdrs = {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": "opal-capital", "x-origin-verify": "cloudfront",
            "x-user-email": SUBJECT}
    event = {"headers": hdrs, "routeKey": ROUTE}
    if selected is not None:
        event["queryStringParameters"] = {"selected_tenant": selected}
    code = None
    try:
        res = entry.handle(event)
        code = (res.get("status") or {}).get("public_reason_code") if isinstance(res, dict) else None
    except Reached:
        code = "REACHED_ENFORCER"
    except Exception as exc:  # noqa: BLE001 -- recorded, not hidden
        code = "HARNESS_" + type(exc).__name__
    roster = seen["roster"]
    out = {"roster": roster, "bound": seen["tenant"], "code": code, "principal_class": None, "reason": None,
           "permitted_account_set": None}
    if roster != "NOT_CALLED":
        scope = resolve.resolve(hdrs, DIRECTORY, ownership={}, opal_principal_ids=frozenset(roster or ()))
        out["principal_class"] = scope.get("principal_class")
        out["reason"] = (scope.get("census") or {}).get("principal_reason")
        out["permitted_account_set"] = sorted(scope.get("permitted_account_set") or [])
        out["scope_keys"] = sorted(scope)[:12]
    return out


cases = {
    "no_row_no_selection": drive(None, None),
    "no_row_selecting_other": drive(None, "inflection"),
    "row_listed_no_selection": drive({"allowedFirmIds": ["cottonwood"]}, None),
}
json.dump({"label": label, "served_file": served.__file__, "resolve_file": resolve.__file__, "cases": cases},
          open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s %s" % (label, {k: (v["principal_class"], v["roster"], len(v["permitted_account_set"] or [])) for k, v in cases.items()}))
