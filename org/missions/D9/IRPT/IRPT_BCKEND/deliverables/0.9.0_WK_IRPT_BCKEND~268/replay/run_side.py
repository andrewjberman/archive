"""IB-pr-405 replay, ONE side: the REAL irpt-status Lambda modules from ONE extracted zip (flat layout, as /var/task) driven through
the real `entry.build_owned_entry` + `served.lambda_entry`, with offline doubles for storage only (no AWS, no network).

    python -I run_side.py <extracted_zip_dir> <label> <out_json>

The code under test is the zip's own: `served`, `entry`, `owned_requests`, `owned_report`, `repository`, `prospect`,
`interactive_access`. The doubles are the acceptance table, the artifact index, the report-index table and the retention
service. The authorization rule is the resident's (`reports/resident_installed.py make_authorize`, copied verbatim in shape):
an OPAL_GLOBAL principal reads any owner's record in the data firm; any other class reads only its own records.

Every arm's outcome is {ok, code, data_keys, data_sha256, persist_inputs_keys}; the composer (compose.py) compares the two sides.
ASCII only. Prints OK:/ERROR: lines.
"""
import copy
import hashlib
import json
import os
import sys

zip_dir, label, out_path = sys.argv[1:4]
sys.path.insert(0, zip_dir)
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
    {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})

import entry as ops_entry              # noqa: E402  the zip's ops/entry.py
import served                          # noqa: E402
import owned_requests                  # noqa: E402
import owned_report                    # noqa: E402
import repository                      # noqa: E402

POLICY = "irpt-custody-x10-v1"
SVC = "svc-custody-statement"
READ_ROUTE = "GET /api/scoped/investor-reporting/analysis/requests/{requestId}"
HISTORY_ROUTE = "GET /api/scoped/investor-reporting/analysis/requests"


def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def authorize(principal, owner):
    """resident_installed.make_authorize, in shape."""
    if not isinstance(principal, dict) or not isinstance(owner, dict) or not isinstance(owner.get("principal_id"), str) \
            or not owner["principal_id"]:
        return False
    firm = owner.get("firm_id")
    if not isinstance(firm, str) or not firm.strip() or firm in ("global", "opal-capital"):
        return False
    if principal.get("principal_class") == "OPAL_GLOBAL":
        return True
    return bool(principal.get("firm_id")) and firm == principal.get("firm_id") and owner["principal_id"] == principal.get("principal_id")


class Retention:
    def __init__(self):
        self.fail = None

    def reference(self, owner, family, logical_id, policy_revision=POLICY):
        return {"retention_id": "RET-" + repository.digest({"o": owner, "f": family, "l": logical_id, "p": policy_revision}),
                "policy_revision": policy_revision}

    def require_live(self, principal, ref, accepted=False, **_):
        if self.fail is not None:
            raise self.fail
        return {"state": "ACCEPTED"}


class Artifacts:
    def __init__(self, retention):
        self.retention, self.rows, self.blobs = retention, {}, {}

    def add(self, firm, owner, logical_id, data):
        aid = "ART-" + repository.digest({"owner": owner, "family": "REQUEST_COMPOSITION", "logical_id": logical_id})
        ref = {"artifact_id": aid, "family": "REQUEST_COMPOSITION", "sha256": hashlib.sha256(data).hexdigest(),
               "version_id": "v-" + aid[4:12], "byte_length": len(data), "content_type": "application/json", "immutable": True,
               "retention_ref": self.retention.reference(owner, "REQUEST_COMPOSITION", logical_id, "irpt-x10-v1")}
        self.rows[(firm, "ARTIFACT#" + aid)] = {"tenant": firm, "request_revision": "ARTIFACT#" + aid, "owner": owner,
                                                  "logical_id": logical_id, "ref": ref, "blob": {"version_id": ref["version_id"]}}
        self.blobs[aid] = data
        return ref

    def _index_get(self, firm, key):
        return copy.deepcopy(self.rows.get((firm, key)))

    def _artifact(self, principal, aid, data_firm=None):
        firm = data_firm or principal["firm_id"]
        row = self.rows.get((firm, "ARTIFACT#" + aid))
        if row is None or not authorize(principal, row["owner"]):
            raise repository.ReportDenied("artifact unavailable")
        self.retention.require_live(principal, row["ref"]["retention_ref"])
        return row

    def head(self, principal, aid, *, data_firm=None):
        return copy.deepcopy(self._artifact(principal, aid, data_firm)["ref"])

    def read(self, principal, aid, *, data_firm=None):
        row = self._artifact(principal, aid, data_firm)
        return {"ref": copy.deepcopy(row["ref"]), "data": self.blobs[aid]}


