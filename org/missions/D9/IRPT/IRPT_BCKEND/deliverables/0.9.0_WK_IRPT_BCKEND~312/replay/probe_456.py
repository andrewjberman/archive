"""IB-pr-456 replay probe: ONE extracted package tree, offline. Run as
    python -I probe_456.py <extracted_zip_dir> <label> <registry_json> <out_json>
boto3 is never imported: every client is the in-memory MemoryDynamo below; every socket connect is refused. The tree is data: its modules are
imported through sys.path exactly as the Lambda's flat /var/task layout does, nothing else is executed. Synthetic ids only (no real firm,
principal, client or account). Each section records an OUTCOME STRING (returned / the exception class and its code) so the driver compares
live against built value by value. ASCII only."""
import copy
import hashlib
import inspect
import json
import os
import socket
import sys
from pathlib import Path
from unittest.mock import Mock

zip_dir, label, registry, out_path = sys.argv[1:5]
sys.dont_write_bytecode = True
sys.path.insert(0, zip_dir)
os.environ["IRPT_FIRM_REGISTRY"] = registry


def _refuse(self, *a, **k):
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
_real_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, *a, **k: _real_gai(host, *a, **k) if host in (None, "localhost", "127.0.0.1", "::1", "") else (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))

FIRM, VERIFIED = "synthetic-firm-one", "synthetic-verified-principal"
OWNER = {"firm_id": FIRM, "principal_id": VERIFIED, "advisor_id": VERIFIED, "ownership_fingerprint": "b" * 64}
REF = {"artifact_id": "ART-one", "sha256": "a" * 64, "version_id": "version-one"}
BASE = {"request_id": "areq-1234", "client_id": "C-one", "account_ids": ["A-one"], "snapshot_id": "SNAP-one", "variant": "overview",
        "comparison_keys": [], "report_title": None, "prepared_for": "Synthetic recipient"}


def body(**extra):
    return dict(copy.deepcopy(BASE), **extra)


def outcome(fn):
    try:
        return {"returned": fn()}
    except BaseException as exc:  # noqa: BLE001 -- recorded, never raised
        return {"raised": type(exc).__name__ + ":" + str(getattr(exc, "code", None) or exc)[:80].replace(VERIFIED, "<principal>")}


class MemoryDynamo:
    def __init__(self):
        self.items, self.writes = {}, []

    @staticmethod
    def _k(table, key):
        return (table, json.dumps(key, sort_keys=True))

    def get_item(self, TableName, Key, ConsistentRead=True):
        item = self.items.get(self._k(TableName, Key))
        return {"Item": item} if item else {}

    def transact_write_items(self, TransactItems):
        for w in TransactItems:
            put = w["Put"]
            key = {k: put["Item"][k] for k in ("tenant", "request_revision", "job") if k in put["Item"]}
            self.items[self._k(put["TableName"], key)] = put["Item"]
            self.writes.append(put["TableName"])

    def update_item(self, **kw):
        return {}

    def put_record(self, table, tenant, request_id, record):
        key = {"tenant": {"S": tenant}, "request_revision": {"S": "analysis#" + request_id + "#1"}}
        self.items[self._k(table, key)] = dict(key, record={"S": json.dumps(record)})


out = {"label": label}
import submission as sub  # noqa: E402

# ---- 1. the closed set, as the tree's validate_public_request reads it
S = {"public_fields_has_commentary_requested": "commentary_requested" in sub.PUBLIC_FIELDS}
cases = {"without_member": body(), "member_true": body(commentary_requested=True), "member_false": body(commentary_requested=False),
         "member_string_true": body(commentary_requested="true"), "member_int_1": body(commentary_requested=1), "member_none": body(commentary_requested=None),
         "member_list": body(commentary_requested=[True]), "unknown_member": body(commentary="yes")}
S["validate_public_request"] = {k: outcome(lambda b=b: {"keys": sorted(sub.validate_public_request(b)), "equal_to_input": sub.validate_public_request(b) == b})
                                for k, b in cases.items()}
out["submission"] = S

# ---- 2. acceptance over an in-memory store
import acceptance as acc  # noqa: E402

takes_actor = "acting_principal_id" in inspect.signature(acc.DynamoAcceptance.accept).parameters
out["acceptance_signature_takes_acting_principal_id"] = takes_actor


def accept(store, b):
    kw = {"acting_principal_id": VERIFIED} if takes_actor else {}
    return store.accept(OWNER, b, REF, ingestion_revision="v1", destination_revision="v1", **kw)


def record_view(rec):
    return None if rec is None else {"keys": sorted(rec), "commentary_requested": rec.get("commentary_requested", "<absent>"),
                                     "ticket_id": rec.get("ticket_id", "<absent>")}


def fresh():
    c = MemoryDynamo()
    return c, acc.DynamoAcceptance(c, requests_table="irpt-requests", jobs_table="irpt-jobs", now=lambda: 100)


