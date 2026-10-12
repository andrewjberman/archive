"""IB-pr-460 replay probe: ONE extracted package tree of irpt-commentary-draft-store-lambda, offline. Run as
    python -I probe_460.py <extracted_zip_dir> <label> <out_json>
boto3 is never imported: the request, ref and artifact ports are the in-memory fakes below; every socket connect is refused. The tree is data:
its modules are imported through sys.path exactly as the Lambda's flat /var/task layout does, nothing else is executed. Synthetic ids only
(no real firm, principal, client, account or ticket). Each section records the OUTCOME (the answer returned, or the exception class and code)
so the driver compares live against built value by value. ASCII only."""
import hashlib
import json
import socket
import sys

zip_dir, label, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
sys.path.insert(0, zip_dir)


def _refuse(self, *a, **k):
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
_real_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, *a, **k: _real_gai(host, *a, **k) if host in (None, "localhost", "127.0.0.1", "::1", "") else (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))

import commentary_draft_store as cds  # noqa: E402
import repository  # noqa: E402

TENANT, OTHER = "synthetic-firm-one", "synthetic-firm-two"
RID = "REQ-" + "a" * 24
RID2 = "REQ-" + "b" * 24
TICKET = "TCK-20261011-0a1b2c3d"
DRAFT = {"request_id": RID, "draft_text": "A synthetic draft."}
GONE = object()


def record(request_id=RID, tenant=TENANT, ticket=GONE):
    r = {"identity": {"tenant_firm_id": tenant, "request_id": request_id, "revision": 1, "immutable": True},
         "owner": {"firm_id": tenant, "principal_id": "synthetic-principal", "account_ids": ["acc-a"]},
         "composition_ref": {"artifact_id": "ART-" + "c" * 64}, "accepted_at": 1}
    if ticket is not GONE:
        r["ticket_id"] = ticket
    return r


class Requests:
    def __init__(self, records):
        self.records, self.calls = records, []

    def get(self, tenant, request_id):
        self.calls.append((tenant, request_id))
        return self.records.get((tenant, request_id))


class Refs:
    def __init__(self):
        self.values, self.sets = {}, []

    def get(self, tenant, request_id):
        return self.values.get((tenant, request_id))

    def set_once(self, tenant, request_id, ref):
        self.sets.append((tenant, request_id, ref))
        if (tenant, request_id) in self.values:
            raise cds.DraftStoreRefused("ALREADY_WRITTEN")
        self.values[(tenant, request_id)] = ref


class Index:
    def __init__(self):
        self.rows = {}

    def get(self, tenant, key):
        return self.rows.get((tenant, key))


class Artifacts:
    """put() writes once per logical id; a second put raises the tree's own ArtifactAlreadyWritten with the first artifact id."""

    def __init__(self):
        self.index, self.by_logical, self.puts = Index(), {}, 0

    def put(self, principal, owner, family, logical_id, data, content_type):
        if logical_id in self.by_logical:
            raise repository.ArtifactAlreadyWritten(self.by_logical[logical_id])
        sha = hashlib.sha256(data).hexdigest()
        aid = "ART-" + hashlib.sha256((logical_id + sha).encode()).hexdigest()
        ref = {"artifact_id": aid, "sha256": sha, "version_id": "version-1", "family": family}
        self.index.rows[(owner["firm_id"], "ARTIFACT#" + aid)] = {"tenant": owner["firm_id"], "ref": ref}
        self.by_logical[logical_id] = aid
        self.puts += 1
        return ref


def outcome(fn):
    try:
        return {"returned": fn()}
    except BaseException as exc:  # noqa: BLE001 -- recorded, never raised
        return {"raised": type(exc).__name__ + ":" + str(getattr(exc, "code", None) or exc)[:80]}


class W:
    def __init__(self, ticket=GONE):
        self.requests = Requests({(TENANT, RID): record(ticket=ticket), (TENANT, RID2): record(RID2)})
        self.refs, self.artifacts = Refs(), Artifacts()

    def call(self, event):
        return cds.handle(self.requests, self.refs, self.artifacts, event)

    def put(self, request_id=RID, tenant=TENANT):
        return self.call({"op": "put", "tenant": tenant, "request_id": request_id, "draft": DRAFT})

    def get_ref(self):
        return self.call({"op": "get_ref", "tenant": TENANT, "request_id": RID})


out = {"label": label}


def scenario(ticket):
    w = W(ticket)
    s = {"get_ref_before": w.get_ref()}
    s["first_persist"] = w.put()
    s["requests_get_calls_for_the_first_persist"] = len(w.requests.calls) - 1
    s["get_ref_after"] = w.get_ref()
    n = len(w.requests.calls)
    s["replay"] = w.put()
    s["requests_get_calls_for_the_replay"] = len(w.requests.calls) - n
    s["artifact_puts"] = w.artifacts.puts
    s["ref_sets"] = len(w.refs.sets)
    s["refusal_other_tenant"] = w.put(tenant=OTHER)
    s["refusal_reserved_tenant"] = w.put(tenant="global")
    s["refusal_unknown_op"] = w.call({"op": "delete", "tenant": TENANT, "request_id": RID})
    s["refusal_extra_key"] = w.call({"op": "put", "tenant": TENANT, "request_id": RID, "draft": DRAFT, "principal": {}})
    s["refusal_missing_draft"] = w.call({"op": "put", "tenant": TENANT, "request_id": RID})
    s["refusal_absent_record"] = w.put(request_id="REQ-" + "f" * 24)
    return s


out["no_ticket_key"] = scenario(GONE)
out["ticket"] = scenario(TICKET)
out["ticket_empty_string"] = scenario("")
out["ticket_none"] = scenario(None)
out["ticket_int"] = scenario(7)
out["ticket_list"] = scenario([TICKET])


def crash(ticket):
    w = W(ticket)
    first = w.artifacts.put(cds.service_principal(cds.SUBJECT, TENANT), record()["owner"], cds.FAMILY, RID, b'{"first":1}', "application/json")
    healed = w.put()
    return {"first_artifact_ref_keys": sorted(k for k in first if k != "family"), "healed": healed, "artifact_puts": w.artifacts.puts, "ref_sets": len(w.refs.sets)}


out["crash_recovery_with_ticket"] = crash(TICKET)
out["crash_recovery_no_ticket"] = crash(GONE)
w = W(TICKET)
out["resolve_request"] = outcome(lambda: [type(x).__name__ if isinstance(x, dict) else x for x in cds.resolve_request(w.requests, TENANT, RID)])
out["resolve_request_arity"] = outcome(lambda: len(cds.resolve_request(w.requests, TENANT, RID)))
out["tree_has_resolve_record"] = hasattr(cds, "_resolve_record")
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(out, indent=1, sort_keys=True) + "\n")
print("probe %s ok" % label)