class ArtifactIndex:
    def __init__(self, artifacts):
        self.artifacts = artifacts

    def get(self, firm, key):
        return self.artifacts._index_get(firm, key)


class Artifacts2(Artifacts):
    """The ArtifactRepository surface the readers touch: head, get (the blob), index.get, retention."""
    def __init__(self, retention):
        super().__init__(retention)
        self.index = ArtifactIndex(self)

    def get(self, principal, aid, *, data_firm=None):
        return self.read(principal, aid, data_firm=data_firm)


class Acceptance:
    def __init__(self):
        self.rows = {}

    def get(self, firm, request_id):
        return copy.deepcopy(self.rows.get((firm, request_id)))


class Table:
    def __init__(self):
        self.rows = {}
        self.queries = []

    def query(self, KeyConditionExpression, ExpressionAttributeNames, ExpressionAttributeValues, ConsistentRead, Limit, **_):
        self.queries.append(Limit)
        tenant, prefix = ExpressionAttributeValues[":t"], ExpressionAttributeValues[":r"]
        rows = [copy.deepcopy(r) for (t, k), r in sorted(self.rows.items()) if t == tenant and k.startswith(prefix)]
        return {"Items": rows[:Limit]}


class Reports:
    def __init__(self, retention):
        self.retention = retention
        self.table = Table()
        self.index = type("I", (), {"table": self.table})()


def adv_headers(firm, email, principal_class_hdr="partner", advisor="one"):
    return {"x-contract-version": "v1", "x-origin-verify": "cloudfront", "x-firm-id": firm, "x-user-email": email,
            "x-user-role": "advisor", "x-user-type": principal_class_hdr, "x-advisor-id": advisor}


def svc_headers(firm="cottonwood", email=SVC):
    return {"X-Contract-Version": "v1", "X-Firm-Id": firm, "x-origin-verify": "cloudfront", "x-user-email": email,
            "x-user-role": "user", "x-user-type": "service"}


def build():
    """-> world: a 49financial request (REQ-a) with a persisted custody report, one without (REQ-b), a cottonwood request (REQ-c)."""
    from prospect import resolve_prospect_owner
    retention = Retention()
    artifacts, acceptance, reports = Artifacts2(retention), Acceptance(), Reports(retention)
    world = {"retention": retention, "acceptance": acceptance, "artifacts": artifacts, "reports": reports, "ids": {}}
    plan = [("a", "49financial", "advisor@example.invalid", True), ("b", "49financial", "advisor@example.invalid", False),
            ("c", "cottonwood", "adv@cottonwood.example", True)]
    for tag, firm, email, persisted in plan:
        owner = resolve_prospect_owner(adv_headers(firm, email), firm)
        request_id = "REQ-" + hashlib.sha256(tag.encode()).hexdigest()[:24]
        data = json.dumps({"schema_version": "irpt-analysis-composition.v1", "browser": {"client_id": "client-" + tag},
                           "resolved": {"owner": {"firm_id": firm}, "comparison_catalog": {}}}, sort_keys=True).encode()
        art_owner = {"firm_id": firm, "principal_id": owner["principal_id"], "account_ids": ["acc-" + tag],
                     "account_set_id": "set-" + tag, "schema_version": "custody-owner-v1"}
        ref = artifacts.add(firm, art_owner, request_id, data)
        acceptance.rows[(firm, request_id)] = {
            "identity": {"tenant_firm_id": firm, "request_id": request_id, "revision": 1, "immutable": True,
                         "ingestion_gate_revision": "v1", "destination_policy_revision": "offline-v1"},
            "owner": {"firm_id": firm, "principal_id": owner["principal_id"]}, "accepted_at": 1_800_000_000,
            "composition_ref": copy.deepcopy(ref)}
        world["ids"][tag] = {"request_id": request_id, "firm": firm, "artifact_id": ref["artifact_id"], "sha256": ref["sha256"],
                             "policy": ref["retention_ref"]["policy_revision"]}
        if persisted:
            owner_n = repository._owner(art_owner)
            report_id = "RPT-" + repository.digest({"owner": owner_n, "kind": "CUSTODY_REPORT", "request_id": ref["artifact_id"]})[:32]
            revision = hashlib.sha256(("report-" + tag).encode()).hexdigest()
            key = "REPORT#" + report_id + "#" + revision
            reports.table.rows[(firm, key)] = {
                "tenant": firm, "request_revision": key, "owner": owner_n,
                "ref": {"report_id": report_id, "revision": revision, "sha256": revision, "report_kind": "CUSTODY_REPORT",
                        "immutable": True},
                "blob": {"bucket": "b", "key": "k", "version_id": "v"},
                "retention_ref": retention.reference(owner_n, "CUSTODY_REPORT", key, POLICY)}
            world["ids"][tag]["report"] = {"report_id": report_id, "revision": revision}
    requests = owned_requests.OwnedRequestReader(acceptance=acceptance, artifacts=artifacts, authorize_current=authorize)
    reader = owned_report.OwnedAnalysisReader(requests=requests, reports=reports)
    world["boundary"] = ops_entry.build_owned_entry(requests=requests, reports=reader)
    world["requests"] = requests
    return world