A = {}
for name, b in cases.items():
    c, st = fresh()
    o = outcome(lambda: record_view(accept(st, copy.deepcopy(b))))
    rid = acc.request_id_for(FIRM, VERIFIED, b["request_id"])
    A[name] = {"accept": o, "transactions_written": len(c.writes), "read_back_get": outcome(lambda: record_view(st.get(FIRM, rid)))}
out["accept_new"] = A

# replay of the SAME request id: same body again; the member added; dropped; changed
R = {}


def replay(first, second):
    c, st = fresh()
    o1 = outcome(lambda: record_view(accept(st, copy.deepcopy(first))))
    n1 = len(c.writes)
    o2 = outcome(lambda: record_view(accept(st, copy.deepcopy(second))))
    return {"first": o1, "second": o2, "transactions_after_first": n1, "transactions_after_second": len(c.writes)}


R["same_body_twice_without_member"] = replay(body(), body())
R["same_body_twice_with_member_true"] = replay(body(commentary_requested=True), body(commentary_requested=True))
R["same_request_id_member_added"] = replay(body(), body(commentary_requested=True))
R["same_request_id_member_dropped"] = replay(body(commentary_requested=True), body())
R["same_request_id_member_true_then_false"] = replay(body(commentary_requested=True), body(commentary_requested=False))
R["same_request_id_member_false_then_true"] = replay(body(commentary_requested=False), body(commentary_requested=True))
out["replay_same_request_id"] = R

# a stored record WITHOUT the member (accepted before any release), looked up with each body
c, st = fresh()
rid = acc.request_id_for(FIRM, VERIFIED, BASE["request_id"])
OLD = {"identity": {"tenant_firm_id": FIRM, "request_id": rid, "revision": 1, "immutable": True, "ingestion_gate_revision": "v1", "destination_policy_revision": "v1"},
       "owner": OWNER, "browser_sha256": sub.digest(body()), "composition_ref": dict(REF, family="REQUEST_COMPOSITION", immutable=True, retention_ref={"id": "ret-one"}),
       "accepted_at": 100}
c.put_record("irpt-requests", FIRM, rid, OLD)
out["record_accepted_before"] = {
    "get_old_record": outcome(lambda: record_view(st.get(FIRM, rid))),
    "lookup_same_body": outcome(lambda: record_view(st.lookup(OWNER, body()))),
    "lookup_body_with_member": outcome(lambda: record_view(st.lookup(OWNER, body(commentary_requested=True))))}

# ---- 3. the submission service pair (only where the tree packages submission_service.py)
if (Path(zip_dir) / "submission_service.py").is_file():
    from composition_admission import CompositionAdmission  # noqa: E402
    from submission_service import SubmissionService  # noqa: E402

    def service_run(bodies):
        c, store = fresh()
        input_ref = {"input_id": "portfolio_" + "a" * 64, "content_sha256": "a" * 64,
                     "artifact_ref": {"artifact_id": "ART-input", "family": "NORMALIZED_PORTFOLIO", "sha256": "a" * 64, "retention_ref": {"id": "ret-one"}}}
        resolved = {"owner": OWNER, "input_ref": input_ref, "source_descriptors": {}, "client": {"client_id": "C-one", "account_ids": ["A-one"]},
                    "holdings": {"snapshot_id": "SNAP-one"}}
        sent = []

        class FakeArtifacts:
            """In-memory retained repository: put keeps the bytes and returns an immutable REQUEST_COMPOSITION ref; head/get read them back."""
            def __init__(self):
                self.refs, self.data = {"ART-input": input_ref["artifact_ref"]}, {}
                self.retention = Mock()
                self.retention.require_live.side_effect = lambda principal, rr, **kw: {"owner": OWNER, "dependencies": [input_ref["artifact_ref"]["retention_ref"]]}

            def put(self, principal, owner, family, logical_id, data, content_type, **kw):
                ref = {"artifact_id": "ART-" + hashlib.sha256(logical_id.encode()).hexdigest()[:16], "family": family, "sha256": hashlib.sha256(data).hexdigest(),
                       "version_id": "version-one", "immutable": True, "retention_ref": {"id": "ret-comp"}}
                self.refs[ref["artifact_id"]], self.data[ref["artifact_id"]] = ref, data
                return ref

            def head(self, principal, artifact_id, **kw):
                return self.refs[artifact_id]

            def get(self, principal, artifact_id, **kw):
                return {"ref": self.refs[artifact_id], "data": self.data[artifact_id]}

        artifacts = FakeArtifacts()
        admission = Mock(spec=CompositionAdmission)
        admission.validate.side_effect = lambda doc: sub.canonical_bytes(doc)
        principal = {"principal_id": VERIFIED, "firm_id": FIRM}
        res = []
        for b in bodies:
            svc = SubmissionService(acceptance=store, artifacts=artifacts, resolve_owner=lambda *a: (principal, OWNER), authorize_current=lambda *a: True,
                                    resolve_inputs=lambda *a: copy.deepcopy(resolved), settings={"fee": 0}, recipe_version="v1", ingestion_revision="v1",
                                    destination_revision="v1", send=lambda url, text: sent.append(url), queue_url="offline", admission=admission)
            res.append(outcome(lambda: {"stage": svc.submit(copy.deepcopy(b), None, {}, {}, None)["stage"]}))
        recs = [json.loads(v["record"]["S"]) for (t, _), v in c.items.items() if t == "irpt-requests"]
        return {"calls": res, "transactions_written": len(c.writes), "queue_sends": len(sent), "stored_records": [record_view(r) for r in recs]}

    out["service_pair"] = {"without_member": service_run([body()]), "member_true": service_run([body(commentary_requested=True)]),
                           "member_false": service_run([body(commentary_requested=False)]),
                           "member_wrong_type": service_run([body(commentary_requested="true")]),
                           "same_request_id_member_added": service_run([body(), body(commentary_requested=True)]),
                           "same_request_id_member_dropped": service_run([body(commentary_requested=True), body()]),
                           "replay_without_member": service_run([body(), body()])}