def call(world, route, headers, request_id, include=None):
    query = {} if include is None else {"include": include}
    event = {"routeKey": route, "headers": dict(headers), "pathParameters": {"requestId": request_id} if request_id else {}}
    if query:
        event["queryStringParameters"] = query
    try:
        out = served.lambda_entry(world["boundary"])(event)
    except Exception as exc:  # noqa: BLE001 -- a harness fault is recorded, never hidden
        return {"ok": False, "code": "HARNESS_" + type(exc).__name__, "data_keys": None, "data_sha256": None,
                "persist_inputs_keys": None, "detail": str(exc)[:160]}
    data = out.get("data") if isinstance(out, dict) else None
    pi = data.get("persist_inputs") if isinstance(data, dict) else None
    ok = isinstance(out, dict) and out.get("ok") is not False and data is not None
    return {"ok": ok, "code": None if ok else ((out.get("status") or {}).get("public_reason_code") if isinstance(out, dict) else None),
            "data_keys": sorted(data) if isinstance(data, dict) else None,
            "data_sha256": sha(data) if ok else None,
            "persist_inputs_keys": sorted(pi) if isinstance(pi, dict) else None,
            "persist_inputs": pi if ok else None}


def main():
    w = build()
    A, B, C = w["ids"]["a"], w["ids"]["b"], w["ids"]["c"]
    adv49 = adv_headers("49financial", "advisor@example.invalid")
    other_firm_user = adv_headers("cottonwood", "adv@cottonwood.example")
    other_user_same_firm = adv_headers("49financial", "someone.else@example.invalid")
    arms = {}
    arms["owner_plain"] = call(w, READ_ROUTE, adv49, A["request_id"])
    arms["owner_include_composition"] = call(w, READ_ROUTE, adv49, A["request_id"], "composition")
    arms["owner_include_comparisons"] = call(w, READ_ROUTE, adv49, A["request_id"], "comparisons")
    arms["owner_include_persist_inputs_persisted"] = call(w, READ_ROUTE, adv49, A["request_id"], "persist_inputs")
    arms["owner_include_persist_inputs_not_persisted"] = call(w, READ_ROUTE, adv49, B["request_id"], "persist_inputs")
    arms["other_firm_plain"] = call(w, READ_ROUTE, other_firm_user, A["request_id"])
    arms["other_firm_include_composition"] = call(w, READ_ROUTE, other_firm_user, A["request_id"], "composition")
    arms["other_firm_include_persist_inputs"] = call(w, READ_ROUTE, other_firm_user, A["request_id"], "persist_inputs")
    arms["non_owner_same_firm_plain"] = call(w, READ_ROUTE, other_user_same_firm, A["request_id"])
    arms["non_owner_same_firm_include_composition"] = call(w, READ_ROUTE, other_user_same_firm, A["request_id"], "composition")
    arms["non_owner_same_firm_include_persist_inputs"] = call(w, READ_ROUTE, other_user_same_firm, A["request_id"], "persist_inputs")
    arms["svc_cottonwood_include_persist_inputs"] = call(w, READ_ROUTE, svc_headers(), C["request_id"], "persist_inputs")
    arms["svc_cottonwood_plain_read"] = call(w, READ_ROUTE, svc_headers(), C["request_id"])
    arms["svc_cottonwood_for_49financial_request"] = call(w, READ_ROUTE, svc_headers(), A["request_id"], "persist_inputs")
    arms["svc_claims_inflection"] = call(w, READ_ROUTE, svc_headers("inflection"), C["request_id"], "persist_inputs")
    arms["svc_claims_49financial"] = call(w, READ_ROUTE, svc_headers("49financial"), A["request_id"], "persist_inputs")
    arms["svc_cottonwood_history_sibling_read"] = call(w, HISTORY_ROUTE, svc_headers(), None)
    arms["svc_other_email_cottonwood"] = call(w, READ_ROUTE, svc_headers(email="svc-commentary"), C["request_id"], "persist_inputs")
    # controls on the harness itself (BUILT-side behaviour only matters where include=persist_inputs is accepted)
    w["retention"].fail = RuntimeError("RETENTION_EXPIRED_FIXTURE")
    arms["ctl_retention_dead_owner_include_persist_inputs"] = call(w, READ_ROUTE, adv49, A["request_id"], "persist_inputs")
    arms["ctl_retention_dead_owner_plain"] = call(w, READ_ROUTE, adv49, A["request_id"])
    w["retention"].fail = None
    arms["ctl_recovered_owner_include_persist_inputs"] = call(w, READ_ROUTE, adv49, A["request_id"], "persist_inputs")
    # a second report revision under the same report id: refused, never chosen
    k2 = "REPORT#%s#%s" % (A["report"]["report_id"], "f" * 64)
    first_key = [k for (t, k) in w["reports"].table.rows if k.startswith("REPORT#" + A["report"]["report_id"])][0]
    row2 = copy.deepcopy(w["reports"].table.rows[("49financial", first_key)])
    row2["request_revision"], row2["ref"]["revision"], row2["ref"]["sha256"] = k2, "f" * 64, "f" * 64
    row2["retention_ref"] = w["retention"].reference(row2["owner"], "CUSTODY_REPORT", k2, POLICY)
    w["reports"].table.rows[("49financial", k2)] = row2
    arms["ctl_two_report_revisions_owner_include_persist_inputs"] = call(w, READ_ROUTE, adv49, A["request_id"], "persist_inputs")
    # static facts about the packaged stack (what the zip itself carries), read from the zip's own modules
    sys.path.insert(1, os.path.join(zip_dir, "lib"))
    static = {"repository_KINDS": list(repository.KINDS)}
    try:
        import opal_naming
        pol = opal_naming.reporting_policy("irpt-custody-x10-v1")
        static["packaged_policy_irpt_custody_x10_v1"] = {"state": pol.get("state"), "families": sorted(pol.get("families", {}))}
    except Exception as exc:  # noqa: BLE001 -- recorded, never hidden
        static["packaged_policy_irpt_custody_x10_v1"] = "ABSENT:" + type(exc).__name__
    import inspect
    import retention
    static["retention_reference_params"] = list(inspect.signature(retention.RetentionPolicy.reference).parameters)
    # the installed handler composes from the zip's OWN stack (retention, repository, composition, registry, acceptance ...)
    try:
        from types import SimpleNamespace
        import status_installed as si
        import opal_naming as on

        def active(policy_id):
            return dict(on.reporting_policy(policy_id), state="ACTIVE")
        clients = {"dynamodb": SimpleNamespace(meta=SimpleNamespace(service_model=SimpleNamespace(service_name="dynamodb"))),
                   "table": SimpleNamespace(name="irpt-requests"), "s3": SimpleNamespace()}
        ports = si.compose_ports(clients=clients, clock=lambda: 1000.0,
                                 environ={si.REQUESTS_TABLE_ENV: "irpt-requests", si.JOBS_TABLE_ENV: "irpt-jobs"},
                                 reporting_policy=active)
        boundary = si.build_boundary(ports)
        static["installed_handler_composes"] = {"ok": True, "operations": sorted(boundary.operations),
                                                "readers": [type(ports["requests"]).__name__, type(ports["reports"]).__name__]}
    except Exception as exc:  # noqa: BLE001 -- recorded, never hidden
        static["installed_handler_composes"] = {"ok": False, "error": type(exc).__name__ + ": " + str(exc)[:120]}
    json.dump({"label": label, "zip_dir": zip_dir, "static": static, "served_file": served.__file__,
               "svc_ops": sorted(getattr(served, "SVC_CUSTODY_STATEMENT_OPERATIONS", [])),
               "has_persist_inputs_method": hasattr(owned_report.OwnedAnalysisReader, "persist_inputs"),
               "ids": {k: {kk: vv for kk, vv in v.items()} for k, v in w["ids"].items()}, "arms": arms},
              open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("OK: %s arms=%d" % (label, len(arms)))


main()