# ---- 4. readers the tree holds, each over a stored record without and with the member
def stored(c, rid2, member):
    rec = copy.deepcopy(OLD)
    rec["identity"]["request_id"] = rid2
    if member != "<absent>":
        rec["commentary_requested"] = member
    c.put_record("irpt-requests", FIRM, rid2, rec)


RD = {}
RID2 = "REQ-" + "0" * 24
members = {"record_without_member": "<absent>", "record_with_member_true": True, "record_with_member_false": False}
if (Path(zip_dir) / "owned_requests.py").is_file():
    import owned_requests as orq  # noqa: E402
    for nm, mv in members.items():
        c, st2 = fresh()
        stored(c, RID2, mv)
        arts = Mock()
        arts.head.return_value = dict(REF, family="REQUEST_COMPOSITION", immutable=True, retention_ref={"id": "ret-one"})
        arts.retention.require_live.return_value = {"dependencies": []}
        reader = orq.OwnedRequestReader(acceptance=st2, artifacts=arts, authorize_current=lambda p, o: True)
        RD.setdefault("OwnedRequestReader.read", {})[nm] = outcome(lambda: reader.read({"firm_id": FIRM, "principal_id": VERIFIED}, RID2))
if (Path(zip_dir) / "commentary_composition.py").is_file():
    import commentary_composition as cc  # noqa: E402
    for nm, mv in members.items():
        c, st2 = fresh()
        stored(c, RID2, mv)
        rec = st2.get(FIRM, RID2)
        rec["composition_ref"] = dict(rec["composition_ref"], artifact_id="ART-0123456789abcdef", family=cc.FAMILY, sha256="a" * 64)
        c.put_record("irpt-requests", FIRM, RID2, rec)
        arts = Mock()
        data = json.dumps({"schema_version": "v1"}).encode("utf-8")
        arts.get.return_value = {"ref": {"family": cc.FAMILY, "sha256": "a" * 64, "byte_length": len(data)}, "data": data}
        jobs = Mock()
        jobs.state.return_value = cc.READY_STATE
        RD.setdefault("commentary_composition.read_composition", {})[nm] = outcome(
            lambda: {k: v for k, v in cc.read_composition(st2, arts, {"tenant": FIRM, "request_id": RID2}, jobs).items() if k in ("status", "tenant", "request_ref")})
if (Path(zip_dir) / "commentary_draft_store.py").is_file():
    import commentary_draft_store as ds  # noqa: E402
    for nm, mv in members.items():
        c, st2 = fresh()
        stored(c, RID2, mv)
        RD.setdefault("commentary_draft_store.resolve_request", {})[nm] = outcome(lambda: list(ds.resolve_request(st2, FIRM, RID2))[0])
if (Path(zip_dir) / "resident_worker.py").is_file():
    import resident_worker as rw  # noqa: E402
    RD["resident_worker.has_send_ready_if_ticketed"] = hasattr(rw, "send_ready_if_ticketed")
    RD["resident_worker.has_producer_for"] = hasattr(rw, "producer_for")
out["readers"] = RD

# ---- 5. the packaged contract (the ingestion_gate_revision a new record would carry is a digest over contracts/*.schema.json)
if (Path(zip_dir) / "contracts").is_dir():
    rows = [p.name + ":" + hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((Path(zip_dir) / "contracts").glob("*.schema.json"))]
    out["ingestion_revision_rule_digest"] = "schemas-" + hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()
    sc = json.loads((Path(zip_dir) / "contracts" / "AnalysisSubmissionRequest.schema.json").read_text(encoding="utf-8"))
    out["schema"] = {"properties_has_commentary_requested": "commentary_requested" in sc.get("properties", {}),
                     "additionalProperties": sc.get("additionalProperties"),
                     "commentary_requested_type": (sc.get("properties", {}).get("commentary_requested") or {}).get("type")}
Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print("OK: %s sections=%s" % (label, sorted(out)))
